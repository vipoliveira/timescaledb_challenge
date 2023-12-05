from sqlalchemy.orm import Mapped, MappedAsDataclass, DeclarativeBase, mapped_column
from datetime import datetime


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class StockTrades(Base):
    __tablename__ = 'stock_trades'
    __hypertable_field__ = 'date'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(default=None)
    date: Mapped[datetime] = mapped_column(default=None, primary_key=True, index=True)
    open: Mapped[float] = mapped_column(default=None)
    high: Mapped[float] = mapped_column(default=None)
    low: Mapped[float] = mapped_column(default=None)
    close: Mapped[float] = mapped_column(default=None)
    adj_close: Mapped[float] = mapped_column(default=None)
    volume: Mapped[int] = mapped_column(default=None)

class StockMetadata(Base):
    __tablename__ = 'stock_metadata'
    __hypertable_field__ = 'date'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nasdaq_traded: Mapped[str] = mapped_column(default=None)
    symbol: Mapped[str] = mapped_column(default=None)
    security_name: Mapped[str] = mapped_column(default=None)
    listing_exchange: Mapped[str] = mapped_column(default=None)
    market_category: Mapped[str] = mapped_column(default=None)
    etf: Mapped[str] = mapped_column(default=None)
    round_lot_size: Mapped[str] = mapped_column(default=None)
    test_issue: Mapped[str] = mapped_column(default=None)
    financial_status: Mapped[str] = mapped_column(default=None)
    cqs_symbol: Mapped[str] = mapped_column(default=None)
    nasdaq_symbol: Mapped[str] = mapped_column(default=None)
    nextshares: Mapped[str] = mapped_column(default=None)
