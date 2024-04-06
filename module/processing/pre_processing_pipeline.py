from bson.objectid import ObjectId
import numpy as np


# TODO đổi lại cái trucking về mặc định là 200
def query_result_data(user_object_ids, collection, trucking_size:int=None):
    if trucking_size is None:
        trucking_size = 200
    
    pipeline = [
    {
        "$match": {
            "player._id": {"$in": [id for id in user_object_ids]}
        }
    },
    {
        "$project": {
            "player_id": {"$toString": "$player._id"},
            "questions": {"$slice": ["$questions", trucking_size]}  # Slice the questions array to limit its size
        }
    },
    {"$unwind": "$questions"},  # Unwind the sliced questions array
    {
        "$project": {
            "_id": 0,
            "player_id": 1,
            "question_id": "$questions._id",
            "outcome": "$questions.outcome"
        }
    }
    ]

    result = list(collection.aggregate(pipeline))

    
    return result

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
    matrix = df.pivot(index='question_id', columns='player_id', values='outcome')
    # matrix = matrix.fillna(0)

    return matrix

# Example usage:
# df = create_dataframe(player_question_data)
# print(df)
