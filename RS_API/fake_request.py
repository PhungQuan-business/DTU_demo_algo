import requests
import random

# Make 20 requests
for _ in range(20):
    # Generate random uid and iid
    uid = str(random.randint(1, 6040))
    iid = str(random.randint(1, 3952))

    # Make request to Flask server
    url = 'http://127.0.0.1:5000/get_prediction'
    params = {'uid': uid, 'iid': iid}
    response = requests.get(url, params=params)

    # Print response
    print(response.json())
