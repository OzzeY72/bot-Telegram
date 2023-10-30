from typing import Optional
from typing import List
from typing import Set

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass
class Lector(Base):
    __tablename__ = "lector"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    secondname: Mapped[Optional[str]]
    zoomcode: Mapped[Optional[str]]
    zoompass: Mapped[Optional[str]]
    isteams: Mapped[Optional[bool]]
    subject: Mapped[Optional[Set["Subject"]]] = relationship(back_populates="lector")

    def __reprshort__(self) -> str:
        zoom = ""
        if not self.isteams:
            zoom = f"<b>Zoomcode:</b> {self.zoomcode}\n<b>Zoompass:</b> {self.zoompass}"
        return zoom
    
    def __repr__(self) -> str:
        zoom = self.__reprshort__()
        return f"<b>Ім'я:</b> {self.surname} {self.name} {self.secondname!r}\n {'' if self.isteams else zoom})"
    

class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    day: Mapped[str] = mapped_column(String(30))
    lesson: Mapped[int]
    weektype: Mapped[int]
    group: Mapped[int]
    lector_id: Mapped[int] = mapped_column(ForeignKey("lector.id"))
    lector: Mapped["Lector"] = relationship(back_populates="subject")

    def lesson_time_convert(self,lesson) -> str:
        if lesson == 1:
            return "08:00"
        elif lesson == 2:
            return "9:35"
        elif lesson == 3:
            return "11:25"
        elif lesson == 4:
            return "12:55"
        elif lesson == 5:
            return "14:30"
        elif lesson == 6:
            return "16:00"

    def __repr__(self) -> str:
        return f"<b>Предмет</b>: {self.name}\n<b>День:</b> {self.day}\n<b>Час:</b> {self.lesson_time_convert(self.lesson)}\n<b>Тиждень:</b> {'Чисельник' if self.weektype == 1 else 'Знаменник' if self.weektype == 2 else 'Чисельник і знаменник'}\n<b>Підгруппа:</b> {'Обидві' if self.group == 3 else self.group}\n{self.lector.__reprshort__()}"

class BindAlarm(Base):
    __tablename__ = "bindalarm"

    id: Mapped[int] = mapped_column(primary_key=True)
    telid: Mapped[str]
    alarm: Mapped[bool]