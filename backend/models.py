from datetime import datetime
from annotated_types import T
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class BaseDB(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class HistoryDB(BaseDB):
    __tablename__ = "history"
    question: Mapped[str]
    context: Mapped[str]
    answer: Mapped[str]
    answer_date: Mapped[datetime] = mapped_column(default=datetime.now())
