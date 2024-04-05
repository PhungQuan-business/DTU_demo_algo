import pandas as pd
# import torch
import json
from pprint import pprint
import scipy.sparse as sparse
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# from module.processing.pipeline import generate_monogo_template
from module.processing.pre_processing_pipeline import query_result_data, create_question_player_matrix
from module.annoy.knn_annoy import annoy_knn
# Initial Mongo Atlas Client
def initialCLient(username='admin', password='admin123'):
    uri = f'mongodb+srv://{username}:{password}@cluster0.jmil5cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0' # cái này đẩy vào configure
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

# Query dữ liệu từ Mongo | chuyển thành function
def get_collection(collection_list=['players', 'questions', 'answered_questions']):
    client = initialCLient()  # Assuming initialCLient() is a function that returns the client
    db = [client['dtu'][collection] for collection in collection_list]
    return db

playersCollection, questionsCollection, resultCollection = get_collection()

# print("Players Collection:", playersCollection,
#       "\n\nQuestions Collection:", questionsCollection,
#       "\n\nAnswered Questions Collection:", resultCollection)

'''

'''
# degree = [1,2,3,4,5]
degree = [1]
result = [annoy_knn(degree=index, players_collection=playersCollection,k=200) 
          for index in degree] #trả về một object, với mỗi value là 1 object
# print(list(result[0]))
data_for_algo = query_result_data(result[0], resultCollection) # trả về
print(data_for_algo)
# matrix  = create_question_player_matrix(result)
# print(matrix)


# thử với degree=1




# print(content)
# result =query_result_data(content, resultCollection)
# print(result[0])



# result = annoy_knn(playersCollection,200) # kết quả trả về là mảng bao gồm id của 200 player

'''
xây pipeline để lấy dữ liệu từ 200 thằng đó ra
'''
# template = [{
#         "$project": {
#             "player_id": 1,
#             "degree": 1,
#             "ability": 1,
#             "majot":1,
#             "mean_time_spent":1,
#             "std_time_spent":1,        }
#     }]

# playerDataObject = playersCollection.aggregate(pipeline)

# for doc in result:
#     player_questions = doc["questions"]
#     for question in player_questions:
#         question_id = question["_id"]
#         status = question["status"]
#         question_statuses[question_id] = status
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
