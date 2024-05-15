import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sps
from utils import read_sql_table

# Define the navigation structure
def exploration_page():
    #### Date & Variables ####
    # Reading in our datatable
    df = read_sql_table("gold_cpw")
    # Define available variables to choose from
    available_variables = ['spot_price_dkk', 'temp_mean_past1h', 'wind_speed_past1h', 'humidity_past1h', 'precip_past1h']

    #### Sidebar ####
    # Sidebar - User Input
    st.sidebar.header('Choose Input')
    
    # Allow user to select a variable to plot alongside 'consumption_kwh'
    selected_variable = st.sidebar.selectbox('Select Variable for Line Chart', available_variables)

    # Sidebar - Select variable for histogram and boxplot
    visualization_variable = st.sidebar.selectbox('Select Variable for Histogram & Boxplot',
        ['consumption_kwh', 'spot_price_dkk', 'temp_mean_past1h', 'wind_speed_past1h', 'humidity_past1h', 'precip_past1h'], index=0)
 
    #### Application ####
    # App title
    st.title('Energy Consumption')
    
    # Dataframe
    # Display a preview of the Dataframe
    st.write('### Dataframe')
    st.write(df.head(10))

    # Visualizations for selected histogram and boxplot variable
    # Histogram
    st.write(f'### Histogram of {visualization_variable}')
    histogram = alt.Chart(df).mark_bar().encode(
        alt.X(f"{visualization_variable}:Q", bin=True, title=f'{visualization_variable}'),
        alt.Y('count()', title='Frequency')
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(histogram, use_container_width=True)

    # Boxplot
    st.write(f'### Boxplot of {visualization_variable}')
    boxplot = alt.Chart(df).mark_boxplot(size=40).encode(
        x=alt.X(f"{visualization_variable}:Q",
                title=f'{visualization_variable}',
                axis=alt.Axis(labelAngle=-45))
    ).properties(
        width='container',
        height=300
    )
    st.altair_chart(boxplot, use_container_width=True)
 
    # Line Chart
    # Plotting a chart based on user selection using Altair
    df_selected = df[['hour_utc', 'consumption_kwh', selected_variable]].copy()
    base = alt.Chart(df_selected).encode(x='hour_utc:T')
    consumption_chart = base.mark_line(color='skyblue').encode(
        y=alt.Y('consumption_kwh:Q', title='Consumption (kWh)')
    )
    selected_variable_chart = base.mark_line(color='grey').encode(
        y=alt.Y(f"{selected_variable}:Q", title=selected_variable.capitalize())
    )
    chart = alt.layer(consumption_chart, selected_variable_chart).resolve_scale(
        y='independent'
    ).properties(
        width=800,
        height=500
    )
    st.altair_chart(chart, use_container_width=True)

    # Correlation matrix
    st.write('### Correlation Matrix')
    remaining_variables = available_variables.copy()
    corr_matrix = df[remaining_variables + ['consumption_kwh']].corr()
    corr_matrix = corr_matrix.stack().reset_index()
    corr_matrix.columns = ['variable1', 'variable2', 'value']
    heatmap = alt.Chart(corr_matrix).mark_rect().encode(
        x='variable1:N',
        y='variable2:N',
        color='value:Q',
        tooltip=['variable1', 'variable2', 'value']
    ).properties(
        width=500,
        height=400
    )
    text = heatmap.mark_text(baseline='middle').encode(
        text=alt.Text('value:Q', format=".2f"),
        color=alt.condition(
            "datum.value > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )
    st.altair_chart(heatmap + text, use_container_width=True)

def analysis_page():

    st.title('Data Analysis')
    st.write("This page is currently empty.")

# Sidebar for navigation

st.sidebar.title('Navigation')
page = st.sidebar.radio("Choose a page", ('Data Exploration', 'Data Analysis'))

# Display pages based on navigation choice
if page == 'Data Exploration':
    exploration_page()
elif page == 'Data Analysis':
    analysis_page()