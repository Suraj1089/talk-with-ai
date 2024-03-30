from sqlmodel import SQLModel, create_engine


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///db.sqlite", echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
