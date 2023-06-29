from pydantic import BaseModel

class MensagemResposta(BaseModel):
    """Representação de uma mensagem de retorno seja de erro ou sucesso"""
    mensagem: str