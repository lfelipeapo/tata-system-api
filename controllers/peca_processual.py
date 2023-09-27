from typing import Union, List, Tuple
from models.peca_processual import PecaProcessual
from models import Session
from models.upload import pecas
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from smb.SMBConnection import SMBConnection
import os
from dotenv import load_dotenv


class PecaProcessualController:
    
    
    def allowed_file(self, filename: str) -> bool:
        ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_unique_filename(self, path: str, filename: str) -> str:
        counter = 1
        name, extension = os.path.splitext(filename)
        while os.path.exists(os.path.join(path, filename)):
            filename = f"{name}_{counter}{extension}"
            counter += 1
        return filename

    def get_unique_filename_samba(self, conn, share_name, path, filename) -> str:
        counter = 1
        name, extension = os.path.splitext(filename)
        files_on_samba = conn.listPath(share_name, path)
        while any(file.filename == filename for file in files_on_samba):
            filename = f"{name}_{counter}{extension}"
            counter += 1
        return filename

    def criar_peca(self, categoria: str, nome_peca: str, documento_localizacao: Union[str, None] = None, documento_url: Union[str, None] = None):
        session = Session()

        if not categoria or not nome_peca or (not documento_localizacao and not documento_url):
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400

        try:
            peca = PecaProcessual(documento_url=documento_url, documento_localizacao=documento_localizacao, categoria=categoria, nome_peca=nome_peca)
            session.add(peca)
            session.commit()

            return self.apresenta_peca(peca), 200

        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro " + str(e)}, 400

        finally:
            session.close()

    def atualizar_peca(self, id: int, categoria: str, nome_peca: str, documento_localizacao: Union[str, None] = None, documento_url: Union[str, None] = None):
        session = Session()

        if not id or not categoria or not nome_peca or (not documento_localizacao and not documento_url):
            return {'mensagem': 'Parâmetros obrigatórios não informados'}, 400

        try:
            peca = session.query(PecaProcessual).get(id)
            if not peca:
                return {'mensagem': "Peça processual não encontrada"}, 404

            peca.documento_url = documento_url
            peca.documento_localizacao = documento_localizacao
            peca.categoria = categoria
            peca.nome_peca = nome_peca

            session.add(peca)
            session.commit()

            return self.apresenta_peca(peca), 200

        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro " + str(e)}, 400

        finally:
            session.close()

    def deletar_peca(self, id: int):
        session = Session()

        try:
            peca = session.query(PecaProcessual).get(id)
            if not peca:
                return {'mensagem': 'Peça processual não encontrada'}, 404

            session.delete(peca)
            session.commit()

            return {'mensagem': 'Peça processual excluída com sucesso!'}, 200

        except Exception as e:
            session.rollback()
            return {'mensagem': "Erro: " + str(e)}, 400

        finally:
            session.close()

    def obter_peca(self, id: int):
        session = Session()

        try:
            peca = session.query(PecaProcessual).get(id)
            if not peca:
                return {'mensagem': 'Peça processual não encontrada'}, 404

            return self.apresenta_peca(peca), 200

        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro ao obter a peça processual: ' + str(e)}, 500

        finally:
            session.close()

    def obter_pecas(self):
        session = Session()

        try:
            pecas = session.query(PecaProcessual).all()
            if not pecas:
                return {'mensagem': 'Nenhuma peça processual encontrada'}, 404

            return self.apresenta_pecas(pecas), 200

        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro ao obter as peças processuais: ' + str(e)}, 400

        finally:
            session.close()
            
    def upload_peca(self, peca: FileStorage, local_ou_samba: str, categoria: str) -> Tuple[dict, int]:
        if not peca:
            return {"mensagem": "Nenhuma peça foi enviada"}, 400

        if peca.filename == '':
            return {"mensagem": "Nenhuma peça foi selecionada"}, 400

        if not self.allowed_file(peca.filename):
            return {"mensagem": "Tipo de arquivo não permitido"}, 400

        filename = secure_filename(peca.filename)

        try:
            if local_ou_samba == 'local':
                categoria_path = os.path.join(pecas.config.destination, categoria)
                if not os.path.exists(categoria_path):
                    os.makedirs(categoria_path)
                filename = self.get_unique_filename(categoria_path, filename)
                file_path = os.path.join(categoria_path, filename)
                peca.save(file_path)
                if not os.path.exists(file_path):
                    return {"mensagem": "Erro ao salvar a peça localmente"}, 500
                return {
                    "mensagem": "Peça enviada com sucesso",
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

                categoria_path = os.path.join(pecas.config.destination, categoria)
                if not os.path.exists(categoria_path):
                    os.makedirs(categoria_path)
                file_path = os.path.join(categoria_path, filename)
                peca.save(file_path)

                remote_categoria_path = os.path.join(remote_path, categoria)
                
                try:
                    conn.listPath(share_name, remote_categoria_path)
                except:
                    conn.createDirectory(share_name, remote_categoria_path)

                filename = self.get_unique_filename_samba(conn, share_name, remote_categoria_path, filename)
                remote_file_path = os.path.join(remote_categoria_path, filename)

                with open(file_path, 'rb') as file_obj:
                    conn.storeFile(share_name, remote_file_path, file_obj)

                files_on_samba = conn.listPath(share_name, remote_categoria_path)
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

    def atualizar_peca_no_armazenamento(self, peca: FileStorage, local_ou_samba: str, local_ou_samba_antigo: str, categoria: str, filename_antigo: str) -> Tuple[dict, int]:
        delete_result, delete_status = self.excluir_peca_do_armazenamento(local_ou_samba_antigo, categoria, filename_antigo)
        
        if delete_status != 200:
            return delete_result, delete_status
        
        return self.upload_peca(peca, local_ou_samba, categoria)

    def excluir_peca_do_armazenamento(self, local_ou_samba: str, categoria: str, filename: str) -> Tuple[dict, int]:
        try:
            if local_ou_samba == 'local':
                categoria_path = os.path.join(pecas.config.destination, categoria)
                file_path = os.path.join(categoria_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return {"mensagem": "Peça excluída com sucesso do armazenamento local"}, 200
                else:
                    return {"mensagem": "Peça não encontrada no armazenamento local"}, 404

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

                remote_categoria_path = os.path.join(remote_path, categoria)
                remote_file_path = os.path.join(remote_categoria_path, filename)

                files = conn.listPath(share_name, remote_categoria_path)
                file_exists = any(file.filename == filename for file in files)

                if file_exists:
                    conn.deleteFiles(share_name, remote_file_path)
                    return {"mensagem": "Peça excluída com sucesso do samba"}, 200
                else:
                    return {"mensagem": "Peça não encontrada no samba"}, 404

            else:
                return {"mensagem": "Opção inválida para 'local_ou_samba'"}, 400

        except Exception as e:
            return {"mensagem": f"Ocorreu um erro: {e}"}, 500

    @staticmethod
    def apresenta_peca(peca: PecaProcessual):
        return {
            "id": peca.id,
            "documento_url": peca.documento_url,
            "documento_localizacao": peca.documento_localizacao,
            "categoria": peca.categoria,
            "nome_peca": peca.nome_peca
        }

    @staticmethod
    def apresenta_pecas(pecas: List[PecaProcessual]):
        result = []
        for peca in pecas:
            result.append({
                "id": peca.id,
                "documento_url": peca.documento_url,
                "documento_localizacao": peca.documento_localizacao,
                "categoria": peca.categoria,
                "nome_peca": peca.nome_peca
            })
        return {"pecas_processuais": result}
