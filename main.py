import pandas as pd
# import torch
import json
import numpy as np
from pprint import pprint
import scipy.sparse as sparse
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# from module.processing.pipeline import generate_monogo_template
from module.processing.pre_processing_pipeline import query_result_data, create_question_player_matrix, create_dataframe
from module.annoy.knn_annoy import annoy_knn
from module.algorithm.calculate_IFF import calculate_IFF

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
    client = initialCLient()
    db = [client['dtu'][collection] for collection in collection_list]
    return db

playersCollection, questionsCollection, resultCollection = get_collection()

# print("Players Collection:", playersCollection,
#       "\n\nQuestions Collection:", questionsCollection,
#       "\n\nAnswered Questions Collection:", resultCollection)

# degree = [1,2,3,4,5]
degree = [1]
result = [annoy_knn(degree=index, 
                    players_collection=playersCollection,k=3) # len(result) = k
                    for index in degree] #trả về một object, với mỗi value là 1 object

'''
#TODO nhớ chuyển thành vòng for, hiện tại cho đang tính cho 1 Object
#TODO: cho tên biến mới
'''
data_for_algo = query_result_data(result[0], resultCollection, trucking_size=5) 

# print(data_for_algo)
df= create_dataframe(data_for_algo)
df_matrix = np.asarray(df)

# print(df_matrix)
information_gain = calculate_IFF(df_matrix)
print(information_gain)

'''
note for commit comment:
delete estimate_params.py file
'''