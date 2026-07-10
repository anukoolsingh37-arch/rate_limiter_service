const API_BASE = 'http://localhost:8000';

// Create Client Form
document.getElementById('createClientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const clientKey = document.getElementById('clientKey').value;
    const capacity = parseInt(document.getElementById('capacity').value);
    const refillRate = parseFloat(document.getElementById('refillRate').value);
    
    const resultDiv = document.getElementById('createResult');
    
    try {
        const response = await fetch(`${API_BASE}/clients/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_key: clientKey,
                capacity: capacity,
                refill_rate_per_second: refillRate
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.className = 'result success';
            resultDiv.innerHTML = `
                <strong>Success!</strong>
                <p>Client: ${data.client_key}</p>
                <p>Capacity: ${data.capacity} tokens</p>
                <p>Refill Rate: ${data.refill_rate_per_second}/sec</p>
            `;
            loadClients();
        } else {
            resultDiv.className = 'result error';
            resultDiv.innerHTML = `<strong>Error:</strong> ${data.detail || 'Failed to create client'}`;
        }
    } catch (error) {
        resultDiv.className = 'result error';
        resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
    }
});

// Check Rate Limit Form
document.getElementById('checkRateLimitForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const clientKey = document.getElementById('checkClientKey').value;
    const endpoint = document.getElementById('endpoint').value;
    
    const resultDiv = document.getElementById('checkResult');
    
    try {
        const response = await fetch(`${API_BASE}/rate-limit/check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_key: clientKey,
                endpoint: endpoint
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.allowed) {
                resultDiv.className = 'result success';
                resultDiv.innerHTML = `
                    <strong>✅ Request Allowed</strong>
                    <p>Remaining tokens: ${data.remaining_tokens}</p>
                    <p>Limit: ${data.limit}</p>
                `;
            } else {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <strong>❌ Rate Limit Exceeded</strong>
                    <p>Retry after: ${data.retry_after_seconds} seconds</p>
                    <p>Remaining tokens: ${data.remaining_tokens}</p>
                `;
            }
        } else {
            resultDiv.className = 'result error';
            resultDiv.innerHTML = `<strong>Error:</strong> ${data.detail || 'Client not found'}`;
        }
    } catch (error) {
        resultDiv.className = 'result error';
        resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
    }
    
    loadLogs();
    loadStats();
});

// Load Clients
async function loadClients() {
    const container = document.getElementById('clientsList');
    container.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/clients/`);
        const clients = await response.json();
        
        if (clients.length === 0) {
            container.innerHTML = '<p>No clients found. Create one above!</p>';
            return;
        }
        
        container.innerHTML = clients.map(client => `
            <div class="client-item">
                <h4>${client.client_key}</h4>
                <p>Capacity: ${client.capacity} | Refill: ${client.refill_rate_per_second}/sec</p>
                <p>Current Tokens: ${client.current_tokens}</p>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Error loading clients: ${error.message}</p>`;
    }
}

// Load Logs
async function loadLogs() {
    const container = document.getElementById('logsList');
    const clientKey = document.getElementById('logClientKey').value;
    
    container.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const url = clientKey 
            ? `${API_BASE}/logs/?client_key=${clientKey}`
            : `${API_BASE}/logs/`;
        
        const response = await fetch(url);
        const logs = await response.json();
        
        if (logs.length === 0) {
            container.innerHTML = '<p>No logs found.</p>';
            return;
        }
        
        container.innerHTML = logs.slice(0, 10).map(log => `
            <div class="log-item">
                <h4>${log.client_key} → ${log.endpoint}</h4>
                <p>Status: ${log.allowed ? '✅ Allowed' : '❌ Denied'}</p>
                <p>Tokens: ${log.remaining_tokens} | ${log.timestamp}</p>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Error loading logs: ${error.message}</p>`;
    }
}

// Load Stats
async function loadStats() {
    const container = document.getElementById('statsContainer');
    
    try {
        const response = await fetch(`${API_BASE}/logs/stats`);
        const stats = await response.json();
        
        container.innerHTML = `
            <div class="stat-card">
                <h3>${stats.total_requests}</h3>
                <p>Total Requests</p>
            </div>
            <div class="stat-card">
                <h3>${stats.allowed_requests}</h3>
                <p>Allowed</p>
            </div>
            <div class="stat-card">
                <h3>${stats.denied_requests}</h3>
                <p>Denied</p>
            </div>
            <div class="stat-card">
                <h3>${stats.allow_rate}</h3>
                <p>Allow Rate</p>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `<p class="error">Error loading stats: ${error.message}</p>`;
    }
}

// Event Listeners
document.getElementById('refreshClients').addEventListener('click', loadClients);
document.getElementById('refreshLogs').addEventListener('click', loadLogs);

// Initial Load
loadClients();
loadLogs();
loadStats();