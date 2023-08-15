from typing import Union, List, Tuple
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from smb.SMBConnection import SMBConnection
import socket
from models.upload import documents
from models.documentos import Documento
from models import Session
import os
from dotenv import load_dotenv

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

    def upload_documento(self, documento: FileStorage, local_ou_samba: str) -> Tuple[dict, int]:
        if not documento:
            return {"mensagem": "Nenhum arquivo foi enviado"}, 400

        if documento.filename == '':
            return {"mensagem": "Nenhum arquivo foi selecionado"}, 400

        if not self.allowed_file(documento.filename):
            return {"mensagem": "Tipo de arquivo não permitido"}, 400

        filename = secure_filename(documento.filename)

        try:
            if local_ou_samba == 'local':
                file_path = os.path.join(documents.config.destination, filename)
                documento.save(file_path)
                if not os.path.exists(file_path):
                    return {"mensagem": "Erro ao salvar o arquivo localmente"}, 500

            elif local_ou_samba == 'samba':
                load_dotenv()
                server_name = os.getenv('SERVER_NAME')
                username = os.getenv('USERNAME')
                password = os.getenv('PASSWORD')
                share_name = os.getenv('SHARENAME')
                # samba_path = os.path.join(share_name, filename)
                machine_name = os.getenv('MACHINE_NAME')
                server_ip = os.getenv('SERVER_IP')
                remote_path = os.getenv('REMOTE_PATH')

                conn = SMBConnection(username, password, machine_name, server_name, domain='WORKGROUP', use_ntlm_v2=True)

                if not conn.connect(server_ip, 445):
                    return {"mensagem": "Erro ao conectar ao servidor Samba"}, 500

                else:
                    file_path = os.path.join(documents.config.destination, filename)
                    documento.save(file_path)

                    remote_file_path = os.path.join(remote_path, filename)

                    with open(file_path, 'rb') as file_obj:
                        conn.storeFile(share_name, remote_file_path, file_obj)

                    files_on_samba = conn.listPath(share_name, remote_path)
                if not any(file.filename == filename for file in files_on_samba):
                    return {"mensagem": "Erro ao salvar o arquivo no samba"}, 500

            else:
                return {"mensagem": "Opção inválida para 'local_ou_samba'"}, 400

            return {"mensagem": "Documento enviado com sucesso"}, 200

        except Exception as e:
            return {"mensagem": f"Ocorreu um erro: {e}"}, 500
        
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
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}