from fastapi import (
    FastAPI,
    WebSocket,
    HTTPException,
    Depends,
    Request
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from dotenv import (
    load_dotenv
)

from typing import (
    List,
    Dict
)

import uvicorn, jwt, os

load_dotenv()

api = FastAPI(docs_url='/')
SECRET_KEY = os.getenv('SECRET_KEY')

print(jwt.encode({'test': 'test'}, SECRET_KEY, algorithm='HS256'))

active_users: List[WebSocket] = []

auth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    
@api.websocket('/ws/chat')
async def chat(websocket: WebSocket):
    token = websocket.query_params.get('token')

    if not token:
        await websocket.close(1008)
        raise HTTPException(status_code=401, detail='Token not provided')

    try:
        verify_token(token)
    except jwt.PyJWTError as e:
        await websocket.close()
        raise HTTPException(status_code=401, detail='Invalid token')
    
    await websocket.accept()
    active_users.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for user in active_users:
                if user != websocket:
                    await user.send_text(data)

    except Exception as e:
        print(f'СТалася помилка: {e}')

    finally:
        active_users.remove(websocket)
        await websocket.close()

active_chats: Dict[str, WebSocket] = {}

@api.websocket('/ws/chat/with/user')
async def chat_by_id(websocket: WebSocket):
    url_data = websocket.query_params

    token, my_id, user_id = url_data.get('token'), url_data.get('my_id'), url_data.get('user_id')

    if not token or not my_id or not user_id:
        await websocket.close()
        raise HTTPException(status_code=400, detail="Missing token or ids")

    try:
        verify_token(token)
    except jwt.PyJWTError as e:
        await websocket.close()
        raise HTTPException(status_code=401, detail='Invalid token')
    
    await websocket.accept()
    active_chats[my_id] = websocket
 
    print(f'Active chats: {active_chats}')

    try:
        while True:
            data = await websocket.receive_text()

            user = active_chats[user_id]

            if user:
                await user.send_text(f'{my_id}: {data}')
        
    except Exception as e:
        print(f'Салася помилка: {e}')


if __name__ == '__main__':
    uvicorn.run('main:api', reload=True)
