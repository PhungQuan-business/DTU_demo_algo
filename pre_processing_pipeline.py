import numpy as np

# use for create unique user_id and question_id list
def create_unique_id(input):
    combined_id = np.concatenate(input, axis=0)
    unique_id = np.unique(combined_id)

    return unique_id
