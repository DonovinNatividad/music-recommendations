'''create a venv for the project, or 
maybe a docker environment, whichever is easier for the project package management
so that I can install packages
'''
import requests

def get_recommendations(access_token, seed_tracks):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    params = {
        'seed_tracks': ','.join(seed_tracks),
        'limit': 10, # Number of recommendations to return to user
    }
    
    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)
    
    return response.json()
