import pandas as pd
import time
import json
import pprint as pp
import numpy as np
from pprint import pprint
import scipy.sparse as sparse
import pandas as pd

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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

def get_collection(collection_list=['players', 'questions', 'answered_questions']):
    client = initialCLient()
    db = [client['dtu'][collection] for collection in collection_list]
    return db

playersCollection, questionsCollection, resultCollection = get_collection()


# degree = [1,2,3,4,5]
degree = [1]
result = [annoy_knn(degree=index, 
                    players_collection=playersCollection,k=3) # len(result) = k
                    for index in degree] #trả về một object, với mỗi value là 1 object

'''
#TODO nhớ chuyển thành vòng for, hiện tại cho đang tính cho 1 Object
#TODO: cho tên biến mới
'''
def main(input, collection, trucking_size):
    start_time = time.time()
    data_for_algo = query_result_data(input, collection, trucking_size=trucking_size) 

    df = create_dataframe(data_for_algo)
    columns_name_list = df.columns
    row__name_list = df.index
    one_df = pd.DataFrame(1, columns=columns_name_list, index=row__name_list)

    # Tính giá trị phù hợp cho từng người chơi với từng câu hỏi
    df_matrix = np.asarray(df)
    # np.savetxt('array.csv', df_matrix, delimiter=',')
    information_gain = np.asarray(calculate_IFF(df_matrix)).T
    # print(information_gain)

    result = one_df.mul(information_gain)

    top_questions_indices = {}
    for player_id, column in result.items():
        top_indices = column.nlargest(10).index.tolist()
        top_questions_indices[str(player_id)] = top_indices

    pp.pprint(top_questions_indices)

    end_time = time.time()
    total_time = end_time - start_time
    print("Total running time:", total_time, "seconds")

    return top_questions_indices

if __name__ == "__main__":
    start_time = time.time()

    all_result = []
    for i in range(2):
        degree = [1]
        result = [annoy_knn(degree=index, 
                    players_collection=playersCollection,k=3) # len(result) = k
                    for index in degree] #trả về một object, với mỗi value là 1 object
        
        result = main(result[0], resultCollection, trucking_size=10)
        all_result.append(result)

    end_time = time.time()
    total_time = end_time - start_time
    print("Total running time:", total_time, "seconds")

    # all_result = np.array(all_result)
    print(all_result)
    # with open('array.json', 'w') as json_file:
    #     json.dump(all_result, json_file, indent=4)