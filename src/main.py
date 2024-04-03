import pandas as pd
import torch
import scipy.sparse as sparse
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# import calculate_IFF, estimate_IRT_params

# Initial Mongo Atlas Client
username = 'admin'
password ='admin123'
uri = f'mongodb+srv://{username}:{password}@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Query dữ liệu từ Mongo
db = client['dtu']
playersCollection = db['players']
questionsCollection = db['questions']
resultCollection = db['answered_questions']

# cho cái template này vào 1 chỗ khác vì sẽ có nhiều template
# TODO viết thêm template lọc dữ liệu trả về
template = [
    {"$project": {
        "player_id": 1,
        "degree": 1,
        "ability": 1
    }},
    {"$limit": 10}  # Limiting to 500 records
]
pipeline = [
    {
        "$match": {"level": 5}
    },
    {"$project": {
        "_id": 1,
        "major": 1,
        "birth_year": 1,
        "occupation": 1,
        "full_name": 1,
        "email": 1,
        "level": 1,
        "current_assessment_score": 1,
        "correct_ratio": 1
    }},
    {"$limit": 2}  # Limiting to 500 records
]

# Pull dữ liệu từ Atlas
playerDataObject = playersCollection.aggregate(pipeline)
for batch in playerDataObject:
    # Process each batch of data
    # player_ids = batch["player_id"]
    # # player_degree
    # questions_lists = batch["questions"]
    
    # print(f"Processing batch for player IDs: {player_ids}")
    # print(f"Questions lists: {questions_lists}")
    
    print(batch)
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
