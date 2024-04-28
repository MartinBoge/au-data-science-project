import streamlit as st
import pandas as pd
import numpy as np

# App title
st.title('Energy Consumption')

# Sidebar
st.sidebar.header('User Input')

# Example: Slider for selecting a value
user_input = st.sidebar.slider('Select a value', 0, 100, 50)

# Example: Display a dataframe
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]
})
st.write('## Display DataFrame')
st.write(df)

# Example: Plotting a chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# Display raw code
st.code('print("Hello, Streamlit!")')

