"""
Folder endpoints.

Handles creating, browsing, and deleting folders. The browse endpoint
returns both subfolders and files for a given folder in a single
response.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.logger import get_logger
from app.repositories import files_repo, folders_repo

router = APIRouter(prefix="/folders", tags=["folders"])
logger = get_logger(__name__)


@router.get("", response_model=list[schemas.FolderOut])
def get_all_folders(db: Session = Depends(get_db)):
    
    folders = folders_repo.get_all_folders(db)
    logger.info("Listed all folders, count=%d", len(folders))
    return folders


@router.get("/browse", response_model=schemas.FolderContents)
def browse(parent_id: int | None = None, db: Session = Depends(get_db)):

    if parent_id is not None and folders_repo.get_folder(db, parent_id) is None:
        raise HTTPException(status_code=404, detail=f"Folder {parent_id} does not exist")
    contents = schemas.FolderContents(
        subfolders=folders_repo.list_subfolders(db, parent_id),
        files=files_repo.list_files(db, parent_id),
    )
    logger.info("Browsed folder parent_id=%s, subfolders=%d files=%d", parent_id, len(contents.subfolders), len(contents.files))
    return contents


@router.post("", response_model=schemas.FolderOut, status_code=201)
def create_folder(payload: schemas.FolderCreate, db: Session = Depends(get_db)):

    try:
        folder = folders_repo.create_folder(db, **payload.model_dump())
        logger.info("Created folder id=%d name='%s' parent_id=%s", folder.id, folder.name, folder.parent_id)
        return folder
    except ValueError as exc:
        logger.warning("Failed to create folder: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{folder_id}")
def delete_folder(folder_id: int, db: Session = Depends(get_db)):

    try:
        folders_repo.delete_folder(db, folder_id)
        logger.info("Deleted folder id=%d", folder_id)
        return {"message": f"Folder {folder_id} deleted successfully"}
    except ValueError as exc:
        logger.warning("Failed to delete folder id=%d: %s", folder_id, exc)
        raise HTTPException(status_code=404, detail=str(exc))
    

@router.get("/{folder_id}", response_model=schemas.FolderOut)
def get_folder(folder_id: int, db: Session = Depends(get_db)):
    
    folder = folders_repo.get_folder(db, folder_id)
    if folder is None:
        raise HTTPException(status_code=404, detail=f"Folder {folder_id} does not exist")
    return folder
