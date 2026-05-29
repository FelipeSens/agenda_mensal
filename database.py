import sqlite3
import os
from datetime import datetime

DB_PATH = 'responsabilidades.db'

# O banco de dados SQLite armazena as responsabilidades localmente.
# Cada função abaixo abre uma conexão, executa uma query e fecha a conexão.
# O uso de sqlite3.Row permite acessar colunas por nome e converter facilmente
# o resultado em um dicionário para retornar JSON ao frontend.

def get_connection():
    """Cria conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responsabilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_execucao DATE NOT NULL,
            situacao TEXT NOT NULL DEFAULT 'pendente',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def adicionar_responsabilidade(descricao, data_execucao, situacao='pendente'):
    """Adiciona uma nova responsabilidade"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO responsabilidades (descricao, data_execucao, situacao)
        VALUES (?, ?, ?)
    ''', (descricao, data_execucao, situacao))
    
    conn.commit()
    resp_id = cursor.lastrowid
    conn.close()
    
    return resp_id

def obter_responsabilidades():
    """Obtém todas as responsabilidades"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM responsabilidades ORDER BY data_execucao')
    responsabilidades = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return responsabilidades

def obter_responsabilidade_por_id(resp_id):
    """Obtém uma responsabilidade pelo ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM responsabilidades WHERE id = ?', (resp_id,))
    responsabilidade = cursor.fetchone()
    
    conn.close()
    return dict(responsabilidade) if responsabilidade else None

def atualizar_responsabilidade(resp_id, descricao, data_execucao, situacao):
    """Atualiza uma responsabilidade"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE responsabilidades 
        SET descricao = ?, data_execucao = ?, situacao = ?, data_atualizacao = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (descricao, data_execucao, situacao, resp_id))
    
    conn.commit()
    conn.close()

def atualizar_situacao(resp_id, situacao):
    """Atualiza apenas a situação de uma responsabilidade"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE responsabilidades 
        SET situacao = ?, data_atualizacao = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (situacao, resp_id))
    
    conn.commit()
    conn.close()

def excluir_responsabilidade(resp_id):
    """Exclui uma responsabilidade"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM responsabilidades WHERE id = ?', (resp_id,))
    
    conn.commit()
    conn.close()

def obter_responsabilidades_do_mes(ano, mes):
    """Obtém responsabilidades de um mês específico"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM responsabilidades 
        WHERE strftime('%Y', data_execucao) = ? 
        AND strftime('%m', data_execucao) = ?
        ORDER BY data_execucao
    ''', (str(ano).zfill(4), str(mes).zfill(2)))
    
    responsabilidades = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return responsabilidades

def obter_estatisticas():
    """Obtém estatísticas gerais"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN situacao = 'pendente' THEN 1 ELSE 0 END) as pendentes,
            SUM(CASE WHEN situacao = 'em_progresso' THEN 1 ELSE 0 END) as em_progresso,
            SUM(CASE WHEN situacao = 'concluido' THEN 1 ELSE 0 END) as concluidos
        FROM responsabilidades
    ''')
    
    resultado = cursor.fetchone()
    conn.close()
    
    return {
        'total': resultado[0] or 0,
        'pendentes': resultado[1] or 0,
        'em_progresso': resultado[2] or 0,
        'concluidos': resultado[3] or 0
    }

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")
