# 📅 Agenda Mensal de Responsabilidades Contabéis

Sistema web para gerenciar responsabilidades contábeis mensais com banco de dados persistente e relatórios em PDF.

## ✨ Funcionalidades

### ✅ Implementadas
- **Banco de Dados SQLite**: Armazenamento persistente e seguro
- **CRUD Completo**: Criar, editar, excluir e visualizar responsabilidades
- **Gerenciamento de Situação**: Pendente → Em Progresso → Concluído
- **Relatórios em PDF**: Download de relatório mensal formatado
- **Estatísticas**: Dashboard com resumo geral
- **API RESTful**: Endpoints para integração
- **Interface Responsiva**: Funciona em desktop e mobile

### 🚀 Como Usar

#### 1. **Instalação de Dependências**

```bash
# Opção 1: Usar pip
pip install -r requirements.txt

# Opção 2: Usar script Python
python install_deps.py
```

#### 2. **Executar a Aplicação**

```bash
python app.py
```

O servidor vai iniciar em: `http://localhost:5000`

#### 3. **Usar a Aplicação**

**Na seção Home:**
- Visualizar descrição da agenda
- Entender funcionalidades principais

**Na seção Agenda:**
- ➕ **Adicionar**: Preencher formulário e clicar "Adicionar Responsabilidade"
- 🔄 **Alterar Situação**: Clique no botão para ciclar entre situações
- ✏️ **Editar**: Modifique descrição e data
- 🗑️ **Excluir**: Remova com confirmação
- 📄 **Baixar Relatório**: Gere PDF com todas as responsabilidades do mês

**Dados Persistentes:**
- Todos os dados são salvos no banco de dados SQLite
- Não são perdidos ao fechar o navegador
- Arquivo: `responsabilidades.db`

---

## 🗄️ Estrutura do Banco de Dados

```sql
CREATE TABLE responsabilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    data_execucao DATE NOT NULL,
    situacao TEXT NOT NULL DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🌐 Endpoints da API

### Responsabilidades

**GET** `/api/responsabilidades`
- Obtém todas as responsabilidades
- Resposta: Array JSON

**POST** `/api/responsabilidades`
- Cria nova responsabilidade
- Body: `{ "descricao": "...", "data": "YYYY-MM-DD", "situacao": "pendente" }`

**GET** `/api/responsabilidades/<id>`
- Obtém responsabilidade específica

**PUT** `/api/responsabilidades/<id>`
- Atualiza responsabilidade
- Body: `{ "descricao": "...", "data": "YYYY-MM-DD", "situacao": "..." }`

**PATCH** `/api/responsabilidades/<id>/situacao`
- Altera apenas a situação
- Body: `{ "situacao": "em_progresso" }`

**DELETE** `/api/responsabilidades/<id>`
- Deleta responsabilidade

### Estatísticas

**GET** `/api/estatisticas`
- Retorna: `{ "total": 10, "pendentes": 3, "em_progresso": 2, "concluidos": 5 }`

### Relatórios

**GET** `/api/relatorio/pdf?ano=2024&mes=5`
- Faz download do relatório em PDF
- Parâmetros: `ano` e `mes` (opcionais, usa mês atual se não informado)

---

## 📁 Estrutura do Projeto

```
meu_projeto/
├── app.py                           # Aplicação Flask principal
├── database.py                      # Operações do banco de dados
├── relatorios.py                    # Geração de PDF
├── install_deps.py                  # Script para instalar dependências
├── requirements.txt                 # Dependências Python
├── responsabilidades.db             # Banco de dados (criado automaticamente)
├── FUNCIONALIDADES_EXTRAS.md        # Funcionalidades que podem ser adicionadas
├── README.md                        # Este arquivo
├── templates/
│   └── index.html                   # Frontend (HTML)
├── static/
│   ├── style_novo.css               # Estilos atualizados para todas as páginas
│   └── script.js                    # Lógica frontend (JavaScript)
└── relatorios/                      # Pasta para relatórios salvos
```

---

## 🔧 Técnicas Utilizadas

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite3
- **Relatórios**: ReportLab (PDF)
- **API**: RESTful com JSON

### Frontend
- **HTML5**: Marcação semântica
- **CSS3**: Estilos responsivos
- **JavaScript**: Fetch API para comunicação com backend

---

## 📊 Próximas Funcionalidades Recomendadas

Veja `FUNCIONALIDADES_EXTRAS.md` para:
- Dashboard com gráficos
- Relatórios personalizados
- Exportar para Excel
- Notificações por email
- Tarefas recorrentes
- E mais!

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'reportlab'"
```bash
pip install reportlab
```

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask
```

### Porta 5000 já em uso
```bash
# Usar outra porta
python -c "from app import app; app.run(port=5001)"
```

### Banco de dados corrompido
```bash
# Delete e recrie
rm responsabilidades.db
python -c "from database import init_db; init_db()"
```

---

## 📝 Licença

Projeto para uso educacional e profissional.

---

## 👤 Desenvolvido com ❤️

Sistema contábil inteligente para facilitar sua vida!
