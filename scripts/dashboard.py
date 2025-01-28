import streamlit as st
import pandas as pd
import altair as alt

# Set up the page layout
st.set_page_config(page_title="MediaVu Dashboard", layout="wide")

st.title("📊 MediaVu Dashboard")

# Load and validate the dataset
try:
    data = pd.read_csv("data/media_data.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Error: Data file not found. Please upload a valid file.")
    st.stop()

# Validate required columns
required_columns = ["Date", "Channel", "Spend", "Impressions", "Clicks", "Conversions"]
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"Error: Missing required columns: {', '.join(missing_columns)}")
    st.stop()

# Convert 'Date' column to datetime format
try:
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    if data["Date"].isnull().any():
        st.error("Error: Invalid date format in the 'Date' column.")
        st.stop()
except Exception as e:
    st.error(f"Error while processing 'Date' column: {e}")
    st.stop()

# Sidebar Navigation
tab = st.sidebar.radio("Navigation", ["Data Overview", "Visualization", "Budget Modeling"])

# Tab 1: Data Overview
if tab == "Data Overview":
    st.header("Data Overview")
    st.write("Explore and filter the raw data.")

    # Date Range Filter
    min_date, max_date = data["Date"].min(), data["Date"].max()
    date_range = st.date_input("Filter by Date Range", [min_date, max_date])
    filtered_data = data[(data["Date"] >= date_range[0]) & (data["Date"] <= date_range[1])]

    # Channel Filter
    selected_channels = st.multiselect("Filter by Channels", options=data["Channel"].unique(), default=data["Channel"].unique())
    filtered_data = filtered_data[filtered_data["Channel"].isin(selected_channels)]

    st.write(filtered_data)

# Tab 2: Visualization
elif tab == "Visualization":
    st.header("Visualization")

    # Bar Chart: Total Spend by Channel
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="Channel:N",
        y="sum(Spend):Q",
        color="Channel:N",
        tooltip=["Channel", "sum(Spend):Q"]
    ).properties(title="Total Spend by Channel")
    st.altair_chart(bar_chart, use_container_width=True)

    # Line Chart: Spend Trend Over Time
    line_chart = alt.Chart(data).mark_line().encode(
        x="Date:T",
        y="Spend:Q",
        color="Channel:N"
    ).properties(title="Daily Spend Trend")
    st.altair_chart(line_chart, use_container_width=True)

# Tab 3: Budget Modeling
elif tab == "Budget Modeling":
    st.header("Budget Modeling")

    # Total Budget Slider
    total_budget = st.slider("Total Budget", min_value=1000, max_value=100000, value=50000, step=1000)

    # Budget Allocation Recommendation
    metric_weights = data.groupby("Channel")["Conversions"].sum().to_dict()
    total_weight = sum(metric_weights.values())
    recommendations = {
        channel: (weight / total_weight) * total_budget for channel, weight in metric_weights.items()
    }

    st.write("### Budget Allocation Recommendation")
    for channel, budget in recommendations.items():
        st.write(f"{channel}: ${budget:,.2f}")

    # Sliders for Hypothetical Allocation
    st.write("### Adjust Hypothetical Allocations")
    sliders = {}
    for channel in data["Channel"].unique():
        sliders[channel] = st.slider(f"{channel} Budget", 0, int(total_budget), int(recommendations[channel]))

    total_allocated = sum(sliders.values())
    st.write(f"Total Allocated Budget: ${total_allocated:,.2f}")
