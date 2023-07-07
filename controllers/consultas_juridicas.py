from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models.consultas_juridicas import ConsultaJuridica 
from models.clientes import Cliente 
from models import Session
from models.fuso_horario import now_saopaulo
from typing import Union, List

class ConsultaJuridicaController:

    def criar_consulta(self, consulta: ConsultaJuridica):
        session = Session()
        if not consulta:
            return {'mensagem': 'Parâmetros obrigatórios não informados'}
        try:
            if not consulta.valida_consulta_dia(consulta.cpf_cliente, consulta.data_consulta):
                return {'mensagem': 'Já existe uma consulta agendada para este CPF nesta data'}, 409

            if not consulta.valida_consulta_periodo(consulta.cpf_cliente, consulta.data_consulta, consulta.horario_consulta):
                return {'mensagem': 'Já existe uma consulta agendada para este CPF neste período'}, 409
            
            cliente = session.query(Cliente).filter_by(cpf_cliente=consulta.cpf_cliente).first()
            if not cliente:
                cliente = Cliente(consulta.nome_cliente, consulta.cpf_cliente)
                session.add(cliente)
                session.commit()

            consulta.cliente_id = cliente.id
            session.add(consulta)
            session.commit()
            
            return self.apresenta_consulta(consulta), 200
        
        except Exception as e:
            return {'mensagem': str(e)}, 400
        
        except IntegrityError as e:
            return {"mensagem": "Consulta idêntica já cadastrada na base"}, 409

        finally:
            session.close()  

    def atualizar_consulta(self, 
                           consulta_id: int, 
                           nome_cliente: Union[str, None] = None, 
                           cpf_cliente: Union[str, None] = None, 
                           data_consulta: Union[str, None] = None,
                           horario_consulta: Union[str, None] = None,
                           detalhes_consulta: Union[str, None] = None
                           ):
        session = Session()
        if not consulta_id:
            return {'mensagem': 'Parâmetro Id é obrigatório.'}
        consulta = session.query(ConsultaJuridica).get(consulta_id)
        if not consulta:
            return {'mensagem': 'Consulta Jurídica não encontrada'}, 404
        try:

            if cpf_cliente and data_consulta:
                if not consulta.valida_consulta_dia(cpf_cliente, data_consulta):
                    return {'mensagem': 'Já existe uma consulta agendada para este CPF nesta data'}, 409

            if cpf_cliente and horario_consulta and horario_consulta:
                if not consulta.valida_consulta_periodo(cpf_cliente, data_consulta, horario_consulta):
                    return {'mensagem': 'Já existe uma consulta agendada para este CPF neste período'}, 409

            if nome_cliente: 
                consulta.nome_cliente = nome_cliente
            if cpf_cliente: 
                if len(cpf_cliente) > 11:
                    return {"mensagem": "Digite apenas números. O CPF deve ter no máximo 11 caracteres."}, 400
                consulta.cpf_cliente = cpf_cliente
            if data_consulta and data_consulta != '': 
                consulta.data_consulta = datetime.strptime(data_consulta, "%d-%m-%Y").date()
            if horario_consulta and horario_consulta != '': 
                consulta.horario_consulta = datetime.strptime(horario_consulta, "%H:%M").time()
            if detalhes_consulta: 
                consulta.detalhes_consulta = detalhes_consulta

            cliente = session.query(Cliente).filter(Cliente.id == consulta.cliente_id).first()

            if not cliente:
                return {'mensagem': 'Não existem clientes para este agendamento'}, 404
            
            cliente.cpf_cliente = consulta.cpf_cliente
            cliente.nome_cliente = consulta.nome_cliente
            cliente.data_atualizacao = now_saopaulo()

            session.add(cliente)
            session.add(consulta)
            session.commit()

            return self.apresenta_consulta(consulta), 200
        except ValueError as e:
            return {'mensagem': str(e)}, 422
        finally:
            session.close()

    def excluir_consulta(self, consulta_id: int):
        try:
            session = Session()
            if not consulta_id:
                return {'mensagem': 'Parâmetro Id é obrigatório'}, 400
            consulta_juridica = session.query(ConsultaJuridica).get(consulta_id)
            if not consulta_juridica:
                return {'mensagem': 'Consulta Jurídica não encontrada'}, 404
            session.delete(consulta_juridica)
            session.commit()
            return {'mensagem': 'Consulta Jurídica excluída'}, 200
        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro: " + str(e)}, 500
        finally:
            session.close()

    def obter_consultas(self, 
                        data: Union[str, None] = None, 
                        nome: Union[str, None] = None, 
                        cpf: Union[str, None] = None):
        session = Session()
        try:
            if data:
                consultas = session.query(ConsultaJuridica).filter_by(data_consulta=datetime.strptime(data, '%d/%m/%Y').date()).all()
            elif nome:
                consultas = session.query(ConsultaJuridica).filter_by(nome_cliente=nome).all()
            elif cpf:
                consultas = session.query(ConsultaJuridica).filter_by(cpf_cliente=cpf).all()
            else:
                consultas = session.query(ConsultaJuridica).all()

            if not consultas:
                return {'mensagem': 'Nenhuma consulta encontrada para os parâmetros informados'}, 404

            return self.apresenta_consultas(consultas), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter consultas: ' + str(e)}, 500
        finally:
            session.close()

    def obter_consultas_hoje(self):
        session = Session()
        try:
            consultas = session.query(ConsultaJuridica).filter_by(data_consulta=datetime.today().date()).all()
            if not consultas:
                return {'mensagem': 'Nenhuma consulta encontrada para hoje'}, 404

            return self.apresenta_consultas(consultas), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter consultas: ' + str(e)}, 500
        finally:
            session.close()

    def obter_consultas_horario(self, data: Union[str, None] = None, horario: Union[str, None] = None):
        session = Session()
        try:
            if not data or not horario:
                return {'mensagem': 'Os parâmetros data e horario são obrigatórios'}, 400
            consultas = session.query(ConsultaJuridica).filter_by(data_consulta=datetime.strptime(data, '%d/%m/%Y').date(), horario_consulta=datetime.strptime(horario, '%H:%M').time()).all()
            if not consultas:
                return {'mensagem': 'Nenhuma consulta encontrada para a data e horário informados'}, 404

            return self.apresenta_consultas(consultas), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter consultas por horário: ' + str(e)}, 500
        finally:
            session.close()

    def obter_consulta_por_id(self, consulta_id: int):
        session = Session()
        try:
            if not consulta_id:
                return {'mensagem': 'Parâmetro Id é obrigatório'}, 400
            consulta = session.query(ConsultaJuridica).get(consulta_id)
            if not consulta:
                return {'mensagem': 'Consulta Jurídica não encontrada'}, 404
            
            return self.apresenta_consulta(consulta), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter a consulta: ' + str(e)}, 500
        finally:
            session.close()
    
    @staticmethod
    def apresenta_consulta(consulta: ConsultaJuridica):
        return {
                "id": consulta.id,
                "nome_cliente": consulta.nome_cliente,
                "cpf_cliente": consulta.cpf_cliente,
                "data_consulta": consulta.data_consulta.strftime('%d/%m/%Y'),
                "horario_consulta": consulta.horario_consulta.strftime("%H:%M"),
                "detalhes_consulta": consulta.detalhes_consulta
            }
    
    @staticmethod
    def apresenta_consultas(consultas: List[ConsultaJuridica]):
        result = []
        for consulta in consultas:
            result.append({
                "id": consulta.id,
                "nome_cliente": consulta.nome_cliente,
                "cpf_cliente": consulta.cpf_cliente,
                "data_consulta": consulta.data_consulta.strftime('%d/%m/%Y'),
                "horario_consulta": consulta.horario_consulta.strftime("%H:%M"),
                "detalhes_consulta": consulta.detalhes_consulta
            })
        return {"consultas": result}
