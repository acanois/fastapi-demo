from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def home():
    message = {"message": "home"}
    
    return JSONResponse(message)
