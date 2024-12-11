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
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app import db
from flask import session as sess
from flask import Response, send_file, make_response
from markupsafe import escape

import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


engine = sa.create_engine("sqlite+pysqlite:///app.db")
md = model.ravdess_metadata
session = Session(engine)

# Audio Features class instantiation
ctl = sel.FormControl()
af = AudioFeatures(ctl.get_first_file(md,session))



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()

    
    
    record_info=''
 

    if request.method == 'POST':
        if form.submit.data:
            
            ctl.set_filter_dict(form,sess)
            
            sess['file_list']= ctl.get_file_list(form, md, session)
            
            sess['record_count'] = len(sess['file_list'])
            sess['record_num']=0
            
            sess['fp'] = sess['file_list'][sess['record_num']]
            
            form.submit.data = False
            
        if next_button.next.data:

            if  'record_num' in sess:
                sess['record_num'] += 1
            else:
                sess['record_num'] = 1
            
            ctl.set_form_data(form, sess)
            
            

            if 'file_list' in sess:
                sess['fp'] = sess['file_list'][sess['record_num']]
            else:
                sess['file_list']= ctl.get_file_list(form, md, session)
                sess['fp'] = sess['file_list'][sess['record_num']]
            
            sess['record_count'] = len(sess['file_list'])
            
    
        af.change_file(sess['fp'])
        record_info = f'Displaying record {sess['record_num']+1} of {sess['record_count']}'
       


    return render_template('feature-explorer.html',
        title='Home', 
        form=form, 
        next_button=next_button, 
        record_text=record_info)


@bp.route('/audio-player', methods=['GET', 'POST'])
def get_audio_blob():
  
    wav = af.get_audio_data()

    response = make_response(wav.getvalue()) 
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
    
    return response


@bp.route('/plot-wav',  methods=['GET', 'POST'])
def plot_wav():
    
    #fig = af.get_waveform_plot()
    ap = PlotAggregator(af)
    fig = ap.get_record_viz()
    return send_file(fig, mimetype='image/png')

'''
@bp.route('/plot-spectro',  methods=['GET', 'POST'])
def plot_spectro():
    
    fig = af.get_spectrogram_plot()

    return send_file(fig, mimetype='image/png')

@bp.route('/plot-mels',  methods=['GET', 'POST'])
def plot_mels():
    
    n_mels = 128

    if 'filter_dict' in sess:
        n_mels = int(sess['filter_dict']['num_mels'])

    fig = af.get_mel_plot(n_mels)

    return send_file(fig, mimetype='image/png')

@bp.route('/plot-mfcc',  methods=['GET', 'POST'])
def plot_mfcc():
    
    n_mfcc = 40
    n_mels= 128

    if 'filter_dict' in sess:
        n_mfcc = int(sess['filter_dict']['num_mfcc'])
        n_mels = int(sess['filter_dict']['num_mels'])


    fig = af.get_mfcc_plot(n_mels,n_mfcc)

    return send_file(fig, mimetype='image/png')

'''