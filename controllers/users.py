from models import Session
from models.users import User
from typing import Union, List

class UserController:

    def create_user(self, username:str, password:str, name:str, image:Union[str,None]=None):
        session = Session()
        try:
            if not username or not password or not name:
                return {'mensagem': 'Dados de usuários faltantes'}, 400
            user = User(username=username, name=name, image=image)
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user and existing_user.id != user.id:
                return {'mensagem': 'Nome de usuário já está em uso'}, 409
            user.set_password(password)
            session.add(user)
            session.commit()
            return self.apresenta_usuario(user), 201
        
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro' + str(e)}, 422
        
        finally:
            session.close()

    def authenticate_user(self, username, password):
        session = Session()
        try:
            if not username or not password:
                return {'mensagem': "Usuário ou senha são obrigatórios"}, 400
            user = session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                return self.apresenta_usuario(user)
            return False
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro' + str(e)}, 422
        finally:
            session.close()
    
    def atualizar_user(self, id:int, username:Union[str,None]=None, password:Union[str,None]=None, name:Union[str,None]=None, image:Union[str,None]=None):
        session = Session()
        if not id:
            return {'mensagem': 'É obrigatório informar o id do usuário'}, 400
        try:

            user = session.query(User).get(id)
            if not user:
                return {'mensagem': 'Usuário não encontrado'}, 404

            if username:
                user.username = username
            if password:
                user.set_password(password)
            if name:
                user.name = name

            user.image = image

            session.add(user)
            session.commit()

            return self.apresenta_usuario(user), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422
        finally:
            session.close()

    def excluir_user(self, id: int):
        if not id:
            return {'mensagem': "É obrigatório informar o Id do usuário"}
        session = Session()
        try:
            user = session.query(User).get(id)
            if not user:
                return {'mensagem': 'Usuário não encontrado'}, 404

            session.delete(user)
            session.commit()

            return {'mensagem': 'Usuário ' + str(user.id) + ' excluído com sucesso'}, 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422
        finally:
            session.close()

    def obter_user_por_id(self, id: int):
        if not id:
            return {'mensagem': 'É obrigatório informar o Id do usuário'}, 400
        session = Session()
        try:
            user = session.query(User).get(id)
            if not user:
                return {'mensagem': 'Usuário não encontrado'}, 404

            return self.apresenta_usuario(user), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': str(e)}, 422
        finally:
            session.close()

    def obter_users(self):
        session = Session()
        try:
            users = session.query(User).all()

            if not users:
                return {'mensagem': 'Nenhum usuário encontrado'}, 404

            return self.apresenta_usuarios(users), 200
        except Exception as e:
            session.rollback()
            return {'mensagem': 'Erro:' + str(e)}, 422
        finally:
            session.close()

    @staticmethod
    def apresenta_usuario(usuario: User):
        return {
            'id': usuario.id,
            'username': usuario.username,
            'password': usuario.password_hash,
            'name': usuario.name,
            'image': usuario.image if usuario.image else None
        }

    @staticmethod
    def apresenta_usuarios(usuarios: List[User]):
        result = []
        for usuario in usuarios:
            result.append({
                'id': usuario.id,
                'username': usuario.username,
                'password': usuario.password_hash,
                'name': usuario.name,
                'image': usuario.image if usuario.image else None
            })
        return {"users": result}
