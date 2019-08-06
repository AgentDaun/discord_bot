import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjcxZmY4NjEyNTU4OGYwN2EiLCJpYXQiOjE1NjUxMDE5ODYsIm5iZiI6MTU2NTEwMTk4NiwiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjoxMDg3NDYifQ.JdHE1FSoFXEHBwNMqD8k6lytWk1Rqdq5PAzoRMSTrDU"
SERVER_ID = 3717791

API_URL = "https://api.battlemetrics.com/servers/" 


def make_request(token, url, params=None):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers, params=params)
    return r.json()['data']

def get_server_info(server_id=SERVER_ID):
    url = API_URL + str(server_id)
    server_info = make_request(API_TOKEN, url)
    return server_info