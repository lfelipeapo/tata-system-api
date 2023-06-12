from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime, time

db = SQLAlchemy()

class ConsultaJuridica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(80), nullable=False)
    cpf_cliente = db.Column(db.String(11), nullable=False)
    data_consulta = db.Column(db.Date, nullable=False)
    horario_consulta = db.Column(db.Time, nullable=False)
    detalhes_consulta = db.Column(db.String(200))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)

    UniqueConstraint('cpf_cliente', 'data_consulta', name='consulta_unico')

    def __init__(self, dados):
        if not self.valida_data(dados['data_consulta']) or not self.valida_hora(dados['horario_consulta']):
            raise ValueError('Formato de data ou horário inválido')
        self.nome_cliente = dados['nome_cliente']
        self.cpf_cliente = dados['cpf_cliente']
        self.data_consulta = datetime.strptime(dados['data_consulta'], '%d/%m/%Y').date()
        self.horario_consulta = datetime.strptime(dados['horario_consulta'], '%H:%M').time()
        self.detalhes_consulta = dados['detalhes_consulta']

        cliente = Cliente.query.filter_by(cpf_do_cliente=self.cpf_cliente).first()
        if cliente:
            self.cliente = cliente

    @staticmethod
    def valida_data(data_str):
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def valida_hora(hora_str):
        try:
            datetime.strptime(hora_str, '%H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def valida_consulta_dia(cpf_cliente, data_consulta):
        consulta = ConsultaJuridica.query.filter_by(cpf_cliente=cpf_cliente, data_consulta=data_consulta).first()
        return consulta is None

    @staticmethod
    def valida_consulta_periodo(cpf_cliente, data_consulta, horario_consulta):
        manha_inicio = time(9, 0)
        manha_fim = time(12, 0)
        tarde_inicio = time(13, 0)
        tarde_fim = time(18, 0)
        
        consulta_periodo = ConsultaJuridica.query.filter_by(cpf_cliente=cpf_cliente, data_consulta=data_consulta).first()
        if consulta_periodo is None:
            return True
        
        if horario_consulta >= manha_inicio and horario_consulta <= manha_fim:
            return consulta_periodo.horario_consulta < manha_inicio or consulta_periodo.horario_consulta > manha_fim
        elif horario_consulta >= tarde_inicio and horario_consulta <= tarde_fim:
            return consulta_periodo.horario_consulta < tarde_inicio or consulta_periodo.horario_consulta > tarde_fim
        else:
            return False

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nome_cliente': self.nome_cliente,
            'cpf_cliente': self.cpf_cliente,
            'data_consulta': self.data_consulta.strftime('%d/%m/%Y'),
            'horario_consulta': self.horario_consulta.strftime('%H:%M'),
            'detalhes_consulta': self.detalhes_consulta
        }
