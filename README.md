# TOPSIS Web Service

A web-based implementation of the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) multi-criteria decision-making method using Streamlit.

## Features

- 📊 Upload CSV files with decision matrices
- ⚖️ Configure custom weights for each criterion
- ➕➖ Set positive or negative impacts for criteria
- 📈 Calculate TOPSIS scores and rankings
- 💾 Download results as CSV

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EarnTHYPart/Topsis-Web-Service.git
cd Topsis-Web-Service
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser at `http://localhost:8501`

3. Upload your CSV file:
   - First column: Item names/IDs
   - Remaining columns: Numeric criteria values

4. Enter weights (comma-separated): `1,1,1,1,1`

5. Enter impacts (comma-separated): `+,+,+,+,+`
   - `+` for benefit criteria (higher is better)
   - `-` for cost criteria (lower is better)

6. Click "Run TOPSIS" to calculate scores

7. Download the result CSV with scores and rankings

## CSV Format Example

```csv
Model,Price,Storage,Camera,Looks,Battery
M1,250,16,12,5,3000
M2,200,16,8,3,2500
M3,300,32,16,4,4000
M4,275,32,8,4,3500
M5,225,16,16,2,2800
```

## Requirements

- Python 3.8+
- streamlit
- pandas
- numpy

## License

MIT License

## Author

EarnTHYPart
