from fastapi import APIRouter
from pydantic import BaseModel
import requests
from utils.token_manager import token_manager

api = APIRouter()

class RecommendationRequest(BaseModel):
    seed_tracks: list[str]

def get_access_token():
    token = token_manager.get_token()
    return {'Authorization': f'Bearer {token}'}

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
