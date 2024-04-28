import streamlit as st
import pandas as pd
import altair as alt
from utils import read_sql_table

#### Date & Variables ####
# Reading in our datatable
df = read_sql_table("gold_cpw")
# Define available variables to choose from
available_variables = ['spot_price_dkk', 'spot_price_eur', 'temp_mean_past1h', 'wind_speed_past1h']


#### Sidebar ####
# Sidebar - User Input
st.sidebar.header('Choose Input')

# Allow user to select a variable to plot alongside 'consumption_kwh'
selected_variable = st.sidebar.selectbox('Select Variable to Plot', available_variables)

#### Application ####
# App title
st.title('Energy Consumption')

# Dataframe
    # Display a preview of the Dataframe
st.write('### Dataframe')
st.write(df.head(10))

# Chart
    # Plotting a chart based on user selection using Altair
    # Create a DataFrame with 'hour_utc', 'consumption_kwh', and selected variable
df_selected = df[['hour_utc', 'consumption_kwh', selected_variable]].copy()

    # Configure Altair chart
base = alt.Chart(df_selected).encode(
    x='hour_utc:T'
)

    # Plot consumption_kwh on left y-axis
consumption_chart = base.mark_line(color='skyblue').encode(
    y=alt.Y('consumption_kwh:Q', title='Consumption (kWh)')
)

    # Plot selected variable on right y-axis
selected_variable_chart = base.mark_line(color='grey').encode(
    y=alt.Y(selected_variable + ':Q', title=selected_variable.capitalize())
)

    # Combine charts with dual y-axes
chart = alt.layer(consumption_chart, selected_variable_chart).resolve_scale(
    y='independent'
).properties(
    width=800,
    height=500
)

    # Display the chart using st.altair_chart()
st.write(f'### Energy Consumption Line Chart (Consumption & {selected_variable.capitalize()})')
st.altair_chart(chart, use_container_width=True)