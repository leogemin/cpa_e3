# CPA E3 - API de Licitações IFPI

_API construída utilizando Flask e Pandas para consulta de dados de licitações._

## Descrição

Este projeto consiste em uma API RESTful que expõe dados de licitações do IFPI, lidos a partir do arquivo `ifpi-administracao-licitacoes-set2025.csv`. A API permite consultar, adicionar, atualizar e deletar registros de licitações.

## Como executar

Para executar o projeto, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd cpa_e3
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    Com o ambiente virtual ativado, instale as dependências a partir do arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    O servidor Flask será iniciado em modo de desenvolvimento.
    ```bash
    python src/api.py
    ```

    A API estará disponível em `http://127.0.0.1:5000`.

## Endpoints da API

A seguir estão os endpoints disponíveis para interagir com os dados de licitações.

---


### 1. Listar as N primeiras licitações

Retorna um número `n` de licitações do início do conjunto de dados.

-   **URL:** `/licitacoes/<n>`
-   **Método:** `GET`
-   **Parâmetros da URL:**
    -   `n` (inteiro, obrigatório): O número de registros a serem retornados.
-   **Exemplo de uso (curl):**
    ```bash
    curl http://127.0.0.1:5000/licitacoes/5
    ```

---


### 2. Filtrar por modalidade

Busca licitações que contenham um termo específico na coluna `modalidade`.

-   **URL:** `/licitacoes/modalidade/<modalidade_nome>`
-   **Método:** `GET`
-   **Parâmetros da URL:**
    -   `modalidade_nome` (string, obrigatório): O termo a ser buscado na modalidade da licitação.
-   **Exemplo de uso (curl):**
    ```bash
    curl http://127.0.0.1:5000/licitacoes/modalidade/dispensa
    ```

---


### 3. Filtro avançado por campos

Permite filtrar os dados com base em múltiplos critérios enviados no corpo da requisição em formato JSON. A busca não diferencia maiúsculas de minúsculas.

-   **URL:** `/licitacoes/filter`
-   **Método:** `POST`
-   **Corpo da Requisição (JSON):**
    ```json
    {
      "nome_do_campo": "valor_a_buscar",
      "outro_campo": "outro_valor"
    }
    ```
-   **Exemplo de uso (curl):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
      -d '''{"modalidade": "PREGÃO ELETRÔNICO", "uasg_nome": "IFPI/CAMPUS PARNAIBA"}''' \
      http://127.0.0.1:5000/licitacoes/filter
    ```

---


### 4. Adicionar uma nova licitação

Insere um novo registro de licitação no conjunto de dados em memória.

-   **URL:** `/licitacoes`
-   **Método:** `POST`
-   **Corpo da Requisição (JSON):**
    Um objeto JSON com as colunas e valores da nova licitação.
-   **Exemplo de uso (curl):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
      -d '''{"licitacao": "999999", "modalidade": "CONVITE", "uasg_nome": "IFPI/REITORIA"}''' \
      http://127.0.0.1:5000/licitacoes
    ```
-   **Resposta de Sucesso:**
    ```json
    {
      "status": "success",
      "message": "Licitação adicionada."
    }
    ```

---


### 5. Atualizar uma licitação

Modifica um registro existente com base em seu índice na lista.

-   **URL:** `/licitacoes/<index>`
-   **Método:** `PUT`
-   **Parâmetros da URL:**
    -   `index` (inteiro, obrigatório): O índice do registro a ser atualizado.
-   **Corpo da Requisição (JSON):**
    Um objeto JSON com os campos e os novos valores.
-   **Exemplo de uso (curl):**
    ```bash
    curl -X PUT -H "Content-Type: application/json" \
      -d '''{"objeto": "Novo objeto para a licitação"}''' \
      http://127.0.0.1:5000/licitacoes/0
    ```

---


### 6. Deletar uma licitação

Remove um registro com base em seu índice.

-   **URL:** `/licitacoes/<index>`
-   **Método:** `DELETE`
-   **Parâmetros da URL:**
    -   `index` (inteiro, obrigatório): O índice do registro a ser deletado.
-   **Exemplo de uso (curl):**
    ```bash
    curl -X DELETE http://127.0.0.1:5000/licitacoes/0
    ```