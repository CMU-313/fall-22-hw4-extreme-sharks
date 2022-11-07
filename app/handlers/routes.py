from app.handlers.validation import *
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os


def configure_routes(app):
    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    # clf = joblib.load(model_path)

    schema = [
        BinaryParameter('sex', 'F', 'M'),
        NumericParameter('age', 15, 22),

        BinaryParameter('address', 'U', 'R'),
        BinaryParameter('famsize', 'LE3', 'GT3'),
        BinaryParameter('Pstatus', 'T', 'A'),

        NumericParameter('Medu', 0, 4),
        NumericParameter('Fedu', 0, 4),

        NominalParameter('Mjob', ['teacher', 'health', 'services', 'at_home', 'other']),
        NominalParameter('Fjob', ['teacher', 'health', 'services', 'at_home', 'other']),
        NominalParameter('reason', ['home', 'reputation', 'course', 'other']),
        NominalParameter('guardian', ['mother', 'father', 'other']),

        NumericParameter('traveltime', 1, 4),
        NumericParameter('studytime', 1, 4),
        NumericParameter('failures', 1, 4),

        BinaryParameter('schoolsup', 'true', 'false'),
        BinaryParameter('famsup', 'true', 'false'),
        BinaryParameter('paid', 'true', 'false'),
        BinaryParameter('activities', 'true', 'false'),
        BinaryParameter('nursery', 'true', 'false'),
        BinaryParameter('higher', 'true', 'false'),
        BinaryParameter('internet', 'true', 'false'),
        BinaryParameter('romantic', 'true', 'false'),

        NumericParameter('famrel', 1, 5),
        NumericParameter('freetime', 1, 5),
        NumericParameter('goout', 1, 5),
        NumericParameter('Dalc', 1, 5),
        NumericParameter('Walc', 1, 5),
        NumericParameter('health', 1, 5),
        NumericParameter('absences', 0, 93),
    ]

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/predict')
    def predict():
        # Parse and validate the input
        try:
            model_input = validate_model_parameters(request.args, schema)
        except ValidationError as validation_error:
            return jsonify({'error': validation_error.message}), 400

        return jsonify(model_input)

        # use entries from the query string here but could also use json
        age = request.args.get('age')
        absences = request.args.get('absences')
        health = request.args.get('health')
        data = [[age], [health], [absences]]

        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })

        # prediction = clf.predict(query)
        # prediction = 1
        # return jsonify(np.ndarray.item(prediction))
        return jsonify({'isQualified': True})
