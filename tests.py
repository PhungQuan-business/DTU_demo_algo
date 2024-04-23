import random

def read_player_ids(filename, batch_size, truncate=None):
    with open(filename, 'r') as file:
        player_ids = [line.strip() for line in file]
        
        # If truncate is None, default to 1000
        if truncate is None:
            truncate = 100
        # If truncate is 'all', take all values in the input file
        elif truncate == 'all':
            truncate = len(player_ids)
        
        # Truncate the list if necessary
        player_ids = player_ids[:truncate]
    
    # Shuffle the player IDs to randomize
    random.shuffle(player_ids)
    
    # Split into batches
    player_ids_batches = [player_ids[i:i+batch_size] for i in range(0, len(player_ids), batch_size)]
    return player_ids_batches

result = read_player_ids('new_objectidv1.txt', 20, 200)
print(result)