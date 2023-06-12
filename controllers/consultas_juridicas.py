from flask import request, jsonify
from datetime import datetime
from models import db, ConsultaJuridica, Cliente

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
            
            cliente = Cliente.query.filter_by(cpf_do_cliente=cpf_cliente).first()
            if not cliente:
                cliente = Cliente(nova_consulta.nome_cliente, cpf_cliente)
            
            cliente.consultas.append(nova_consulta)
            
            db.session.add(cliente)
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
