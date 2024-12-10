from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Length








def create_range():
        rng = list(range(1,25))
        nums = ['all']
        for i in rng:
             item = (str(i),str(i))
             nums.append(item)      
        return nums

class PostForm(FlaskForm):

    submit = SubmitField('Submit')
    
    select = SelectField('Data Distributions', choices=[
        ('emotions.jpg'),
        ('mfcc.jpg'),
        ('actor_sex.jpg'),
        ('labels.jpg')
    ])
    
    

class DataSetFilterForm(FlaskForm):
    
    submit = SubmitField('Submit')
    actor = SelectMultipleField('Actor Number', choices=create_range())
    sex  = SelectField('Sex',choices=['all','female','male'],default='all')
    statement = SelectField('Statement',choices=['all','1','2'],default='all')
    emotion =  SelectMultipleField('Emotion', choices=[('all','all'),
                                                        ('neutral','neutral'),
                                                        ('calm','calm'),
                                                        ('happy','happy'),
                                                        ('sad','sad'),
                                                        ('angry','angry'),
                                                        ('fearful','fearful'),
                                                        ('disgust','disgust'),
                                                        ('surprised','surprised')],
                                                        default='all')

    intensity = SelectField('Intensity',choices=['all','1','2'],default='all')

    mel_filter_count = RadioField("Mel Filter Count", choices=[('512','512'),
                                                               ('256','256'),
                                                               ('128','128'),
                                                               ('64','64'),
                                                               ('32','32')],
                                                               default='128')
    
    mfcc_count = RadioField("MFCC Count", choices=[('160','160'),
                                                   ('80','80'),
                                                   ('40','40'),
                                                   ('20','20'),
                                                   ('10','10')],
                                                   default='40')


class NextRecord(FlaskForm):
     next = SubmitField('Next')