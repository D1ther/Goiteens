from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    BackgroundTasks
)

from typing import (
    List,
)

from PIL import (
    Image
)

import uvicorn, shutil, io

api = FastAPI(docs_url='/')

def resize_image(image_data: bytes, size: tuple = (1920, 1080)):
    with Image.open(io.BytesIO(image_data)) as image:
        image.thumbnail(size)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        return image_bytes.getvalue()
    
async def proces_resizing(path: str):
    with open(path, 'rb') as f:
        resized_image = resize_image(f.read())
    with open(path, 'wb') as file:
        file.write(resized_image)

@api.post('/upload/photo')
async def upload_phot(bgt: BackgroundTasks, files: List[UploadFile] = File(...)):
    if len(files) >= 1:
        for file in files:    
            with open(f'temp/{file.filename}', 'wb') as f:       
                if file.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                    if file.size < 7 * 1024 * 1024:
                        f.write(file.file.read())
                        
                        bgt.add_task(proces_resizing, f'temp/{file.filename}')
                    else:
                        raise HTTPException(status_code=413, detail='Файл занадто великий')  
                else:
                    raise HTTPException(status_code=415, detail='Цей тип даних не підтримується')
            return {'message': f'Файли {file.filename} успішно надіслано'}
    else:
        raise HTTPException(status_code=400, detail='Ви не надіслали жодного файлу')


if __name__ == '__main__':
    uvicorn.run('main:api', reload=True)
