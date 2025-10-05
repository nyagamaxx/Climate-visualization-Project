import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data_path = 'data/GlobalLandTemperaturesByCountry.csv'
df = pd.read_csv(data_path)

# Clean and prepare data
df['dt'] = pd.to_datetime(df['dt'])
df = df.rename(columns={'AverageTemperature': 'Temp'})
df = df.dropna(subset=['Temp'])

# Group global average by year
df['year'] = df['dt'].dt.year
global_trend = df.groupby('year')['Temp'].mean().reset_index()

# Plot global temperature trend
plt.figure(figsize=(10,5))
plt.plot(global_trend['year'], global_trend['Temp'], color='orange')
plt.title('Global Average Temperature Over Time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.savefig('global_temperature_trend.png', dpi=300)
plt.show()

# Plot specific country (example: Kenya)
country = 'Kenya'
country_data = df[df['Country'] == country].groupby('year')['Temp'].mean().reset_index()

plt.figure(figsize=(10,5))
plt.plot(country_data['year'], country_data['Temp'], color='green')
plt.title(f'Average Temperature Trend - {country}')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.savefig(f'{country.lower()}_temperature_trend.png', dpi=300)
plt.show()
