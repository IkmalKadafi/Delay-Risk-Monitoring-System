
document.addEventListener('DOMContentLoaded', async () => {
    const tableHead = document.querySelector('#data-table thead');
    const tableBody = document.querySelector('#data-table tbody');

    try {
        const response = await fetch('/api/data/sample');
        const data = await response.json();

        if (data.error) {
            tableBody.innerHTML = `<tr><td colspan="5">Error: ${data.error}</td></tr>`;
            return;
        }

        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5">No data available.</td></tr>';
            return;
        }

        // Headers
        const columns = Object.keys(data[0]); // Take keys from first object
        const headerRow = document.createElement('tr');
        columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

        // Body
        data.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(col => {
                const td = document.createElement('td');
                td.textContent = row[col];
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });

    } catch (err) {
        console.error("Failed to load dataset:", err);
        tableBody.innerHTML = `<tr><td colspan="5">Failed to load data.</td></tr>`;
    }
});
