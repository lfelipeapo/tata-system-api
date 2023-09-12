
import os
from flask_cors import CORS
from flask import redirect, request, send_from_directory, __name__, url_for
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI, Info, Tag
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

import jwt

from controllers import *
from models.database import db_url
from models.fuso_horario import exp
from models.consultas_juridicas import ConsultaJuridica
from models.clientes import Cliente
from models.upload import documents
from models.users import User
from models.documentos import Documento
from schemas import *

info = Info(title="Thata System API", version='1.0.0')
app = OpenAPI(__name__, info=info)
db = SQLAlchemy()
migrate = Migrate(app, db)
images = UploadSet('images', IMAGES)
db.init_app(app)
CORS(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'America/Sao_Paulo'
app.config['UPLOADED_DOCUMENTS_DEST'] = os.path.abspath('public/uploads/documents')
app.config['UPLOADED_IMAGES_DEST'] = os.path.abspath('public/uploads/images')

# Configuração Uploads Local
configure_uploads(app, documents)
configure_uploads(app, images)

# Definir tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(name="Consulta Jurídica", description="Criação, atualização, exclusão e obtenção de consultas jurídicas")
cliente_tag = Tag(name="Cliente", description="Criação, atualização, exclusão e obtenção de clientes")
documento_tag = Tag(name="Documento", description="Criação, atualização, exclusão e obtenção de documentos")
image_tag = Tag(name="Image", description="Upload de imagens")
usuario_tag = Tag(name="Usuário", description="Criação, atualização, exclusão, obtenção e autenticação de usuários")

# Inicializar os controladores
consultas_controller = ConsultaJuridicaController()
clientes_controller = ClientesController()
documentos_controller = DocumentoController()
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

@app.post('/documento', tags=[documento_tag],
          responses={"200": DocumentoViewSchema, "400": MensagemResposta, "409": MensagemResposta, "422": MensagemResposta})
def criar_documento(body: DocumentoSchema):
    """Cria um novo Documento.

    Retorna um novo documento criado.
    """
    return documentos_controller.criar_documento(body.documento_nome, body.cliente_id, body.consulta_id, body.documento_localizacao, body.documento_url)

@app.put('/documento', tags=[documento_tag],
         responses={"200": DocumentoViewSchema, "404": MensagemResposta, "409": MensagemResposta, "422": MensagemResposta})
def atualizar_documento(body: DocumentoAtualizadoSchema):
    """Atualiza um Documento existente.

    Retorna uma representação de um documento atualizado.
    """
    return documentos_controller.atualizar_documento(body.id, body.documento_nome, body.cliente_id, body.consulta_id, body.documento_localizacao, body.documento_url)

@app.delete('/documento', tags=[documento_tag],
            responses={"200": MensagemResposta, "404": MensagemResposta})
def excluir_documento(query: DocumentoBuscaSchema):
    """Exclui um Documento.
    """
    return documentos_controller.excluir_documento(query.documento_id)

@app.get('/documento', tags=[documento_tag],
         responses={"200": DocumentoViewSchema, "404": MensagemResposta})
def obter_documento_por_id(query: DocumentoBuscaSchema):
    """Obtém um Documento pelo ID.
    """
    return documentos_controller.obter_documento_por_id(query.documento_id)

@app.get('/documentos', tags=[documento_tag],
         responses={"200": DocumentoListagemSchema, "404": MensagemResposta})
def obter_todos_documentos():
    """Obtém todos os Documentos.
    """
    return documentos_controller.obter_todos_documentos()
@app.post('/documento/upload', tags=[documento_tag],
          responses={"200": MensagemResposta, "400": MensagemResposta, "422": MensagemResposta})
def upload_route():
    """Faz o upload de um documento PDF.

    Retorna uma mensagem de sucesso ou erro.
    """
    documento = request.files.get('documento')
    local_ou_samba = request.form.get('local_ou_samba')
    nome_cliente = request.form.get('nome_cliente')

    if not documento:
        return {"mensagem": "Nenhum arquivo foi enviado"}, 400
    if not local_ou_samba:
        return {"mensagem": "Parâmetro 'local_ou_samba' não fornecido"}, 400
    if not nome_cliente:
        return {"mensagem": "Parâmetro 'nome_cliente' não fornecido"}, 400

    try:
        return documentos_controller.upload_documento(documento, local_ou_samba, nome_cliente)
    except Exception as e:
        return {"mensagem": f"Erro ao fazer upload: {str(e)}"}, 500

@app.put('/documento/armazenamento', tags=[documento_tag],
         responses={"200": MensagemResposta, "400": MensagemResposta, "404": MensagemResposta, "422": MensagemResposta})
def atualizar_documento_no_armazenamento_route(body: DocumentoAtualizadoComArquivoSchema):
    """Atualiza um Documento no armazenamento.

    Retorna uma mensagem de sucesso ou erro.
    """
    documento = request.files.get('documento')
    local_ou_samba = request.form.get('local_ou_samba')
    nome_cliente = request.form.get('nome_cliente')
    filename_antigo = request.form.get('filename_antigo')

    if not documento or not local_ou_samba or not nome_cliente or not filename_antigo:
        return {"mensagem": "Parâmetros obrigatórios não fornecidos"}, 400

    try:
        return documentos_controller.atualizar_documento_no_armazenamento(documento, local_ou_samba, nome_cliente, filename_antigo)
    except Exception as e:
        return {"mensagem": f"Erro ao atualizar documento: {str(e)}"}, 500

@app.delete('/documento/armazenamento', tags=[documento_tag],
            responses={"200": MensagemResposta, "400": MensagemResposta, "404": MensagemResposta})
def excluir_documento_do_armazenamento_route(query: DocumentoExclusaoArmazenamentoSchema):
    """Exclui um Documento do armazenamento.

    Retorna uma mensagem de sucesso ou erro.
    """
    local_ou_samba = query.local_ou_samba
    nome_cliente = query.nome_cliente
    filename = query.filename

    if not local_ou_samba or not nome_cliente or not filename:
        return {"mensagem": "Parâmetros obrigatórios não fornecidos"}, 400

    try:
        return documentos_controller.excluir_documento_do_armazenamento(local_ou_samba, nome_cliente, filename)
    except Exception as e:
        return {"mensagem": f"Erro ao excluir documento: {str(e)}"}, 500

@app.post('/user/create', tags=[usuario_tag],
          responses={"201": UserViewSchema, "400": MensagemResposta, "422": MensagemResposta})
def create_user(body: UserSchema):
    """Cria um usuário.

    Retorna uma representação do usuário salvo no banco de dados.
    """
    return users_controller.create_user(body.username, body.password, body.name, body.image)

@app.route('/uploads/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)

@app.post('/upload/image', tags=[image_tag])
def upload_image():
    if 'image' not in request.files:
        return {"mensagem": "Nenhum arquivo foi enviado"}, 400

    image = request.files['image']
    filename = images.save(image)
    server_url = request.url_root
    relative_path = url_for('uploaded_file', filename=filename)
    full_url = server_url.rstrip('/') + relative_path
    return {"url": full_url}, 200


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
