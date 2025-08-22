from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Produto(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    preco: float
    categoria: str
    vendedor: str
    data_criacao: Optional[datetime] = None

class ProdutoCreate(BaseModel):
    titulo: str
    descricao: str
    preco: float
    categoria: str
    vendedor: str