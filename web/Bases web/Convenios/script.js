document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const tableBody = document.querySelector("#data-table tbody");
    const chartCanvas = document.getElementById("chart");

    let data = [];
    let filteredData = [];
    let chartInstance;

    function formatCurrency(value) {
        return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
    }

    function renderTable(data) {
        tableBody.innerHTML = "";
        data.forEach(entry => {
            entry.decretos.forEach(decreto => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td class="data-date">${entry.date}</td>
                    <td>${formatCurrency(decreto.valor)}</td>
                    <td>${decreto.interessado}</td>
                `;
                tableBody.appendChild(row);
            });
        });
    }

    function updateChart() {
        const monthlyData = {};

        filteredData.forEach(entry => {
            const month = entry.date.slice(0, 7); // Get YYYY-MM
            if (!monthlyData[month]) {
                monthlyData[month] = 0;
            }
            monthlyData[month] += entry.total_gasto_dia;
        });

        const labels = Object.keys(monthlyData).sort();
        const values = labels.map(month => monthlyData[month]);

        if (chartInstance) {
            chartInstance.destroy(); // Destroy the old chart instance
        }

        chartInstance = new Chart(chartCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Gasto Mensal',
                    data: values,
                    backgroundColor: '#007bff',
                    borderColor: '#0056b3',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Mês'
                        },
                        ticks: {
                            autoSkip: false,
                            maxRotation: 90,
                            minRotation: 45
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Valor (R$)'
                        },
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                }
            }
        });
    }

    function fetchData() {
        fetch('resultados_convenio.json')
            .then(response => response.json())
            .then(json => {
                data = json.resultados;
                filteredData = data; // Initialize filtered data
                renderTable(filteredData);
                updateChart();
            });
    }

    function search() {
        const query = searchInput.value.toLowerCase();
        filteredData = data.filter(entry =>
            entry.decretos.some(decreto =>
                decreto.interessado.toLowerCase().includes(query)
            )
        );
        renderTable(filteredData);
        updateChart();
    }

    searchInput.addEventListener('input', search);

    fetchData();
});
