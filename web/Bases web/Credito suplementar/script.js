document.addEventListener('DOMContentLoaded', () => {
    const jsonFilePath = 'resultados_credito.json';

    fetch(jsonFilePath)
        .then(response => response.json())
        .then(data => {
            const resultados = data.resultados;

            const monthlyData = {};
            resultados.forEach(res => {
                const month = res.date.substring(0, 7);
                if (!monthlyData[month]) {
                    monthlyData[month] = 0;
                }
                monthlyData[month] += res.decretos.length;
            });

            const labels = Object.keys(monthlyData).reverse();
            const decreesCounts = Object.values(monthlyData).reverse();

            const ctx = document.getElementById('decretosChart').getContext('2d');
            const decretosChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Número de Decretos',
                        data: decreesCounts,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        borderRadius: 8,
                        barThickness: 30
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Mês/Ano',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
                            grid: {
                                display: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                maxRotation: 45,
                                minRotation: 45
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Número de Decretos',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
                            grid: {
                                color: 'rgba(200, 200, 200, 0.3)'
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                callback: function(value) {
                                    return value.toLocaleString('pt-BR');
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                font: {
                                    size: 14
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Decretos: ${context.parsed.y.toLocaleString('pt-BR')}`;
                                }
                            }
                        }
                    },
                    animation: {
                        duration: 1500,
                        easing: 'easeOutQuart'
                    }
                }
            });
            
            // Tabela de histórico
            const toggleHistoryButton = document.getElementById('toggleHistory');
            const historyTable = document.getElementById('historyTable');
            const historyBody = document.getElementById('historyBody');

            toggleHistoryButton.addEventListener('click', () => {
                historyTable.classList.toggle('hidden');
            });

            // Preenchendo a tabela de histórico
            resultados.reverse().forEach(res => {
                const row = document.createElement('tr');
                row.classList.add('expandable');
                row.innerHTML = `
                    <td>${res.date}</td>
                    <td>${res.decretos.length}</td>
                `;
                row.addEventListener('click', () => {
                    row.nextElementSibling.classList.toggle('hiddenRow');
                });

                const detailRow = document.createElement('tr');
                detailRow.classList.add('hiddenRow');
                detailRow.innerHTML = `
                    <td colspan="2">
                        <ul>
                            ${res.decretos.map(dec => `
                                <li>
                                    Decreto: ${dec.decreto} - Valor: R$${dec.valor.toLocaleString('pt-BR')}
                                </li>`).join('')}
                            <li><a href="${res.url}" target="_blank">Link para o PDF</a></li>
                        </ul>
                    </td>
                `;

                historyBody.appendChild(row);
                historyBody.appendChild(detailRow);
            });
        })
        .catch(error => console.error('Erro ao carregar o JSON:', error));
});
