from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from api.utils.base_sql import BaseModel


class Quotas(BaseModel):
    __tablename__ = 'quotas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(ForeignKey('action.id'), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    action = relationship('Action')
