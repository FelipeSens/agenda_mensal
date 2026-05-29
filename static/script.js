/*
  script.js: lógica frontend da página de agenda.
  - Busca responsabilidades via API (/api/responsabilidades)
  - Atualiza a tabela HTML dinamicamente
  - Envia POST/PUT/PATCH/DELETE para o backend
  - Controla a experiência do usuário sem recarregar a página
*/

// Seleciona os elementos do DOM usados pelo script.
const formResponsabilidade = document.getElementById('formResponsabilidade');
const tabelaResponsabilidades = document.getElementById('tabelaResponsabilidades');

let responsabilidades = [];

// Envia o formulário para criar uma nova responsabilidade.
// O evento é interceptado para evitar recarregar a página.
formResponsabilidade.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const descricao = document.getElementById('descricao').value;
    const data = document.getElementById('data').value;
    const situacao = document.getElementById('situacao').value;
    
    try {
        const response = await fetch('/api/responsabilidades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                descricao,
                data,
                situacao
            })
        });
        
        if (response.ok) {
            formResponsabilidade.reset();
            await carregarResponsabilidades();
        } else {
            alert('Erro ao adicionar responsabilidade');
        }
    } catch (erro) {
        console.error('Erro:', erro);
        alert('Erro ao comunicar com o servidor');
    }
});

// Busca todas as responsabilidades do backend e atualiza a tabela.
// Esta função é usada na inicialização e sempre que ocorre uma alteração.
async function carregarResponsabilidades() {
    try {
        const response = await fetch('/api/responsabilidades');
        responsabilidades = await response.json();
        atualizarTabela();
    } catch (erro) {
        console.error('Erro ao carregar responsabilidades:', erro);
    }
}

// Atualiza a tabela HTML que mostra as responsabilidades.
// Se não houver registros, exibe uma mensagem padrão.
function atualizarTabela() {
    tabelaResponsabilidades.innerHTML = '';
    
    if (responsabilidades.length === 0) {
        tabelaResponsabilidades.innerHTML = '<tr><td colspan="4" class="sem-dados">Nenhuma responsabilidade adicionada ainda</td></tr>';
        return;
    }
    
    responsabilidades.forEach(resp => {
        const linha = document.createElement('tr');
        
        // Formatar data
        const dataFormatada = new Date(resp.data_execucao + 'T00:00:00').toLocaleDateString('pt-BR');
        
        // Mapear situação para label
        const labelSituacao = {
            'pendente': 'Pendente',
            'em_progresso': 'Em Progresso',
            'concluido': 'Concluído'
        };
        
        linha.innerHTML = `
            <td>${resp.descricao}</td>
            <td>${dataFormatada}</td>
            <td><span class="situacao-${resp.situacao}">${labelSituacao[resp.situacao]}</span></td>
            <td>
                <button class="btn-acao btn-status" onclick="alterarSituacao(${resp.id})">🔄 Alterar</button>
                <button class="btn-acao btn-editar" onclick="editarResponsabilidade(${resp.id})">✏️ Editar</button>
                <button class="btn-acao btn-excluir" onclick="excluirResponsabilidade(${resp.id})">🗑️ Excluir</button>
            </td>
        `;
        
        tabelaResponsabilidades.appendChild(linha);
    });
}

// Altera a situação de uma responsabilidade em ciclo:
// pendente -> em_progresso -> concluido -> pendente
async function alterarSituacao(id) {
    const resp = responsabilidades.find(r => r.id === id);
    if (!resp) return;
    
    const situacoes = ['pendente', 'em_progresso', 'concluido'];
    const indexAtual = situacoes.indexOf(resp.situacao);
    const proximoIndex = (indexAtual + 1) % situacoes.length;
    
    const novaSituacao = situacoes[proximoIndex];
    
    try {
        const response = await fetch(`/api/responsabilidades/${id}/situacao`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ situacao: novaSituacao })
        });
        
        if (response.ok) {
            await carregarResponsabilidades();
        }
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

// Permite editar descrição e data usando prompts básicos do navegador.
async function editarResponsabilidade(id) {
    const resp = responsabilidades.find(r => r.id === id);
    if (!resp) return;
    
    const novaDescricao = prompt('Nova descrição:', resp.descricao);
    if (novaDescricao === null) return;
    
    const novaData = prompt('Nova data (YYYY-MM-DD):', resp.data_execucao);
    if (novaData === null) return;
    
    try {
        const response = await fetch(`/api/responsabilidades/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                descricao: novaDescricao,
                data: novaData,
                situacao: resp.situacao
            })
        });
        
        if (response.ok) {
            await carregarResponsabilidades();
        }
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

// Exclui uma responsabilidade após confirmação do usuário.
async function excluirResponsabilidade(id) {
    if (!confirm('Tem certeza que deseja excluir esta responsabilidade?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/responsabilidades/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await carregarResponsabilidades();
        }
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

// Solicita ao backend a geração do PDF do relatório mensal e força o download.
async function baixarRelatorio() {
    const agora = new Date();
    const ano = agora.getFullYear();
    const mes = agora.getMonth() + 1;
    
    try {
        const response = await fetch(`/api/relatorio/pdf?ano=${ano}&mes=${mes}`);
        const blob = await response.blob();
        
        // Criar link para download
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `relatorio_responsabilidades_${ano}_${mes.toString().padStart(2, '0')}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (erro) {
        console.error('Erro ao baixar relatório:', erro);
        alert('Erro ao gerar relatório');
    }
}

// Carregar responsabilidades na inicialização
carregarResponsabilidades();