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
    
    def _encode_credentials(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def _set_new_token(self, grant_type='client_credentials', authorization_code=None, redirect_uri='http://localhost:8000'):
        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {self._encode_credentials()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': grant_type
        }
        
        if grant_type == 'authorization_code':
            data.update({
                'code': authorization_code,
                'redirect_uri': redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        
        if response.status_code == 200:
            response_data = response.json()
            self.token = response_data['access_token']
            self.token_expiry = time.time() + response_data['expires_in']
        else:
            # Handle errors
            response_data = response.json()
            error_message = response_data.get('error_description', 'Unknown error')
            print(f"Error obtaining token: {error_message}")
            raise Exception(f"Token request failed: {error_message}")

    def get_user_token(self, authorization_code=None, redirect_uri=None):
        """Get token using Authorization Code Flow (user-specific data)"""
        if self.token is None or time.time() >= self.token_expiry:
            self._set_new_token(grant_type='authorization_code', authorization_code=authorization_code, redirect_uri=redirect_uri)
        return self.token

    def get_app_token(self):
        """Get token using Client Credentials Flow (public data)"""
        if self.token is None or time.time() >= self.token_expiry:
            self._set_new_token(grant_type='client_credentials')
        return self.token

token_manager = TokenManager()