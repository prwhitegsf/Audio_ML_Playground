import app.src.models as model
import sqlalchemy as sa
from  config import Config
import os

'''
def test_write_to_database(session):
    new_record = model.ravdess_metadata(
            filepath="somepath",
            actor=1,
            sex='female',
            statement='1',
            emotion='angry',
            intensity=1,
            label=1,
            sample_rate=48000,
            filesize=100
    )
    
    session.add(new_record)
    session.commit()

    out = sa.select(model.ravdess_metadata).where(model.ravdess_metadata.actor == 1)
    result = session.execute(out).all()
    


    assert len(result) == 1
'''


def test_get_record_from_db(session):
    stmt = sa.select(model.ravdess_metadata)
    result = session.execute(stmt).all()

    assert len(result) == 360

