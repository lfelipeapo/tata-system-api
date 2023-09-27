from sqlalchemy_utils import database_exists, create_database
import os

# Importe a classe Base do arquivo base.py
from models.base import Base
from models.consultas_juridicas import ConsultaJuridica
from models.clientes import Cliente
from models.fuso_horario import now_saopaulo
from models.database import engine, Session
from models.documentos import Documento
from models.users import User
from models.peca_processual import PecaProcessual

db_path = "database/"

# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# Instancia um criador de seção com o banco
session = Session()

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
