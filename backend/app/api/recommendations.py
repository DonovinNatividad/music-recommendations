from fastapi import APIRouter
from pydantic import BaseModel
import requests
from utils.token_manager import token_manager
from dotenv import load_dotenv
import os

# These are all imported for the login library 
from fastapi.responses import RedirectResponse, JSONResponse
import random
import string
import urllib.parse

# Load environment variables from .env file
load_dotenv()

api = APIRouter()

class RecommendationRequest(BaseModel):
    seed_tracks: list[str]

def get_access_token():
    token = token_manager.token
    return {'Authorization': f'Bearer {token}'}

def generate_random_string(length: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@api.get('/login')
def login():
    state = generate_random_string(16)
    scope = 'user-read-private user-read-email'
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URI').strip()
    
    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }
    
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
    return RedirectResponse(url)

@api.get('/callback')
def callback(code: str, state: str):
    # Check if code and state are received properly
    print(f"Received code: {code}, state: {state}")
    
    # Grab the success URI
    redirect_uri = os.getenv('REDIRECT_URI').strip()

    # Validate that you received a valid code and state
    if not code or not state:
        return JSONResponse(content={"error": "Missing code or state"}, status_code=400)

    # Exchange the authorization code for a token
    user_token = token_manager.get_user_token(code, redirect_uri)
    
    return JSONResponse(content={'message': 'Authorization successful', 'token': user_token}, status_code=200)


@api.post('/recommendations')
def get_recommendations(request: RecommendationRequest):
    
    # Call util function to get the access token 
    headers = get_access_token()
    
    response = requests.get(f"https://api.spotify.com/v1/recommendations?limit=5&seed_tracks={','.join(request.seed_tracks)}", headers=headers)
    
    # Get JSON Response
    json_response = response.json()
    
    # Return the 'tracks' part of the response if it exists
    tracks = json_response.get('tracks', {'error': 'Tracks not found'})

    ret = []

    # Find out how to index the artists in the json object
    for track in tracks:
        artists = track.get('artists', '')
        artist_str = artists[0].get('name', 'No artist found')
        for i in range(1, len(artists)):
            artist_str += f", {artists[i].get('name', 'No artist found')}"
        
        if not artist_str:
            artist_str = 'No artist found'
            
        ret.append((track.get('name', 'No song name'), f'By {artist_str}'))
    
    return ret
