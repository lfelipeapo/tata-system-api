from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from models.base import Base
from models.fuso_horario import now_saopaulo
from typing import Union

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome_cliente = Column(String(80), nullable=False)
    cpf_cliente = Column(String(11), nullable=False, unique=True)
    data_cadastro = Column(DateTime, nullable=False, default=now_saopaulo())
    data_atualizacao = Column(DateTime)

    def __init__(self, nome_cliente:str, cpf_cliente:str, data_cadastro: Union[DateTime, None] = None):
        """
        Cria um Cliente

        Arguments:
            nome_cliente: nome do cliente.
            cpf_cliente: cpf do cliente.
            data_cadastro: data de quando o cliente foi inserido à base
            data_atualização: data de atualização do cadastro do cliente
        """
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente

        if (data_cadastro):
            self.data_cadastro = data_cadastro

