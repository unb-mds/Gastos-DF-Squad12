// Carrega os dados do arquivo JSON
fetch('resultados_compras.json')
    .then(response => response.json())
    .then(data => {
        inicializarDados(data);
    })
    .catch(error => console.error('Erro ao carregar o arquivo JSON:', error));

let dadosGlobais = [];

function inicializarDados(data) {
    // Converte os dados para um formato mais fácil de trabalhar
    dadosGlobais = Object.entries(data).flatMap(([data, compras]) => 
        compras.map(compra => ({
            data: new Date(data),
            ...compra
        }))
    );

    // Ordena os dados pela data mais recente
    dadosGlobais.sort((a, b) => b.data - a.data);

    // Inicializa o gráfico
    atualizarGrafico('dia');

    // Configura os event listeners
    document.getElementById('btnDia').addEventListener('click', () => atualizarGrafico('dia'));
    document.getElementById('btnSemana').addEventListener('click', () => atualizarGrafico('semana'));
    document.getElementById('btnMes').addEventListener('click', () => atualizarGrafico('mes'));
    document.getElementById('btnDetalhes').addEventListener('click', toggleDetalhes);
    document.getElementById('campoPesquisa').addEventListener('input', pesquisar);
    document.getElementById('colunaPesquisa').addEventListener('change', pesquisar);
}

let grafico;

function atualizarGrafico(periodo) {
    const ctx = document.getElementById('graficoGastos').getContext('2d');
    const dadosAgrupados = agruparDados(periodo);

    if (grafico) {
        grafico.destroy();
    }

    grafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dadosAgrupados.map(d => d.label),
            datasets: [{
                label: 'Total de Gastos',
                data: dadosAgrupados.map(d => d.total),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Valor (R$)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: periodo.charAt(0).toUpperCase() + periodo.slice(1)
                    }
                }
            }
        }
    });
}

function agruparDados(periodo) {
    let grupoDados = {};

    dadosGlobais.forEach(item => {
        let chave;
        switch (periodo) {
            case 'dia':
                chave = item.data.toISOString().split('T')[0];
                break;
            case 'semana':
                let primeiroDiaSemana = new Date(item.data.getFullYear(), item.data.getMonth(), item.data.getDate() - item.data.getDay());
                chave = primeiroDiaSemana.toISOString().split('T')[0];
                break;
            case 'mes':
                chave = `${item.data.getFullYear()}-${(item.data.getMonth() + 1).toString().padStart(2, '0')}`;
                break;
        }

        if (!grupoDados[chave]) {
            grupoDados[chave] = 0;
        }
        grupoDados[chave] += parseFloat(item.Valor.replace('R$', '').replace(',', '.'));
    });

    return Object.entries(grupoDados)
        .map(([label, total]) => ({ label, total }))
        .sort((a, b) => new Date(b.label) - new Date(a.label));
}

function toggleDetalhes() {
    const tabelaDetalhes = document.getElementById('tabelaDetalhes');
    const areaPesquisa = document.getElementById('areaPesquisa');
    if (tabelaDetalhes.style.display === 'none') {
        tabelaDetalhes.style.display = 'block';
        areaPesquisa.style.display = 'block';
        preencherTabela(dadosGlobais);
    } else {
        tabelaDetalhes.style.display = 'none';
        areaPesquisa.style.display = 'none';
    }
}

function preencherTabela(dados) {
    const corpoTabela = document.getElementById('corpoTabela');
    corpoTabela.innerHTML = '';

    dados.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.data.toLocaleDateString()}</td>
            <td>${item.Objeto}</td>
            <td>${item.Valor}</td>
            <td>${item.Empresa}</td>
            <td>${item.CNPJ}</td>
        `;
        corpoTabela.appendChild(tr);
    });
}

function pesquisar() {
    const termoPesquisa = document.getElementById('campoPesquisa').value.toLowerCase();
    const colunaPesquisa = document.getElementById('colunaPesquisa').value;

    const dadosFiltrados = dadosGlobais.filter(item => {
        let valorComparar;
        switch (colunaPesquisa) {
            case 'data':
                valorComparar = item.data.toLocaleDateString();
                break;
            case 'objeto':
                valorComparar = item.Objeto;
                break;
            case 'valor':
                valorComparar = item.Valor;
                break;
            case 'empresa':
                valorComparar = item.Empresa;
                break;
            case 'cnpj':
                valorComparar = item.CNPJ;
                break;
        }
        return valorComparar.toLowerCase().includes(termoPesquisa);
    });

    preencherTabela(dadosFiltrados);
}

// Função para autocompletar (simplificada)
function autocompletar() {
    const termoPesquisa = document.getElementById('campoPesquisa').value.toLowerCase();
    const colunaPesquisa = document.getElementById('colunaPesquisa').value;

    const sugestoes = dadosGlobais
        .map(item => {
            switch (colunaPesquisa) {
                case 'data': return item.data.toLocaleDateString();
                case 'objeto': return item.Objeto;
                case 'valor': return item.Valor;
                case 'empresa': return item.Empresa;
                case 'cnpj': return item.CNPJ;
            }
        })
        .filter((valor, index, self) => self.indexOf(valor) === index) // Remove duplicatas
        .filter(valor => valor.toLowerCase().includes(termoPesquisa));

    // Aqui você pode implementar a lógica para exibir as sugestões
    console.log(sugestoes); // Por enquanto, apenas logamos as sugestões
}

document.getElementById('campoPesquisa').addEventListener('input', autocompletar);

