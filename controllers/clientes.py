from flask import jsonify, request
from datetime import datetime
from models.clientes import Cliente
from models.consultas_juridicas import ConsultaJuridica
from models import Session
from models.fuso_horario import saopaulo_tz, now_saopaulo
from typing import List, Union
from sqlalchemy import func

class ClientesController:
    def criar_cliente(self, cliente: Cliente):
        session = Session()
        try:
            nome_cliente = cliente.nome_cliente
            cpf_cliente = cliente.cpf_cliente

            if not nome_cliente or not cpf_cliente:
                return {'mensagem': 'Nome do cliente e CPF do cliente são obrigatórios'}, 400


            if len(cpf_cliente) > 11:
                    return {"mensagem": "Digite apenas números. O CPF deve ter no máximo 11 caracteres."}, 400
            
            cliente_existente = session.query(Cliente).filter_by(
                cpf_cliente=cpf_cliente).first()
            if cliente_existente:
                return {'mensagem': 'Já existe um cliente cadastrado com o CPF informado'}, 409

            novo_cliente = Cliente(
                nome_cliente=nome_cliente, cpf_cliente=cpf_cliente)
            session.add(novo_cliente)
            session.commit()

            return self.apresenta_cliente(novo_cliente), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422

    def atualizar_cliente(self, cliente_id: int, nome_cliente: Union[str, None] = None, cpf_cliente: Union[str, None] = None):
        if not cliente_id:
            return {'mensagem': 'É obrigatório informar o id do cliente'}, 400
        session = Session()
        try:

            if not nome_cliente and not cpf_cliente:
                return {'mensagem': 'Nenhum dado de cliente para atualizar'}, 400

            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                return {'mensagem': 'Cliente não encontrado'}, 404

            if cpf_cliente:
                if len(cpf_cliente) > 11:
                    return {"mensagem": "Digite apenas números. O CPF deve ter no máximo 11 caracteres."}, 400
                cliente_existente = session.query(Cliente).filter(
                    Cliente.cpf_cliente == cpf_cliente, Cliente.id != cliente_id).first()
                if cliente_existente:
                    return {'mensagem': 'Já existe um cliente cadastrado com o CPF informado'}, 409

                cliente.cpf_cliente = cpf_cliente

            if nome_cliente:
                cliente.nome_cliente = nome_cliente

            cliente.data_atualizacao = now_saopaulo()

            session.commit()

            return self.apresenta_cliente(cliente), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422

    def excluir_cliente(self, cliente_id: int):
        if not cliente_id:
            return {'mensagem': "É obrigatório informar o Id do cliente"}
        session = Session()
        try:
            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                return {'mensagem': 'Cliente não encontrado'}, 404

            consulta = session.query(ConsultaJuridica).filter_by(cliente_id=cliente_id).first()

            session.delete(cliente)
            if consulta:
                session.delete(consulta)
            session.commit()

            return {'mesangem': 'Cliente excluído com sucesso'}, 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422

    def obter_cliente_por_id(self, cliente_id: int):
        if not cliente_id:
            return {'mensagem': 'É obrigatório informar o Id do cliente'}, 400
        session = Session()
        try:
            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                return {'mensagem': 'Cliente não encontrado'}, 404

            return self.apresenta_cliente(cliente), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422

    def obter_clientes(self, nome: Union[str, None] = None, cpf: Union[str, None] = None, data_cadastro: Union[str, None] = None, data_atualizacao: Union[str, None] = None):
        session = Session()
        try:
            query = session.query(Cliente)

            if nome:
                query = query.filter(Cliente.nome_cliente.ilike(f'%{nome}%'))
            if cpf:
                query = query.filter(Cliente.cpf_cliente == cpf)
            if data_cadastro:
                data_cadastro = datetime.strptime(data_cadastro, '%d/%m/%Y').date()
                query = query.filter(func.date(Cliente.data_cadastro) == data_cadastro)
            if data_atualizacao:
                data_atualizacao = datetime.strptime(data_atualizacao, '%d/%m/%Y').date()
                query = query.filter(func.date(Cliente.data_atualizacao) == data_atualizacao)

            clientes = query.all()

            if not clientes:
                return {'mensagem': 'Nenhum cliente encontrado'}, 404

            return self.apresenta_clientes(clientes), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro:' + str(e)}, 422

    @staticmethod
    def apresenta_cliente(cliente: Cliente):
        return {
            'id': cliente.id,
            'nome_cliente': cliente.nome_cliente,
            'cpf_cliente': cliente.cpf_cliente,
            'data_cadastro': cliente.data_cadastro.astimezone(saopaulo_tz).strftime('%d/%m/%Y %H:%M:%S'),
            'data_atualizacao': cliente.data_atualizacao.astimezone(saopaulo_tz).strftime('%d/%m/%Y %H:%M:%S') if cliente.data_atualizacao else None
        }

    @staticmethod
    def apresenta_clientes(clientes: List[Cliente]):
        result = []
        for cliente in clientes:
            result.append({
                'id': cliente.id,
                'nome_cliente': cliente.nome_cliente,
                'cpf_cliente': cliente.cpf_cliente,
                'data_cadastro': cliente.data_cadastro.astimezone(saopaulo_tz).strftime('%d/%m/%Y %H:%M:%S'),
                'data_atualizacao': cliente.data_atualizacao.astimezone(saopaulo_tz).strftime('%d/%m/%Y %H:%M:%S') if cliente.data_atualizacao else None
            })
        return {"clientes": result}
