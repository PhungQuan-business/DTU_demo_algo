from bson.objectid import ObjectId

def query_result_data(user_object_ids, collection):
    pipeline = [
        {"$match": {"player._id": {"$in": [id for id in user_object_ids]}}},
        {"$project": {
            "player_id": {"$toString": "$player._id"},
            "100_ques": "$questions._id",
            "100_ques_result": "$questions.outcome"
        }}
    ]

    result = list(collection.aggregate(pipeline))
    return result

def create_question_player_matrix(user_info):
    question_player_matrix = {}

    for user in user_info:
        player_id = user['player_id']
        questions = user['100_ques']
        results = user['100_ques_result']

        for question, result in zip(questions, results):
            if question not in question_player_matrix:
                question_player_matrix[question] = {}
            question_player_matrix[question][player_id] = result

    return question_player_matrix

# Example usage:
# question_player_matrix = create_question_player_matrix(user_info)
# print(question_player_matrix)


# Example usage:
# user_object_ids = ['6119e085390ae7433f02916b', '6119e08a390ae7433f02916c']
# user_info = extract_user_info(user_object_ids, your_collection)
# print(user_info)
