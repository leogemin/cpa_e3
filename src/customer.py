import requests
import json

def main():
    """Função principal que executa todos os testes da API."""
    BASE_URL = 'http://127.0.0.1:5000'

    print("--- INICIANDO TESTES NO CLIENTE ---")

    # 1. Consultando as 5 primeiras licitações
    print("\n--- Teste 1: Consultando as 5 primeiras licitações ---")
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/5", timeout=5)
        response.raise_for_status()  # Lança um erro se a requisição falhar (ex: 404, 500)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    # 2. Filtrando por modalidade = 'Pregão'
    print("\n--- Teste 2: Buscando licitações da modalidade 'Pregão' ---")
    try:
        response = requests.get(f"{BASE_URL}/licitacoes/modalidade/Pregão", timeout=5)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisição: {e}")

    # 3. Adicionando uma nova licitação (com colunas de exemplo)
    print("\n--- Teste 3: Adicionando uma nova licitação (exemplo) ---")
    try:
        # Dicionário com os nomes de coluna CORRETOS (minúsculos)
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
    # Este bloco garante que a função main() só será executada
    # quando o script for rodado diretamente.
    main()