import streamlit as st
import pandas as pd
import altair as alt

# Load Data
st.set_page_config(page_title="MediaVu Dashboard", layout="wide")
st.title("📊 MediaVu Dashboard")
st.sidebar.header("Navigation")

# Load the data
try:
    data = pd.read_csv("data/media_data.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Error: Data file not found. Please upload a valid file in the Data tab.")

# Navigation Tabs
tab = st.sidebar.radio("Go to", ["Data Overview", "Visualization", "Budget Modeling", "Insights"])

# Tab 1: Data Overview
if tab == "Data Overview":
    st.header("Data Overview")
    st.write("Explore the raw data and apply filters for analysis.")
    
    # Date Range Filter
    date_range = st.date_input("Filter by Date Range", [])
    if date_range:
        data["Date"] = pd.to_datetime(data["Date"])
        filtered_data = data[
            (data["Date"] >= date_range[0]) & (data["Date"] <= date_range[1])
        ]
    else:
        filtered_data = data

    # Channel Filter
    selected_channels = st.multiselect("Filter by Channels", options=data["Channel"].unique(), default=data["Channel"].unique())
    filtered_data = filtered_data[filtered_data["Channel"].isin(selected_channels)]

    # Display filtered data
    st.write(filtered_data)

# Tab 2: Visualization
elif tab == "Visualization":
    st.header("Visualization")
    st.write("Interactive charts to analyze media performance.")
    
    # Total Spend by Channel
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="Channel:N",
        y="sum(Spend):Q",
        color="Channel:N",
        tooltip=["Channel", "sum(Spend):Q"]
    ).properties(title="Total Spend by Channel")
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Daily Spend Trend
    line_chart = alt.Chart(data).mark_line().encode(
        x="Date:T",
        y="Spend:Q",
        color="Channel:N"
    ).properties(title="Daily Spend Trend")
    st.altair_chart(line_chart, use_container_width=True)
    
    # Spend vs Conversions
    scatter_plot = alt.Chart(data).mark_circle(size=100).encode(
        x="Spend:Q",
        y="Conversions:Q",
        color="Channel:N",
        tooltip=["Channel", "Spend", "Conversions"]
    ).properties(title="Spend vs Conversions")
    st.altair_chart(scatter_plot, use_container_width=True)

# Tab 3: Budget Modeling
elif tab == "Budget Modeling":
    st.header("Budget Modeling")
    st.write("Allocate budgets and predict outcomes.")
    
    # User Input: Total Budget
    total_budget = st.slider("Total Budget", min_value=1000, max_value=100000, value=50000, step=1000)
    
    # Budget Allocation Recommendation
    st.write("### Budget Recommendations")
    metric_weights = data.groupby("Channel")["Conversions"].sum().to_dict()
    total_weight = sum(metric_weights.values())
    recommendations = {
        channel: (weight / total_weight) * total_budget for channel, weight in metric_weights.items()
    }
    for channel, budget in recommendations.items():
        st.write(f"{channel}: ${budget:,.2f}")

    # Sliders for Hypothetical Allocation
    st.write("### Adjust Hypothetical Allocations")
    sliders = {}
    for channel in data["Channel"].unique():
        sliders[channel] = st.slider(f"{channel} Budget", 0, int(total_budget), int(recommendations[channel]))
    
    # Display Updated Totals
    total_allocated = sum(sliders.values())
    st.write(f"Total Allocated Budget: ${total_allocated:,.2f}")

# Tab 4: Insights
elif tab == "Insights":
    st.header("Insights")
    st.write("Extract meaningful insights from the data.")
    
    # Top Performing Channels
    st.write("### Top Performing Channels")
    top_channels = data.groupby("Channel").sum().sort_values(by="Conversions", ascending=False).head(3)
    st.write(top_channels)

    # Conversion Rates
    st.write("### Conversion Rates")
    data["Conversion Rate"] = (data["Conversions"] / data["Clicks"]) * 100
    conversion_chart = alt.Chart(data).mark_bar().encode(
        x="Channel:N",
        y="Conversion Rate:Q",
        color="Channel:N",
        tooltip=["Channel", "Conversion Rate:Q"]
    ).properties(title="Conversion Rates by Channel")
    st.altair_chart(conversion_chart, use_container_width=True)
