document.addEventListener('DOMContentLoaded', function() {
    // Fetch data and render charts
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            renderGenderChart(data.genderData);
            renderStateChart(data.stateData);
            renderCollegeChart(data.collegeData);
            renderAgeChart(data.ageData);
        });

    function renderGenderChart(data) {
        const ctx = document.getElementById('genderChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Male', 'Female'],
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)', // Blue for Male
                        'rgba(255, 99, 132, 0.7)'  // Red for Female
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dropouts by Gender'
                    }
                }
            }
        });
    }

    function renderStateChart(data) {
        const ctx = document.getElementById('stateChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dropouts by State'
                    }
                }
            }
        });
    }

    function renderCollegeChart(data) {
        const ctx = document.getElementById('collegeChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Number of Dropouts',
                    data: data.values,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dropouts by College'
                    }
                }
            }
        });
    }

    function renderAgeChart(data) {
        const ctx = document.getElementById('ageChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Dropouts by Age',
                    data: data.values,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dropouts by Age'
                    }
                }
            }
        });
    }
});