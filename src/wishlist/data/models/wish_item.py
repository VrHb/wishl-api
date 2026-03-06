import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DECIMAL

from src.base import Base
from src.user.data.models.user import UserModel
from src.wishlist.data.models.wishlist import WishlistModel


class WishItemModel(Base):
    """Model for wishlist items."""

    __tablename__ = "wish_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_uuid = Column(UUID, unique=True, default=uuid.uuid4, nullable=False)
    name = Column(String(length=100), index=True, nullable=False)
    link = Column(String(length=200))
    price = Column(DECIMAL(10, 2), index=True)
    description = Column(String(length=300))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reserved_by_name = Column(String(length=100))
    reserved_at = Column(DateTime(timezone=True))

    reserved_by_user_id = Column(Integer, ForeignKey("users.id"))
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)

    wishlist: Mapped[WishlistModel] = relationship(WishlistModel, back_populates="wish_items", lazy="selectin")
    reserved_by_user = relationship(UserModel, back_populates="reserved_items", lazy="selectin")
