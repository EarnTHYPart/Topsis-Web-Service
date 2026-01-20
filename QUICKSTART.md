# Quick Start Guide

Get the TOPSIS Web Service running in 5 minutes!

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/topsis-web-service.git
cd topsis-web-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Run the Server

```bash
python run.py
```

You should see:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

## 3. Test the API

### Option A: Using curl

```bash
curl http://localhost:5000/api/topsis/health
```

### Option B: Using Python

```python
import requests

response = requests.get('http://localhost:5000/api/topsis/health')
print(response.json())
```

### Option C: Using your browser

Visit: `http://localhost:5000/`

## 4. Perform TOPSIS Evaluation

```bash
curl -X POST http://localhost:5000/api/topsis/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_matrix": [
      [8, 7, 6],
      [6, 8, 7],
      [7, 6, 8]
    ],
    "weights": [0.3, 0.3, 0.4],
    "impacts": ["benefit", "benefit", "benefit"],
    "alternative_names": ["Option A", "Option B", "Option C"]
  }'
```

## 5. Understand the Response

```json
{
  "success": true,
  "message": "TOPSIS evaluation completed successfully",
  "data": {
    "results": [
      {
        "alternative": "Option B",
        "score": 0.6234,
        "rank": 1
      },
      ...
    ],
    "summary": {
      "best_alternative": "Option B",
      "best_score": 0.6234
    }
  }
}
```

**What it means:**
- `score`: Similarity to ideal solution (0-1, higher is better)
- `rank`: Position (1 = best, 3 = worst)

## Common API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API Information |
| GET | `/api/topsis/health` | Health Check |
| GET | `/api/topsis/info` | TOPSIS Information |
| POST | `/api/topsis/evaluate` | Perform TOPSIS Analysis |

## Request Format

```json
{
  "decision_matrix": [
    [value1, value2, value3],
    [value1, value2, value3],
    ...
  ],
  "weights": [0.3, 0.3, 0.4],
  "impacts": ["benefit", "benefit", "cost"],
  "alternative_names": ["A", "B", "C"],
  "criterion_names": ["Price", "Quality", "Speed"]
}
```

**Notes:**
- `decision_matrix`: Your evaluation data (rows=alternatives, columns=criteria)
- `weights`: Importance of each criterion (will be auto-normalized)
- `impacts`: "benefit" for maximize, "cost" for minimize
- `alternative_names` & `criterion_names`: Optional labels

## Example Use Cases

### 1. Selecting Best Laptop

```bash
curl -X POST http://localhost:5000/api/topsis/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_matrix": [
      [16, 1200, 45000, 8],
      [8, 512, 30000, 10],
      [12, 1000, 40000, 7]
    ],
    "weights": [0.3, 0.2, 0.3, 0.2],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["MacBook Pro", "Budget Laptop", "Mid-Range"],
    "criterion_names": ["RAM (GB)", "Storage (GB)", "Price", "Performance"]
  }'
```

### 2. Vendor Selection

```bash
curl -X POST http://localhost:5000/api/topsis/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_matrix": [
      [9, 8, 100, 7],
      [8, 9, 120, 8],
      [7, 7, 80, 6]
    ],
    "weights": [0.3, 0.3, 0.2, 0.2],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["Vendor X", "Vendor Y", "Vendor Z"],
    "criterion_names": ["Quality", "Reliability", "Cost", "Support"]
  }'
```

## Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_topsis.py::TestTOPSIS::test_evaluate_basic -v
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
python -c "from run import app; app.run(port=5001)"
```

### Module Not Found Error
```bash
# Make sure you installed dependencies
pip install -r requirements.txt

# Verify Flask is installed
python -c "import flask; print(flask.__version__)"
```

### CORS Errors (Using from Different Domain)
The API has CORS enabled by default, so cross-origin requests should work.

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Explore Examples**: Check [tests/example_data.py](tests/example_data.py)
3. **Deploy**: See production deployment options in README
4. **Contribute**: Read [CONTRIBUTING.md](CONTRIBUTING.md)

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or feature requests

Happy TOPSIS Analysis! 🚀
