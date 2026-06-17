"""
Pydantic schemas for request validation and response serialisation.

Keeping folder and file schemas separate mirrors the model layer and
makes it immediately clear what each endpoint accepts and returns.
`model_config = {"from_attributes": True}` allows returning SQLAlchemy
model instances directly from endpoints.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Folder schemas
# ---------------------------------------------------------------------------


class FolderCreate(BaseModel):
    name: str
    parent_id: int | None = None


class FolderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None
    created_at: datetime


# ---------------------------------------------------------------------------
# File schemas
# ---------------------------------------------------------------------------


class FileCreate(BaseModel):
    name: str
    folder_id: int | None = None


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    folder_id: int | None
    created_at: datetime


# ---------------------------------------------------------------------------
# Browse schema — returned when listing the contents of a folder
# ---------------------------------------------------------------------------


class FolderContents(BaseModel):
    subfolders: list[FolderOut]
    files: list[FileOut]
