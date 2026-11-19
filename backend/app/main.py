from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from schemas.folder import FolderCreate, FolderResponse, FolderUpdate
from schemas.file import FileRead
from uuid import UUID, uuid4
import storage

app = FastAPI()

folders: dict[UUID, FolderResponse] = {}

files: dict[UUID, FileRead] = {}

@app.get('/health')
def health_check():
    return {'status': 'active'}

# Folder related endpoints

@app.get('/folders', response_model=list[FolderResponse])
def list_folders(parent_id: UUID | None = None):
    if parent_id is not None and parent_id not in folders:
        raise HTTPException(status_code=404, detail='Parent folder not found')
    folder_list = []
    for folder in folders.values():
        if folder.parent_id == parent_id:
            folder_list.append(folder)
    return folder_list


@app.get('/folders/{folder_id}', response_model=FolderResponse)
def read_folder(folder_id: UUID):
    if folder_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    return folders[folder_id]

@app.post('/folders', response_model=FolderResponse)
def create_folder(folder: FolderCreate):
    if folder.parent_id:
        if folder.parent_id not in folders:
            raise HTTPException(status_code=404, detail='Folder not found')
        
    response = FolderResponse(id=uuid4(), name=folder.name, parent_id=folder.parent_id)
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
'''
@app.get('/files/{file_id}', response_model=FileRead)
def read_file(file_id: UUID):
    if file_id not in files:
        raise HTTPException(status_code=404, detail='File not found')
    return files[file_id]
'''

# Create file
@app.post('/files', response_model=FileRead)
def create_file(file: UploadFile, parent_id: UUID | None = None):
    if parent_id is not None and parent_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    if file.filename is None:
        raise HTTPException(status_code=400, detail='File must have a name')
    response = FileRead(name=file.filename, id=uuid4(), parent_id=parent_id)
    storage.save_file(response.id, file.file)

    files[response.id] = response
    return response

@app.delete('/files/{file_id}')
def delete_file(file_id: UUID):
    if file_id not in files:
        raise HTTPException(status_code=404, detail='File not found')
    storage.delete_file(file_id)
    del files[file_id]

@app.get('/files/{file_id}/download', response_class=FileResponse)
def download_file(file_id: UUID):
    if file_id not in files:
        raise HTTPException(status_code=404, detail='File not found')
    path = storage.get_file_path(file_id)
    if not path.is_file():
        raise HTTPException(status_code=404, detail='File data missing')

    file_metadata = files[file_id]

    response = FileResponse(path=path, filename=file_metadata.name)

    return response

@app.get('/files/')
def get_files_in_folder(parent_id: UUID | None = None):
    if parent_id is not None and parent_id not in folders:
        raise HTTPException(status_code=404, detail='Folder not found')
    files_in_folder = []
    for file in files.values():
        if file.parent_id == parent_id:
            files_in_folder.append(file)
    return files_in_folder
