"""
SQLAlchemy ORM models.

Folders and files are kept in separate tables. This makes the schema
easier to reason about, avoids nullable columns caused by a type
discriminator, and leaves room for each table to gain its own
attributes (e.g. file size/MIME type, folder icon/colour) without
polluting a shared table.

Relationships
-------------
Folder → Folder  (self-referential, parent_id)
    A folder can contain subfolders. Deleting a parent cascades to
    all descendants via the DB-level ON DELETE CASCADE.

Folder → File  (one-to-many, folder_id)
    A file lives inside exactly one folder (or at the root when
    folder_id is NULL). Deleting a folder cascades to its files.

Unique constraints
------------------
(parent_id, name) on folders — two sibling folders can't share a name.
(folder_id, name) on files   — two files in the same folder can't share
                                a name.
"""

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(
        Integer,
        ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=True,  # NULL → lives at the root level
        index=True,
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # relationships
    parent = relationship(
        "Folder",
        back_populates="subfolders",
        remote_side="Folder.id",
    )
    subfolders = relationship(
        "Folder",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    files = relationship(
        "File",
        back_populates="folder",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        # Sibling folders must have unique names
        UniqueConstraint("parent_id", "name", name="uq_folders_parent_name"),
    )


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    folder_id = Column(
        Integer,
        ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=True,  # NULL → lives at the root level
        index=True,
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # relationships
    folder = relationship("Folder", back_populates="files")

    __table_args__ = (
        # Files within the same folder must have unique names
        UniqueConstraint("folder_id", "name", name="uq_files_folder_name"),
        # Autocomplete/search filter on name — explicit index for clarity
        Index("ix_files_name", "name"),
    )
