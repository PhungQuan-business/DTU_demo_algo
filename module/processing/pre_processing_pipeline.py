from bson.objectid import ObjectId
import numpy as np


def query_result_data(user_object_ids, collection, trucking:int=None):
    if trucking is None:
        trucking = 10
    pipeline = [
        {"$match": {"player._id": {"$in": [id for id in user_object_ids]}}},
        {"$project": {
            "_id": 0,
            "player_id": {"$toString": "$player._id"},
            "100_ques": {"$slice": ["$questions._id", trucking]},
            # "100_ques_result": "$questions.outcome"
            "100_ques_result": {"$slice": ["$questions.outcome", trucking]}
        }}
    ]

    # pipeline2 = [
    #     {"$match": {"player._id": {"$in": [id for id in user_object_ids]}}},
    #     {"$project": {
    #         "player_id": {"$toString": "$player._id"},
    #         "questions": {"$slice": ["$questions._id", 10]},  # Take first 10 questions
    #         "results": {"$slice": ["$questions.outcome", 10]}  # Take first 10 results
    #     }},
        # {"$unwind": "$questions"},
        # {"$unwind": "$results"},
        # {"$project": {
        #     "player_id": 1,
        #     "Question_ID": "$questions._id",
        #     "Result": "$results"
        # }}
    # ]

    result = list(collection.aggregate(pipeline))

    
    return result

'''
# TODO:
điều kiện check input phải là numpy(không cần nữa)
điều chỉnh lại input đầu vào
'''

def create_question_player_matrix(data):
     # Get unique questions and players
    all_questions = set()
    all_players = set()
    for player_data in data:
        all_questions.update(player_data['100_ques'])
        all_players.add(player_data['player_id'])

    # Create nan matrix
    nan_matrix = np.empty((len(all_questions), len(all_players)))
    nan_matrix[:] = np.nan
    
    question_to_index = {question: index for index, question in enumerate(all_questions)}
    
    # Fill in matrix with player data
    for player_data in data:
        player_id = player_data['player_id']
        questions = player_data['100_ques']
        results = player_data['100_ques_result']
        
        player_index = list(all_players).index(player_id)
        
        for question, result in zip(questions, results):
            question_index = question_to_index[question]
            nan_matrix[question_index, player_index] = result
    
    return nan_matrix, list(all_questions), list(all_players)

import pandas as pd

def create_dataframe(player_question_data):
    # Convert player_question_data into DataFrame
    df = pd.DataFrame(player_question_data)

    # Explode '100_ques' and '100_ques_result' columns
    # df = df.explode('100_ques').explode('100_ques_result')
    df1 = df[['player_id', '100_ques']]
    df1 = df1.explode('100_ques')

    df2 = df[['player_id', '100_ques_result']]
    df2 = df2.explode("100_ques_result")
    
    merged_df = pd.merge(df1, df2, on='player_id')
    merged_df = merged_df.drop_duplicates(subset='player_id')
    return merged_df
    # Rename columns
    merged_df.rename(columns={'100_ques': 'Question_ID', '100_ques_result': 'Result'}, inplace=True)

    # Convert 'player_id' to string
    merged_df['player_id'] = merged_df['player_id'].astype(str)
    excel_file_path = r'D:\DuyTan_algorithm_demo\output.csv'
    merged_df.to_csv(excel_file_path, index=False)

    return merged_df

# Example usage:
# df = create_dataframe(player_question_data)
# print(df)
