from schemas.clientes import ClienteSchema, ClienteAtualizadoSchema, ClienteBuscaSchema, ClientesFiltradosSchema, ClienteListagemSchema, ClienteViewSchema
from schemas.consultas_juridicas import ConsultaJuridicaSchema, ConsultaJuridicaAtualizadaSchema, ConsultaJuridicaListagemSchema, ConsultaJuridicaViewSchema, ConsultaJuridicaBuscaSchema, ConsultasFiltradasBuscaSchema, ConsultaJuridicaBuscaPorDataEHoraSchema
from schemas.mensagem import MensagemResposta
from schemas.users import UserSchema, UserAuthenticateSchema, UserAtualizadoSchema, UserBuscaSchema, UserViewSchema, UsersListagemSchema
from schemas.documentos import DocumentoSchema, DocumentoBuscaSchema, DocumentoViewSchema, DocumentoListagemSchema, DocumentoAtualizadoSchema, DocumentoAtualizadoComArquivoSchema, DocumentoExclusaoArmazenamentoSchema
from schemas.peca_processual import (
    PecaProcessualSchema,
    PecaProcessualViewSchema,
    PecaProcessualListagemSchema,
    PecaProcessualBuscaSchema,
    PecaProcessualAtualizadoSchema,
    PecaProcessualExclusaoArmazenamentoSchema
)