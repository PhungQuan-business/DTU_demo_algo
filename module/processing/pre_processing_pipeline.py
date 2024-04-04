import numpy as np
import pymongo
from bson import ObjectId
'''
đầu vào là danh sách id của 200 player
'''
def query_result_data(playerObjectIdList, collection):
    # query = {"_id": {"$in": [ObjectId(player_id) for player_id in playerObjectIdList['nearest_players']]}}
    # query = [collection.find({"player._id": ObjectId:f'{player_id}'} for player_id in playerObjectIdList['nearest_players'])]
    000
    query = [collection.find({'player._id':ObjectId(player_id)}) for player_id in playerObjectIdList['nearest_players']]
    # print(query)

    # # lấy được 
    # cursor = collection.find(query)

    # for player_data in cursor:
    # # Process each player's data as needed
    #     print(player_data)

    # # Close the cursor, and free resources
    # cursor.close()
