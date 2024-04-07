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
from module.processing.pre_processing_pipeline import query_result_data, create_dataframe
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

df = create_dataframe(data_for_algo)
print(df)
# tạo matrix-1 cùng chiều với với df
columns_name_list = df.columns
row__name_list = df.index
one_df = pd.DataFrame(1, columns=columns_name_list, index=row__name_list)
# print(one_df)

# Tính giá trị phù hợp cho từng người chơi với từng câu hỏi
df_matrix = np.asarray(df)
information_gain = np.asarray(calculate_IFF(df_matrix)).T
print(information_gain)

result = one_df.mul(information_gain)
print(result)

top_questions_indices = {}
for player_id, column in result.items():
    # Find the indices of the top 10 questions with highest scores
    top_indices = column.nlargest(10).index.tolist()
    # Store the indices in the dictionary
    top_questions_indices[player_id] = top_indices

print(top_questions_indices)

# '''
# note for commit comment:
# delete estimate_params.py file
# '''
