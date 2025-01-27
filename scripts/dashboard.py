import streamlit as st
import pandas as pd
import altair as alt

# Set up the app layout
st.set_page_config(
    page_title="MediaVu Dashboard",
    page_icon="📊",
    layout="wide",
)

# Navigation menu
menu = st.sidebar.radio(
    "Navigation", ["Data", "Visualization", "Transform", "Modeling", "Reporting"]
)

st.title("📊 MediaVu Dashboard")
st.caption("Modern Media Mix Modeling and Visualization Tool")

# Data tab
if menu == "Data":
    st.subheader("📄 Data Management")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File", type=["csv", "xlsx"]
    )

    if uploaded_file:
        try:
            # Load data
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            # Validate data
            required_columns = ["Date", "Channel", "Spend", "Impressions", "Clicks", "Conversions"]
            if all(col in data.columns for col in required_columns):
                st.success("File uploaded and validated successfully!")
                st.write("### Uploaded Data")
                st.dataframe(data)
            else:
                st.error(f"Missing required columns: {', '.join(required_columns)}")

        except Exception as e:
            st.error(f"Error reading file: {e}")

# Transform tab
elif menu == "Transform":
    st.subheader("🔄 Data Transformation")

    if "data" in locals():
        grouped_data = data.groupby(["Date", "Channel"]).agg(
            Spend=("Spend", "sum"),
            Impressions=("Impressions", "sum"),
            Clicks=("Clicks", "sum"),
            Conversions=("Conversions", "sum"),
        ).reset_index()

        # Add CTR and Conversion Rate
        grouped_data["CTR"] = grouped_data["Clicks"] / grouped_data["Impressions"]
        grouped_data["Conversion Rate"] = grouped_data["Conversions"] / grouped_data["Clicks"]

        st.write("### Transformed Data")
        st.dataframe(grouped_data)

    else:
        st.warning("Please upload data in the 'Data' tab first.")

# Visualization tab
elif menu == "Visualization":
    st.subheader("📊 Data Visualization")

    if "data" in locals():
        # Line Chart
        st.write("### Daily Spend by Channel")
        line_chart = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="Date:T",
                y="Spend:Q",
                color="Channel:N",
                tooltip=["Date", "Channel", "Spend"]
            )
        )
        st.altair_chart(line_chart, use_container_width=True)

        # Bar Chart
        st.write("### Total Metrics by Channel")
        bar_chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x="Channel:N",
                y=alt.Y("sum(Spend):Q", title="Total Spend"),
                color="Channel:N",
                tooltip=["Channel", "sum(Spend)"]
            )
        )
        st.altair_chart(bar_chart, use_container_width=True)

        # Scatter Plot
        st.write("### Spend vs. Conversions")
        scatter_plot = (
            alt.Chart(data)
            .mark_circle(size=100)
            .encode(
                x="Spend:Q",
                y="Conversions:Q",
                color="Channel:N",
                tooltip=["Spend", "Conversions", "Channel"]
            )
        )
        st.altair_chart(scatter_plot, use_container_width=True)

    else:
        st.warning("Please upload data in the 'Data' tab first.")
