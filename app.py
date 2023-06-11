from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import unquote
from flask_cors import CORS
from controllers.consultas_juridicas import ConsultasController
from controllers.clientes import ClientesController

app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o OpenAPI
info = Info(title="Minha API", version="1.0.0")
openapi = OpenAPI(app, info=info)

# Definir tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(name="Consulta Jurídica", description="Criação, atualização, exclusão e obtenção de consultas jurídicas")
cliente_tag = Tag(name="Cliente", description="Criação, atualização, exclusão e obtenção de clientes")

# Inicializar os controladores
consultas_controller = ConsultasController()
clientes_controller = ClientesController()

# Rotas
@app.route('/', methods=['GET'], endpoint='home')
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/consultas', tags=[consulta_tag],
          responses={"201": "Consulta Jurídica criada", "409": "Consulta Jurídica já existe", "422": "Formato de data ou horário inválido"})
def criar_consulta():
    """Cria uma nova Consulta Jurídica.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ConsultaJuridica
          required:
            - nome_cliente
            - cpf_cliente
            - data_consulta
            - horario_consulta
            - detalhes_consulta
          properties:
            nome_cliente:
              type: string
              description: O nome do cliente
            cpf_cliente:
              type: string
              description: O CPF do cliente
            data_consulta:
              type: string
              description: A data da consulta
            horario_consulta:
              type: string
              description: O horário da consulta
            detalhes_consulta:
              type: string
              description: Os detalhes da consulta
    responses:
      201:
        description: Consulta Jurídica criada
      409:
        description: Consulta Jurídica já existe
      422:
        description: Formato de data ou horário inválido
    """
    return consultas_controller.criar_consulta()

@app.put('/consultas/<int:consulta_id>', tags=[consulta_tag],
         responses={"200": "Consulta Jurídica atualizada", "404": "Consulta Jurídica não encontrada", "409": "Outra consulta já existe para este cliente neste horário", "422": "Formato de data ou horário inválido"})
def atualizar_consulta(consulta_id):
    """Atualiza uma Consulta Jurídica existente.
    ---
    parameters:
      - name: consulta_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: ConsultaJuridicaAtualizada
          properties:
            nome_cliente:
              type: string
              description: O nome do cliente
            cpf_cliente:
              type: string
              description: O CPF do cliente
            data_consulta:
              type: string
              description: A data da consulta
            horario_consulta:
              type: string
              description: O horário da consulta
            detalhes_consulta:
              type: string
              description: Os detalhes da consulta
    responses:
      200:
        description: Consulta Jurídica atualizada
      404:
        description: Consulta Jurídica não encontrada
      409:
        description: Outra consulta já existe para este cliente neste horário
      422:
        description: Formato de data ou horário inválido
    """
    return consultas_controller.atualizar_consulta(consulta_id)

@app.delete('/consultas/<int:consulta_id>', tags=[consulta_tag],
            responses={"200": "Consulta Jurídica excluída", "404": "Consulta Jurídica não encontrada"})
def excluir_consulta(consulta_id):
    """Exclui uma Consulta Jurídica.
    ---
    parameters:
      - name: consulta_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Consulta Jurídica excluída
      404:
        description: Consulta Jurídica não encontrada
    """
    return consultas_controller.excluir_consulta(consulta_id)

@app.get('/consultas', tags=[consulta_tag],
         responses={"200": "Lista de consultas encontradas", "404": "Nenhuma consulta encontrada para os parâmetros informados"})
def obter_consultas():
    """Obtém todas as consultas jurídicas ou consultas por data, nome do cliente ou CPF do cliente.
    ---
    parameters:
      - name: data
        in: query
        type: string
      - name: nome_cliente
        in: query
        type: string
      - name: cpf_cliente
        in: query
        type: string
    responses:
      200:
        description: Lista de consultas encontradas
      404:
        description: Nenhuma consulta encontrada para os parâmetros informados
    """
    return consultas_controller.obter_consultas()

@app.get('/consultas/hoje', tags=[consulta_tag],
         responses={"200": "Lista de consultas encontradas para hoje", "404": "Nenhuma consulta encontrada para hoje"})
def obter_consultas_hoje():
    """Obtém as consultas jurídicas de hoje.
    ---
    responses:
      200:
        description: Lista de consultas encontradas para hoje
      404:
        description: Nenhuma consulta encontrada para hoje
    """
    return consultas_controller.obter_consultas_hoje()

@app.get('/consultas/horario', tags=[consulta_tag],
         responses={"200": "Lista de consultas encontradas para a data e horário informados", "400": "Os parâmetros data e horario são obrigatórios", "404": "Nenhuma consulta encontrada para a data e horário informados"})
def obter_consultas_horario():
    """Obtém as consultas jurídicas em um horário específico.
    ---
    parameters:
      - name: data
        in: query
        type: string
        required: true
      - name: horario
        in: query
        type: string
        required: true
    responses:
      200:
        description: Lista de consultas encontradas para a data e horário informados
      400:
        description: Os parâmetros data e horario são obrigatórios
      404:
        description: Nenhuma consulta encontrada para a data e horário informados
    """
    return consultas_controller.obter_consultas_horario()

@app.post('/clientes', tags=[cliente_tag],
          responses={"201": "Cliente criado com sucesso", "409": "Já existe um cliente cadastrado com o CPF informado"})
def criar_cliente():
    """Cria um novo cliente.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Cliente
          required:
            - nome_cliente
            - cpf_cliente
          properties:
            nome_cliente:
              type: string
              description: O nome do cliente
            cpf_cliente:
              type: string
              description: O CPF do cliente
    responses:
      201:
        description: Cliente criado com sucesso
      409:
        description: Já existe um cliente cadastrado com o CPF informado
    """
    return clientes_controller.criar_cliente()

@app.put('/clientes/<int:cliente_id>', tags=[cliente_tag],
         responses={"200": "Cliente atualizado com sucesso", "404": "Cliente não encontrado", "409": "Já existe um cliente cadastrado com o CPF informado"})
def atualizar_cliente(cliente_id):
    """Atualiza um cliente existente.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: ClienteAtualizado
          properties:
            nome_cliente:
              type: string
              description: O nome do cliente
            cpf_cliente:
              type: string
              description: O CPF do cliente
    responses:
      200:
        description: Cliente atualizado com sucesso
      404:
        description: Cliente não encontrado
      409:
        description: Já existe um cliente cadastrado com o CPF informado
    """
    return clientes_controller.atualizar_cliente(cliente_id)

@app.delete('/clientes/<int:cliente_id>', tags=[cliente_tag],
            responses={"200": "Cliente excluído com sucesso", "404": "Cliente não encontrado"})
def excluir_cliente(cliente_id):
    """Exclui um cliente.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cliente excluído com sucesso
      404:
        description: Cliente não encontrado
    """
    return clientes_controller.excluir_cliente(cliente_id)

@app.get('/clientes', tags=[cliente_tag],
         responses={"200": "Lista de clientes encontrados", "404": "Nenhum cliente encontrado para os parâmetros informados"})
def obter_clientes():
    """Obtém todos os clientes ou clientes filtrados por nome, CPF, data de cadastro ou data de atualização.
    ---
    parameters:
      - name: nome
        in: query
        type: string
      - name: cpf
        in: query
        type: string
      - name: data_cadastro
        in: query
        type: string
      - name: data_atualizacao
        in: query
        type: string
    responses:
      200:
        description: Lista de clientes encontrados
      404:
        description: Nenhum cliente encontrado para os parâmetros informados
    """
    return clientes_controller.obter_clientes()

@app.get('/clientes/<int:cliente_id>', tags=[cliente_tag],
         responses={"200": "Cliente encontrado", "404": "Cliente não encontrado"})
def obter_cliente_por_id(cliente_id):
    """Obtém um cliente pelo ID.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cliente encontrado
      404:
        description: Cliente não encontrado
    """
    return clientes_controller.obter_cliente_por_id(cliente_id)

@app.get('/clientes/filtrados', tags=[cliente_tag],
         responses={"200": "Lista de clientes encontrados para os parâmetros informados", "404": "Nenhum cliente encontrado para os parâmetros informados"})
def obter_clientes_filtrados():
    """Obtém clientes filtrados por nome, CPF, data de cadastro ou data de atualização.
    ---
    parameters:
      - name: nome
        in: query
        type: string
      - name: cpf
        in: query
        type: string
      - name: data_cadastro
        in: query
        type: string
      - name: data_atualizacao
        in: query
        type: string
    responses:
      200:
        description: Lista de clientes encontrados para os parâmetros informados
      404:
        description: Nenhum cliente encontrado para os parâmetros informados
    """
    return clientes_controller.obter_clientes_filtrados()

if __name__ == '__main__':
    app.run(debug=True)
