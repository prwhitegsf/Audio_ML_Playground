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
from app.src.ResultsEvaluator import EvaluateResults 
from app import db

# Audio Features class instantiation
dbc = DBControl(db)
s = SessionManager(dbc)
af = AudioFeatures()
er = EvaluateResults(af)



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



#@bp.route('/', methods=['GET', 'POST'])
#@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/feature-extractor', methods=['GET', 'POST'])
def feature_extractor():
    
    form = forms.DataSetFilterForm()
    next_button = forms.NextRecord()   
    if request.method == 'GET':
        s.init_sess(sess,form)
   
    if request.method == 'POST':
        
        if form.submit.data:
            
            s.set_filters(form, sess)
            s.set_record_list(sess)
            form.submit.data = False
            
        if next_button.next.data:
            
            s.get_next_record(sess)
            s.set_form_data(form,sess)
           

        af.change_audio_file(sess)
 
    return render_template('feature-extractor.html',
        title='Home', 
        form=form, 
        next_button=next_button, 
        record_text=sess['single_message'])




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/label-selector',methods=['GET','POST'])
def get_label_mfccs():

    if request.method == 'GET':
        sess.clear()

    form = forms.DataSetFilterForm()
    next_group = forms.NextRecord()
    next_audio_file = forms.NextAudioRecord()
    

    
    s.init_sess(sess,form)

    if request.method == 'POST':
        
        if form.submit.data:
            s.set_filters(form, sess)
            s.set_record_list(sess)
            af.choose_npy_array(sess)
        
            form.submit.data = False
            
        if next_group.next.data:
            s.advance_record_group(sess)
            s.set_form_data(form,sess)
        
        if next_audio_file.next_audio_file.data:
            s.advance_record_within_group(sess)
            s.set_form_data(form,sess)
         
        af.change_group_audio_file(sess)

    return render_template('label-selector.html',
        title='Home', 
        form=form, 
        next_group=next_group, 
        next_audio_file=next_audio_file,
        visual_message=sess['visual_message'],
        audio_message = sess['audio_message'])

@bp.route('/training-results',methods=['GET','POST'])
def show_training_results():
    
    svc_results = []

    if request.method == 'GET':
        er.get_features_and_labels()
        er.scale_features()
        er.encode_labels()
        er.split_dataset()
    
    svc_results = er.get_SVC_scores()
    linsvc_results = er.get_LinearSVC_scores()
    #svc_results = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    
    
    return render_template('training-results.html',
        title='Home',
        svc_results = svc_results,
        linsvc_results = linsvc_results)
    # features, labels = af.get_filtered_df()
    # create distro table (will be delivered in a separate function call)
    # scale, label encoder and split
    # define models and apply training function
    # return 2D array to html and loop to make table
    
@bp.route('/training-results',methods=['POST'])
def show_testing_results():
    pass

@bp.route('/label-distribution')
def view_label_distribution():
    fig = er.show_label_distribution()
    return send_file(fig, mimetype='image/png')


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

    fig = ap.get_record_viz(sess,n_mels=s.get_num_mels(sess), n_mfcc=s.get_num_mfcc(sess))
    return send_file(fig, mimetype='image/png')





@bp.route('/view-mfcc-group',  methods=['GET', 'POST'])
def view_mfcc_group():
    
    ap = PlotAggregator(af)
    fig = ap.get_mfcc_plots_for_label(sess)
    
    return send_file(fig, mimetype='image/png')

