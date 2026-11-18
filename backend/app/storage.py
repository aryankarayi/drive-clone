from pathlib import Path
import io, shutil
from typing import BinaryIO
from uuid import UUID

STORAGE_DIR = Path('storage')
STORAGE_DIR.mkdir(exist_ok=True)

def save_file(file_id: UUID, content: BinaryIO) -> None:
    with open(STORAGE_DIR / str(file_id), 'wb') as dest:
        shutil.copyfileobj(content, dest)

def get_file_path(file_id: UUID) -> Path:
    return STORAGE_DIR / str(file_id)

def delete_file(file_id: UUID) -> None:
    (STORAGE_DIR / str(file_id)).unlink(missing_ok=True)