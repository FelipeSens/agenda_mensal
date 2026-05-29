# Fluxo do Projeto: Agenda de Responsabilidades Contábeis

## 1. Visão Geral
O projeto é uma aplicação web simples em Flask que gerencia responsabilidades mensais com:
- CRUD de tarefas
- Banco de dados SQLite
- Relatórios em PDF
- Frontend em HTML/CSS/JavaScript

## 2. Arquivos Principais

### `app.py`
- Arquivo principal do backend.
- Inicializa o Flask e o banco de dados (`init_db()`).
- Renderiza as páginas HTML em rotas como `/`, `/agenda`, `/relatorio`, `/config`.
- Expõe API REST para o frontend consumir:
  - `GET /api/responsabilidades`
  - `POST /api/responsabilidades`
  - `PUT /api/responsabilidades/<id>`
  - `PATCH /api/responsabilidades/<id>/situacao`
  - `DELETE /api/responsabilidades/<id>`
  - `GET /api/estatisticas`
  - `GET /api/relatorio/pdf`
- Usa `database.py` para acessar o banco e `relatorios.py` para gerar PDF.

### `database.py`
- Conecta ao banco `responsabilidades.db`.
- Cria a tabela `responsabilidades` se não existir.
- Funções principais:
  - `init_db()`
  - `adicionar_responsabilidade()`
  - `obter_responsabilidades()`
  - `obter_responsabilidade_por_id()`
  - `atualizar_responsabilidade()`
  - `atualizar_situacao()`
  - `excluir_responsabilidade()`
  - `obter_responsabilidades_do_mes()`
  - `obter_estatisticas()`

### `relatorios.py`
- Gera relatórios em PDF usando ReportLab.
- `gerar_relatorio_pdf(ano, mes)` retorna bytes de PDF.
- O backend chama essa função na rota `/api/relatorio/pdf`.
- O JavaScript baixa o PDF do navegador.

### `templates/` (HTML)
- `index.html`: página inicial.
- `agenda.html`: página de cadastro e visualização de responsabilidades.
- `relatorio.html`: explicação sobre relatórios.
- `config.html`: página de configurações.

Cada template carrega o CSS em `/static/style_novo.css` e mostra um `section` com `id` específico.

### `static/script.js`
- Faz chamadas `fetch()` para a API do Flask.
- Atualiza a tabela na página de agenda.
- Tem funções para:
  - carregar responsabilidades
  - adicionar responsabilidade
  - editar responsabilidade
  - alterar situação
  - excluir responsabilidade
  - baixar relatório em PDF

### `static/style_novo.css`
- Estilos usados por todas as páginas.
- Define o aspecto da barra de navegação, formulários e tabelas.
- Agora é o único CSS usado pelo projeto, para manter consistência.

## Como cada arquivo se conecta
- `index.html`, `agenda.html`, `relatorio.html` e `config.html` são renderizados pelo Flask.
- `app.py` chama `render_template()` para cada uma dessas páginas.
- `agenda.html` também carrega `static/script.js`, que faz requisições para as rotas `/api/*`.
- `database.py` trata todas as operações de leitura/escrita no SQLite.
- `relatorios.py` gera o PDF quando o frontend pede `/api/relatorio/pdf`.
- O backend é responsável pelas regras de negócio; o frontend apenas exibe e pede dados.

## 3. Fluxo de uma requisição típica
1. O usuário abre `/agenda` no navegador.
2. O Flask retorna `templates/agenda.html`.
3. O navegador carrega `static/style_novo.css` e `static/script.js`.
4. `script.js` chama `GET /api/responsabilidades`.
5. O backend responde com os dados do banco via `database.obter_responsabilidades()`.
6. O JavaScript renderiza as linhas da tabela.
7. Ao cadastrar algo, o formulário envia `POST /api/responsabilidades`.
8. O backend grava no SQLite e retorna sucesso.
9. O frontend recarrega a tabela.

## 4. Como rodar
1. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o servidor:
   ```bash
   python app.py
   ```
3. Abra no navegador:
   `http://localhost:5000`

## 5. Observações úteis
- O banco de dados do projeto é `responsabilidades.db`.
- Se precisar recomeçar, pode apagar esse arquivo e reiniciar o app.
- `install_deps.py` também instala as dependências automaticamente.
