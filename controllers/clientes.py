from flask import jsonify, request
from datetime import datetime
from app import db
from models.clientes import Cliente

class ClientesController:
    def criar_cliente(self):
        dados = request.get_json()
        nome_cliente = dados.get('nome_cliente')
        cpf_cliente = dados.get('cpf_cliente')

        if not nome_cliente or not cpf_cliente:
            return jsonify({'mensagem': 'Nome do cliente e CPF do cliente são obrigatórios'}), 400

        cliente_existente = Cliente.query.filter_by(cpf_cliente=cpf_cliente).first()
        if cliente_existente:
            return jsonify({'mensagem': 'Já existe um cliente cadastrado com o CPF informado'}), 409

        novo_cliente = Cliente(nome_cliente=nome_cliente, cpf_cliente=cpf_cliente)
        db.session.add(novo_cliente)
        db.session.commit()

        return jsonify({'mensagem': 'Cliente criado com sucesso'}), 201

    def atualizar_cliente(self, cliente_id):
        dados = request.get_json()
        nome_cliente = dados.get('nome_cliente')
        cpf_cliente = dados.get('cpf_cliente')

        if not nome_cliente or not cpf_cliente:
            return jsonify({'mensagem': 'Nome do cliente e CPF do cliente são obrigatórios'}), 400

        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({'mensagem': 'Cliente não encontrado'}), 404

        cliente_existente = Cliente.query.filter(Cliente.cpf_cliente == cpf_cliente, Cliente.id != cliente_id).first()
        if cliente_existente:
            return jsonify({'mensagem': 'Já existe um cliente cadastrado com o CPF informado'}), 409

        cliente.nome_cliente = nome_cliente
        cliente.cpf_cliente = cpf_cliente
        cliente.data_atualizacao = datetime.now()

        db.session.commit()

        return jsonify({'mensagem': 'Cliente atualizado com sucesso'}), 200

    def excluir_cliente(self, cliente_id):
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({'mensagem': 'Cliente não encontrado'}), 404

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({'mensagem': 'Cliente excluído com sucesso'}), 200

    def obter_clientes(self):
        clientes = Cliente.query.order_by(Cliente.data_cadastro).all()

        if not clientes:
            return jsonify({'mensagem': 'Nenhum cliente encontrado'}), 404

        return jsonify([cliente.serialize for cliente in clientes]), 200

    def obter_cliente_por_id(self, cliente_id):
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({'mensagem': 'Cliente não encontrado'}), 404

        return jsonify(cliente.serialize), 200

    def obter_clientes_filtrados(self):
        nome = request.args.get('nome')
        cpf = request.args.get('cpf')
        data_cadastro = request.args.get('data_cadastro')
        data_atualizacao = request.args.get('data_atualizacao')

        clientes = Cliente.query

        if nome:
            clientes = clientes.filter(Cliente.nome_cliente.ilike(f'%{nome}%'))

        if cpf:
            clientes = clientes.filter(Cliente.cpf_cliente == cpf)

        if data_cadastro:
            clientes = clientes.filter(Cliente.data_cadastro == datetime.strptime(data_cadastro, '%d/%m/%Y'))

        if data_atualizacao:
            clientes = clientes.filter(Cliente.data_atualizacao == datetime.strptime(data_atualizacao, '%d/%m/%Y'))

        clientes = clientes.order_by(Cliente.data_cadastro).all()

        if not clientes:
            return jsonify({'mensagem': 'Nenhum cliente encontrado para os parâmetros informados'}), 404

        return jsonify([cliente.serialize for cliente in clientes]), 200
