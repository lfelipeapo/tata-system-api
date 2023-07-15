from pydantic import BaseModel, validator
from datetime import date, time
from typing import List, Optional

class ConsultaJuridicaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa uma consulta.
    """
    nome_cliente: str
    cpf_cliente: str
    data_consulta: str
    horario_consulta: str
    detalhes_consulta: Optional[str]

class ConsultaJuridicaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de uma consulta. Que será
        feita apenas com base no id da consulta.
    """
    consulta_id: int

class ConsultaJuridicaBuscaPorDataEHoraSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de uma consulta. Que será
        feita com base na data e horário da consulta.
    """
    data_consulta: str
    horario_consulta: str

class ConsultasFiltradasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de consultas, esperando parâmetros ou não.
    """
    data_consulta: Optional[str] 
    nome_cliente: Optional[str]
    cpf: Optional[str]

class ConsultaJuridicaAtualizadaSchema(BaseModel):
    """Define como é a estrutura de uma consulta jurídica atualizada"""
    consulta_id: int
    nome_cliente: Optional[str]
    cpf_cliente: Optional[str]
    data_consulta: Optional[date]
    horario_consulta: Optional[time]
    detalhes_consulta: Optional[str]


class ConsultaJuridicaListagemSchema(BaseModel):
    """ Define como uma listagem de consultas será retornada.
    """
    consultas: List[ConsultaJuridicaSchema]


class ConsultaJuridicaViewSchema(BaseModel):
    """ Define como uma consulta jurídica será retornada: consulta.
    """
    id: int
    nome_cliente: str
    cpf_cliente: str
    data_consulta: str
    horario_consulta: str
    detalhes_consulta: Optional[str]