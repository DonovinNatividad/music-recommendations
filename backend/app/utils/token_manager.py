import requests
import base64
import os
from dotenv import load_dotenv
import time


load_dotenv()

class TokenManager:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.token = None
        self.token_expiry = 0
    
    def _get_new_token(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = {
            'Authorization': f'Basic {self._encode_credentials()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        auth_data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(auth_url, headers=auth_header, data=auth_data)
        response_data = response.json()
        self.token = response_data['access_token']
        self.token_expiry = time.time() + response_data['expires_in']
    
    def _encode_credentials(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()
    
    def get_token(self):
        if self.token is None or time.time() >= self.token_expiry:
            self._get_new_token()
        return self.token

token_manager = TokenManager()
