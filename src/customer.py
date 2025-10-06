import requests
import json

def main():
    """Função principal que executa todos os testes da API."""
    BASE_URL = 'http://127.0.0.1:5000'

    print("--- INICIANDO TESTES ---")

    # Consultando as 5 primeiras licitações
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/5", timeout=5)
        response.raise_for_status()  # Lança um erro se a requisição falhar (ex: 404, 500)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    # Filtrando por modalidade = 'Pregão'
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/modalidade/Pregão", timeout=5)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    # Adicionando uma nova licitação
    try:
        # Dicionário com os nomes de coluna
        nova_licitacao = {
            "modalidade": "Convite",
            "objetoCompra": "Aquisição de material de escritório para o IFPI"
        }
        response = requests.post(f"{BASE_URL}/licitacoes", json=nova_licitacao, timeout=5)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    print("\n--- FIM DOS TESTES ---")


if __name__ == "__main__":
    main()