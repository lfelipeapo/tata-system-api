from sqlalchemy import Column, String, Integer, Date, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, time
from models.base import Base 
from models.database import Session
from models.clientes import Cliente
from typing import Union

class ConsultaJuridica(Base):
    __tablename__ = 'consulta_juridica'

    id = Column("pk_consulta", Integer, primary_key=True)
    nome_cliente = Column(String(80))
    cpf_cliente = Column(String(11))
    data_consulta = Column(Date)
    horario_consulta = Column(Time)
    detalhes_consulta = Column(String(200))
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente', backref='consultas')

    UniqueConstraint('cpf_cliente', 'data_consulta', name='consulta_unico')

    def __init__(self, nome_cliente: str, cpf_cliente: str, data_consulta: Date, horario_consulta: Time, detalhes_consulta: Union[str, None] = None):
        """
        Inicializa uma consulta jurídica

        Arguments:
            nome_cliente: nome do cliente.
            cpf_cliente: CPF do cliente.
            data_consulta: data da consulta
            horario_consulta: horário de agendamento da consulta
            detalhes_consulta:  informações a respeito da consulta
            Deve incluir 'nome_cliente', 'cpf_cliente', 'data_consulta', 'horario_consulta' e 'detalhes_consulta'
        """
        try:
            session = Session()
            if not self.valida_data(data_consulta) or not self.valida_hora(horario_consulta):
                raise ValueError('Formato de data ou horário inválido')
            self.nome_cliente = nome_cliente
            self.cpf_cliente = cpf_cliente
            self.data_consulta = datetime.strptime(
                data_consulta, '%d/%m/%Y').date()
            self.horario_consulta = datetime.strptime(
                horario_consulta, '%H:%M').time()
            self.detalhes_consulta = detalhes_consulta

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def valida_data(data_str: str) -> bool:
        """
        Verifica se uma string está em um formato de data válido

        Arguments:
            data_str: A string a ser verificada

        Returns:
            True se a string estiver em um formato válido, False caso contrário
        """
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def valida_hora(hora_str: str) -> bool:
        """
        Verifica se uma string está em um formato de hora válido

        Arguments:
            hora_str: A string a ser verificada

        Returns:
            True se a string estiver em um formato válido, False caso contrário
        """
        try:
            datetime.strptime(hora_str, '%H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def valida_consulta_dia(cpf_cliente: str, data_consulta: Date) -> bool:
        """
        Verifica se já existe uma consulta no mesmo dia para o cliente

        Arguments:
            cpf_cliente: O CPF do cliente
            data_consulta: A data da consulta

        Returns:
            True se não houver consulta no mesmo dia, False caso contrário
        """
        session = Session()
        consulta = session.query(ConsultaJuridica).filter_by(
            cpf_cliente=cpf_cliente, data_consulta=data_consulta).first()
        return consulta is None

    @staticmethod
    def valida_consulta_periodo(cpf_cliente: str, data_consulta: Date, horario_consulta: Time) -> bool:
        """
        Verifica se já existe uma consulta no mesmo período para o cliente

        Arguments:
            cpf_cliente: O CPF do cliente
            data_consulta: A data da consulta
            horario_consulta: O horário da consulta

        Returns:
            True se não houver consulta no mesmo período, False caso contrário
        """
        manha_inicio = time(9, 0)
        manha_fim = time(12, 0)
        tarde_inicio = time(13, 0)
        tarde_fim = time(18, 0)

        session = Session()
        consulta_periodo = session.query(ConsultaJuridica).filter_by(
            cpf_cliente=cpf_cliente, data_consulta=data_consulta).first()
        if consulta_periodo is None:
            return True

        if horario_consulta >= manha_inicio and horario_consulta <= manha_fim:
            return consulta_periodo.horario_consulta < manha_inicio or consulta_periodo.horario_consulta > manha_fim
        elif horario_consulta >= tarde_inicio and horario_consulta <= tarde_fim:
            return consulta_periodo.horario_consulta < tarde_inicio or consulta_periodo.horario_consulta > tarde_fim
        else:
            return False
