from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, or_, and_
from datetime import datetime, time

db = SQLAlchemy()

class ConsultaJuridica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(80), nullable=False)
    cpf_cliente = db.Column(db.String(11), nullable=False)
    data_consulta = db.Column(db.Date, nullable=False)
    horario_consulta = db.Column(db.Time, nullable=False)
    detalhes_consulta = db.Column(db.String(200))

    UniqueConstraint('cpf_cliente', 'data_consulta', name='consulta_unico')

    def __init__(self, dados):
        if not self.valida_data(dados['data_consulta']) or not self.valida_hora(dados['horario_consulta']):
            raise ValueError('Formato de data ou horário inválido')
        self.nome_cliente = dados['nome_cliente']
        self.cpf_cliente = dados['cpf_cliente']
        self.data_consulta = datetime.strptime(dados['data_consulta'], '%d/%m/%Y').date()
        self.horario_consulta = datetime.strptime(dados['horario_consulta'], '%H:%M').time()
        self.detalhes_consulta = dados['detalhes_consulta']

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

class ConsultaJuridicaController:
    def criar_consulta(self):
        dados = request.get_json()
        try:
            nova_consulta = ConsultaJuridica(dados)
            cpf_cliente = nova_consulta.cpf_cliente
            data_consulta = nova_consulta.data_consulta
            
            if not nova_consulta.valida_consulta_dia(cpf_cliente, data_consulta):
                return jsonify({'mensagem': 'Já existe uma consulta agendada para este CPF nesta data'}), 409
            
            if not nova_consulta.valida_consulta_periodo(cpf_cliente, data_consulta, nova_consulta.horario_consulta):
                return jsonify({'mensagem': 'Já existe uma consulta agendada para este CPF neste período'}), 409
            
            db.session.add(nova_consulta)
            db.session.commit()
            return jsonify({'mensagem': 'Consulta Jurídica criada'}), 201
        except ValueError as e:
            return jsonify({'mensagem': str(e)}), 422

    def atualizar_consulta(self, id):
        dados = request.get_json()
        consulta_juridica = ConsultaJuridica.query.get(id)
        if not consulta_juridica:
            return jsonify({'mensagem': 'Consulta Jurídica não encontrada'}), 404
        try:
            cpf_cliente = dados['cpf_cliente']
            data_consulta = datetime.strptime(dados['data_consulta'], '%d/%m/%Y').date()
            horario_consulta = datetime.strptime(dados['horario_consulta'], '%H:%M').time()

            if not consulta_juridica.valida_consulta_dia(cpf_cliente, data_consulta):
                return jsonify({'mensagem': 'Já existe uma consulta agendada para este CPF nesta data'}), 409

            if not consulta_juridica.valida_consulta_periodo(cpf_cliente, data_consulta, horario_consulta):
                return jsonify({'mensagem': 'Já existe uma consulta agendada para este CPF neste período'}), 409

            consulta_juridica.nome_cliente = dados['nome_cliente']
            consulta_juridica.cpf_cliente = dados['cpf_cliente']
            consulta_juridica.data_consulta = datetime.strptime(dados['data_consulta'], '%d/%m/%Y').date()
            consulta_juridica.horario_consulta = datetime.strptime(dados['horario_consulta'], '%H:%M').time()
            consulta_juridica.detalhes_consulta = dados['detalhes_consulta']
            db.session.commit()
            return jsonify({'mensagem': 'Consulta Jurídica atualizada'}), 200
        except ValueError as e:
            return jsonify({'mensagem': str(e)}), 422

    def excluir_consulta(self, id):
        consulta_juridica = ConsultaJuridica.query.get(id)
        if not consulta_juridica:
            return jsonify({'mensagem': 'Consulta Jurídica não encontrada'}), 404
        db.session.delete(consulta_juridica)
        db.session.commit()
        return jsonify({'mensagem': 'Consulta Jurídica excluída'}), 200

    def obter_consultas(self):
        data = request.args
        if 'data' in data:
            consultas = ConsultaJuridica.query.filter_by(data_consulta=datetime.strptime(data['data'], '%d/%m/%Y').date()).all()
        elif 'nome_cliente' in data:
            consultas = ConsultaJuridica.query.filter_by(nome_cliente=data['nome_cliente']).all()
        elif 'cpf_cliente' in data:
            consultas = ConsultaJuridica.query.filter_by(cpf_cliente=data['cpf_cliente']).all()
        else:
            consultas = ConsultaJuridica.query.all()
        if not consultas:
            return jsonify({'mensagem': 'Nenhuma consulta encontrada para os parâmetros informados'}), 404
        return jsonify([consulta.serialize for consulta in consultas]), 200

    def obter_consultas_hoje(self):
        consultas = ConsultaJuridica.query.filter_by(data_consulta=datetime.today().date()).all()
        if not consultas:
            return jsonify({'mensagem': 'Nenhuma consulta encontrada para hoje'}), 404
        return jsonify([consulta.serialize for consulta in consultas]), 200

    def obter_consultas_horario(self):
        data = request.args.get('data')
        horario = request.args.get('horario')
        if not data or not horario:
            return jsonify({'mensagem': 'Os parâmetros data e horario são obrigatórios'}), 400
        consultas = ConsultaJuridica.query.filter_by(data_consulta=datetime.strptime(data, '%d/%m/%Y').date(), horario_consulta=datetime.strptime(horario, '%H:%M').time()).all()
        if not consultas:
            return jsonify({'mensagem': 'Nenhuma consulta encontrada para a data e horário informados'}), 404
        return jsonify([consulta.serialize for consulta in consultas]), 200
