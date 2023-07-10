from flask_cors import CORS
from flask import redirect, __name__
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI, Info, Tag
from flask_sqlalchemy import SQLAlchemy
from models.database import db_url
from models.fuso_horario import exp
from models.consultas_juridicas import ConsultaJuridica
from models.clientes import Cliente
from models.users import User
import jwt
from controllers import *
from schemas import *

info = Info(title="Tata System API", version='1.0.0')
app = OpenAPI(__name__, info=info)
db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'America/Sao_Paulo'

# Definir tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(name="Consulta Jurídica",
                   description="Criação, atualização, exclusão e obtenção de consultas jurídicas")
cliente_tag = Tag(
    name="Cliente", description="Criação, atualização, exclusão e obtenção de clientes")
usuario_tag = Tag(
    name="Usuário", description="Criação, atualização, exclusão, obtenção e autenticação de usuários")

# Inicializar os controladores
consultas_controller = ConsultaJuridicaController()
clientes_controller = ClientesController()
users_controller = UserController()

# Rotas

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/consulta', tags=[consulta_tag],
          responses={"200": ConsultaJuridicaViewSchema, "400": MensagemResposta, "409": MensagemResposta, "422": MensagemResposta})
def add_consulta(body: ConsultaJuridicaSchema):
    """Cria uma nova Consulta Jurídica.

    Retorna uma representação de um nova consulta jurídica.
    """
    required_fields = ["nome_cliente", "cpf_cliente",
                       "data_consulta", "horario_consulta"]
    if not all(getattr(body, field, None) for field in required_fields):
        return {"mensagem": "Faltam parâmetros para realizar o cadastro"}, 400
    try:
        consulta = ConsultaJuridica(body.nome_cliente, body.cpf_cliente,
                                    body.data_consulta, body.horario_consulta, body.detalhes_consulta)
    except ValueError:
        return {"mensagem": "Dados informados inválidos ou com erro"}, 400

    return consultas_controller.criar_consulta(consulta)


@app.put('/consulta', tags=[consulta_tag],
         responses={"200": ConsultaJuridicaViewSchema, "404": MensagemResposta, "409": MensagemResposta, "422": MensagemResposta})
def atualizar_consulta(body: ConsultaJuridicaAtualizadaSchema):
    """Atualiza uma Consulta Jurídica existente.

    Retorna uma consulta atualizada.
    """

    return consultas_controller.atualizar_consulta(body.consulta_id,
                                                   body.nome_cliente,
                                                   body.cpf_cliente,
                                                   body.data_consulta,
                                                   body.horario_consulta,
                                                   body.detalhes_consulta)


@app.delete('/consulta', tags=[consulta_tag],
            responses={"200": MensagemResposta, "404": MensagemResposta})
def excluir_consulta(query: ConsultaJuridicaBuscaSchema):
    """Exclui uma Consulta Jurídica.
    """
    return consultas_controller.excluir_consulta(query.consulta_id)


@app.get('/consultas', tags=[consulta_tag],
         responses={"200": ConsultaJuridicaListagemSchema, "404": MensagemResposta})
def obter_consultas(query: ConsultasFiltradasBuscaSchema):
    """Obtém todas as consultas jurídicas ou consultas por data, nome do cliente ou CPF do cliente.
    """
    return consultas_controller.obter_consultas(query.data_consulta, query.nome_cliente, query.cpf)


@app.get('/consultas/hoje', tags=[consulta_tag],
         responses={"200": ConsultaJuridicaListagemSchema, "404": MensagemResposta})
def obter_consultas_hoje():
    """Obtém as consultas jurídicas de hoje.
    """
    return consultas_controller.obter_consultas_hoje()


@app.get('/consultas/horario', tags=[consulta_tag],
         responses={"200": ConsultaJuridicaListagemSchema, "400": MensagemResposta, "404": MensagemResposta})
def obter_consultas_horario(query: ConsultaJuridicaBuscaPorDataEHoraSchema):
    """Obtém as consultas jurídicas em um horário específico para determinada data.
    """
    return consultas_controller.obter_consultas_horario(query.data_consulta, query.horario_consulta)


@app.get('/consulta', tags=[consulta_tag],
         responses={"200": ConsultaJuridicaViewSchema, "404": MensagemResposta})
def obter_consulta_por_id(query: ConsultaJuridicaBuscaSchema):
    """Obtém uma consulta jurídica pelo ID.
    """
    return consultas_controller.obter_consulta_por_id(query.consulta_id)


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": MensagemResposta, "404": MensagemResposta, "400": MensagemResposta, "422": MensagemResposta})
def criar_cliente(body: ClienteSchema):
    """Cria um novo cliente.

    Retorna um novo cliente criado.
    """

    required_fields = ["nome_cliente", "cpf_cliente"]
    if not all(getattr(body, field, None) for field in required_fields):
        return {"mensagem": "Faltam parâmetros para realizar o cadastro"}, 400
    try:
        cliente = Cliente(body.nome_cliente, body.cpf_cliente)
    except ValueError:
        return {"mensagem": "Dados informados inválidos ou com erro"}, 400

    return clientes_controller.criar_cliente(cliente)


@app.put('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": MensagemResposta, "409": MensagemResposta, "400": MensagemResposta, "422": MensagemResposta})
def atualizar_cliente(body: ClienteAtualizadoSchema):
    """Atualiza um cliente existente.

    Retorna uma representação de um cliente atualizado.
    """
    return clientes_controller.atualizar_cliente(body.cliente_id, body.nome_cliente, body.cpf_cliente)


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": MensagemResposta, "404": MensagemResposta, "422": MensagemResposta})
def excluir_cliente(query: ClienteBuscaSchema):
    """Exclui um cliente.

    Retorna uma mensagem de confirmação ou não da exclusão.
    """
    return clientes_controller.excluir_cliente(query.cliente_id)


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ClienteListagemSchema, "404": MensagemResposta, "422": MensagemResposta})
def obter_clientes(query: ClientesFiltradosSchema):
    """Obtém todos os clientes ou clientes filtrados por nome, CPF, data de cadastro ou data de atualização.

    Retorna uma lista de clientes.
    """
    return clientes_controller.obter_clientes(query.nome,
                                              query.cpf,
                                              query.data_cadastro,
                                              query.data_atualizacao
                                              )


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": MensagemResposta, "422": MensagemResposta})
def obter_cliente_por_id(query: ClienteBuscaSchema):
    """Obtém um cliente pelo ID.

    Retorna uma representação de um cliente.
    """
    return clientes_controller.obter_cliente_por_id(query.cliente_id)


@app.post('/user/create', tags=[usuario_tag],
          responses={"201": UserViewSchema, "400": MensagemResposta, "422": MensagemResposta})
def create_user(body: UserSchema):
    """Cria um usuário.

    Retorna uma representação do usuário salvo no banco de dados.
    """
    return users_controller.create_user(body.username, body.password, body.name, body.image)


@app.post('/user/authenticate', tags=[usuario_tag],
          responses={"200": UserViewSchema, "401": MensagemResposta})
def authenticate_user(body: UserAuthenticateSchema):
    """Realiza a autenticação de usuário

    Retorna uma mensagem de sucesso ou dados inválidos.
    """
    user = users_controller.authenticate_user(body.username, body.password)
    if user:
        payload = {
            'user_id': user['id'],
            'exp': exp
        }
        token = jwt.encode(payload, user['password'], algorithm='HS256')
        return {'user_id': user['id'], 'token': token}, 200
    else:
        return {'mensagem': 'Dados de usuário ou senha inválidos'}, 401


@app.put('/user', tags=[usuario_tag],
         responses={"200": UserViewSchema, "404": MensagemResposta, "409": MensagemResposta, "400": MensagemResposta, "422": MensagemResposta})
def atualizar_user(body: UserAtualizadoSchema):
    """Atualiza um usuário existente.

    Retorna uma representação de um usuário atualizado.
    """
    return users_controller.atualizar_user(body.id, body.username, body.password, body.name, body.image)


@app.delete('/user', tags=[usuario_tag],
            responses={"200": MensagemResposta, "404": MensagemResposta, "422": MensagemResposta})
def excluir_user(query: UserBuscaSchema):
    """Exclui um usuário.

    Retorna uma mensagem de confirmação ou não da exclusão.
    """
    return users_controller.excluir_user(query.id)


@app.get('/user', tags=[usuario_tag],
         responses={"200": UserViewSchema, "404": MensagemResposta, "422": MensagemResposta})
def obter_user_por_id(query: UserBuscaSchema):
    """Obtém um usuário pelo ID.

    Retorna uma representação de um usuário.
    """
    return users_controller.obter_user_por_id(query.id)


@app.get('/users', tags=[usuario_tag],
         responses={"200": UsersListagemSchema, "404": MensagemResposta, "422": MensagemResposta})
def obter_users():
    """Obtém todos os usuários do banco de dados.

    Retorna uma lista de usuários.
    """
    return users_controller.obter_users()


if __name__ == '__main__':
    app.run(debug=True)
