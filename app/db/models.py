import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Table, TIMESTAMP, text 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tabel asosiasi many-to-many antara Note dan Tag
note_tag_association = Table(
    'notetag',
    Base.metadata,
    Column('note_id', UUID(as_uuid=True), ForeignKey('note.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tag.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    avatar_url = Column(String, nullable=True)  # Bisa opsional
    created_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    # Relationship
    notes = relationship("Note", back_populates="user")


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    # Relationship
    notes = relationship("Note", secondary=note_tag_association, back_populates="tags")


class Note(Base):
    __tablename__ = 'note'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)  # Bisa kosong
    avatar_url = Column(String, nullable=True)  # Opsional
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)  # Bisa None jika note tidak punya pemilik

    created_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes")