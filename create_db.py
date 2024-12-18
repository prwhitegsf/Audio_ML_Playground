from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import insert
import os, glob
import pandas as pd
import soundfile
import sys



class CreateRAVDESSMetadata():

    def __init__(self, db_name='db_name', folder='app/static/datasets/RAVDESS/audio/'):
        
        self.emotions = {
            '01':'neutral',
            '02':'calm',
            '03':'happy',
            '04':'sad',
            '05':'angry',
            '06':'fearful',
            '07':'disgust',
            '08':'surprised'
        }

        self.dataset_folder = folder

        self.engine = self.get_engine(db_name)

        self.metadata_obj = MetaData()

        self.rav_table = Table(
            "ravdess_metadata",
            self.metadata_obj,
            Column("id",Integer,primary_key=True),
            Column("filepath",String(100),nullable=False),
            Column("actor",Integer,nullable=False),
            Column("sex",String(10),nullable=False),
            Column("statement",Integer,nullable=False),
            Column("emotion",String(20),nullable=False),
            Column("intensity",Integer,nullable=False),
            Column("sample_rate",Integer,nullable=False),
            Column("filesize",Integer,nullable=False),
        )

        self.metadata_obj.create_all(self.engine)


    def get_engine(self,db_name):
        return create_engine(f'sqlite+pysqlite:///{db_name}')


    def get_angry_label(self, filename):  
        # emotions are the 3rd part of the numerical id   
        if self.emotions[filename.split("-")[2]] == 'angry': return 1 
        else: return 0

    def get_actor(self, filename):
        return int(filename.split("-")[6].split('.')[0]) 
        
    def get_actor_sex(self,filename):
        # gender is the 7th part of the numerical id
        if int(filename.split("-")[6].split('.')[0]) % 2 == 0: return 'female'
        else: return 'male'
   
    def get_sample_rate(self, filename):
        with soundfile.SoundFile(filename) as audio:
            waveform = audio.read(dtype="float32")
            sample_rate = audio.samplerate
            return sample_rate
        

    def get_metadata(self):
        count = 0
        
        for file in glob.glob(f'{self.dataset_folder}Actor_*/*.wav'):
            
            id = count
            file = os.path.normpath(file)
            filename = os.path.basename(file)
            
            actor = self.get_actor(filename)
            sex = self.get_actor_sex(filename)
            statement = filename.split("-")[4]
            emotion = self.emotions[filename.split("-")[2]]
            intensity = filename.split("-")[3]
            #label = self.get_angry_label(filename)
            sample_rate = self.get_sample_rate(file)
            filesize = os.path.getsize(file)

            with self.engine.connect() as connection:

                stmt = insert(self.rav_table).values(
                        id=id,
                        filepath=file,
                        actor=actor,
                        sex=sex,
                        statement=statement,
                        emotion=emotion,
                        intensity=intensity,
                       # label=label,
                        sample_rate=sample_rate,
                        filesize=filesize
                    )
                
                result = connection.execute(stmt)
                connection.commit()
                #print(file)


            count += 1

dbname = 'dbtest.db'

if len(sys.argv) > 1:
    dbname=sys.argv[1]

md = CreateRAVDESSMetadata(db_name=dbname)

md.get_metadata()