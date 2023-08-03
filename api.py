import os

def get_api_data():
    headers = {
        "X-RapidAPI-Key": os.environ['API_KEY'],
        "X-RapidAPI-Host": os.environ['API_HOST']
    }

    return headers