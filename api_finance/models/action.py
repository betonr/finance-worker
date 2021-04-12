from sqlalchemy import Boolean, Column, String, Integer, DateTime, func

from api.utils.base_sql import BaseModel


class Action(BaseModel):
    __tablename__ = 'action'

    id = Column(String(150), nullable=False, primary_key=True)
    company_name = Column(String(150), nullable=False)
    company_full_name = Column(String(150), nullable=True)
    sector = Column(String(150), nullable=True)
    segment = Column(String(150), nullable=True)
    provider = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)