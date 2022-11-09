from app.handlers.validation import *
from flask import jsonify, request
import joblib
import pandas as pd
import os


def configure_routes(app):
    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    schema = [
        NumericParameter('Dalc', 1, 5),
        NumericParameter('Fedu', 0, 4),
        NominalParameter('Fjob', ['teacher', 'health', 'services', 'at_home', 'other']),
        NumericParameter('Medu', 0, 4),
        NominalParameter('Mjob', ['teacher', 'health', 'services', 'at_home', 'other']),
        BinaryParameter('Pstatus', 'T', 'A'),
        NumericParameter('Walc', 1, 5),
        NumericParameter('absences', 0, 93),
        BinaryParameter('activities', 'true', 'false'),
        BinaryParameter('address', 'U', 'R'),
        NumericParameter('age', 15, 22),
        NumericParameter('failures', 1, 4),
        NumericParameter('famrel', 1, 5),
        BinaryParameter('famsize', 'LE3', 'GT3'),
        BinaryParameter('famsup', 'true', 'false'),
        NumericParameter('freetime', 1, 5),
        NumericParameter('goout', 1, 5),
        NominalParameter('guardian', ['mother', 'father', 'other']),
        NumericParameter('health', 1, 5),
        BinaryParameter('higher', 'true', 'false'),
        BinaryParameter('internet', 'true', 'false'),
        BinaryParameter('nursery', 'true', 'false'),
        BinaryParameter('paid', 'true', 'false'),
        NominalParameter('reason', ['home', 'reputation', 'course', 'other']),
        BinaryParameter('romantic', 'true', 'false'),
        BinaryParameter('schoolsup', 'true', 'false'),
        BinaryParameter('sex', 'F', 'M'),
        NumericParameter('studytime', 1, 4),
        NumericParameter('traveltime', 1, 4),
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

        # Wrap values in pandas series
        model_input_series = {}
        for parameter in model_input:
            model_input_series[parameter] = pd.Series(model_input[parameter])

        # Run the model
        query_df = pd.DataFrame(model_input_series)
        prediction = clf.predict(query_df)[0]

        return jsonify({'isQualified': bool(prediction == 1)})
