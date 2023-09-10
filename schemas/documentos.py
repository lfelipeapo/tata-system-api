from pydantic import BaseModel, validator
from typing import List, Optional

class DocumentoSchema(BaseModel):
    """ Define como deve ser a estrutura de um documento.
    """
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: Optional[int]

class DocumentoViewSchema(BaseModel):
    """ Define como deve ser a estrutura de visualização de um documento.
    """
    id: int
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: Optional[int]

class DocumentoListagemSchema(BaseModel):
    """ Define como uma lista de documentos será retornada.
    """
    documentos: List[DocumentoViewSchema]

class DocumentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura de busca de um documento.
    """
    documento_id: int

class DocumentoAtualizadoSchema(BaseModel):
    """ Define como deve ser a estrutura de atualização de um documento.
    """
    id: int
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: int