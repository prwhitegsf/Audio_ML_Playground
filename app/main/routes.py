# controls the page routing

from flask import render_template, request
from flask import session as sess
from flask import send_file, make_response, jsonify,current_app

from app.main import bp
import app.main.forms as forms
from app.src.DatabaseController import DBControl 

#from app.src.models import ravdess_metadata as md
from app.src.FeatureExtractors import AudioFeatures 
from app.src.AggregatePlots import PlotAggregator
from app.src.SessionManager import SessionManager
from app import db

# Audio Features class instantiation
dbc = DBControl(db)
s = SessionManager(dbc)
af = AudioFeatures()




@bp.route('/data-inspector', methods=['GET', 'POST'])
def data_inspector():

    form = forms.PostForm()
    fp = '/datasets/RAVDESS/metadata/img/emotions.jpg'
    if request.method == 'POST':
        if form.select.data:
         
            if form.validate_on_submit():
                
                fp = '/static/datasets/RAVDESS/metadata/img/' + form.select.data
                return jsonify({'result': f'{fp}'})
    
    return render_template('data-inspector.html',title='Home', image=fp, form=form, result=fp)




@bp.route('/feature-extractor', methods=['GET', 'POST'])
def feature_extractor():
    
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()
    
   
    s.initialize_session(sess)
    
 
    if request.method == 'POST':
        
        if form.submit.data:
            
            s.set_filters(form, sess)
            s.set_file_list(sess)
            af.choose_npy_array(sess)
            form.submit.data = False
            
        if next_button.next.data:
            
            s.get_next_record(sess)
            s.set_form_data(form,sess)
           

        af.change_file(sess)
      


    return render_template('feature-extractor.html',
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


@bp.route('/view-audio-features',  methods=['GET', 'POST'])
def view_audio_features():
    
    ap = PlotAggregator(af)

    s.initialize_session(sess)
    fig = ap.get_record_viz(sess,n_mels=s.get_num_mels(sess), n_mfcc=s.get_num_mfcc(sess))
    return send_file(fig, mimetype='image/png')



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/view-label-mfcc',methods=['GET','POST'])
def get_label_mfccs():
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()
    
   
    s.initialize_session(sess)
    s.init_mfcc_img_groups(sess)
    
 
    if request.method == 'POST':
        
        if form.submit.data:
            
            s.set_filters(form, sess)
            s.set_file_list(sess)
            af.choose_npy_array(sess)
            form.submit.data = False
            
        if next_button.next.data:
            
            s.get_next_record_group(sess)
            s.set_form_data(form,sess)
           

        af.change_file(sess)
      


    return render_template('label-selector.html',
        title='Home', 
        form=form, 
        next_button=next_button, 
        record_text=sess['record_message'])

@bp.route('/view-mfcc-group',  methods=['GET', 'POST'])
def view_mfcc_group():
    
    ap = PlotAggregator(af)

    s.initialize_session(sess)
    fig = ap.get_mfcc_plots_for_label(sess)
    
    return send_file(fig, mimetype='image/png')

