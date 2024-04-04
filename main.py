import pandas as pd
# import torch
import json
import scipy.sparse as sparse
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# from module.processing.pipeline import generate_monogo_template
from module.processing.pre_processing_pipeline import query_result_data

# Initial Mongo Atlas Client
def initialCLient(username, password):
    uri = f'mongodb+srv://{username}:{password}@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

# Đẩy những params này vào config
username = 'admin'
password = 'admin123'
client = initialCLient(username, password)

# Query dữ liệu từ Mongo | chuyển thành function
db = client['dtu']
playersCollection = db['players']
questionsCollection = db['questions']
resultCollection = db['answered_questions']

with open(r'D:\DuyTan_algorithm_demo\sample.json', 'r') as f:
    content = json.load(f)

result =query_result_data(content, resultCollection)

template = [{
        "$project": {
            "player_id": 1,
            "degree": 1,
            "ability": 1,
            "majot":1,
            "mean_time_spent":1,
            "std_time_spent":1,        }
    }]

playerDataObject = playersCollection.aggregate(pipeline)

for doc in result:
    player_questions = doc["questions"]
    for question in player_questions:
        question_id = question["_id"]
        status = question["status"]
        question_statuses[question_id] = status
# iterable_list = [1,2,3]
# pipline_list = generate_monogo_template(r"/Users/phunghongquan/Documents/DuyTan/DTU_demo_algo/config/result_template.json",
#                          [1,2,3])




# Pull dữ liệu từ Atlas
# for pipeline in pipline_list:
#     playerDataObject = playersCollection.aggregate(pipeline)
#     for batch in playerDataObject:
#     # Process each batch of data
#     # player_ids = batch["player_id"]
#     # # player_degree
#     # questions_lists = batch["questions"]
    
#     # print(f"Processing batch for player IDs: {player_ids}")
#     # print(f"Questions lists: {questions_lists}")
    
#         print(batch)
    # Optionally, clear batch from memory
    # del batch
# player_df = pd.DataFrame(list(players_data))



'''
#TODO
thêm tính toán bằng CUDA

dữ liệu đi vào
    mongo query
gọi 2 function để tính

trả về dữ liệu cho từng Player_ID
lưu vào database
'''
