import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_question: Mapped[str] = mapped_column(String(200))
    answer: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now())

    def __repr__(self) -> str:
        return f"Вопрос(id={self.id!r}, текст вопроса={self.text_question!r}, ответ={self.answer!r})"

