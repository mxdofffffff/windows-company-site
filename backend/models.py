from datetime import datetime
from decimal import Decimal

from backend.database import Base
from sqlalchemy import Integer,String,func,Text,Numeric,text,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

class Product(Base):
    __tablename__= "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100),nullable=False)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())
    description:Mapped[str] = mapped_column(Text)
    price:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(),onupdate=func.now())
    is_active:Mapped[bool] = mapped_column(server_default=text("true"),nullable=False)
    images:Mapped[list["ProductImage"]] = relationship(back_populates="product")
    requests:Mapped[list["Request"]] = relationship(back_populates="product")
class ProductImage(Base):
    __tablename__ = "product_images"
    id:Mapped[int] = mapped_column(primary_key=True)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    sort_order:Mapped[int] = mapped_column(Integer)
    image_path:Mapped[str] = mapped_column(String(255),nullable=False)
    product: Mapped["Product"] = relationship(back_populates="images")

class Request(Base):
    __tablename__ = "requests"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50),nullable=False)
    phone:Mapped[str] = mapped_column(String(15),nullable=False)
    comment:Mapped[str | None] = mapped_column(Text)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())
    status:Mapped[str] = mapped_column(String(50),default="Новый заказ",nullable=False)
    product:Mapped["Product"] = relationship(back_populates="requests")

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    hashed_password:Mapped[str] = mapped_column(String(255),nullable=False)
    role:Mapped[str] = mapped_column(String,nullable=False, default="admin")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
