from sqlalchemy import Column, String, Integer, DateTime, Boolean

from api_finance.utils.base_sql import BaseModel


class Worker(BaseModel):
    __tablename__ = 'worker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False)
    actions_errors = Column(String(555), nullable=True)
    qnt_errors = Column(String(555), nullable=False)
    obs = Column(String(555), nullable=True)
    qnt_new_actions = Column(Integer, nullable=False)
    qnt_update_quota = Column(Integer, nullable=False)
    qnt_update_indicators = Column(Integer, nullable=False)
    qnt_update_balance = Column(Integer, nullable=False)
