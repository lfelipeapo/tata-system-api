from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    """Define a forma como deve ser criado um usuário"""
    username: str
    password: str
    name: str
    image: Optional[str]

class UserAuthenticateSchema(BaseModel):
    """Define como deve ser autenticado um usuário"""
    username: str
    password: str

class UserViewSchema(BaseModel):
    """Define a representação de um usuário"""
    id: int
    username: str
    password: str
    name: str
    image: Optional[str]

class UserAtualizadoSchema(BaseModel):
    """Define como deve ser atualizado e representado a atualização de um cliente"""
    id: int
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]
    image: Optional[str]

class UserBuscaSchema(BaseModel):
    """Define uma busca de um usuário por id"""
    id: int

class UsersListagemSchema(BaseModel):
    """Define a representação de uma lista de usuários"""
    users: List[UserSchema]