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

    def __repr__(self) -> str:
         return f"Lector(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, secondname={self.secondname!r}, zoomcode={self.zoomcode!r}, zoompass={self.zoompass!r}), isteams={self.isteams!r}"

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

    def __repr__(self) -> str:
        return f"Subject(id={self.id!r}, name={self.name!r}, day={self.day!r}, lesson={self.lesson!r}, weektype={self.weektype!r}, group={self.group!r})"
