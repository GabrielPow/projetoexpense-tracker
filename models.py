from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transacao(BaseModel):
    id: Optional[int] = None
    descricao: str = Field(..., min_length=3, max_length=100)
    valor: float = Field(..., gt=0)
    categoria: str = Field(...)
    tipo: str = Field(...)  # "receita" ou "despesa"
    data_criacao: Optional[datetime] = None

class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = Field(None, min_length=3, max_length=500)
    valor: Optional[float] = None
    categoria: Optional[str] = None

RECEITAS_VALIDAS = ["Salário", "Freelance", "Vendas", "Outros"]

DESPESAS_VALIDAS = ["Alimentação", "Transporte", "Lazer", "Contas", "Outros"]