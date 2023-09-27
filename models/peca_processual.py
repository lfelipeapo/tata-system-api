from sqlalchemy import Column, String, Integer, ForeignKey
from models.base import Base

class PecaProcessual(Base):
    __tablename__ = 'peca_processual'

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_url = Column(String(255), nullable=True)
    documento_localizacao = Column(String(255), nullable=True)
    categoria = Column(String(100), nullable=False)
    nome_peca = Column(String(150), nullable=False)

    def __init__(self, documento_url:str, documento_localizacao:str, categoria:str, nome_peca:str):
        """
        Cria uma PecaProcessual

        Arguments:
            documento_url: URL do documento se estiver hospedado na nuvem.
            documento_localizacao: localização do arquivo no sistema de arquivos.
            categoria: Categoria da peça processual (ex: Trabalhista, Civil, etc.)
            nome_peca: Nome da peça processual (ex: "Petição Inicial", "Recurso", etc.)
        """
        self.documento_url = documento_url
        self.documento_localizacao = documento_localizacao
        self.categoria = categoria
        self.nome_peca = nome_peca