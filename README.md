# TOPSIS MCDM Web Service

A comprehensive web service for Multi-Criteria Decision Making (MCDM) using the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method.

## Overview

TOPSIS is a well-known decision-making method that ranks alternatives based on their similarity to an ideal solution. This web service provides RESTful API endpoints to perform TOPSIS analysis on your decision problems.

### What is TOPSIS?

TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) is a multi-criteria decision making method that:
- Ranks alternatives based on distance from ideal best and ideal worst solutions
- Handles both benefit and cost criteria
- Provides normalized scores between 0 and 1 for easy comparison
- Supports weighted criteria for flexible decision-making

## Features

- ✅ RESTful API for TOPSIS evaluation
- ✅ Support for multiple alternatives and criteria
- ✅ Flexible criterion types (benefit/cost)
- ✅ Weighted criteria support
- ✅ CORS enabled for cross-origin requests
- ✅ Comprehensive error handling
- ✅ Full test suite included
- ✅ Example data and documentation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/topsis-web-service.git
cd topsis-web-service
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

#### Development Mode
```bash
python run.py
```

The API will be available at `http://localhost:5000`

#### Production Mode
```bash
set FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### API Endpoints

#### 1. Health Check
```
GET /api/topsis/health
```
Check if the API is running.

**Response:**
```json
{
  "success": true,
  "message": "TOPSIS API is running",
  "status": "healthy"
}
```

#### 2. API Information
```
GET /api/topsis/info
```
Get information about the TOPSIS method and available endpoints.

**Response:**
```json
{
  "success": true,
  "message": "Information about TOPSIS method",
  "data": {
    "name": "TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)",
    "description": "A multi-criteria decision-making method...",
    "methodology": [
      "1. Normalize the decision matrix",
      "2. Calculate weighted normalized matrix",
      ...
    ]
  }
}
```

#### 3. Evaluate (Main Endpoint)
```
POST /api/topsis/evaluate
```

Perform TOPSIS evaluation on your decision problem.

**Request Body:**
```json
{
  "decision_matrix": [
    [8, 7, 6],
    [6, 8, 7],
    [7, 6, 8]
  ],
  "weights": [0.3, 0.3, 0.4],
  "impacts": ["benefit", "benefit", "benefit"],
  "alternative_names": ["Project A", "Project B", "Project C"],
  "criterion_names": ["Cost Efficiency", "Quality", "Speed"]
}
```

**Parameters:**
- `decision_matrix` (required): 2D array of values (alternatives × criteria)
- `weights` (required): Array of criterion weights (will be normalized)
- `impacts` (required): Array of impact types: "benefit" or "cost"
- `alternative_names` (optional): Names for alternatives
- `criterion_names` (optional): Names for criteria

**Response:**
```json
{
  "success": true,
  "message": "TOPSIS evaluation completed successfully",
  "data": {
    "results": [
      {
        "alternative": "Project B",
        "index": 1,
        "score": 0.6234,
        "rank": 1
      },
      {
        "alternative": "Project A",
        "index": 0,
        "score": 0.5123,
        "rank": 2
      },
      {
        "alternative": "Project C",
        "index": 2,
        "score": 0.4891,
        "rank": 3
      }
    ],
    "summary": {
      "n_alternatives": 3,
      "n_criteria": 3,
      "best_alternative": "Project B",
      "best_score": 0.6234
    }
  }
}
```

## Examples

### Example 1: Project Selection

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
    "alternative_names": ["Project A", "Project B", "Project C"],
    "criterion_names": ["Cost Efficiency", "Quality", "Speed"]
  }'
```

### Example 2: Vendor Selection

```bash
curl -X POST http://localhost:5000/api/topsis/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_matrix": [
      [10, 8, 7, 5],
      [8, 9, 6, 8],
      [9, 7, 8, 6],
      [7, 6, 9, 7]
    ],
    "weights": [0.25, 0.25, 0.25, 0.25],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["Vendor A", "Vendor B", "Vendor C", "Vendor D"],
    "criterion_names": ["Quality", "Reliability", "Price", "Support"]
  }'
```

### Example 3: Python Script

```python
import requests
import json

url = "http://localhost:5000/api/topsis/evaluate"

data = {
    "decision_matrix": [
        [8.5, 7.2, 45000, 8.0],
        [7.8, 8.5, 52000, 7.5],
        [9.2, 6.8, 38000, 8.8]
    ],
    "weights": [0.3, 0.2, 0.3, 0.2],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["Toyota Camry", "Honda Accord", "Mazda 6"],
    "criterion_names": ["Performance", "Comfort", "Price", "Fuel Efficiency"]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

## TOPSIS Methodology

### Step 1: Normalize the Decision Matrix
Convert all criteria to a comparable scale using vector normalization.

### Step 2: Calculate Weighted Normalized Matrix
Apply weights to the normalized matrix to reflect criterion importance.

### Step 3: Determine Ideal Solutions
- **Ideal Best (Ideal Positive Solution)**: Maximum value for benefit criteria, minimum for cost
- **Ideal Worst (Ideal Negative Solution)**: Minimum value for benefit criteria, maximum for cost

### Step 4: Calculate Separation Distances
Calculate the distance of each alternative from ideal best and ideal worst solutions.

### Step 5: Calculate TOPSIS Scores
```
Score = Distance to Ideal Worst / (Distance to Ideal Best + Distance to Ideal Worst)
```

Score ranges from 0 to 1, where:
- 1 = Closest to ideal solution (best)
- 0 = Closest to worst solution

### Step 6: Rank Alternatives
Rank alternatives in descending order of TOPSIS scores.

## Project Structure

```
topsis-web-service/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Data models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── topsis_routes.py     # API routes
│   └── utils/
│       ├── __init__.py
│       └── topsis.py            # TOPSIS algorithm
├── config/
│   ├── __init__.py
│   └── config.py                # Configuration settings
├── tests/
│   ├── example_data.py          # Example datasets
│   ├── test_topsis.py           # Unit tests
│   └── __init__.py
├── run.py                        # Entry point
├── requirements.txt              # Dependencies
├── README.md                     # This file
└── .gitignore                    # Git ignore file
```

## Testing

### Run Unit Tests
```bash
python -m pytest tests/test_topsis.py -v
```

Or using unittest:
```bash
python -m unittest tests.test_topsis -v
```

### Test with Example Data
```python
from tests.example_data import EXAMPLE_1, EXAMPLE_2
from app.utils.topsis import TOPSIS
import numpy as np

topsis = TOPSIS()
scores, ranks = topsis.evaluate(
    np.array(EXAMPLE_1['decision_matrix']),
    np.array(EXAMPLE_1['weights']),
    EXAMPLE_1['impacts']
)

print("Scores:", scores)
print("Ranks:", ranks)
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Configuration Files

Configuration is defined in `config/config.py`:
- `DevelopmentConfig`: For development with debug mode
- `TestingConfig`: For running tests
- `ProductionConfig`: For production deployment

## Error Handling

The API returns appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "success": false,
  "message": "Missing required fields: decision_matrix, weights",
  "error": "Missing fields: decision_matrix, weights"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "message": "Endpoint not found",
  "error": "404 Not Found"
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "message": "An error occurred during evaluation",
  "error": "Error details here"
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

- Hwang, C. L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. Springer.
- Opricovic, S., & Tzeng, G. H. (2004). The TOPSIS with interval numbers for decision-making. Journal of Systems Science and Systems Engineering.

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

## Changelog

### Version 1.0.0 (Initial Release)
- Initial release of TOPSIS Web Service
- Basic TOPSIS algorithm implementation
- RESTful API with Flask
- Full test coverage
- Comprehensive documentation
