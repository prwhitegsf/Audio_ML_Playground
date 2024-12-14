from app.src.models import ravdess_metadata as md
from tests.param_inputs import feature_extraction_filters as fef
from app import db
import pytest
import os.path 


def test_get_all_records_from_db(app, app_ctx):
    stmt = db.session.execute(db.select(md)).all()
    assert len(stmt) == 360


def test_home_response(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Feature Explorer</h1>" in response.data


@pytest.mark.parametrize('filter_data',fef.fe_filter_form_data)
def test_form_filter_responses(client,filter_data):
    response = client.post('/', data=filter_data)
    assert response.status_code == 200


# tests that we never go over the number of available records
def test_next_button(client):
    # this will return 6 records
    response = client.post('/', data=fef.fe_filter_form_least_results)
    assert response.status_code == 200
    # presds the next button 8 times
    for i in range(8):
        response = client.post('/',data={ 'next' : 'Next'})
        assert response.status_code == 200


def test_all_audio_files_exist(app, app_ctx):
   
    stmt = db.session.execute(db.select(md)).scalars()
    files = [row.filepath for row in stmt]
    for fp in files:
        assert os.path.isfile(fp)
   