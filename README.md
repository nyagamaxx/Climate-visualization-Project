
# 🌍 Climate Change Data Visualization (Streamlit)

### Student Project by Maxwell Nyaga
Interactive Streamlit dashboard that visualizes global temperature trends using Matplotlib.

## How to use
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the dataset **GlobalLandTemperaturesByCountry.csv** from Kaggle:
   https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
   Place it in the `data/` folder OR upload it through the app sidebar.
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features
- Interactive country selection and year filtering
- Global average overlay
- Option to normalize to a zero baseline (relative change)
- Optional smoothing (rolling mean)
- Country comparison bar chart

## Files
- `app.py` - main Streamlit application
- `requirements.txt` - Python dependencies
- `data/` - folder where the dataset should be placed

## Author
Maxwell Nyaga
