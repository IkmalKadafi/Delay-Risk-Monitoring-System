
document.addEventListener('DOMContentLoaded', () => {
    const thresholdInput = document.getElementById('param-threshold');
    const thresholdVal = document.getElementById('val-threshold');
    const costFnInput = document.getElementById('param-cost-fn');
    const costFpInput = document.getElementById('param-cost-fp');
    const runBtn = document.getElementById('btn-run');

    let costChartInstance = null;
    let tradeoffChartInstance = null;

    // Update label on slide
    thresholdInput.addEventListener('input', (e) => {
        thresholdVal.textContent = parseFloat(e.target.value).toFixed(2);
    });

    const runSimulation = async () => {
        const payload = {
            threshold: parseFloat(thresholdInput.value),
            cost_fn: parseFloat(costFnInput.value),
            cost_fp: parseFloat(costFpInput.value)
        };

        try {
            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.detail || data.error) {
                console.error("Simulation Error", data);
                return;
            }

            const impact = data.impact;
            const curves = data.curves;

            // Update Metrics
            const formatter = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 });
            document.getElementById('sim-total-cost').textContent = formatter.format(impact.total_cost);

            const savingsEl = document.getElementById('sim-savings');
            savingsEl.textContent = formatter.format(impact.savings_vs_baseline);
            savingsEl.className = impact.savings_vs_baseline >= 0 ? "stat-value text-success" : "stat-value text-danger";

            document.getElementById('sim-interventions').textContent = impact.intervention_count.toLocaleString();
            document.getElementById('sim-missed').textContent = impact.missed_sla_count.toLocaleString();

            // Update Charts
            updateCharts(curves, impact.threshold);

        } catch (err) {
            console.error(err);
        }
    };

    const updateCharts = (curves, currentThreshold) => {
        const labels = curves.map(c => c.threshold.toFixed(2));
        const costs = curves.map(c => c.total_cost);
        const interventions = curves.map(c => c.intervention_rate * 100);

        // Chart 1: Cost Curve
        const ctx1 = document.getElementById('costCurveChart').getContext('2d');
        if (costChartInstance) costChartInstance.destroy();

        costChartInstance = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Expected Cost (Rp)',
                    data: costs,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                xMin: labels.indexOf(currentThreshold.toFixed(2)),
                                xMax: labels.indexOf(currentThreshold.toFixed(2)),
                                borderColor: 'white',
                                borderWidth: 2,
                                borderDash: [5, 5]
                            }
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'Threshold' } },
                    y: { title: { display: true, text: 'Cost (Rp)' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });

        // Chart 2: Tradeoff
        const ctx2 = document.getElementById('tradeoffChart').getContext('2d');
        if (tradeoffChartInstance) tradeoffChartInstance.destroy();

        tradeoffChartInstance = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Intervention Rate (%)',
                    data: interventions,
                    borderColor: '#eab308',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Threshold' } },
                    y: { title: { display: true, text: '%' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    };

    // Auto-run on load
    runSimulation();

    // Attach listener
    runBtn.addEventListener('click', runSimulation);
    // Also run on drag end for slider?
    thresholdInput.addEventListener('change', runSimulation);
});
