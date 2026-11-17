from fastapi import FastAPI, HTTPException
from schemas.folder import FolderCreate, FolderResponse, FolderUpdate
from schemas.file import FileCreate, FileResponse
from uuid import UUID, uuid4

app = FastAPI()

folders: dict[UUID, FolderResponse] = {}

files: dict[UUID, FileResponse] = {}

@app.get('/health')
def health_check():
    return {'status': 'active'}

# Folder related endpoints

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
    updated_folder = folder.model_copy(update=update_data)
    folders[folder_id] = updated_folder
    return updated_folder

# File related endpoints

@app.get('/folders/{folder_id}/files/{file_id}', response_model=FileResponse)
def read_file(folder_id: UUID, file_id: UUID):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    if file_id not in files:
        raise HTTPException(status_code=404, detail='File not found')
    if folder_id != files[file_id].parent_id:
        raise HTTPException(status_code=404, detail='File not found')
    return files[file_id]

@app.post('/folders/{folder_id}/files', response_model=FileResponse)
def create_file(folder_id: UUID, file: FileCreate):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    response = FileResponse(id=uuid4(), name=file.name, parent_id=folder_id)
    files[response.id] = response
    return response

@app.delete('/folders/{folder_id}/files/{file_id}')
def delete_file(folder_id: UUID, file_id: UUID):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    if file_id not in files:
        raise HTTPException(status_code=404, detail='File not found')
    if folder_id != files[file_id].parent_id:
        raise HTTPException(status_code=404, detail='File not found')
    del files[file_id]