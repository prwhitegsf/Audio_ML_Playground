import app.main.forms as forms
import sqlalchemy as sa





class FormControl():

    def __init__(self):
        pass
        

    def create_where_clause(self,form):
    
        stmt = 'ravdess_metadata.id >= 0'

        if form.sex.data != 'all':
            #print(type(form.sex.data))
            stmt += f' AND ravdess_metadata.sex = "{form.sex.data}"'

        if form.statement.data != 'all':
            stmt += f' AND ravdess_metadata.statement = {form.statement.data}'
        
        print(form.emotion.data)

        

        if len(form.emotion.data) != 0 and form.emotion.data[0] != 'all':
            # for the multiselect, you need a function to
            #   loop through the elements in form.emotion.data
            # may need to tranform the array to a tuple for sql
            em = ['dummy']
            for emo in form.emotion.data:
                em.append(emo)
         

            stmt+= f' AND ravdess_metadata.emotion in {tuple(em)}'

        if form.intensity.data != 'all':
            stmt+= f' AND ravdess_metadata.intensity = {form.intensity.data}'


        return stmt
    
    def get_file_list(self, form, md,session):

        files=[]        
        stmt = sa.select(md).where(sa.text(self.create_where_clause(form)))
        
        for row in session.scalars(stmt):
            files.append(row.filepath)

        return files


    def get_first_file(self,md,session):
        stmt = sa.select(md.filepath)
        return session.scalars(stmt).first()
       
    def set_filter_dict(self, form, sess):

        sess['filter_dict'] = {'sex'         : form.sex.data, 
                                'statement'  : form.statement.data,
                                'emotion'    : form.emotion.data,
                                'intensity'  : form.intensity.data,
                                'num_mels'   : form.mel_filter_count.data,
                                'num_mfcc'   : form.mfcc_count.data}        

    def set_form_data(self,form, sess):

        if 'filter_dict' in sess:
                form.sex.data       = sess['filter_dict']['sex']
                form.statement.data = sess['filter_dict']['statement']
                form.emotion.data   = sess['filter_dict']['emotion']
                form.intensity.data = sess['filter_dict']['intensity']
                
                form.mel_filter_count.data  = sess['filter_dict']['num_mels']
                form.mfcc_count.data        = sess['filter_dict']['num_mfcc']