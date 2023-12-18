import requests
import pytest
import uuid
import random
import csv
import time



def read_global_token_from_csv():
    with open("token.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "token":
                return row[1]
                  
token = read_global_token_from_csv()  

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    url = "https://im-stg.imdevs.net/_matrix/client/r0/wallet/config"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    data = {

    }
    print("token:" , token)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(10):
        # Make the POST request
        response = requests.get(url, json=data, headers=headers)

        # Validate the response
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        # Assuming the response body is in JSON format
        response_data = response.json()
        print("Response Data :" , response_data)
    end_time = time.time()
    
    diff_time = end_time - start_time
    assert diff_time < 5, f"too slow {diff_time}"



if __name__ == "__main__":
    pytest.main([__file__])







