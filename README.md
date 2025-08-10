# Global Peace Index Analysis

A Streamlit web application for exploring and visualizing Global Peace Index data.

## About

This project analyzes Global Peace Index (GPI) data from 2008-2022, providing interactive visualizations to explore peace rankings and trends across different countries and regions.

## Features

- Interactive data visualization using Streamlit
- Analysis of peace index trends over time
- Country and regional comparisons
- Data exploration of GPI scores and domains

## Data Sources

- Global Peace Index 2022 overall scores and domains (2008-2022)
- CSV data for detailed analysis

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1

# On Windows (Git Bash)
source .venv/Scripts/activate

# On Mac/Linux
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install streamlit pandas numpy matplotlib seaborn
```

## Usage

Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Files

- `streamlit_app.py` - Main Streamlit application
- `global_peace_index.csv` - GPI data in CSV format
- `GPI-2022-overall-scores-and-domains-2008-2022.xlsx` - Complete Excel dataset
- `requirements.txt` - Python package dependencies (if created)

## About the Global Peace Index

The Global Peace Index (GPI) is produced by the Institute for Economics and Peace (IEP). It measures the relative position of nations' and regions' peacefulness based on various indicators including ongoing conflict, safety and security, and militarization.

## Contributing

Feel free to fork this project and submit pull requests for improvements.

## License

This project is for educational and analysis purposes.