import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#Carrega as variáveis de ambiente:
load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db = os.getenv('POSTGRES_DB')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')

# url de acesso ao banco
if os.getenv('DOCKER_ENV'):
    db_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
else:
    db_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/tata'

# cria a engine de conexão com o banco
engine = create_engine(db_url)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)