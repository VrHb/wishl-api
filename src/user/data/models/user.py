import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from src.base import Base
from src.wishlist.data.models.wish_item import WishItemModel
from src.wishlist.data.models.wishlist import WishlistModel


class UserModel(Base):
    """Model for user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_uuid = Column(UUID, unique=True, default=uuid.uuid4, nullable=False)
    username = Column(String(length=64), unique=True, index=True, nullable=False)
    email = Column(String(length=64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), index=True, server_default=func.now())

    wishlists: Mapped[list[WishlistModel]] = relationship(WishlistModel, back_populates="user", cascade="all, delete-orphan")
    reserved_items: Mapped[list[WishItemModel]] = relationship(WishlistModel, back_populates="reserved_by_user", cascade="all, delete-orphan")
