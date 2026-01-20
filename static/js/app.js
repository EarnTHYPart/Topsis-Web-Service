// API Configuration
const API_BASE_URL = window.location.origin;

// Example datasets
const EXAMPLES = {
    project: {
        decision_matrix: [
            [8, 7, 6],
            [6, 8, 7],
            [7, 6, 8]
        ],
        weights: [0.3, 0.3, 0.4],
        impacts: ["benefit", "benefit", "benefit"],
        alternative_names: ["Project A", "Project B", "Project C"],
        criterion_names: ["Cost Efficiency", "Quality", "Speed"]
    },
    vendor: {
        decision_matrix: [
            [10, 8, 7, 5],
            [8, 9, 6, 8],
            [9, 7, 8, 6],
            [7, 6, 9, 7]
        ],
        weights: [0.25, 0.25, 0.25, 0.25],
        impacts: ["benefit", "benefit", "cost", "benefit"],
        alternative_names: ["Vendor A", "Vendor B", "Vendor C", "Vendor D"],
        criterion_names: ["Quality", "Reliability", "Price", "Support"]
    },
    car: {
        decision_matrix: [
            [8.5, 7.2, 45000, 8.0],
            [7.8, 8.5, 52000, 7.5],
            [9.2, 6.8, 38000, 8.8]
        ],
        weights: [0.3, 0.2, 0.3, 0.2],
        impacts: ["benefit", "benefit", "cost", "benefit"],
        alternative_names: ["Toyota Camry", "Honda Accord", "Mazda 6"],
        criterion_names: ["Performance", "Comfort", "Price", "Fuel Efficiency"]
    },
    realestate: {
        decision_matrix: [
            [5, 8, 400000, 20, 9],
            [8, 6, 350000, 15, 7],
            [6, 7, 380000, 25, 8],
            [7, 9, 420000, 18, 6]
        ],
        weights: [0.2, 0.2, 0.2, 0.2, 0.2],
        impacts: ["benefit", "benefit", "cost", "benefit", "benefit"],
        alternative_names: ["Property A", "Property B", "Property C", "Property D"],
        criterion_names: ["Location", "Amenities", "Price", "Space", "Safety"]
    }
};

// Tab switching
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Build matrix input table
function buildMatrix() {
    const numAlts = parseInt(document.getElementById('numAlternatives').value);
    const numCrit = parseInt(document.getElementById('numCriteria').value);

    if (numAlts < 2 || numCrit < 2) {
        alert('Please enter at least 2 alternatives and 2 criteria');
        return;
    }

    // Build matrix table
    let html = '<table class="matrix-table"><thead><tr><th>Alternative</th>';
    for (let j = 0; j < numCrit; j++) {
        html += `<th>Criterion ${j + 1}</th>`;
    }
    html += '</tr></thead><tbody>';

    for (let i = 0; i < numAlts; i++) {
        html += `<tr><td><input type="text" id="alt_${i}" value="Alternative ${i + 1}" class="form-input" style="width: 150px;"></td>`;
        for (let j = 0; j < numCrit; j++) {
            html += `<td><input type="number" step="0.01" id="matrix_${i}_${j}" value="0" required></td>`;
        }
        html += '</tr>';
    }
    html += '</tbody></table>';

    document.getElementById('matrixPreview').innerHTML = html;

    // Build criteria config
    html = '';
    for (let j = 0; j < numCrit; j++) {
        html += `
            <div class="criteria-row">
                <input type="text" id="crit_${j}" value="Criterion ${j + 1}" class="form-input" placeholder="Criterion name">
                <input type="number" step="0.01" id="weight_${j}" value="${(1 / numCrit).toFixed(2)}" class="form-input" placeholder="Weight" required>
                <select id="impact_${j}" class="form-select" required>
                    <option value="benefit">Benefit (↑)</option>
                    <option value="cost">Cost (↓)</option>
                </select>
                ${j > 0 ? '<button type="button" class="btn btn-danger" onclick="removeCriterion(' + j + ')">×</button>' : ''}
            </div>
        `;
    }

    document.getElementById('criteriaConfig').innerHTML = html;
}

// Load example
function loadExample(exampleName) {
    const example = EXAMPLES[exampleName];
    if (!example) return;

    // Set matrix dimensions
    document.getElementById('numAlternatives').value = example.decision_matrix.length;
    document.getElementById('numCriteria').value = example.decision_matrix[0].length;

    // Build matrix
    buildMatrix();

    // Fill in values
    example.decision_matrix.forEach((row, i) => {
        if (example.alternative_names && example.alternative_names[i]) {
            document.getElementById(`alt_${i}`).value = example.alternative_names[i];
        }
        row.forEach((val, j) => {
            document.getElementById(`matrix_${i}_${j}`).value = val;
        });
    });

    // Fill criteria config
    example.criterion_names.forEach((name, j) => {
        document.getElementById(`crit_${j}`).value = name;
        document.getElementById(`weight_${j}`).value = example.weights[j];
        document.getElementById(`impact_${j}`).value = example.impacts[j];
    });

    // Switch to manual tab
    switchTab('manual');
    document.querySelectorAll('.tab-button')[0].classList.add('active');

    showAlert('Example loaded successfully! Click "Evaluate with TOPSIS" to see results.', 'success');
}

// Reset form
function resetForm() {
    document.getElementById('topsisForm').reset();
    document.getElementById('results').innerHTML = '';
    document.getElementById('results').classList.add('hidden');
    buildMatrix();
}

// Form submission
document.getElementById('topsisForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const numAlts = parseInt(document.getElementById('numAlternatives').value);
    const numCrit = parseInt(document.getElementById('numCriteria').value);

    // Collect data
    const decision_matrix = [];
    const alternative_names = [];

    for (let i = 0; i < numAlts; i++) {
        const row = [];
        alternative_names.push(document.getElementById(`alt_${i}`).value);
        for (let j = 0; j < numCrit; j++) {
            row.push(parseFloat(document.getElementById(`matrix_${i}_${j}`).value));
        }
        decision_matrix.push(row);
    }

    const weights = [];
    const impacts = [];
    const criterion_names = [];

    for (let j = 0; j < numCrit; j++) {
        criterion_names.push(document.getElementById(`crit_${j}`).value);
        weights.push(parseFloat(document.getElementById(`weight_${j}`).value));
        impacts.push(document.getElementById(`impact_${j}`).value);
    }

    // Validate
    if (decision_matrix.some(row => row.some(val => isNaN(val)))) {
        showAlert('Please fill in all matrix values with valid numbers', 'error');
        return;
    }

    if (weights.some(w => isNaN(w) || w < 0)) {
        showAlert('Please enter valid positive weights', 'error');
        return;
    }

    const payload = {
        decision_matrix,
        weights,
        impacts,
        alternative_names,
        criterion_names
    };

    // Show loading
    showLoading();

    // Call API
    try {
        const response = await fetch(`${API_BASE_URL}/api/topsis/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.data);
        } else {
            showAlert(data.message || 'An error occurred', 'error');
            document.getElementById('results').classList.add('hidden');
        }
    } catch (error) {
        showAlert(`Network error: ${error.message}`, 'error');
        document.getElementById('results').classList.add('hidden');
    }
});

// Display results
function displayResults(data) {
    const resultsDiv = document.getElementById('results');

    let html = `
        <div class="results-container">
            <div class="results-header">
                <h3>📊 TOPSIS Results</h3>
            </div>
            
            <div class="summary-cards">
                <div class="summary-card">
                    <h4>Best Alternative</h4>
                    <p>${data.summary.best_alternative}</p>
                </div>
                <div class="summary-card">
                    <h4>Best Score</h4>
                    <p>${data.summary.best_score.toFixed(4)}</p>
                </div>
                <div class="summary-card">
                    <h4>Total Alternatives</h4>
                    <p>${data.summary.n_alternatives}</p>
                </div>
                <div class="summary-card">
                    <h4>Total Criteria</h4>
                    <p>${data.summary.n_criteria}</p>
                </div>
            </div>
            
            <div class="results-table">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Alternative</th>
                            <th>TOPSIS Score</th>
                            <th>Score Bar</th>
                        </tr>
                    </thead>
                    <tbody>
    `;

    data.results.forEach(result => {
        const rankClass = result.rank <= 3 ? `rank-${result.rank}` : 'rank-other';
        html += `
            <tr>
                <td><span class="rank-badge ${rankClass}">${result.rank}</span></td>
                <td><strong>${result.alternative}</strong></td>
                <td>${result.score.toFixed(6)}</td>
                <td>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${result.score * 100}%"></div>
                    </div>
                </td>
            </tr>
        `;
    });

    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;

    resultsDiv.innerHTML = html;
    resultsDiv.classList.remove('hidden');

    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show loading state
function showLoading() {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Calculating TOPSIS scores...</p>
        </div>
    `;
    resultsDiv.classList.remove('hidden');
}

// Show alert
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<strong>${type === 'error' ? '❌' : '✅'}</strong> ${message}`;

    const form = document.getElementById('topsisForm');
    form.insertBefore(alertDiv, form.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    buildMatrix();

    // Check API health
    fetch(`${API_BASE_URL}/api/topsis/health`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ TOPSIS API is running');
            }
        })
        .catch(error => {
            console.warn('⚠️ Could not connect to API:', error);
        });
});
