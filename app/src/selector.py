
from sqlalchemy import text
from app.src.models import ravdess_metadata as md






class DBControl():

    def __init__(self):
        pass
        
    def create_where_clause(self,sess):
    
        stmt = 'ravdess_metadata.id >= 0'

        if sess['filters']['sex'] != 'all':
            #print(type(form.sex.data))
            stmt += f' AND ravdess_metadata.sex = "{sess['filters']['sex']}"'

        if sess['filters']['statement'] != 'all':
            stmt += f' AND ravdess_metadata.statement = {sess['filters']['statement']}'
        
        if len(sess['filters']['emotion']) != 0 and sess['filters']['emotion'][0] != 'all':
            # for the multiselect, you need a function to
            #   loop through the elements in form.emotion.data

            em = ['dummy']
            for emo in sess['filters']['emotion']:
                em.append(emo)
         

            stmt+= f' AND ravdess_metadata.emotion in {tuple(em)}'

        if sess['filters']['intensity'] != 'all':
            stmt+= f' AND ravdess_metadata.intensity = {sess['filters']['intensity']}'

        return stmt



    def get_full_file_list(self,db):
            
        stmt = db.session.execute(db.select(md)).scalars()
        files = [row.filepath for row in stmt]

        return files


    def get_filtered_file_list(self, sess,db):

        stmt = db.session.execute(db.select(md).where(text(self.create_where_clause(sess)))).scalars()  
        files = [row.filepath for row in stmt]
        return files






