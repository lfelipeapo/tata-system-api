from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# url de acesso ao banco
db_url = 'postgresql+psycopg2://postgres:postgres@db:5432/tata'

# cria a engine de conexão com o banco
engine = create_engine(db_url)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)