import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# 1. Consultando as 5 primeiras licitações
print("--- Consultando as 5 primeiras licitações ---")
response = requests.get(f"{BASE_URL}/licitacoes/5")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 2. Filtrando por modalidade = 'Pregão'
# ATENÇÃO: Troque 'Pregão' por um valor que exista na sua coluna 'Modalidade'
print("\n--- Buscando licitações da modalidade 'Pregão' ---")
response = requests.get(f"{BASE_URL}/licitacoes/modalidade/Pregão")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 3. Adicionando uma nova licitação (com colunas de exemplo)
print("\n--- Adicionando uma nova licitação (exemplo) ---")
# ATENÇÃO: Adapte as chaves ('Modalidade', 'Objeto') para colunas que existam no seu CSV
nova_licitacao = {
    "modalidade": "Convite",
    "objetoCompra": "Aquisição de material de escritório",
    "Valor": 15000.00
}
response = requests.post(f"{BASE_URL}/licitacoes", json=nova_licitacao)
print(response.json())

# 4. Deletando a licitação no índice 0
print("\n--- Deletando a licitação no índice 0 ---")
response = requests.delete(f"{BASE_URL}/licitacoes/0")
print(response.json())