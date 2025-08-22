from fastapi import FastAPI, HTTPException
from models import Produto, ProdutoCreate
from datetime import datetime
from typing import List

app = FastAPI(title="ExpenseTracker API", version="1.0.0")

# Base de dados temporária (em memória)
produtos_db = []
next_id = 1

@app.get("/")
def root():
    return {"message": "ExpenseTracker API - Marketplace Universitário"}

@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    return produtos_db

@app.post("/produtos", response_model=Produto)
def criar_produto(produto: ProdutoCreate):
    global next_id
    novo_produto = Produto(
        id=next_id,
        titulo=produto.titulo,
        descricao=produto.descricao,
        preco=produto.preco,
        categoria=produto.categoria,
        vendedor=produto.vendedor,
        data_criacao=datetime.now()
    )
    produtos_db.append(novo_produto)
    next_id += 1
    return novo_produto

@app.get("/produtos/{produto_id}", response_model=Produto)
def buscar_produto(produto_id: int):
    produto = next((p for p in produtos_db if p.id == produto_id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)