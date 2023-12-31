import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#Carrega as variáveis de ambiente:
project_dir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(project_dir, '..', '.env')
load_dotenv(dotenv_path)

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
engine = create_engine(db_url, pool_size=50, max_overflow=0)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)