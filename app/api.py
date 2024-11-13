"""API"""

from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

@app.get('/')
async def home():
    message = {'message': 'home'}
    
    return JSONResponse(message)

@app.get('/items')
async def read_items(token: Annotated[str, Depends(oauth2_schema)]):
    return {'token': token}
