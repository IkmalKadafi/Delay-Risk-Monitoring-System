
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        if (stats.error) {
            console.error(stats.error);
            return;
        }

        // Update Text Metrics
        document.getElementById('total-deliveries').textContent = stats.total_deliveries.toLocaleString();
        document.getElementById('predicted-breaches').textContent = stats.predicted_breaches.toLocaleString();
        document.getElementById('breach-rate').textContent = (stats.breach_rate * 100).toFixed(1) + '%';

        // Format Currency (IDR)
        const formatter = new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            maximumFractionDigits: 0
        });
        document.getElementById('risk-exposure').textContent = formatter.format(stats.total_risk_exposure);

        // Render Chart
        const ctx = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    label: '# of Deliveries',
                    data: [
                        stats.risk_distribution.low,
                        stats.risk_distribution.medium,
                        stats.risk_distribution.high
                    ],
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.6)', // Green
                        'rgba(234, 179, 8, 0.6)', // Yellow
                        'rgba(239, 68, 68, 0.6)'  // Red
                    ],
                    borderColor: [
                        'rgba(34, 197, 94, 1)',
                        'rgba(234, 179, 8, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });

        // Populate Action List (based on High Risk count)
        const actionList = document.getElementById('action-list');
        actionList.innerHTML = '';

        const highRisk = stats.risk_distribution.high;
        const mediumRisk = stats.risk_distribution.medium;

        if (highRisk > 0) {
            actionList.innerHTML += `
                <li style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center;">
                    <span style="width: 10px; height: 10px; background: #ef4444; border-radius: 50%; margin-right: 10px;"></span>
                    <span><strong>Escalate:</strong> ${highRisk} deliveries require immediate intervention.</span>
                </li>`;
        }
        if (mediumRisk > 0) {
            actionList.innerHTML += `
                <li style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center;">
                    <span style="width: 10px; height: 10px; background: #eab308; border-radius: 50%; margin-right: 10px;"></span>
                    <span><strong>Prioritize:</strong> ${mediumRisk} deliveries at risk. Monitor closely.</span>
                </li>`;
        }
        if (highRisk === 0 && mediumRisk === 0) {
            actionList.innerHTML = '<li style="padding: 10px;">All systems nominal. No immediate actions required.</li>';
        }

    } catch (err) {
        console.error("Dashboard error:", err);
    }
});
