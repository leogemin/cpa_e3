from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

try:
    # Nome do novo arquivo de dados
    file_name = 'ifpi-administracao-licitacoes-set2025.csv'
    
    # O caminho agora aponta para o arquivo na mesma pasta do script (src)
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, file_name)

    # Lendo o CSV completo
    df = pd.read_csv(
        csv_path, 
        sep=';', 
        encoding='utf-8',
        on_bad_lines='skip' 
    )
    print(f"Arquivo '{file_name}' carregado com sucesso com {len(df)} linhas.")

except FileNotFoundError:
    print(f"ERRO: O arquivo '{file_name}' não foi encontrado na pasta 'src'.")
    df = pd.DataFrame()

# Retornar as N primeiras licitações
@app.route('/licitacoes/<int:n>', methods=['GET'])
def get_first_n(n):
    return jsonify(df.head(n).to_dict(orient='records'))

# Filtrar por uma coluna específica (Ex: Modalidade da licitação)
@app.route('/licitacoes/modalidade/<string:modalidade_nome>', methods=['GET'])
def get_by_modalidade(modalidade_nome):
    if df.empty:
        return jsonify({'status': 'error', 'message': 'Dataset não carregado.'}), 500
    
    result = df[df['modalidade'].str.contains(modalidade_nome, case=False)]
    return jsonify(result.to_dict(orient='records'))

# Filtro avançado
@app.route('/licitacoes/filter', methods=['POST'])
def advanced_filter():
    if df.empty:
        return jsonify({'status': 'error', 'message': 'Dataset não carregado.'}), 500
    filters = request.get_json()
    result = df.copy()
    for field, value in filters.items():
        if field in result.columns:
            result = result[result[field].astype(str).str.lower() == str(value).lower()]
    return jsonify(result.to_dict(orient='records'))

# Adicionar uma nova licitação
@app.route('/licitacoes', methods=['POST'])
def add_licitacao():
    # Tenta pegar o JSON. Se não for válido, retorna erro.
    new_data = request.get_json()
    if not new_data:
        return jsonify({'status': 'error', 'message': 'Corpo da requisição está vazio ou não é um JSON válido.'}), 400

    # Verifica se os campos que consideramos essenciais estão presentes.
    required_fields = ['modalidade', 'objetoCompra']
    if not all(field in new_data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': f'Dados incompletos. Campos obrigatórios ausentes. É necessário ter: {required_fields}'
        }), 400

    # Tenta adicionar ao DataFrame.
    try:
        global df
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Retorna sucesso.
        return jsonify({'status': 'success', 'message': 'Licitação adicionada.'}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Ocorreu um erro interno no servidor.'}), 500

@app.route('/licitacoes/<int:index>', methods=['PUT'])

def update_licitacao(index):
    global df
    if index in df.index:
        updated_data = request.get_json()
        for field, value in updated_data.items():
            if field in df.columns:
                df.loc[index, field] = value
        return jsonify({'status': 'success', 'message': 'Licitação atualizada.'})
    return jsonify({'status': 'error', 'message': 'Índice não encontrado.'}), 404

# Esta única função substitui as duas anteriores (DELETE e PUT)
@app.route('/licitacoes/<int:index>', methods=['DELETE', 'PUT'])
def manipulate_licitacao_by_index(index):
    global df

    # 1. Validação de robustez: Checa se o índice é negativo.
    # Um índice nunca pode ser negativo, então é uma requisição inválida (Erro 400).
    if index < 0:
        return jsonify({'status': 'error', 'message': 'Índice inválido. O índice não pode ser negativo.'}), 400

    # 2. Validação de existência: Checa se o índice existe no DataFrame.
    # Se não existe, o recurso não foi encontrado (Erro 404).
    if index not in df.index:
        return jsonify({'status': 'error', 'message': f'Índice {index} não encontrado.'}), 404

    # --- Lógica para o método DELETE ---
    if request.method == 'DELETE':
        try:
            df = df.drop(index).reset_index(drop=True)
            return jsonify({'status': 'success', 'message': f'Licitação no índice {index} foi deletada.'})
        except Exception as e:
            print(f"ERRO INTERNO AO DELETAR: {e}")
            return jsonify({'status': 'error', 'message': 'Ocorreu um erro interno no servidor ao deletar.'}), 500
    
    # --- Lógica para o método PUT (Atualização) ---
    if request.method == 'PUT':
        try:
            update_data = request.get_json()
            if not update_data:
                return jsonify({'status': 'error', 'message': 'Corpo da requisição está vazio ou não é um JSON válido.'}), 400

            for field, value in update_data.items():
                if field in df.columns:
                    df.loc[index, field] = value
            
            return jsonify({'status': 'success', 'message': f'Licitação no índice {index} foi atualizada.'})
        except Exception as e:
            print(f"ERRO INTERNO AO ATUALIZAR: {e}")
            return jsonify({'status': 'error', 'message': 'Ocorreu um erro interno no servidor ao atualizar.'}), 500

if __name__ == '__main__':
    app.run(debug=True)