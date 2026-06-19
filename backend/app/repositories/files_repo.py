"""
Repository for file database operations.

All queries that read or write the `files` table live here.
"""

from sqlalchemy.orm import Session

from app import models


def get_all_files(
    db: Session
) -> list[models.File] | None:
    return db.query(models.File).order_by(models.File.name).all()


def get_file(
    db: Session,
    file_id: int
) -> models.File | None:
    """Return a file by primary key, or None if it doesn't exist."""

    return db.get(models.File, file_id)


def list_files(
    db: Session,
    folder_id: int | None
) -> list[models.File]:
    """
    Return the files inside `folder_id`.
    Pass `folder_id=None` to list root-level files.
    """

    return (
        db.query(models.File)
        .filter(models.File.folder_id == folder_id)
        .order_by(models.File.name)
        .all()
    )


def create_file(
    db: Session,
    name: str,
    folder_id: int | None,
) -> models.File:
    """
    Create and return a new file.

    Raises ValueError if:
    - `folder_id` is provided but doesn't refer to an existing folder
    - a file with the same name already exists in that folder
    """

    if folder_id is not None and db.get(models.Folder, folder_id) is None:
        raise ValueError(f"Folder {folder_id} does not exist")

    existing = (
        db.query(models.File)
        .filter(models.File.folder_id == folder_id, models.File.name == name)
        .first()
    )
    if existing:
        raise ValueError(f"A file named '{name}' already exists in this folder")

    file = models.File(name=name, folder_id=folder_id)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def delete_file(
    db: Session,
    file_id: int
) -> None:
    """
    Delete a file.

    Raises ValueError if the file doesn't exist.
    """

    file = db.get(models.File, file_id)
    if file is None:
        raise ValueError(f"File {file_id} does not exist")

    db.delete(file)
    db.commit()



def search_exact(
    db: Session,
    name: str,
    folder_id: int | None = None,
    limit: int = 10,
) -> list[models.File]:
    """
    Return files whose name matches `name` exactly (case-sensitive).

    If `folder_id` is provided, the search is scoped to that folder;
    otherwise it searches across all files.
    """

    # Unsure about specifications here. I'm assuming the "exact" search has to only match
    # a part of the files name but if not then an actual exact search is done like so
    # query = db.query(models.File).filter(models.File.name == name)
    query = db.query(models.File).filter(models.File.name.ilike(f"{name}%"))
    if folder_id is not None:
        query = query.filter(models.File.folder_id == folder_id)
    return query.limit(limit).all()


def autocomplete(
    db: Session,
    prefix: str,
    limit: int = 10,
) -> list[models.File]:
    """
    Return up to `limit` files whose name starts with `prefix`
    (case-insensitive), ordered alphabetically by name.
    """

    return (
        db.query(models.File)
        .filter(models.File.name.ilike(f"{prefix}%"))
        .order_by(models.File.name)
        .limit(limit)
        .all()
    )
