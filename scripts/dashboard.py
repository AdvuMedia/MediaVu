import streamlit as st
import pandas as pd
import altair as alt

# App Configuration
st.set_page_config(
    page_title="MediaVu Dashboard",
    page_icon="📊",
    layout="wide",  # Utilize full screen width
)

# App Title
st.title("📊 MediaVu Dashboard")
st.caption("Modern Media Mix Modeling and Visualization Tool")

# Load Dataset
st.write("Loading data...")
try:
    data = pd.read_csv("data/media_data.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# Sidebar
st.sidebar.header("Dashboard Controls")
st.sidebar.write("Adjust parameters and filters here.")

# Budget Slider
total_budget = st.sidebar.slider(
    "Total Budget ($)", min_value=1000, max_value=50000, value=10000, step=1000
)

# Channel Filter
channel_filter = st.sidebar.multiselect(
    "Select Channels", options=data["channel"].unique(), default=data["channel"].unique()
)

# Filtered Data
filtered_data = data[data["channel"].isin(channel_filter)]

# Validate Columns
required_columns = ["CTR%", "Conversions", "FormFills", "Sales"]
missing_columns = [col for col in required_columns if col not in filtered_data.columns]
if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()

# Ensure CTR% is numeric before formatting
try:
    filtered_data["CTR%"] = pd.to_numeric(filtered_data["CTR%"], errors="coerce")
    filtered_data["CTR%"] = filtered_data["CTR%"].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "N/A")
except Exception as e:
    st.error(f"Error processing CTR% column: {e}")
    st.stop()

# Layout: Raw Data and Budget Allocation
st.subheader("💾 Data Overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Raw Data")
    st.dataframe(filtered_data, use_container_width=True)

with col2:
    st.write("### Budget Allocation Recommendation")

    # Budget Allocation Logic
    def recommend_budget(channels_data, total_budget):
        allocation = {
            col: round(total_budget / len(channels_data.columns), 2)
            for col in channels_data.columns
        }
        return allocation

    budget_allocation = recommend_budget(filtered_data[["Conversions", "FormFills"]], total_budget)

    # Format budget as a table
    allocation_df = pd.DataFrame({
        "Metric": budget_allocation.keys(),
        "Allocation ($)": [f"${v:,.2f}" for v in budget_allocation.values()]
    })
    st.table(allocation_df)

# Visualizations
st.subheader("📈 Visualizations")

# Channel Performance Chart
st.write("### Channel Performance by Metric")
performance_chart = (
    alt.Chart(filtered_data)
    .transform_fold(
        ["CTR%", "Conversions", "FormFills"],
        as_=["Metric", "Value"]
    )
    .mark_bar()
    .encode(
        x="Metric:N",
        y="Value:Q",
        color="Metric:N",
        column="channel:N",
        tooltip=["channel:N", "Metric:N", "Value:Q"]
    )
)
st.altair_chart(performance_chart, use_container_width=True)

# Budget Allocation Pie Chart
st.write("### Budget Allocation Distribution")
pie_chart = (
    alt.Chart(allocation_df)
    .mark_arc()
    .encode(
        theta=alt.Theta(field="Allocation ($)", type="quantitative"),
        color=alt.Color(field="Metric", type="nominal"),
        tooltip=["Metric", "Allocation ($)"],
    )
)
st.altair_chart(pie_chart, use_container_width=True)

# Footer
st.write("---")
st.caption("MediaVu Dashboard - Designed with Streamlit")
