import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from src.base import Base
from src.user.data.models.user import UserModel
from src.wishlist.data.models.wish_item import WishItemModel


class WishlistModel(Base):
    """Model for wishlist."""

    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_uuid = Column(UUID, unique=True, default=uuid.uuid4, nullable=False)
    name = Column(String(length=100), index=True, nullable=False)
    description = Column(String(length=300))
    created_at = Column(DateTime(timezone=True), index=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user: Mapped[UserModel] = relationship(UserModel, back_populates="wishlists", lazy="joined")
    wish_items: Mapped[list[WishItemModel]] = relationship(WishItemModel, back_populates="wishlist", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_user_wishlist"),)
