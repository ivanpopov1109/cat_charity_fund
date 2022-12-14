from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class BaseModel:
    __abstract__ = True
    full_amount = Column(Integer)  # Требуемая сумма / сумма пожертвований
    invested_amount = Column(Integer, default=0)  # Внесенная сумма / распределенная сумма из пожертвований
    fully_invested = Column(Boolean, default=False)  # Собрана сумма или нет / переведены все деньги на проект или нет
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
