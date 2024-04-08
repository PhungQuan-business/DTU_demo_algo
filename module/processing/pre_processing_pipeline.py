from bson.objectid import ObjectId
import numpy as np
import pandas as pd

# TODO đổi lại cái trucking về mặc định là 200
# query những người
def query_result_data(user_object_ids, collection, trucking_size:int=None):
    if trucking_size is None:
        trucking_size = 100
    
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
    },
    # {"$group": {"player_id"}}
    ]

    '''
    If the $group stage exceeds 100 megabytes of RAM, MongoDB writes data to temporary files. 
    However, if the allowDiskUse option is set to false, $group returns an error. 
    For more information, refer to Aggregation Pipeline Limits.
    '''
#     pipeline = [
#     {
#         "$match": {
#             "player._id": {"$in": [id for id in user_object_ids]}
#         }
#     },
#     {
#         "$project": {
#             "_id": 0,
#             "player_id": 1,
#             "question_id": "$questions._id",
#             "outcome": "$questions.outcome"
#         }
#     },
#     {
#         "$group": {
#             "_id": "$question_id",
#             "player_outcomes": {
#                 "$push": {
#                     "player_id": "$player_id",
#                     "outcome": "$outcome"
#                 }
#             }
#         }
#     },
#     {
#         "$project": {
#             "question_id": "$_id",
#             "_id": 0,
#             "player_outcomes": 1
#         }
#     },
#     {
#         "$unwind": "$player_outcomes"
#     },
#     {
#         "$group": {
#             "_id": "$question_id",
#             "player_outcomes": {
#                 "$push": {
#                     "player_id": "$player_outcomes.player_id",
#                     "outcome": "$player_outcomes.outcome"
#                 }
#             }
#         }
#     },
#     {
#         "$project": {
#             "question_id": "$_id",
#             "_id": 0,
#             "player_outcomes": 1
#         }
#     },
#     {
#         "$replaceRoot": {"newRoot": "$player_outcomes"}
#     }
# ]

    result = list(collection.aggregate(pipeline))
    
    return result


def create_dataframe(player_question_data):
    # Convert player_question_data into DataFrame
    df = pd.DataFrame(player_question_data)
    matrix = df.pivot(index='question_id', columns='player_id', values='outcome')
    # matrix = matrix.fillna(0)

    return matrix
