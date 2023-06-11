from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from flask_cors import CORS

from consultas_juridicas import ConsultaJuridicaController

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_juridica_tag = Tag(name="Consulta Jurídica", description="Criação, atualização, exclusão e obtenção de consultas jurídicas")

consulta_juridica_controller = ConsultaJuridicaController()


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/consultas', tags=[consulta_juridica_tag],
          responses={"201": "Consulta Jurídica criada", "409": "Consulta Jurídica já existe", "422": "Formato de data ou horário inválido"})
def criar_consulta():
    """Cria uma nova Consulta Jurídica
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
    return consulta_juridica_controller.criar_consulta()


@app.route('/consultas/<int:id>', methods=['PUT'])
@app.put('/consultas/<int:id>', tags=[consulta_juridica_tag],
         responses={"200": "Consulta Jurídica atualizada", "404": "Consulta Jurídica não encontrada", "409": "Outra consulta já existe para este cliente neste horário", "422": "Formato de data ou horário inválido"})
def atualizar_consulta(id):
    """Atualiza uma Consulta Jurídica existente
    ---
    parameters:
      - name: id
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
    return consulta_juridica_controller.atualizar_consulta(id)


@app.route('/consultas/<int:id>', methods=['DELETE'])
@app.delete('/consultas/<int:id>', tags=[consulta_juridica_tag],
            responses={"200": "Consulta Jurídica excluída", "404": "Consulta Jurídica não encontrada"})
def excluir_consulta(id):
    """Exclui uma Consulta Jurídica
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Consulta Jurídica excluída
      404:
        description: Consulta Jurídica não encontrada
    """
    return consulta_juridica_controller.excluir_consulta(id)


@app.route('/consultas', methods=['GET'])
@app.get('/consultas', tags=[consulta_juridica_tag],
         responses={"200": "Lista de consultas encontradas", "404": "Nenhuma consulta encontrada para os parâmetros informados"})
def obter_consultas():
    """Obtém todas as consultas jurídicas ou consultas por data, nome do cliente ou CPF do cliente
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
    return consulta_juridica_controller.obter_consultas()


@app.get('/consultas/hoje', tags=[consulta_juridica_tag],
         responses={"200": "Lista de consultas encontradas para hoje", "404": "Nenhuma consulta encontrada para hoje"})
def obter_consultas_hoje():
    """Obtém as consultas jurídicas de hoje
    ---
    responses:
      200:
        description: Lista de consultas encontradas para hoje
      404:
        description: Nenhuma consulta encontrada para hoje
    """
    return consulta_juridica_controller.obter_consultas_hoje()


@app.get('/consultas/horario', tags=[consulta_juridica_tag],
         responses={"200": "Lista de consultas encontradas para a data e horário informados", "400": "Os parâmetros data e horario são obrigatórios", "404": "Nenhuma consulta encontrada para a data e horário informados"})
def obter_consultas_horario():
    """Obtém as consultas jurídicas em um horário específico
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
    return consulta_juridica_controller.obter_consultas_horario()
