from sqlalchemy import Column, Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    name = Column(String(64))
    image = Column(Text, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
