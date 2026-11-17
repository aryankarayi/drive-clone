from fastapi import FastAPI, HTTPException
from schemas.folder import FolderCreate, FolderResponse, FolderUpdate
from uuid import UUID, uuid4

app = FastAPI()

folders: dict[UUID, FolderResponse] = {}

@app.get('/health')
def health_check():
    return {'status': 'active'}

@app.get('/folders/{folder_id}', response_model=FolderResponse)
def read_folder(folder_id: UUID):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    return folders[folder_id]

@app.post('/folders', response_model=FolderResponse)
def create_folder(folder: FolderCreate):
    response = FolderResponse(id=uuid4(), name=folder.name)
    folders[response.id] = response
    return response

@app.delete('/folders/{folder_id}')
def delete_folder(folder_id: UUID):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    del folders[folder_id]

@app.patch('/folders/{folder_id}', response_model=FolderResponse)
def update_folder(folder_id: UUID, update: FolderUpdate):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    folder = folders[folder_id]
    update_data = update.model_dump(exclude_unset=True)
    updated_folder = folder.model_copy(update_data)
    folders[folder_id] = updated_folder
    return updated_folder