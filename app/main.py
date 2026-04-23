from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI, Header, Query, Path, Body
from typing import Optional
from app.schemas import Notebase
from app.routers.notes import router as notes_router
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Fast api project"
)

app.include_router(notes_router)
app.include_router(auth_router)

@app.get('/')
# @app.route('/', methods=['GET'])
def home():
    return {"Message": "Hello World!"}

@app.get('/items/{item_id}')
def get_item(
    item_id: int = Path(description="Item id to query"),
    limit: Optional[int] = Query(None, lt=100, description='Max items to return'),
    user_agent: str = Header(...)
):
    # request.method
    # request.args.get('priceLow')

    return {
        'item_id': item_id,
        'limit': limit,
        'user_agent': user_agent
    }

@app.post('/test-validation')
def test_validation(
    note: Notebase = Body(...)
):
    return {'Received': note.model_dump()}