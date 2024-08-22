document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const suggestionsBox = document.getElementById('suggestions');
    const chartContext = document.getElementById('lineChart').getContext('2d');

    let schoolsData = [];

    // Carrega o arquivo JSON
    fetch('resultados.json')
        .then(response => response.json())
        .then(data => {
            schoolsData = data;
        });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase();
        suggestionsBox.innerHTML = '';
        
        if (query.length > 1) {
            const filteredSchools = schoolsData.filter(school => 
                school.escola.toLowerCase().includes(query)
            );
            
            filteredSchools.forEach(school => {
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = school.escola;
                suggestionItem.addEventListener('click', () => {
                    searchInput.value = school.escola;
                    suggestionsBox.innerHTML = '';
                    displayChart(school);
                });
                suggestionsBox.appendChild(suggestionItem);
            });
        }
    });

    function displayChart(school) {
        const labels = school.dados.map(item => item.mes);
        const data = school.dados.map(item => item.valor);

        new Chart(chartContext, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `Valores de ${school.escola}`,
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
