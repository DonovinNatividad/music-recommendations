from fastapi import FastAPI
from api.recommendations import api as api_router

app = FastAPI()

# Adding the recommendations route
app.include_router(api_router, prefix='/api')

@app.get('/')
def root():
    return {'message': 'Uvicorn serving app successfully!'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
    