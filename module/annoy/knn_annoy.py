import numpy as np
import random
from annoy import AnnoyIndex

def encode(majors):
    ohe = np.zeros(8, dtype=np.int8)  # Hiện có 8 major
    for major in majors:
        ohe[major] = 1  # Do major đang là số mới làm thế này nhé : )))
    return ohe

# hàm này có thể trả về None khi tất cả người chơi đã được tính toán (status = 1)
# nếu không trả về tối đa k thằng gần nhất
def annoy_knn(degree, players_collection, k=200):
    index = AnnoyIndex(8)  # Hiện có 8 major

    # Pipeline này tìm các document trùng degree và status khác 1 sau đó lấy 2 trường _id và major
    pipeline = [
        {"$match": {"degree": degree, "status": {"$ne": 1}}},
        {"$project": {"major": 1}}
    ]
    data = players_collection.aggregate(pipeline)
    playerIDs_map = {}

    for i, doc in enumerate(data):
        playerIDs_map[i] = doc["_id"]
        index.add_item(i, encode(doc["major"]))
        
    num_of_players = len(playerIDs_map)
    
    # Không còn người chơi nào trong cụm này...
    if num_of_players == 0:
        return

    # building the index
    index.build(n_trees=10)

    # getting indices of nearest neighbors
    nearest_neighbors = index.get_nns_by_item(random.randint(0, num_of_players - 1), 200)

    return (playerIDs_map[idx] for idx in nearest_neighbors) # Trả về generator