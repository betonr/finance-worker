from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from api.utils.base_sql import BaseModel


class Balance(BaseModel):
    __tablename__ = 'balance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(ForeignKey('action.id'), nullable=False)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    net_worth = Column(Float)
    balance_infos = Column(JSONB)
    result_infos = Column(JSONB)
    date = Column(DateTime, nullable=False)

    action = relationship('Action')