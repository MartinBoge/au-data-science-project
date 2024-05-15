import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sps
from etl.utils import read_sql_table
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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
    
    # Load data
    df = read_sql_table("gold_cpw")
    
    # Convert data types
    df['spot_price_dkk'] = pd.to_numeric(df['spot_price_dkk'], errors='coerce')
    df['temp_mean_past1h'] = pd.to_numeric(df['temp_mean_past1h'], errors='coerce')
    df['wind_speed_past1h'] = pd.to_numeric(df['wind_speed_past1h'], errors='coerce')
    df['humidity_past1h'] = pd.to_numeric(df['humidity_past1h'], errors='coerce')
    df['precip_past1h'] = pd.to_numeric(df['precip_past1h'], errors='coerce')

    # Prepare data for models
    X = df[['spot_price_dkk', 'temp_mean_past1h', 'wind_speed_past1h', 'humidity_past1h', 'precip_past1h']]
    y = df['consumption_kwh']
    
    # Add a constant term for the intercept (required for linear regression)
    X = sm.add_constant(X)  

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Button to run models
    if st.button('Run Models'):
        # Linear Regression
        st.header('Linear Regression')
        model_lr = sm.OLS(y_train, X_train).fit()
        y_pred_lr = model_lr.predict(X_test)
        mse_lr = mean_squared_error(y_test, y_pred_lr)
        r2_lr = r2_score(y_test, y_pred_lr)
        st.write('### Linear Regression Model Summary')
        st.text(str(model_lr.summary()))
        st.write('### Linear Regression Prediction Accuracy')
        st.write(f'Mean Squared Error: {mse_lr:,.2f}')
        st.write(f'R-squared: {r2_lr:.2f}')
        
        # Random Forest Regression
        st.header('Random Forest Regression')
        rf_model = RandomForestRegressor(n_estimators=200, bootstrap=True, random_state=42)
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        r2_rf = r2_score(y_test, y_pred_rf)
        st.write('### Random Forest Model Performance')
        st.write(f'Mean Squared Error: {mse_rf:,.2f}')
        st.write(f'R-squared: {r2_rf:.2f}')

        # Feature Importance Plot (for Random Forest)
        st.write('### Feature Importance Plot (Random Forest)')
        feature_importances = pd.Series(rf_model.feature_importances_, index=X_train.columns)
        fig_rf, ax_rf = plt.subplots()
        feature_importances.nlargest(10).plot(kind='barh', ax=ax_rf)
        ax_rf.set_xlabel('Importance')
        ax_rf.set_title('Top 10 Feature Importances (Random Forest)')
        st.pyplot(fig_rf)
        
        # Support Vector Machine Regression
        st.header('Support Vector Machine Regression')
        svm_model = SVR(kernel='linear')
        svm_model.fit(X_train, y_train)
        y_pred_svm = svm_model.predict(X_test)
        mse_svm = mean_squared_error(y_test, y_pred_svm)
        r2_svm = r2_score(y_test, y_pred_svm)
        st.write('### SVM Model Performance')
        st.write(f'Mean Squared Error: {mse_svm:,.2f}')
        st.write(f'R-squared: {r2_svm:.2f}')

        # Visualization of SVM Predictions vs Actuals
        st.write('### Visualization of SVM Predictions vs Actuals')
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred_svm, alpha=0.3)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('SVM: Actual vs Predicted Values')
        st.pyplot(plt)

def analysis_page():

    # Dataframe
    # Display a preview of the Dataframe
    st.write('### Model Summary')
    st.write(df.head(10))

# Sidebar for navigation

st.sidebar.title('Navigation')
page = st.sidebar.radio("Choose a page", ('Data Exploration', 'Data Analysis'))

# Display pages based on navigation choice
if page == 'Data Exploration':
    exploration_page()
elif page == 'Data Analysis':
    analysis_page()