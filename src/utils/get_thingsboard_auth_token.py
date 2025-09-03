import requests

def get_thingsboard_auth_token():
    auth_response = requests.post(
        "https://thingsboard.cloud:443/api/auth/login",
        json={
            "username": "philippe.rivard@macso.ai",
            "password": "ceRh7tTaa@UEjv4"
        }
    )
    auth_token = auth_response.json()['token']\

    return auth_token