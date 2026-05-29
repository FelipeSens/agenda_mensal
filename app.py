import io

from flask import Flask, render_template, request, jsonify, send_file
from database import (
    init_db, adicionar_responsabilidade, obter_responsabilidades,
    obter_responsabilidade_por_id, atualizar_responsabilidade,
    atualizar_situacao, excluir_responsabilidade, obter_estatisticas
)
from relatorios import gerar_relatorio_pdf

# Cria a aplicação Flask. Flask é o microframework que responde às requisições HTTP.
app = Flask(__name__)

# Inicializa o banco de dados SQLite e cria as tabelas se necessário.
#
# Este arquivo é o ponto de entrada da aplicação. Ele:
# - Renderiza as páginas HTML das rotas principais
# - Expõe os endpoints JSON usados pelo frontend JavaScript
# - Integra o backend com o banco de dados e a geração de PDFs
init_db()

# Rotas das páginas principais do site.
# Cada rota retorna um template HTML que será renderizado no navegador.
@app.route('/')
def home():
    # Página inicial
    return render_template('index.html')

@app.route('/agenda')
def agenda():
    # Página de gerenciamento de responsabilidades
    return render_template('agenda.html')

@app.route('/relatorio')
def relatorio():
    # Página de relatórios
    return render_template('relatorio.html')

@app.route('/config')
def config():
    # Página de configurações
    return render_template('config.html')

# Aliases diretos para arquivos HTML antigos / legados.
# Essas rotas não criam novos conteúdos; apenas mantém compatibilidade com URLs
# antigas que podem ter sido usadas em outros lugares.
@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/agenda.html')
def agenda_html():
    return render_template('agenda.html')

@app.route('/relatorio.html')
def relatorio_html():
    return render_template('relatorio.html')

@app.route('/config.html')
def config_html():
    return render_template('config.html')

# Rotas legadas para compatibilidade com âncoras antigas
@app.route('/relatorios')
def relatorios():
    return render_template('relatorio.html')

@app.route('/configuracoes')
def configuracoes():
    return render_template('config.html')

# ROTAS DE RESPONSABILIDADES (API)
# Essas rotas são usadas pelo JavaScript do frontend para buscar e modificar
# dados no backend. Elas retornam JSON em vez de HTML.

@app.route('/api/responsabilidades', methods=['GET'])
def get_responsabilidades():
    """Obtém todas as responsabilidades"""
    responsabilidades = obter_responsabilidades()
    return jsonify(responsabilidades)

@app.route('/api/responsabilidades', methods=['POST'])
def criar_responsabilidade():
    """Cria uma nova responsabilidade"""
    # request.get_json() lê o corpo da requisição como JSON enviado pelo frontend.
    dados = request.get_json()
    
    try:
        resp_id = adicionar_responsabilidade(
            dados.get('descricao'),
            dados.get('data'),
            dados.get('situacao', 'pendente')
        )
        # 201 significa criado com sucesso.
        return jsonify({'id': resp_id, 'mensagem': 'Responsabilidade criada com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retornamos 400 com a mensagem de erro.
        return jsonify({'erro': str(e)}), 400

@app.route('/api/responsabilidades/<int:resp_id>', methods=['GET'])
def obter_responsabilidade(resp_id):
    """Obtém uma responsabilidade específica"""
    resp = obter_responsabilidade_por_id(resp_id)
    if resp:
        return jsonify(resp)
    return jsonify({'erro': 'Responsabilidade não encontrada'}), 404

@app.route('/api/responsabilidades/<int:resp_id>', methods=['PUT'])
def atualizar_resp(resp_id):
    """Atualiza uma responsabilidade"""
    dados = request.get_json()
    
    try:
        atualizar_responsabilidade(
            resp_id,
            dados.get('descricao'),
            dados.get('data'),
            dados.get('situacao')
        )
        return jsonify({'mensagem': 'Responsabilidade atualizada com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/responsabilidades/<int:resp_id>/situacao', methods=['PATCH'])
def alterar_situacao(resp_id):
    """Altera a situação de uma responsabilidade"""
    # PATCH é usado para atualizar apenas um campo parcial.
    dados = request.get_json()
    
    try:
        atualizar_situacao(resp_id, dados.get('situacao'))
        return jsonify({'mensagem': 'Situação atualizada com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/responsabilidades/<int:resp_id>', methods=['DELETE'])
def deletar_responsabilidade(resp_id):
    """Deleta uma responsabilidade"""
    try:
        excluir_responsabilidade(resp_id)
        return jsonify({'mensagem': 'Responsabilidade deletada com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# ROTA DE ESTATÍSTICAS

@app.route('/api/estatisticas', methods=['GET'])
def get_estatisticas():
    """Obtém estatísticas gerais"""
    stats = obter_estatisticas()
    return jsonify(stats)

# ROTA DE RELATÓRIOS

@app.route('/api/relatorio/pdf', methods=['GET'])
def download_relatorio():
    """Gera e faz download do relatório em PDF"""
    # Request args são parâmetros da URL, por exemplo ?ano=2024&mes=5
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    
    try:
        pdf_content = gerar_relatorio_pdf(ano, mes)
        
        # send_file envia o PDF gerado como resposta de download.
        return send_file(
            io.BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_responsabilidades_{ano}_{mes:02d}.pdf'
        )
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# ROTA LEGADA (mantida para compatibilidade)

@app.route('/calcular', methods=['POST'])
def calcular_imposto():
    """Calcula retenção de impostos (legado)"""
    dados = request.get_json()
    valor = float(dados.get('valor', 0))
    
    if valor > 5000:
        resposta = f"Atenção: Nota de R$ {valor:.2f} exige retenção de impostos na fonte."
    else:
        resposta = f"Nota de R$ {valor:.2f} isenta de retenção na fonte."
        
    return jsonify({"mensagem": list([resposta])})

if __name__ == '__main__':
    app.run(debug=True)