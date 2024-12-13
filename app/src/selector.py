import app.main.forms as forms
import sqlalchemy as sa





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
            # may need to tranform the array to a tuple for sql
            em = ['dummy']
            for emo in sess['filters']['emotion']:
                em.append(emo)
         

            stmt+= f' AND ravdess_metadata.emotion in {tuple(em)}'

        if sess['filters']['intensity'] != 'all':
            stmt+= f' AND ravdess_metadata.intensity = {sess['filters']['intensity']}'


        return stmt



    def get_full_file_list(self, md, session):
        
        files=[]        
        stmt = sa.select(md)
        
        for row in session.scalars(stmt):
            files.append(row.filepath)

        return files


    def get_file_list(self, sess, md,session):

        files=[]        
        #stmt = sa.select(md).where(sa.text(self.create_where_clause(sess)))
        stmt = sa.select(md)
        
        for row in session.scalars(stmt):
            files.append(row.filepath)

        return files


    def get_first_file(self,md,session):
        stmt = sa.select(md.filepath)
        return session.scalars(stmt).first()




