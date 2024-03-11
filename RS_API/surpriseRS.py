from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
import random
from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import os

from config import SAVED_MODEL


# Initialize mongoDB connection
 
# mongo_host = os.environ.get('MONGO_HOST')
# mongo_port = int(os.environ.get('MONGO_PORT'))
# client = MongoClient(mongo_host, mongo_port)

client = MongoClient('mongodb://localhost:27017/')
db = client['database-name']
collections = db['fact-table-name']

# app = Flask(__name__)
# api = Api(app)

# @app.route("/get_prediction", method=["GET"])
# def generate_and_predict(SAVED_MODEL, uid, iid):
#     """Generates a random user-item pair and makes a prediction."""
#     uid = str(random.randrange(6040))
#     iid = str(random.randrange(3952))
#     result = SAVED_MODEL.predict(uid, iid, r_ui=4, verbose=False)
#     response = jsonify(result)
#     return result

app = Flask(__name__)

SAVED_MODEL = SAVED_MODEL


@app.route('/')
def hello_world():
    return "Hello world"


@app.route("/get_prediction", methods=["GET"])
def generate_and_predict():
    # Extract uid and iid from request parameters
    uid = str(request.args.get('uid'))
    iid = str(request.args.get('iid'))

    # Perform prediction using your model
    if SAVED_MODEL:
        # Replace this with your actual prediction logic
        # Here, we're just returning random values
        # result = {'uid': uid, 'iid': iid, 'prediction': random.uniform(0, 5)}
        result = SAVED_MODEL.predict(uid, iid, r_ui=4, verbose=False)
    else:
        result = {'error': 'Model not loaded'}

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
