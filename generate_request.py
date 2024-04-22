import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import time
import random

# Function to make request with player_id
def make_request(player_id):
    url = 'http://192.168.49.2:30796/output'
    params = {'player_id': player_id}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # print(f"Player ID {player_id}: {response.text}")
        # print('ok')
        pass
    else:
        print(f"Error for Player ID {player_id}: {response.status_code}")

# Read player IDs from file
def read_player_ids(filename):
    with open(filename, 'r') as file:
        player_ids = [line.strip() for line in file]
    return player_ids

# Main function
def main():
    filename =  r'/home/quan/Documents/DTU_demo_algo/new_objectidv1.txt'  # File containing player IDs, one per line
    player_ids = read_player_ids(filename)
    # random_player_id = player_ids[:100]
    random_player_id = random.sample(player_ids, k=10000)

    # start_time = time.time()
    # for id in random_player_id:
    #     try:
    #         make_request(id)
    #     except KeyboardInterrupt:
    #         print("Ctrl+C detected. Shutting down...")
    #         sys.exit(1)
    # Number of concurrent requests
    max_workers = 20
    # for i in range(10):
    start_time = time.time()   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        try:
            executor.map(make_request, random_player_id)
        except KeyboardInterrupt:
            print("Ctrl+C detected. Shutting down...")
            executor.shutdown(wait=False)
            sys.exit(1)
    end_time = time.time()
    time_took = end_time - start_time
    print(f'Time it took to process 10000 request with parallel processing the time is: ', time_took)

if __name__ == "__main__":
    main()
