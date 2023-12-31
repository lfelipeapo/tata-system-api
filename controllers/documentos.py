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

    def criar_documento(self, documento_nome: str, cliente_id: int, consulta_id: Union[int, None] = None, documento_localizacao: Union[str, None] = None, documento_url: Union[str, None] = None):
        session = Session()
        
        
        if not documento_nome or not cliente_id or (not documento_localizacao and not documento_url):
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400
        try:
            documento = Documento(documento_nome=documento_nome, cliente_id=cliente_id, consulta_id=consulta_id, documento_localizacao=documento_localizacao, documento_url=documento_url)
            session.add(documento)
            session.commit()
            
            return self.apresenta_documento(documento), 200
        
        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro " + str(e)}, 400

        finally:
            session.close()

    def atualizar_documento(self, id: int, documento_nome: str, cliente_id: int, consulta_id: Union[int, None] = None, documento_localizacao: Union[str, None] = None, documento_url: Union[str, None] = None):
        session = Session()
        
        if not id or not documento_nome or not cliente_id or (not documento_localizacao and not documento_url):
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400

        try:
            documento = session.query(Documento).get(id)
            if not documento:
                return {'mensagem': "Documento não encontrado"}, 404
            
            documento.documento_nome = documento_nome
            documento.cliente_id = cliente_id
            documento.consulta_id = consulta_id
            documento.documento_localizacao = documento_localizacao
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
            documento_id = documento.id
            session.delete(documento)
            session.commit()
            return {'mensagem': 'Documento ' + str(documento_id) + " excluído com sucesso!"}, 200
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
            
    def atualizar_documento_no_armazenamento(self, documento: FileStorage, local_ou_samba: str, local_ou_samba_antigo: str, nome_cliente: str, filename_antigo: str) -> Tuple[dict, int]:
        delete_result, delete_status = self.excluir_documento_do_armazenamento(local_ou_samba_antigo, nome_cliente, filename_antigo)
        
        if delete_status != 200:
            return delete_result, delete_status
        
        return self.upload_documento(documento, local_ou_samba, nome_cliente)

    def excluir_documento_do_armazenamento(self, local_ou_samba: str, nome_cliente: str, filename: str) -> Tuple[dict, int]:
        try:
            if local_ou_samba == 'local':
                cliente_path = os.path.join(documents.config.destination, nome_cliente)
                file_path = os.path.join(cliente_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return {"mensagem": "Documento excluído com sucesso do armazenamento local"}, 200
                else:
                    return {"mensagem": "Documento não encontrado no armazenamento local"}, 404

            elif local_ou_samba == 'samba':
                load_dotenv()
                server_name = os.getenv('SERVER_NAME')
                username = os.getenv('USERNAME')
                password = os.getenv('PASSWORD')
                share_name = os.getenv('SHARENAME')
                machine_name = os.getenv('MACHINE_NAME')
                server_ip = os.getenv('SERVER_IP')
                remote_path = os.getenv('REMOTE_PATH')

                conn = SMBConnection(username, password, machine_name, server_name, domain='WORKGROUP', use_ntlm_v2=True)

                if not conn.connect(server_ip, 445):
                    return {"mensagem": "Erro ao conectar ao servidor Samba"}, 500

                remote_cliente_path = os.path.join(remote_path, nome_cliente)
                remote_file_path = os.path.join(remote_cliente_path, filename)

                files = conn.listPath(share_name, remote_cliente_path)
                file_exists = any(file.filename == filename for file in files)

                if file_exists:
                    conn.deleteFiles(share_name, remote_file_path)
                    return {"mensagem": "Documento excluído com sucesso do samba"}, 200
                else:
                    return {"mensagem": "Documento não encontrado no samba"}, 404

            else:
                return {"mensagem": "Opção inválida para 'local_ou_samba'"}, 400

        except Exception as e:
            return {"mensagem": f"Ocorreu um erro: {e}"}, 500

    def upload_documento(self, documento: FileStorage, local_ou_samba: str, nome_cliente: str) -> Tuple[dict, int]:
        if not documento:
            return {"mensagem": "Nenhum arquivo foi enviado"}, 400

        if documento.filename == '':
            return {"mensagem": "Nenhum arquivo foi selecionado"}, 400

        if not self.allowed_file(documento.filename):
            return {"mensagem": "Tipo de arquivo não permitido"}, 400

        filename = secure_filename(documento.filename)

        try:
            if local_ou_samba == 'local':
                cliente_path = os.path.join(documents.config.destination, nome_cliente)
                if not os.path.exists(cliente_path):
                    os.makedirs(cliente_path)
                filename = self.get_unique_filename(cliente_path, filename)
                file_path = os.path.join(cliente_path, filename)
                documento.save(file_path)
                if not os.path.exists(file_path):
                    return {"mensagem": "Erro ao salvar o arquivo localmente"}, 500
                return {
                    "mensagem": "Documento enviado com sucesso",
                    "detalhes": {
                        "nome_arquivo": os.path.basename(file_path),
                        "documento_localizacao": file_path
                    }
                }, 200

            elif local_ou_samba == 'samba':
                load_dotenv()
                server_name = os.getenv('SERVER_NAME')
                username = os.getenv('USERNAME')
                password = os.getenv('PASSWORD')
                share_name = os.getenv('SHARENAME')
                machine_name = os.getenv('MACHINE_NAME')
                server_ip = os.getenv('SERVER_IP')
                remote_path = os.getenv('REMOTE_PATH')

                conn = SMBConnection(username, password, machine_name, server_name, domain='WORKGROUP', use_ntlm_v2=True)

                if not conn.connect(server_ip, 445):
                    return {"mensagem": "Erro ao conectar ao servidor Samba"}, 500

                cliente_path = os.path.join(documents.config.destination, nome_cliente)
                if not os.path.exists(cliente_path):
                    os.makedirs(cliente_path)
                file_path = os.path.join(cliente_path, filename)
                documento.save(file_path)

                remote_cliente_path = os.path.join(remote_path, nome_cliente)
                
                # Verifique se a subpasta com o nome do cliente existe no servidor Samba
                try:
                    conn.listPath(share_name, remote_cliente_path)
                except:
                    # Se a subpasta não existir, crie-a
                    conn.createDirectory(share_name, remote_cliente_path)

                filename = self.get_unique_filename_samba(conn, share_name, remote_cliente_path, filename)
                remote_file_path = os.path.join(remote_cliente_path, filename)

                with open(file_path, 'rb') as file_obj:
                    conn.storeFile(share_name, remote_file_path, file_obj)

                files_on_samba = conn.listPath(share_name, remote_cliente_path)
                if not any(file.filename == filename for file in files_on_samba):
                    return {"mensagem": "Erro ao salvar o arquivo no samba"}, 500

                return {
                    "mensagem": "Documento enviado com sucesso",
                    "detalhes": {
                        "nome_arquivo": os.path.basename(remote_file_path),
                        "documento_url": f"smb://{server_name}/{share_name}/{remote_file_path}"
                    }
                }, 200

            else:
                return {"mensagem": "Opção inválida para 'local_ou_samba'"}, 400

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
    
    @staticmethod
    def file_exists_in_local(cliente_path: str, filename: str) -> bool:
        """Verifica se um arquivo existe no armazenamento local."""
        file_path = os.path.join(cliente_path, filename)
        return os.path.exists(file_path)

    def get_unique_filename(self, cliente_path: str, filename: str) -> str:
        """Retorna um nome de arquivo único para evitar sobrescrita."""
        base_name, ext = os.path.splitext(filename)
        counter = 1
        while self.file_exists_in_local(cliente_path, filename):
            filename = f"{base_name}_{counter}{ext}"
            counter += 1
        return filename

    @staticmethod
    def file_exists_in_samba(conn, share_name, remote_cliente_path, filename) -> bool:
        """Verifica se um arquivo existe no Samba."""
        files = conn.listPath(share_name, remote_cliente_path)
        return any(file.filename == filename for file in files)
    
    def get_unique_filename_samba(self, conn, share_name, remote_cliente_path, filename) -> str:
        """Retorna um nome de arquivo único para evitar sobrescrita no Samba."""
        base_name, ext = os.path.splitext(filename)
        counter = 1
        while self.file_exists_in_samba(conn, share_name, remote_cliente_path, filename):
            filename = f"{base_name}_{counter}{ext}"
            counter += 1
        return filename
