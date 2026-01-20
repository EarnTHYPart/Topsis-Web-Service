// Helper function to show messages
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = 'message ' + type;
    setTimeout(() => {
        messageDiv.className = 'message';
    }, 5000);
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Parse weights from comma-separated string
function parseWeights(weightsStr) {
    return weightsStr.split(',').map(w => {
        const parsed = parseFloat(w.trim());
        return isNaN(parsed) ? null : parsed;
    });
}

// Parse impacts from comma-separated string
function parseImpacts(impactsStr) {
    return impactsStr.split(',').map(i => i.trim());
}

// Read CSV file
function readCSVFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const csv = e.target.result;
                const lines = csv.trim().split('\n');
                const data = lines.map(line =>
                    line.split(',').map(cell => {
                        const parsed = parseFloat(cell.trim());
                        return isNaN(parsed) ? cell.trim() : parsed;
                    })
                );
                resolve(data);
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = () => reject(new Error('Error reading file'));
        reader.readAsText(file);
    });
}

// Form submission handler
document.getElementById('topsisForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileName');
    const weightsInput = document.getElementById('weights').value.trim();
    const impactsInput = document.getElementById('impacts').value.trim();
    const emailInput = document.getElementById('emailId').value.trim();

    // Validation
    if (!fileInput.files.length) {
        showMessage('Please select a file', 'error');
        return;
    }

    if (!weightsInput) {
        showMessage('Please enter weights', 'error');
        return;
    }

    if (!impactsInput) {
        showMessage('Please enter impacts', 'error');
        return;
    }

    if (!emailInput) {
        showMessage('Please enter email address', 'error');
        return;
    }

    // Validate email format
    if (!isValidEmail(emailInput)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }

    // Parse weights and impacts
    const weights = parseWeights(weightsInput);
    const impacts = parseImpacts(impactsInput);

    // Check for parsing errors in weights
    if (weights.includes(null)) {
        showMessage('Invalid weights format. Please use numbers separated by commas', 'error');
        return;
    }

    // Check if impacts are valid
    const validImpacts = impacts.every(imp => imp === '+' || imp === '-' || imp === '+ve' || imp === '-ve');
    if (!validImpacts) {
        showMessage('Impacts must be either +, +ve, -, or -ve', 'error');
        return;
    }

    // Check if number of weights equals number of impacts
    if (weights.length !== impacts.length) {
        showMessage(`Number of weights (${weights.length}) must equal number of impacts (${impacts.length})`, 'error');
        return;
    }

    // Normalize impacts to 'benefit' and 'cost'
    const normalizedImpacts = impacts.map(imp => {
        if (imp === '+' || imp === '+ve') return 'benefit';
        if (imp === '-' || imp === '-ve') return 'cost';
    });

    // Read the file
    try {
        const data = await readCSVFile(fileInput.files[0]);

        if (data.length < 2) {
            showMessage('CSV file must contain at least 2 rows (alternatives)', 'error');
            return;
        }

        // Prepare decision matrix (all rows are alternatives with criteria as columns)
        const decision_matrix = data;
        const n_criteria = decision_matrix[0].length;

        // Validate matrix has same number of columns as impacts
        if (n_criteria !== impacts.length) {
            showMessage(`CSV has ${n_criteria} columns but ${impacts.length} impacts provided`, 'error');
            return;
        }

        // Prepare payload
        const payload = {
            decision_matrix,
            weights,
            impacts: normalizedImpacts,
            email: emailInput
        };

        // Send to API
        const response = await fetch('/api/topsis/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.success) {
            showMessage('TOPSIS analysis successful! Results will be sent to ' + emailInput, 'success');
            document.getElementById('topsisForm').reset();
        } else {
            showMessage(result.message || 'An error occurred', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
});
