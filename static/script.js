async function sendRequest() {
    const method = document.getElementById('method').value;
    const endpoint = document.getElementById('endpoint').value;
    const requestBody = document.getElementById('requestBody').value;
    const responseArea = document.getElementById('response');

    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (method !== 'GET' && method !== 'DELETE' && requestBody) {
            options.body = requestBody;
        }

        const response = await fetch(endpoint, options);
        const data = await response.json();
        responseArea.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        responseArea.textContent = `Error: ${error.message}`;
    }
}

// Enable/disable request body based on method
document.getElementById('method').addEventListener('change', function(e) {
    const requestBody = document.getElementById('requestBody');
    requestBody.disabled = e.target.value === 'GET' || e.target.value === 'DELETE';
});
