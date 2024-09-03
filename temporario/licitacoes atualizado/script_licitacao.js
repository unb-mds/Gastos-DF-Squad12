let licitacoes = [];
const cardsPerPage = 20;
let currentPage = 1;

async function fetchData() {
    const response = await fetch('dados_licitacoes.json');
    licitacoes = await response.json();
    renderCards();
    renderChart();
}

function renderCards(filteredLicitacoes = licitacoes) {
    const container = document.getElementById('licitacoes-container');
    container.innerHTML = '';

    // Paginação
    const startIndex = (currentPage - 1) * cardsPerPage;
    const endIndex = startIndex + cardsPerPage;
    const paginatedLicitacoes = filteredLicitacoes.slice(startIndex, endIndex);

    paginatedLicitacoes.forEach(licitacao => {
        const card = document.createElement('div');
        card.className = 'card';
        
        const dataPub = new Date(licitacao.data_publicacao);
        const dataFormatada = `${dataPub.getDate().toString().padStart(2, '0')}/${(dataPub.getMonth() + 1).toString().padStart(2, '0')}/${dataPub.getFullYear()}`;

        card.innerHTML = `
            <h2>${licitacao.nome_modalidade}</h2>
            <p><strong>Data de Publicação:</strong> <span class="data">${dataFormatada}</span></p>
            <p><strong>Objeto:</strong> ${licitacao.objeto}</p>
        `;

        container.appendChild(card);
    });

    renderPagination(filteredLicitacoes.length);
}

function renderPagination(totalCards) {
    const paginationContainer = document.getElementById('pagination-container');
    if (!paginationContainer) {
        // Adiciona o container de paginação se não existir
        const newPaginationContainer = document.createElement('div');
        newPaginationContainer.id = 'pagination-container';
        newPaginationContainer.style.textAlign = 'center';
        document.querySelector('main').appendChild(newPaginationContainer);
    }

    const pages = Math.ceil(totalCards / cardsPerPage);
    let paginationHTML = '';

    if (pages > 1) {
        if (currentPage > 1) {
            paginationHTML += `<button class="pagination-btn" onclick="changePage(${currentPage - 1})">«</button>`;
        }

        for (let i = 1; i <= pages; i++) {
            if (i === 1 || i === pages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                paginationHTML += `<button class="pagination-btn${i === currentPage ? ' active' : ''}" onclick="changePage(${i})">${i}</button>`;
            } else if (i === currentPage - 3 || i === currentPage + 3) {
                paginationHTML += `<span class="pagination-ellipsis">...</span>`;
            }
        }

        if (currentPage < pages) {
            paginationHTML += `<button class="pagination-btn" onclick="changePage(${currentPage + 1})">»</button>`;
        }
    }

    document.getElementById('pagination-container').innerHTML = paginationHTML;
}

function changePage(page) {
    currentPage = page;
    renderCards();
}

function renderChart() {
    const ctx = document.getElementById('licitacoes-chart').getContext('2d');
    
    const dadosAgrupados = licitacoes.reduce((acc, licitacao) => {
        const data = licitacao.data_publicacao.split('T')[0];
        acc[data] = (acc[data] || 0) + 1;
        return acc;
    }, {});

    const labels = Object.keys(dadosAgrupados).sort((a, b) => new Date(b) - new Date(a)); // Ordem decrescente
    const data = labels.map(label => dadosAgrupados[label]);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Número de Licitações',
                data: data,
                borderColor: '#3498db',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Número de Licitações ao Longo do Tempo'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Data'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Número de Licitações'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const autocompleteResults = document.getElementById('autocomplete-results');

    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        const matchingLicitacoes = licitacoes.filter(licitacao => 
            licitacao.objeto.toLowerCase().includes(searchTerm)
        );

        if (searchTerm.length > 2) {
            renderAutocomplete(matchingLicitacoes);
            autocompleteResults.style.display = 'block';
        } else {
            autocompleteResults.style.display = 'none';
        }

        currentPage = 1; // Reset page number to 1 on search
        renderCards(matchingLicitacoes);
    });

    document.addEventListener('click', (e) => {
        if (!autocompleteResults.contains(e.target) && e.target !== searchInput) {
            autocompleteResults.style.display = 'none';
        }
    });
}

function renderAutocomplete(matchingLicitacoes) {
    const autocompleteResults = document.getElementById('autocomplete-results');
    autocompleteResults.innerHTML = '';

    matchingLicitacoes.slice(0, 5).forEach(licitacao => {
        const div = document.createElement('div');
        div.textContent = licitacao.objeto;
        div.addEventListener('click', () => {
            document.getElementById('search-input').value = licitacao.objeto;
            autocompleteResults.style.display = 'none';
            renderCards([licitacao]);
        });
        autocompleteResults.appendChild(div);
    });
}

fetchData();
setupSearch();
