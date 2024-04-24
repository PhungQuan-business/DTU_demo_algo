import pandas as pd
import numpy as np
import random
import torch
import implicit
import scipy.sparse as sparse

import json
import bson
from bson import json_util
from bson.objectid import ObjectId

from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from py_irt.config import IrtConfig
from py_irt.training import IrtModelTrainer
from py_irt.dataset import Dataset

'''
làm cái queue như nào, nó ở trong hay ngoài thuật toán
    cách lữu trữ của queue như nào, fix hay dynamic
    bao giờ thì fecth cái bacth đó cho thuật toán

#TODO viết lại api để đầu vào là mảng hoặc object
#TODO sửa lại pipeline để query theo bacth 
'''


def initialCLient(username='quan', password='admin'):
    # uri = f'mongodb+srv://{username}:{password}@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
    # cái này đẩy vào configure
    uri = f'mongodb+srv://quan:admin@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
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


def recommend(batch):
    data = get_player_data(batch)
    result = {}
    for d in data:
        dataset = d['response']
        iff = calculate_IFF(dataset)
        rating = [iff[x, y].item() for x, y in zip(
            dataset.observation_subjects, dataset.observation_items)]
        sparse_player_ques = sparse.csr_matrix(
            (
                rating,
                (dataset.observation_subjects,
                 dataset.observation_items),
            )
        )
        model = implicit.als.AlternatingLeastSquares()
        model.fit(sparse_player_ques)
        for player_id, player_ix in dataset.subject_id_to_ix.items():
            ids, _ = model.recommend(
                player_ix, sparse_player_ques[player_ix], N=10, filter_already_liked_items=True
            )
            result[ObjectId(player_id)] = [
                ObjectId(dataset.ix_to_item_id[id]) for id in ids]
    return result


def get_player_data(batch):
    threshold = 0
    clusters = player_clustering(batch)

    for cluster in clusters:
        player_ids = cluster['player_df']['_id'].to_list()
        pipeline = [
            {
                "$match": {
                    "player": {"$in": [id for id in player_ids]}
                }
            },
            {"$unwind": "$questions"},  # Unwind the sliced questions array
            {
                "$project": {
                    "_id": 0,
                    "player": 1,
                    "question_id": {"$toString": "$questions._id"},
                    "outcome": "$questions.outcome"
                }
            },
        ]
        df = pd.DataFrame(
            resultCollection.aggregate(pipeline))
        df = df.pivot(index='player',
                      columns='question_id', values='outcome')

        # Tính tổng của từng cột
        column_sums = df.sum()
        # Chọn các cột có tổng lớn hơn hoặc bằng threshold
        selected_columns = column_sums[column_sums >= threshold].index
        # Loại bỏ các cột không đáp ứng điều kiện
        df = df[selected_columns]
        df['player_id'] = df.index

        # Đầu vào của py_irt
        data = Dataset.from_pandas(df, subject_column="player_id")
        cluster['response'] = data

    return clusters


def player_clustering(batch):
    # Số cụm phân thành
    n_clusters = 5

    pipeline = [
        {
            "$match": {
                "_id": {"$in": [id for id in batch]}
            }
        },
        {
            "$project": {
                "_id": 1,
                "major": 1
            }
        },
    ]

    df = pd.DataFrame(playersCollection.aggregate(pipeline))

    major_dummies = pd.get_dummies(df["major"].explode())
    major_dummies = major_dummies.groupby(major_dummies.index).sum()

    kmeans = KMeans(n_clusters=n_clusters, init='k-means++').fit(major_dummies)

    df['label'] = kmeans.labels_

    clusters = []

    for _, group in df.groupby('label'):
        clusters.append({'player_df': group[['_id', 'major']]})

    return clusters


def estimate_params(dataset, **config):
    # num_of_players = len(dataset.ix_to_subject_id)
    # num_of_questions = len(dataset.ix_to_item_id)
    # print(num_of_questions)
    # if (num_of_players * num_of_questions > 50000): # if the data is large enough
    #     device = 'cuda' if torch.cuda.is_available() else 'cpu' # Use CUDA if exists
    # else:
    #     device = 'cpu' # Use CPU only
    device = 'cpu'

    # Config for IRT
    config = IrtConfig(model_type='2pl', **config)
    # Create a trainer
    trainer = IrtModelTrainer(dataset=dataset, data_path=None, config=config)
    # Start the training process
    trainer.train(device=device)

    return trainer.irt_model.export()


def calculate_IFF(dataset):
    device = torch.device(
        'cuda') if torch.cuda.is_available() else torch.device('cpu')

    params = estimate_params(dataset, epochs=100, priors='hierarchical')

    alpha = torch.tensor(params['disc'], device=device)
    beta = torch.tensor(params['diff'], device=device)
    theta = torch.tensor(params['ability'], device=device)

    theta = theta.unsqueeze(1)
    argument = alpha * (theta - beta)
    P_i = 1 / (1 + torch.exp(-argument)).squeeze()

    Q_i = 1 - P_i
    information_gain = torch.square(alpha) * (P_i) * (Q_i)

    return information_gain


app = Flask(__name__)


@app.route('/process_batch')
def process_batch():
    data = request.json
    playersObjectId = data['playersObjectId']
    # cần thống nhất lại xem param có bao gồm "ObjectID" không
    # 1 batch
    object_ids_batch = [ObjectId(id) for id in playersObjectId[0]]

    result = recommend(object_ids_batch)
    if result:
        result_str = {str(key): [str(oid) for oid in value]
                      for key, value in result.items()}
        # Convert to JSON
        json_result = json.dumps(result_str)
        print(json_result)
        return jsonify(json_result)
    else:
        return jsonify({'error': 'Player not found'}), 404


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=31814)
    app.run(debug=True, host='0.0.0.0')

# ----------Testing----------------

# def read_player_ids(filename, batch_size, truncate=None):
#     with open(filename, 'r') as file:
#         player_ids = [line.strip() for line in file]

#     # If truncate is None, default to 1000
#     if truncate is None:
#         truncate = 1000
#     # If truncate is 'all', take all values in the input file
#     elif truncate == 'all':
#         truncate = len(player_ids)

#     # Truncate the list if necessary
#     player_ids = player_ids[:truncate]

#     # Shuffle the player IDs to randomize
#     random.shuffle(player_ids)

#     # Split into batches
#     player_ids_batches = [player_ids[i:i+batch_size] for i in range(0, len(player_ids), batch_size)]
#     return player_ids_batches


# def process_batch():
#     playersObjectId = read_player_ids('objectid_v2.txt', 100)
#     object_ids = [ObjectId(id) for id in playersObjectId[0]]
#     # print(object_ids)
#     # get_player_data(object_ids)
#     recommend_result = recommend(object_ids)
#     print(recommend_result)

# process_batch()
