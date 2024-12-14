from app.src.models import ravdess_metadata as md
from app import db



def test_get_all_records_from_db(app):
    stmt = db.session.execute(db.select(md)).all()
    assert len(stmt) == 360


    

