# controls the page routing
from datetime import datetime, timezone
from flask import render_template, request
import app.main.forms as forms
from app.main import bp
import os
import app.src.models as model
import app.src.selector as sel
from app.src.FeatureExtractors import AudioFeatures 
from app.src.AggregatePlots import PlotAggregator
from app.src.SessionManager import SessionManager
import sqlalchemy as sa
from sqlalchemy.orm import Session
#from app import db
from flask import session as sess
from flask import Response, send_file, make_response
from markupsafe import escape


import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


m_engine = sa.create_engine("sqlite+pysqlite:///app.db")
md = model.ravdess_metadata
dbsession = Session(m_engine)

# Audio Features class instantiation
ctl = sel.DBControl()
af = AudioFeatures()

#af=[]





@bp.route('/', methods=['GET', 'POST'])
def index():
    
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()
    s = SessionManager(sess)
    s.initialize_session(ctl.get_full_file_list(md, dbsession))
    
 
    if request.method == 'POST':
        
        if form.submit.data:
            
            s.set_filters(form)
            s.set_file_list(ctl.get_file_list(sess, md, dbsession))
            form.submit.data = False
            
        if next_button.next.data:

            s.get_next_record()
            s.set_form_data(form)
           

        af.change_file(sess['fp'])
      


    return render_template('feature-explorer.html',
        title='Home', 
        form=form, 
        next_button=next_button, 
        record_text=sess['record_message'])


@bp.route('/audio-player', methods=['GET', 'POST'])
def get_audio_blob():
  
    wav = af.get_audio_data()

    response = make_response(wav.getvalue()) 
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
    
    return response


@bp.route('/plot-wav',  methods=['GET', 'POST'])
def plot_wav():
    
    ap = PlotAggregator(af)
    # Creating a new session obj b/c initialize session
    # performs all the necessary checks 
    # and I wanted to have getters for num_mels and num_mfcc
    # still...a little bad code smell
    s = SessionManager(sess)
    s.initialize_session(ctl.get_full_file_list(md, dbsession))
    fig = ap.get_record_viz(n_mels=s.get_num_mels(), n_mfcc=s.get_num_mfcc())
    return send_file(fig, mimetype='image/png')

