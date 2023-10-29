from sqlalchemy import create_engine
from models import Base, Lector, Subject
from sqlalchemy.orm import Session
engine = create_engine("sqlite+pysqlite:///C:\\Users\\nabac\\OneDrive\\Desktop\\bot-Telegram\\database.db", echo=True)
#Base.metadata.create_all(engine)

with Session(engine) as session:
    testlector = Lector(
        name = "Maks",
        surname = "Vrutskyi",
        secondname = "Vyacheslavovich",
        zoomcode = "123",
        zoompass = "123",
        isteams = False,
        subject = Subject(
            name = "Math",
            day = "Wednesday",
            lesson = 3,
            weektype = False,
            group = 1,
            lector_id = 1
        )
    )
    session.add_all([testlector])
    session.commit()