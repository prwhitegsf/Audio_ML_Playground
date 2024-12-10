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

