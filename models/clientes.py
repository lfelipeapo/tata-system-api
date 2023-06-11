from datetime import datetime
from sqlalchemy import UniqueConstraint
from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(80), nullable=False)
    cpf_cliente = db.Column(db.String(11), nullable=False, unique=True)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.now())
    data_atualizacao = db.Column(db.DateTime)

    def __init__(self, nome_cliente, cpf_cliente):
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nome_cliente': self.nome_cliente,
            'cpf_cliente': self.cpf_cliente,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M:%S'),
            'data_atualizacao': self.data_atualizacao.strftime('%d/%m/%Y %H:%M:%S') if self.data_atualizacao else None
        }
