from datetime import datetime
from decimal import Decimal

from database import Base
from sqlalchemy import Integer,String,func,Text,Numeric
from sqlalchemy.orm import Mapped,mapped_column

class Product(Base):
    __tablename__= "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100),nullable=False)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())
    description:Mapped[str] = mapped_column(Text)
    price:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(),onupdate=func.now())
    is_active:Mapped[bool] = mapped_column(server_default=True,nullable=False)

