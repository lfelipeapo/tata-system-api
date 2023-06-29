from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ClienteSchema(BaseModel):
    """ Define como um novo cliente deve inserido e deve ser representado"""
    nome_cliente: str
    cpf_cliente: str

class ClienteAtualizadoSchema(BaseModel):
    """Define como deve ser atualizado e representado a atualização de um cliente"""
    cliente_id: int
    nome_cliente: Optional[str]
    cpf_cliente: Optional[str]

class ClienteBuscaSchema(BaseModel):
    """Define uma busca de um cliente por id"""
    cliente_id: int

class ClienteListagemSchema(BaseModel):
    """Define a representação de uma lista de clientes"""
    clientes: List[ClienteSchema]

class ClienteViewSchema(BaseModel):
    """Define a representação de um cliente"""
    id: int
    nome_cliente: str
    cpf_cliente: str
    data_cadastro: datetime
    data_atualizacao: Optional[datetime]

class ClientesFiltradosSchema(BaseModel):
    """Define a representação de uma lista de clientes filtrados e ordenados"""
    nome: Optional[str]
    cpf: Optional[str]
    data_cadastro: Optional[str]
    data_atualizacao: Optional[str]
