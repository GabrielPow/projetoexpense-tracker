from fastapi import FastAPI, HTTPException, Query
from models import (Transacao, TransacaoUpdate,
                    RECEITAS_VALIDAS, DESPESAS_VALIDAS)
from datetime import datetime
from typing import List, Optional

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
    
    # Validar tipo
    if transacao.tipo == 'receita' or transacao.tipo == 'despesa':
        # Validar categoria
        if transacao.tipo == 'receita' and transacao.categoria not in RECEITAS_VALIDAS:
            raise HTTPException(
                status_code=422, 
                detail=f"Categoria inválida. Use uma destas: {', '.join(RECEITAS_VALIDAS)}"
            )
        elif transacao.tipo == 'despesa' and transacao.categoria not in DESPESAS_VALIDAS:
            raise HTTPException(
                status_code=422, 
                detail=f"Categoria inválida. Use uma destas: {', '.join(DESPESAS_VALIDAS)}"
            )
    else:
        raise HTTPException(
            status_code=422,
            detail=f"Tipo inválido. Use um destes tipos: receita, despesa"
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
    transacao_original = transacao_db[transacao_index]
    
    # Validar categoria
    if transacao_atualizado.categoria:
        if transacao_original.tipo == "receita":
            if transacao_atualizado.categoria not in RECEITAS_VALIDAS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Categoria inválida para RECEITA. Use uma destas: {', '.join(RECEITAS_VALIDAS)}"
                )
        elif transacao_original.tipo == "despesa":
            if transacao_atualizado.categoria not in DESPESAS_VALIDAS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Categoria inválida para DESPESA. Use uma destas: {', '.join(DESPESAS_VALIDAS)}"
                )

    
    # Atualizar transacao mantendo ID e data de criação
    transacao_novo = Transacao(
        id=transacao_original.id,
        tipo=transacao_original.tipo,
        data_criacao=transacao_original.data_criacao,
        descricao=transacao_atualizado.descricao or transacao_original.descricao,
        valor=transacao_atualizado.valor or transacao_original.valor,
        categoria=transacao_atualizado.categoria or transacao_original.categoria,
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
from typing import List, Optional, Literal
from fastapi import Query, HTTPException

TIPOS_VALIDOS = ("receita", "despesa")
TODAS_CATEGORIAS = set(RECEITAS_VALIDAS) | set(DESPESAS_VALIDAS)

@app.get("/transacao/buscar", response_model=List[Transacao])
def buscar_transacao(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    termo: Optional[str] = Query(None, min_length=2, description="Buscar na descrição"),
    valor_min: Optional[float] = Query(None, ge=0, description="Valor mínimo"),
    valor_max: Optional[float] = Query(None, ge=0, description="Valor máximo"),
    tipo: Optional[Literal["receita", "despesa"]] = Query(None, description="Tipo de transação")
):
    """Buscar transação com filtros"""
    resultados = transacao_db.copy()

    # valida faixa de valores
    if (valor_min is not None) and (valor_max is not None) and (valor_min > valor_max):
        raise HTTPException(status_code=422, detail="valor_min não pode ser maior que valor_max.")

    # Validação + filtro de categoria
    if categoria:
        if tipo:
            # valida categoria de acordo com o tipo informado
            categorias_validas = RECEITAS_VALIDAS if tipo == "receita" else DESPESAS_VALIDAS
            if categoria not in categorias_validas:
                raise HTTPException(
                    status_code=422,
                    detail=f"Categoria inválida para tipo '{tipo}'. Use uma destas: {', '.join(categorias_validas)}"
                )
        else:
            # sem tipo: valida contra todas
            if categoria not in TODAS_CATEGORIAS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Categoria inválida. Use uma destas: {', '.join(TODAS_CATEGORIAS)}"
                )

        resultados = [p for p in resultados if p.categoria == categoria]

    # Filtro por termo na descrição
    if termo:
        termo_lower = termo.lower()
        resultados = [p for p in resultados if termo_lower in p.descricao.lower()]

    # Filtro por valores
    if valor_min is not None:
        resultados = [p for p in resultados if p.valor >= valor_min]

    if valor_max is not None:
        resultados = [p for p in resultados if p.valor <= valor_max]

    # Filtro por tipo
    if tipo:
        resultados = [p for p in resultados if p.tipo == tipo]

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)