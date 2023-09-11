from pydantic import BaseModel, validator
from typing import List, Optional

class DocumentoSchema(BaseModel):
    """ Define como deve ser a estrutura de um documento. """
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: Optional[int]

class DocumentoViewSchema(BaseModel):
    """ Define como deve ser a estrutura de visualização de um documento. """
    id: int
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: Optional[int]

class DocumentoListagemSchema(BaseModel):
    """ Define como uma lista de documentos será retornada. """
    documentos: List[DocumentoViewSchema]

class DocumentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura de busca de um documento. """
    documento_id: int

class DocumentoAtualizadoSchema(BaseModel):
    """ Define como deve ser a estrutura de atualização de um documento. """
    id: int
    documento_nome: str
    documento_localizacao: Optional[str]
    documento_url: Optional[str]
    cliente_id: int
    consulta_id: int

class DocumentoAtualizadoComArquivoSchema(BaseModel):
    """ Define como deve ser a estrutura de um documento atualizado com arquivo. """
    documento: bytes
    local_ou_samba: str
    nome_cliente: str
    filename_antigo: str

    @validator('documento', pre=True)
    def validate_documento(cls, v):
        if not v:
            raise ValueError("Documento é obrigatório")
        return v

    @validator('local_ou_samba', 'nome_cliente', 'filename_antigo')
    def validate_fields(cls, v):
        if not v:
            raise ValueError("Campo é obrigatório")
        return v

class DocumentoExclusaoArmazenamentoSchema(BaseModel):
    """ Define como deve ser a estrutura para excluir um documento do armazenamento. """
    local_ou_samba: str
    nome_cliente: str
    filename: str

    @validator('local_ou_samba', 'nome_cliente', 'filename')
    def validate_fields(cls, v):
        if not v:
            raise ValueError("Campo é obrigatório")
        return v
