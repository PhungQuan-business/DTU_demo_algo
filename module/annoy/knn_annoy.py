import numpy as np
from annoy import AnnoyIndex

def encode(majors):
    ohe = np.zeros(8, dtype=np.int8)  # Hiện có 8 major
    for major in majors:
        ohe[major] = 1  # Do major đang là số mới làm thế này nhé : )))
    return ohe

# player là dict kiểu {"_id": ObjID(), "major": [], "degree": 1, ...}
# players_collection là cái Collection của PyMongo ấy, hoặc sửa lại tùy :vvv
def annoy_knn(player, players_collection, k=200):
    # Kiểm tra xem đã có kết quả dự đoán chưa
    # Nếu có trả về j đó :vvvv
    if players_collection.find_one({'_id': player["_id"], 'status': 1}):
        return

    index = AnnoyIndex(8)  # Hiện có 8 major

    pipeline = [
        {"$match": {"degree": player["degree"]}},
        {"$project": {"major": 1}}
    ]
    data = players_collection.aggregate(pipeline)
    playerIDs_map = {}

    for i, doc in enumerate(data):
        playerIDs_map[i] = doc["_id"]
        index.add_item(i, encode(doc["major"]))

    # building the index
    index.build(n_trees=10)

    # getting indices of nearest neighbors
    nearest_neighbors = index.get_nns_by_vector(encode(player["major"]), k)

    return (playerIDs_map[idx] for idx in nearest_neighbors) # Trả về generator