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

    # params = {
    #     'seed_tracks': ','.join(request.seed_tracks),
    #     'limit': 5, 
    #     # Number of recommendations to return to user
    # }
    
    response = requests.get(f"https://api.spotify.com/v1/recommendations?limit=5&seed_tracks={','.join(request.seed_tracks)}", headers=headers)
    
    # Get JSON Response
    json_response = response.json()
    
    # Return the 'tracks' part of the response if it exists
    return response.json().get('tracks', {'error': 'Tracks not found'})
