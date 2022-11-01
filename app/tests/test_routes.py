from flask import Flask
import pytest
from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_predict_allFields():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    data = {
        "sex": "F",
        "age" : 18,
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "A",
        "Medu": 4,
        "Fedu": 4,
        "Mjob:": "at_home",
        "Fjob": "teacher",
        "reason" : "course",
        "guardian": "mother",
        "traveltime": 2,
        "studytime": 2,
        "failures": 0,
        "schoolsup": True,
        "famsup": False,
        "paid": False,
        "activities": False,
        "nursery": True,
        "higher": True,
        "internet": False,
        "romantic": False,
        "famrel": 4,
        "freetime": 3,
        "goout": 4,
        "Dalc": 1,
        "Wcal": 1,
        "health": 3,
        "absences": 6
    }
    response = client.get('/predict', json = data)
    output = response.get_data()
    assert response.status_code == 200
    assert output == data
    assert response.headers.get('Content-Type') == 'application/json'

def test_predict_age_missing():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    data = {
        "age" : 18,
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "A",
        "Medu": 4,
        "Fedu": 4,
        "Mjob:": "at_home",
        "Fjob": "teacher",
        "reason" : "course",
        "guardian": "mother",
        "traveltime": 2,
        "studytime": 2,
        "failures": 0,
        "schoolsup": True,
        "famsup": False,
        "paid": False,
        "activities": False,
        "nursery": True,
        "higher": True,
        "internet": False,
        "romantic": False,
        "famrel": 4,
        "freetime": 3,
        "goout": 4,
        "Dalc": 1,
        "Wcal": 1,
        "health": 3,
        "absences": 6
    }
    response = client.get('/predict', json = data)
    output = response.get_data()
    assert response.status_code == 400

def test_predict_age_missing():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    data = {
        "sex": "F",
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "A",
        "Medu": 4,
        "Fedu": 4,
        "Mjob:": "at_home",
        "Fjob": "teacher",
        "reason" : "course",
        "guardian": "mother",
        "traveltime": 2,
        "studytime": 2,
        "failures": 0,
        "schoolsup": True,
        "famsup": False,
        "paid": False,
        "activities": False,
        "nursery": True,
        "higher": True,
        "internet": False,
        "romantic": False,
        "famrel": 4,
        "freetime": 3,
        "goout": 4,
        "Dalc": 1,
        "Wcal": 1,
        "health": 3,
        "absences": 6
    }
    response = client.get('/predict', json = data)
    output = response.get_data()
    assert response.status_code == 400