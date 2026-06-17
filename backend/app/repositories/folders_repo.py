"""
Repository for folder database operations.

All queries that read or write the `folders` table live here.
"""

from sqlalchemy.orm import Session

from app import models


def get_all_folders(
    db: Session
) -> list[models.Folder]:
    return db.query(models.Folder).order_by(models.Folder.name).all()

def get_folder(
    db: Session,
    folder_id: int
) -> models.Folder | None:
    """Return a folder by primary key, or None if it doesn't exist."""
    return db.get(models.Folder, folder_id)


def list_subfolders(
    db: Session,
    parent_id: int | None
) -> list[models.Folder]:
    """
    Return the immediate subfolders of `parent_id`.
    Pass `parent_id=None` to list root-level folders.
    """
    return (
        db.query(models.Folder)
        .filter(models.Folder.parent_id == parent_id)
        .order_by(models.Folder.name)
        .all()
    )


def create_folder(
    db: Session,
    name: str,
    parent_id: int | None,
) -> models.Folder:
    """
    Create and return a new folder.

    Raises ValueError if:
    - `parent_id` is provided but doesn't refer to an existing folder
    - a sibling folder with the same name already exists
    """

    if parent_id is not None and db.get(models.Folder, parent_id) is None:
        raise ValueError(f"Folder {parent_id} does not exist")

    existing = (
        db.query(models.Folder)
        .filter(models.Folder.parent_id == parent_id, models.Folder.name == name)
        .first()
    )
    if existing:
        raise ValueError(f"A folder named '{name}' already exists here")

    folder = models.Folder(name=name, parent_id=parent_id)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def delete_folder(
    db: Session,
    folder_id: int
) -> None:
    """
    Delete a folder and all of its descendants (subfolders + files).

    The cascade is configured on the model relationship, so deleting
    the folder row is sufficient — SQLAlchemy handles the rest.

    Raises ValueError if the folder doesn't exist.
    """
    
    folder = db.get(models.Folder, folder_id)
    if folder is None:
        raise ValueError(f"Folder {folder_id} does not exist")

    db.delete(folder)
    db.commit()
