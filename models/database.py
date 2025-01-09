from sqlmodel import Field, SQLModel, create_engine
from .model import *

# aqui é a função que cria o banco de dados
sql_file_name = 'database.db'
sqlite_url = f"sqlite:///{sql_file_name}"

# aqui é a função que cria o banco de dados e mostra o que está acontecendo no terminal 
engine = create_engine(sqlite_url, echo=True)


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)