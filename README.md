## ExpenseTracker API

API simples para gestão de transações (receitas e despesas) — feita com FastAPI.

Permite criar, listar, atualizar, deletar e buscar transações com filtros, além de calcular o saldo.

## 📌 Descrição do projeto

- Este projeto implementa uma API REST para controle financeiro pessoal:

- Tecnologias: FastAPI, Pydantic, Uvicorn (execução), Python 3.10+

- Armazenamento: In-memory (lista Python) — ideal para estudo e MVP

### Modelos principais:

>**Transacao:** id, descrição, valor, categoria, tipo (receita|despesa), data_criacao

>**TransacaoUpdate:** atualizações parciais (descrição, valor, categoria)

### Validações de domínio:

`tipo deve ser receita ou despesa`

categoria deve estar em listas válidas conforme o tipo

**Receitas:** ["Salário", "Freelance", "Vendas", "Outros"]

**Despesas:** ["Alimentação", "Transporte", "Lazer", "Contas", "Outros"]

### 🔗 Link do GitHub

    https://github.com/GabrielPow/projetoexpense-tracker

🌐 URL da API no Azure

    expensetracker-cchde4hcfbdud3gn.brazilsouth-01.azurewebsites.net

### 📚 Lista de Endpoints

#### Visão geral
> Método	Rota	Descrição
- **GET**	/	Mensagem de boas-vindas
- **GET**	/transacoes	Lista todas as transações
- **POST**	/transacoes	Cria uma nova transação
- **GET**	/transacoes/{id}	Busca transação por ID
- **PUT**	/transacoes/{id}	Atualiza totalmente uma transação (mantém tipo)
- **DELETE**	/transacao/{id}	Deleta transação por ID 
- **GET**	/transacao/buscar	Busca com filtros
- **GET**	/saldo	Retorna o saldo atual


### 🔎 Detalhe dos Endpoints
> GET /
200 OK
{ "message": "Bem vindo a ExpenseTracker!" }

>GET /transacoe
Lista todas as transações.
200 OK → List[Transacao]

>POST /transacoes
Cria uma transação.
Body (application/json)
{
  "descricao": "Transacao",
  "valor": 5000,
  "categoria": "Lazer",
  "tipo": "despesa"
}
Respostas
201/200 OK → Transacao criada (com id e data_criacao)
422 Unprocessable Entity → validação (tipo inválido, categoria incompatível, valor <= 0, etc.)

>GET /transacoes/{id}
200 OK → Transacao
404 Not Found → quando não existe

>PUT /transacoes/{id}
Atualiza descrição / valor / categoria, mantendo tipo e data_criacao originais.
Body (exemplo)
{
  "descricao": "alteracao de valor",
  "valor": 2020
}
Respostas
200 OK → Transacao atualizada
404 Not Found
422 Unprocessable Entity → categoria incompatível com o tipo original

>DELETE /transacao/{id}
200 OK → {"message": "Transação removido com sucesso"}
404 Not Found → quando não existe

>GET /transacao/buscar
Busca com filtros via query params.
Parâmetros (todos opcionais)
categoria: str — valida de acordo com tipo (se informado) ou contra todas
termo: str — busca substring na descrição (mín. 2 chars)
valor_min: float (>= 0)
valor_max: float (>= 0)
tipo: "receita" | "despesa"
Exemplo
GET /transacao/buscar?tipo=despesa&categoria=Lazer
Respostas
200 OK → lista filtrada
422 Unprocessable Entity → faixa de valores inválida (valor_min > valor_max) ou categoria inválida

>GET /saldo
Retorna a soma dos valores de todas as receitas.
200 OK → número (float)

### ▶️ Como executar localmente
Requisitos

    Python 3.10+

    pip

### Passo a passo
#### 1) Criar e ativar venv (opcional, recomendado)
    python -m venv .venv
##### Windows:
    venv\Scripts\activate
##### macOS/Linux:
    source .venv/bin/activate

#### 2) Instalar dependências   
    pip install fastapi uvicorn pydantic

#### 3) Executar servidor
    uvicorn main:app --reload

>A API sobe em: http://127.0.0.1:8000

>Docs interativas (Swagger): http://127.0.0.1:8000/docs


### 🧪 Instruções de como testar

    1. Instale a extensão REST Client (humao.rest-client).

    2. Abra o arquivo test.http.
    
    3. Clique em Send Request em cada bloco.

>Certifique-se que a URL @url = http://localhost:8000 está correta.


### Autoria

    Gabriel Pow:   Implementação e Testes
    Pedro Lacerda:  Documentação e Testes
    Pedro Pintor:   Documentação e Implementação
