from flask import Flask, request, jsonify
import random
from bson.objectid import ObjectId
import bson
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import json


'''
làm cái queue như nào, nó 
'''


app = Flask(__name__)

def initialCLient(username='quan', password='admin'):
    # uri = f'mongodb+srv://{username}:{password}@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
    uri = f'mongodb+srv://quan:admin@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

def get_collection(collection_list=['players', 'questions', 'answered_questions']):
    client = initialCLient()
    db = [client['dtu'][collection] for collection in collection_list]
    return db

playersCollection, questionsCollection, resultCollection = get_collection()

@app.route('/output', methods=["GET"])
def output():
    user_params = request.args
    player_id = user_params.get('player_id')

    pipeline = [
        {
            "$match": {
                "_id": ObjectId(player_id)
            }
        }
    ]
    result = playersCollection.aggregate(pipeline)
     
    if result:
        # return jsonify(list(result))
        return jsonify(json.loads(json_util.dumps(list(result))))
    else:
        return jsonify({'error': 'Player not found'}), 404
    
#TODO find way to store the port value in some where else, avoid manual modify everytime like this
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=31814)
    app.run(debug=True, host='0.0.0.0')

