from pydantic import BaseModel, Field, validator
from typing import List, Optional

class PecaProcessualSchema(BaseModel):
    """ Define como deve ser a estrutura de uma peça processual. """
    nome_peca: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    categoria: str

class PecaProcessualViewSchema(BaseModel):
    """ Define como deve ser a estrutura de visualização de uma peça processual. """
    id: int
    nome_peca: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    categoria: str

class PecaProcessualListagemSchema(BaseModel):
    """ Define como uma lista de peças processuais será retornada. """
    pecas_processuais: List[PecaProcessualViewSchema]

class PecaProcessualBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura de busca de uma peça processual. """
    peca_id: int

class PecaProcessualAtualizadoSchema(BaseModel):
    """ Define como deve ser a estrutura de atualização de uma peça processual. """
    id: int
    nome_peca: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    categoria: str

class PecaProcessualExclusaoArmazenamentoSchema(BaseModel):
    """ Define como deve ser a estrutura para excluir uma peça processual do armazenamento. """
    local_ou_samba: str
    categoria: str
    filename: str
