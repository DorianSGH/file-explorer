"""
File endpoints.

Handles creating and deleting individual files.

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.logger import get_logger
from app.repositories import files_repo

router = APIRouter(prefix="/files", tags=["files"])
logger = get_logger(__name__)

@router.get("", response_model=list[schemas.FileOut])
def get_all_files(db: Session = Depends(get_db)):

    files = files_repo.get_all_files(db)
    logger.info("Listed all files, count=%d", len(files))
    return files


@router.post("", response_model=schemas.FileOut, status_code=201)
def create_file(payload: schemas.FileCreate, db: Session = Depends(get_db)):

    try:
        file = files_repo.create_file(db, **payload.model_dump())
        logger.info("Created file id=%d name='%s' folder_id=%s", file.id, file.name, file.folder_id)
        return file
    except ValueError as exc:
        logger.warning("Failed to create file: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{file_id}", status_code=200)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    
    try:
        files_repo.delete_file(db, file_id)
        logger.info("Deleted file id=%d", file_id)
        return {"message": f"File {file_id} deleted successfully"}
    except ValueError as exc:
        logger.warning("Failed to delete file id=%d: %s", file_id, exc)
        raise HTTPException(status_code=404, detail=str(exc))
    

@router.get("/{file_id}", response_model=schemas.FileOut)
def get_file(file_id: int, db: Session = Depends(get_db)):

    file = files_repo.get_file(db, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail=f"File {file_id} does not exist")
    return file
