from fastapi import FastAPI, HTTPException
from models import Transacao, TransacaoUpdate
from datetime import datetime
from typing import List

app = FastAPI(title="ExpenseTracker API", version="1.0.0")

# Base de dados temporária (em memória)
transacao_db = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Bem vindo a ExpenseTracker!"}

@app.get("/transacoes", response_model=List[Transacao])
def listar_transacoes():
    return transacao_db

@app.post("/transacoes", response_model=Transacao)
def criar_transacao(transacao: Transacao):
    global next_id
    
    # Validar categoria
    if transacao.tipo not in RECEITAS_VALIDAS:
        raise HTTPException(
            status_code=422, 
            detail=f"Categoria inválida. Use uma destas: {', '.join(RECEITAS_VALIDAS)}"
        )
    elif transacao.tipo not in DESPESAS_VALIDAS:
        raise HTTPException(
            status_code=422, 
            detail=f"Categoria inválida. Use uma destas: {', '.join(DESPESAS_VALIDAS)}"
        )
    
    nova_transacao = Transacao(
        id=next_id,
        descricao=transacao.descricao,
        valor=transacao.valor,
        categoria=transacao.categoria,
        tipo=transacao.tipo,
        data_criacao=datetime.now()
    )
    transacao_db.append(nova_transacao)
    next_id += 1
    return nova_transacao

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException, Query
from models import Transacao, RECEITAS_VALIDAS, DESPESAS_VALIDAS
from datetime import datetime
from typing import List, Optional

# ... código existente da aula anterior ...

# Atualizar Transação
@app.put("/transacoes/{id}", response_model=Transacao)
def atualizar_transacao(id: int, transacao_atualizado: TransacaoUpdate):
    """Atualizar transação completo"""
    # Buscar transações existentes
    transacao_index = None
    for i, transacao in enumerate(transacao_db):
        if transacao.id == id:
            transacao_index = i
            break
    
    if transacao_index is None:
        raise HTTPException(status_code=404, detail="Transação não encontrado")
    
    # Validar categoria
    if transacao_atualizado.tipo not in DESPESAS_VALIDAS:
        raise HTTPException(
            status_code=422, 
            detail=f"Categoria inválida. Use uma destas: {', '.join(DESPESAS_VALIDAS)}"
        )
    elif transacao_atualizado.tipo not in RECEITAS_VALIDAS:
        raise HTTPException(
            status_code=422, 
            detail=f"Categoria inválida. Use uma destas: {', '.join(RECEITAS_VALIDAS)}"
        )
    # Atualizar transacao mantendo ID e data de criação
    transacao_original = transacao_db[transacao_index]
    transacao_novo = Transacao(
        id=transacao_original.id,
        descricao=transacao_atualizado.descricao,
        valor=transacao_atualizado.preco,
        categoria=transacao_atualizado.categoria,
        tipo=transacao_original.tipo,
        data_criacao=transacao_original.data_criacao
    )
    
    transacao_db[transacao_index] = transacao_novo
    return transacao_novo

# Deletar Transação
@app.delete("/transacao/{id}")
def deletar_transacao(id: int):
    """Remover transacaos"""
    global transacao_db
    
    # Buscar produto
    produto_existe = False
    for i, transacao in enumerate(transacao_db):
        if transacao.id == id:
            transacao_db.pop(i)
            transacao_existe = True
            break
    
    if not transacao_existe:
        raise HTTPException(status_code=404, detail="Transação não encontrado")
    
    return {"message": "Transação removido com sucesso"}

# Buscar Produtos com filtros
@app.get("/transacao/buscar", response_model=List[Transacao])
def buscar_transacao(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    termo: Optional[str] = Query(None, min_length=2, description="Buscar na descrição"),
    valor_min: Optional[float] = Query(None, ge=0, description="Valor mínimo"),
    valor_max: Optional[float] = Query(None, ge=0, description="Valor máximo"),
    tipo: Optional[str] = Query(None, description="Tipo de transação (receita ou despesa)")
):
    """Buscar transacao com filtros"""
    resultados = transacao_db.copy()
    
    # Filtrar por categoria
    if categoria:
        if categoria not in RECEITAS_VALIDAS:
            raise HTTPException(
                status_code=422, 
                detail=f"Categoria inválida. Use uma destas: {', '.join(RECEITAS_VALIDAS)}"
            )
        elif categoria not in DESPESAS_VALIDAS:
            raise HTTPException(
                status_code=422, 
                detail=f"Categoria inválida. Use uma destas: {', '.join(DESPESAS_VALIDAS)}"
            )
        resultados = [p for p in resultados if p.categoria == categoria]
    
    # Filtrar por termo de busca
    if termo:
        termo_lower = termo.lower()
        resultados = [
            p for p in resultados 
            if termo_lower in p.descricao.lower()
        ]
    
    # Filtrar por preço mínimo
    if valor_min is not None:
        resultados = [p for p in resultados if p.valor >= valor_min]
    
    # Filtrar por preço máximo
    if valor_max is not None:
        resultados = [p for p in resultados if p.valor <= valor_max]
    
    # Filtrar por tipo
    if termo:
        tipo_lower = tipo.lower()
        resultados = [
            p for p in resultados 
            if tipo_lower in p.tipo.lower()
        ]
    
    return resultados

# Pega o Saldo
@app.get("/saldo")
def listar_saldo():
    """Listar saldo"""
    saldo = sum(p.valor for p in transacao_db if p.tipo == "receita")
    return saldo

# Get Transações por ID
@app.get("/transacoes/{id}", response_model=Transacao)
def buscar_transacao(id: int):
    transacao = next((p for p in transacao_db if p.id == id), None)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrado")
    return transacao