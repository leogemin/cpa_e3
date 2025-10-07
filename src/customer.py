import requests
import json

def main():
    """Função principal que executa todos os testes da API."""
    BASE_URL = 'http://127.0.0.1:5000'

    print("--- INICIANDO TESTES ---")

    # Consultando as 5 primeiras licitações
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/5", timeout=5)
        response.raise_for_status()
        print("\n--- GET /licitacoes/5 ---")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    # Filtrando por modalidade = 'Pregão'
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/modalidade/Pregão", timeout=5)
        response.raise_for_status()
        print("\n--- GET /licitacoes/modalidade/Pregão ---")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

        
    nova_licitacao = {
        "modalidade": "Convite",
        "objetoCompra": "Aquisição de material de teste via API"
    }
    dados_para_atualizar = {
        "objetoCompra": "Material de teste ATUALIZADO via API"
    }
    index_alvo = -1

    try:
        # Pega o total atual para saber o índice do novo item
        response_total = requests.get(f"{BASE_URL}/licitacoes/99999", timeout=5)
        response_total.raise_for_status()
        index_alvo = len(response_total.json())

        # Adicionando uma nova licitação (POST)
        print(f"\n--- POST /licitacoes (no índice {index_alvo}) ---")
        response_post = requests.post(f"{BASE_URL}/licitacoes", json=nova_licitacao, timeout=5)
        response_post.raise_for_status()
        print(response_post.json())

        # Atualizando a licitação recém-criada (PUT)
        print(f"\n--- PUT /licitacoes/{index_alvo} ---")
        response_put = requests.put(f"{BASE_URL}/licitacoes/{index_alvo}", json=dados_para_atualizar, timeout=5)
        response_put.raise_for_status()
        print(response_put.json())

        # Deletando a licitação (DELETE)
        print(f"\n--- DELETE /licitacoes/{index_alvo} ---")
        response_delete = requests.delete(f"{BASE_URL}/licitacoes/{index_alvo}", timeout=5)
        response_delete.raise_for_status()
        print(response_delete.json())

    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição de escrita (POST/PUT/DELETE): {e}")


    print("\n--- FIM DOS TESTES ---")


if __name__ == "__main__":
    main()

