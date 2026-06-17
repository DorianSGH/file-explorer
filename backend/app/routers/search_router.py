"""
Search and autocomplete endpoints.

"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories import files_repo

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[schemas.FileOut])
def search_exact(
    q: str,
    folder_id: int | None = None,
    db: Session = Depends(get_db),
):
    return files_repo.search_exact(db, name=q, folder_id=folder_id)


@router.get("/autocomplete", response_model=list[schemas.FileOut])
def autocomplete(q: str, db: Session = Depends(get_db)):
    return files_repo.autocomplete(db, prefix=q, limit=10)
