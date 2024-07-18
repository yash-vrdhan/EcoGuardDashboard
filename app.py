from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Define the path to your dataset
dataset_path = os.path.join(os.path.dirname(__file__), 'GreenZoneData.csv')

# Load the dataset
df = pd.read_csv(dataset_path)
df['sampling_date'] = pd.to_datetime(df['sampling_date'], format='%d-%m-%Y')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualizations')
def visualizations():
    # Distribution of Air Quality Index
    fig1 = px.histogram(df, x='Air Quality Index', nbins=30, title='Distribution of Air Quality Index')

    # Levels of SO2, NO2, and RSPM across different states
    state_mean_levels = df.groupby('state')[['so2', 'no2', 'rspm']].mean().reset_index()
    print(state_mean_levels)  # Print processed data to verify aggregation
    fig2 = px.bar(state_mean_levels.melt(id_vars='state', var_name='Pollutant', value_name='Level'),
                  x='Level', y='state', color='Pollutant', barmode='group',
                  title='Levels of SO2, NO2, and RSPM across States')

    # Trend of Air Quality Index over time
    df['month_year'] = df['sampling_date'].dt.to_period('M').astype(str)
    trend_data = df.groupby('month_year')['Air Quality Index'].mean().reset_index()
    print(trend_data)  # Print processed data to verify time series aggregation
    fig3 = px.line(trend_data, x='month_year', y='Air Quality Index', title='Trend of Air Quality Index Over Time')

    # Proportion of Green Zones
    green_zones_proportion = df['Green Zones'].value_counts(normalize=True) * 100
    green_zones_proportion = green_zones_proportion.reset_index()
    green_zones_proportion.columns = ['Green Zone Indicator', 'Percentage']
    print(green_zones_proportion)  # Print processed data to verify green zones calculation
    fig4 = px.bar(green_zones_proportion, x='Green Zone Indicator', y='Percentage',
                  title='Proportion of Green Zones')

    # Convert plots to JSON
    plots = {
        'fig1': fig1.to_json(),
        'fig2': fig2.to_json(),
        'fig3': fig3.to_json(),
        'fig4': fig4.to_json()
    }

    return render_template('visualizations.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
