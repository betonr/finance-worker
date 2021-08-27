from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from api_finance.utils.base_sql import BaseModel


class Indicators(BaseModel):
    __tablename__ = 'indicators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(ForeignKey('action.id'), nullable=False)
    price_profit = Column(Float, nullable=True)
    price_value_worth = Column(Float, nullable=True)
    price_ebit = Column(Float, nullable=True)
    price_net_revenueear = Column(Float, nullable=True)
    price_active = Column(Float, nullable=True)
    price_working_capital = Column(Float, nullable=True)
    price_net_circle_active = Column(Float, nullable=True)
    div_yield = Column(Float, nullable=True)
    enterprise_value_ebitda = Column(Float, nullable=True)
    enterprise_value_ebit = Column(Float, nullable=True)
    revenue_growth_five_years = Column(Float, nullable=True)
    profit_by_action = Column(Float, nullable=True)
    patrimonial_value = Column(Float, nullable=True)
    gross_margin = Column(Float, nullable=True)
    ebit_margin = Column(Float, nullable=True)
    net_margin = Column(Float, nullable=True)
    ebit_active = Column(Float, nullable=True)
    roic = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    current_assets_liabilities = Column(Float, nullable=True)
    debt_gross_patrimonial = Column(Float, nullable=True)
    asset_turnover = Column(Float, nullable=True)
    date = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    action = relationship('Action')