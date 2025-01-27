import pandas as pd

# Load the dataset
data = pd.read_csv("/Volumes/Colin 2TB/media_mix_modeling/data/media_data.csv")

# Extract marketing channel data and target variable
channels = data[["CTR%", "Conversions", "FormFills"]]  # Use numeric columns
sales = data["Sales"]  # Dependent variable

# Standardize the data
channels = (channels - channels.mean()) / channels.std()
sales = (sales - sales.mean()) / sales.std()

# Display the cleaned and standardized data
print("Standardized Channels Data:")
print(channels.head())

print("\nStandardized Sales Data:")
print(sales.head())

import pandas as pd

# Load the dataset
data = pd.read_csv("/Volumes/Colin 2TB/media_mix_modeling/data/media_data.csv")

# Extract marketing channel data and target variable
channels = data[["CTR%", "Conversions", "FormFills"]]  # Use numeric columns
sales = data["Sales"]  # Dependent variable

# Standardize the data
channels = (channels - channels.mean()) / channels.std()
sales = (sales - sales.mean()) / sales.std()

# Print standardized data
print("Standardized Channels Data:")
print(channels.head())

print("\nStandardized Sales Data:")
print(sales.head())
import streamlit as st

# Display standardized data in the dashboard
st.write("Standardized Channels Data:", channels)
st.write("Standardized Sales Data:", sales)
# Calculate contribution percentages
contributions = (channels.sum() / channels.sum().sum()) * 100

# Display contributions
st.write("Channel Contributions (%):")
st.bar_chart(contributions)
# Add sliders for budget adjustments
ctr_increase = st.slider("Increase CTR% by (%)", min_value=0, max_value=50, value=10)
conversions_increase = st.slider("Increase Conversions by (%)", min_value=0, max_value=50, value=10)
formfills_increase = st.slider("Increase FormFills by (%)", min_value=0, max_value=50, value=10)

# Adjust channels based on slider values
adjusted_channels = channels.copy()
adjusted_channels["CTR%"] *= 1 + (ctr_increase / 100)
adjusted_channels["Conversions"] *= 1 + (conversions_increase / 100)
adjusted_channels["FormFills"] *= 1 + (formfills_increase / 100)

# Display adjusted data
st.write("Adjusted Channels Data:", adjusted_channels)
from scipy.optimize import minimize

# Define an objective function
def objective_function(budgets):
    # Simulate sales based on budgets
    simulated_sales = budgets[0] * contributions["CTR%"] + \
                      budgets[1] * contributions["Conversions"] + \
                      budgets[2] * contributions["FormFills"]
    return -simulated_sales  # Minimize the negative to maximize sales

# Initial budgets
initial_budgets = [1000, 1000, 1000]

# Optimize budgets
result = minimize(objective_function, initial_budgets, method='SLSQP')
optimized_budgets = result.x

# Display optimized budgets
st.write("Optimized Budget Allocation:")
st.json({"CTR% Budget": optimized_budgets[0],
         "Conversions Budget": optimized_budgets[1],
         "FormFills Budget": optimized_budgets[2]})
from sklearn.metrics import mean_squared_error

# Simulate predictions (for now, use actual sales)
predicted_sales = sales  # Replace with your model's predictions

# Calculate mean squared error
mse = mean_squared_error(sales, predicted_sales)
st.write(f"Model Mean Squared Error: {mse}")

from scipy.optimize import minimize

# Define an objective function
def objective_function(budgets):
    # Simulate sales based on budgets
    simulated_sales = budgets[0] * contributions["CTR%"] + \
                      budgets[1] * contributions["Conversions"] + \
                      budgets[2] * contributions["FormFills"]
    return -simulated_sales  # Minimize the negative to maximize sales

# Initial budgets
initial_budgets = [1000, 1000, 1000]

# Optimize budgets
result = minimize(objective_function, initial_budgets, method='SLSQP')
optimized_budgets = result.x

# Display optimized budgets
st.write("Optimized Budget Allocation:")
st.json({"CTR% Budget": optimized_budgets[0],
         "Conversions Budget": optimized_budgets[1],
         "FormFills Budget": optimized_budgets[2]})
# Load the dataset
data = pd.read_csv("data/media_data.csv")  # Use relative path

