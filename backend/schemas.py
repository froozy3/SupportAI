from datetime import datetime
from pydantic import BaseModel

from models import HistoryDB


class UserAsk(BaseModel):
    question: str


class UserConfirm(BaseModel):
    response: str


class UserResponse(BaseModel):
    response: str
    context: list[str]


class History(BaseModel):
    id: int | None = 0
    question: str
    context: list[str]
    answer: str
    answer_date: datetime | None = datetime.now()

    class Config:
        from_attributes = True

    def to_db(self):
        return HistoryDB(
            question=self.question,
            context=self.context[0],
            answer=self.answer,
            answer_date=self.answer_date,
        )
