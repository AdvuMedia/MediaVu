import pandas as pd

# Load the dataset
data = pd.read_csv("data/media_data.csv")  # Relative path

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



