document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    let chart = null;
    let data = null;

    const fetchData = async () => {
        try {
            const response = await fetch('resultados.json');
            data = await response.json();
            updateChart('day');
            updateTable();
        } catch (error) {
            console.error('Erro ao carregar o arquivo JSON:', error);
        }
    };

    const formatData = (period) => {
        const labels = [];
        const values = [];

        data.resultados.forEach(result => {
            const date = new Date(result.date);
            let label = `${date.getDate()}/${date.getMonth() + 1}`;
            
            if (period === 'month') {
                label = `${date.getMonth() + 1}/${date.getFullYear()}`;
            }

            if (!labels.includes(label)) {
                labels.push(label);
                values.push(result.total_gasto_dia);
            } else {
                const index = labels.indexOf(label);
                values[index] += result.total_gasto_dia;
            }
        });

        // Inverte a ordem dos dados para que a data mais recente apareça à direita
        return { labels: labels.reverse(), values: values.reverse() };
    };

    const formatCurrency = (value) => {
        return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    };

    const updateChart = (period) => {
        if (!data) return;

        const { labels, values } = formatData(period);

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Total Gasto',
                    data: values,
                    backgroundColor: '#007bff',
                    borderColor: '#0056b3',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            reverse: false // Garantir que a ordem dos rótulos está correta
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };

    const updateTable = () => {
        if (!data) return;

        const tbody = document.getElementById('decreeTable');
        tbody.innerHTML = '';

        data.resultados.forEach(result => {
            const date = new Date(result.date).toLocaleDateString('pt-BR');

            result.decretos.forEach(decreto => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${date}</td>
                    <td>${decreto.decreto}</td>
                    <td>${formatCurrency(decreto.valor)}</td>
                    <td><a href="${result.url}" target="_blank"><button>Link</button></a></td>
                `;
                tbody.appendChild(row);
            });
        });
    };

    document.getElementById('time-period').addEventListener('change', (e) => {
        updateChart(e.target.value);
    });

    fetchData();
});
