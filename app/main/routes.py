# controls the page routing

from flask import render_template, request
from flask import session as sess
from flask import send_file, make_response

from app.main import bp
import app.main.forms as forms
import app.src.selector as sel

#from app.src.models import ravdess_metadata as md
from app.src.FeatureExtractors import AudioFeatures 
from app.src.AggregatePlots import PlotAggregator
from app.src.SessionManager import SessionManager
from app import db

# Audio Features class instantiation
ctl = sel.DBControl()
af = AudioFeatures()


@bp.route('/', methods=['GET', 'POST'])
def index():
    
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()
    s = SessionManager(sess)
    s.initialize_session(ctl.get_full_file_list(db))
    
 
    if request.method == 'POST':
        
        if form.submit.data:
            
            s.set_filters(form)
            s.set_file_list(ctl.get_filtered_file_list(sess,db))
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
    s.initialize_session(ctl.get_full_file_list(db))
    fig = ap.get_record_viz(n_mels=s.get_num_mels(), n_mfcc=s.get_num_mfcc())
    return send_file(fig, mimetype='image/png')

