# ML-powered applicant performance predictor

This microservice tries to predict whether an applicant is considered to be
qualified for a college program.

## Implementation details

We chose to train the model using all the provided features, except the ones that are not relevant to the Carnegie Mellon University setting. The features we removed are:
* `school`, since the applicants to CMU usually don’t come from one of the two Portuguese schools in the data set.
* `G1` and `G2`, since applicants to CMU usually don’t have grades on a 0–20 scale and grades in the A–F scale can’t be directly mapped to them.

We use [auto-sklearn](https://automl.github.io/auto-sklearn/master/) to train the model and generate predictions. This package automatically applies several ML strategies and identifies which ones work the best.

Using auto-sklearn, we were able to reach 84.8% of accuracy on the training set. This is better than the provided model, which only reaches 79.7% of accuracy under the same circumstances.

## Get Started

### Requirements
* Python 3.8+
* Pipenv with the repository dependencies installed (run `pipenv install`) 
* Linux ([required by auto-sklearn](https://automl.github.io/auto-sklearn/master/installation.html#windows-macos-compatibility), but it is also possible to use the `mfeurer/auto-sklearn:master` Docker image instead and install Flask manually).

### Train the model
The code used to train the model is in the `model_build.ipynb` Jupyter notebook.

### Start the server

To run the Flask API server, execute the following commands from the `app` directory in the pip venv shell.

Set an environment variable for FLASK_APP:
```terminal
export FLASK_APP=app.py
```

To run:
```terminal
pipenv run flask run
```

You can alter the port number that is used by the Flask server by using the `--port` option:

```terminal
pipenv run flask run --port 8080
```

### Use the API endpoint
The `/predict` API endpoint allows you to know the prediction for some input data. A complete API documentation is available in `openapi.yml`.

### Run the automated tests

To run the automated tests, execute the following command from the `app` directory:

```terminal
pipenv run pytest
```
