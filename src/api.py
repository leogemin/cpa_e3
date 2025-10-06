from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# --- CARREGAMENTO DOS DADOS ---
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
        encoding='latin-1',
        on_bad_lines='skip' 
    )
    print(f"Arquivo '{file_name}' carregado com sucesso com {len(df)} linhas.")
    print("Colunas disponíveis:", df.columns.tolist())

except FileNotFoundError:
    print(f"ERRO: O arquivo '{file_name}' não foi encontrado na pasta 'src'. Certifique-se de que ele está lá.")
    df = pd.DataFrame()

# --- Endpoints da API de Licitações ---

# 1. Retornar as N primeiras licitações
@app.route('/licitacoes/<int:n>', methods=['GET'])
def get_first_n(n):
    return jsonify(df.head(n).to_dict(orient='records'))

# 2. Filtrar por uma coluna específica (Exemplo: Modalidade da licitação)
@app.route('/licitacoes/modalidade/<string:modalidade_nome>', methods=['GET'])
def get_by_modalidade(modalidade_nome):
    if df.empty:
        return jsonify({'status': 'error', 'message': 'Dataset não carregado.'}), 500
    
    # ATENÇÃO: Verifique se a coluna 'Modalidade' existe no seu CSV
    result = df[df['Modalidade'].str.contains(modalidade_nome, case=False)]
    return jsonify(result.to_dict(orient='records'))

# 3. Filtro avançado via JSON
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

# --- Endpoints de Inserção, Atualização e Deleção (CRUD) ---

@app.route('/licitacoes', methods=['POST'])
def add_licitacao():
    global df
    new_data = request.get_json()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    return jsonify({'status': 'success', 'message': 'Licitação adicionada.'}), 201

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

@app.route('/licitacoes/<int:index>', methods=['DELETE'])
def delete_licitacao(index):
    global df
    if index in df.index:
        df = df.drop(index).reset_index(drop=True)
        return jsonify({'status': 'success', 'message': 'Licitação deletada.'})
    return jsonify({'status': 'error', 'message': 'Índice não encontrado.'}), 404

if __name__ == '__main__':
    app.run(debug=True)