from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.clientes import Cliente
from models.consultas_juridicas import ConsultaJuridica

class Documento(Base):
    __tablename__ = 'documento'

    id = Column(Integer, primary_key=True)
    documento_nome = Column(String(200), nullable=False)
    documento_localizacao = Column(String(200))
    documento_url = Column(String(200))
    cliente_id = Column(Integer, ForeignKey('cliente.id', ondelete='CASCADE'))
    consulta_id = Column(Integer, ForeignKey('consulta_juridica.pk_consulta'))

    cliente = relationship('Cliente', backref='documentos')
    consulta = relationship('ConsultaJuridica', backref='documentos')

    def __init__(self, documento_nome:str, documento_localizacao:str, documento_url:str, cliente_id:int, consulta_id:int):
        """
        Cria um Documento

        Arguments:
            documento_nome: nome do documento.
            documento_localizacao: localização do arquivo no sistema de arquivos.
            documento_url: URL do documento se estiver hospedado na nuvem.
            cliente_id: ID do cliente associado ao documento.
            consulta_id: ID da consulta associada ao documento.
        """
        self.documento_nome = documento_nome
        self.documento_localizacao = documento_localizacao
        self.documento_url = documento_url
        self.cliente_id = cliente_id
        self.consulta_id = consulta_id
