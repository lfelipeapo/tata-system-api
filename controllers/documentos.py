from models.documentos import Documento
from models import Session
from typing import Union, List

class DocumentoController:
    def criar_documento(self, documento: Documento):
        session = Session()
        
        if not documento.documento_nome or not documento.cliente_id or not documento.consulta_id or documento.documento_localizacao and documento.documento_url:
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400
        try:
            
            session.add(documento)
            session.commit()
            
            return self.apresenta_documento(documento), 200
        
        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro " + str(e)}, 400

        finally:
            session.close()

    def atualizar_documento(self, id: int, documento_nome: str, cliente_id: int, consulta_id: int, documento_localizacao: Union[str, None] = None, documento_url: Union[str, None] = None):
        session = Session()
        
        if not id or not documento_nome or not cliente_id or not consulta_id or documento_localizacao and documento_url:
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400

        try:
            documento = session.query(Documento).get(id)
            if not documento:
                return {'mensagem': "Documento não encontrado"}, 404
            documento.documento_nome = documento_nome
            documento.cliente_id = cliente_id
            documento.consulta_id = consulta_id
            if documento_localizacao:
                documento.documento_localizacao = documento_localizacao
            if documento_url:
                documento.documento_url = documento_url

            session.add(documento)
            session.commit()
            
            return self.apresenta_documento(documento), 200
        
        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro " + str(e)}, 400

        finally:
            session.close()

    def excluir_documento(self, id: int):
        try:
            session = Session()
            if not id:
                return {'mensagem': 'Parâmetro Id é obrigatório'}, 400
            documento = session.query(Documento).get(id)
            if not documento:
                return {'mensagem': 'Documento não encontrado'}, 404
            session.delete(documento)
            session.commit()
            return {'mensagem': 'Documento' + documento.id + "excluído com sucesso!"}, 200
        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro: " + str(e)}, 400
        finally:
            session.close()

    def obter_documento_por_id(self, id: int):
        session = Session()
        try:
            if not id:
                return {'mensagem': 'Parâmetro Id é obrigatório'}, 400
            documento = session.query(Documento).get(id)
            if not documento:
                return {'mensagem': 'Documento não encontrado'}, 404
            
            return self.apresenta_documento(documento), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter o documento: ' + str(e)}, 500
        finally:
            session.close()

    def obter_todos_documentos(self):
        session = Session()
        try:
            documentos = session.query(Documento).all()
            if not documentos:
                return {'mensagem': 'Nenhum documento encontrado'}, 404

            return self.apresenta_documentos(documentos), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Ocorreu um erro ao obter os documentos: ' + str(e)}, 400
        finally:
            session.close()
    
    @staticmethod
    def apresenta_documento(documento: Documento):
        return {
                "id": documento.id,
                "documento_nome": documento.documento_nome,
                "cliente_id": documento.cliente_id,
                "consulta_id": documento.consulta_id,
                "documento_localizacao": documento.documento_localizacao if documento.documento_localizacao else None,
                "documento_url": documento.documento_url if documento.documento_url else None
            }
    
    @staticmethod
    def apresenta_documentos(documentos: List[Documento]):
        result = []
        for documento in documentos:
            result.append({
                "id": documento.id,
                "documento_nome": documento.documento_nome,
                "cliente_id": documento.cliente_id,
                "consulta_id": documento.consulta_id,
                "documento_localizacao": documento.documento_localizacao if documento.documento_localizacao else None,
                "documento_url": documento.documento_url if documento.documento_url else None
            })
        return {"documentos": result}