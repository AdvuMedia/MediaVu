import streamlit as st
import pandas as pd

# Debugging message: Loading data
st.write("Loading data...")

# Load the dataset
try:
    # Ensure the CSV file path is relative to the repository
    data = pd.read_csv("data/media_data.csv")
    st.write("Data loaded successfully!")
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()  # Stop execution if the file is missing

# Display the raw data
st.subheader("Raw Data")
st.dataframe(data)

# Data preprocessing: Standardize the data
st.write("Processing data...")
try:
    # Extract marketing channel data and target variable
    channels = data[["CTR%", "Conversions", "FormFills"]]  # Numeric columns
    sales = data["Sales"]  # Dependent variable

    # Standardize the data
    channels_std = (channels - channels.mean()) / channels.std()
    sales_std = (sales - sales.mean()) / sales.std()

    # Display standardized data
    st.subheader("Standardized Channel Data")
    st.dataframe(channels_std)

    st.subheader("Standardized Sales Data")
    st.write(sales_std.head())
except KeyError as e:
    st.error(f"Column not found: {e}")
    st.stop()  # Stop execution if data processing fails

# Budget Recommendation Section
st.subheader("Budget Allocation Recommendation")

# Placeholder: Add logic for recommending budget allocation
def recommend_budget(channels_data, sales_data):
    """Simple placeholder function for budget allocation."""
    # Example logic: Equal allocation
    total_budget = 10000  # Example total budget
    allocation = {col: total_budget / len(channels_data.columns) for col in channels_data.columns}
    return allocation

try:
    budget_allocation = recommend_budget(channels, sales)
    st.write("Recommended Budget Allocation:")
    st.json(budget_allocation)
except Exception as e:
    st.error(f"Error generating budget recommendation: {e}")

# Footer
st.write("---")
st.caption("MediaVu Dashboard - Powered by Streamlit")

import streamlit as st
import pandas as pd

st.write("Initializing MediaVu...")  # Debug message at the start

try:
    st.write("Attempting to load data...")
    data = pd.read_csv("data/media_data.csv")
    st.write("Data loaded successfully!")
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# Display raw data
st.subheader("Raw Data")
st.dataframe(data)

# Check if required columns exist
st.write("Validating column names...")
required_columns = ["CTR%", "Conversions", "FormFills", "Sales"]
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# Standardize data
st.write("Standardizing data...")
try:
    channels = data[["CTR%", "Conversions", "FormFills"]]
    sales = data["Sales"]

    channels_std = (channels - channels.mean()) / channels.std()
    sales_std = (sales - sales.mean()) / sales.std()

    st.write("Data standardized successfully!")
except Exception as e:
    st.error(f"Error during data standardization: {e}")
    st.stop()

# Display standardized data
st.subheader("Standardized Channel Data")
st.dataframe(channels_std)

st.subheader("Standardized Sales Data")
st.dataframe(sales_std)

# Placeholder for budget recommendation
st.subheader("Budget Allocation Recommendation")
st.write("Calculating budget allocation...")
try:
    def recommend_budget(channels_data, sales_data):
        total_budget = 10000
        allocation = {col: total_budget / len(channels_data.columns) for col in channels_data.columns}
        return allocation

    budget_allocation = recommend_budget(channels_std, sales_std)
    st.json(budget_allocation)
except Exception as e:
    st.error(f"Error during budget allocation: {e}")
    st.stop()

st.write("---")
st.caption("MediaVu Dashboard - Powered by Streamlit")



