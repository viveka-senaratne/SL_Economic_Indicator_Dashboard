import streamlit as st
st.write("Hello Streamlit!")

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --------------------

# --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_economy_data.csv")
    return df[df["Country"] == "Sri Lanka"]

df = load_data()

# --------------------

# --------------------
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {
            background-image: url('https://www.transparenttextures.com/patterns/white-diamond.png');
            background-size: cover;
        }
        .info-box {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #ccc;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            font-size: 1.05rem;
            color: black;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------
# Title and Filters
# --------------------
st.title("📊 Sri Lanka Economic Indicator Dashboard📊")
st.markdown("Explore trends in GDP, inflation, exports, and more from the past two decades using interactive visuals.")

# Sidebar filters
st.sidebar.title(" Filter Options")
years = sorted(df["Year"].unique())
indicators = sorted(df["Indicator"].unique())

selected_years = st.sidebar.slider("Select Year Range", min_value=min(years), max_value=max(years), value=(2000, 2023))
selected_indicators = st.sidebar.multiselect("Select Indicators", indicators, default=[
    "GDP per capita growth (annual %)",
    "Inflation, consumer prices (annual %)",
    "Exports of goods and services (% of GDP)",
    "Gross capital formation (% of GDP)"
])

# Filter data
filtered_df = df[
    (df["Year"] >= selected_years[0]) &
    (df["Year"] <= selected_years[1]) &
    (df["Indicator"].isin(selected_indicators))
]

pivot_df = filtered_df.pivot_table(index="Year", columns="Indicator", values="Value").fillna(0)

# --------------------
# 📦 Key Insight Boxes
# --------------------
st.subheader("📌 Key Economic Insights")

avg_by_year = pivot_df.mean(axis=1)
best_year = avg_by_year.idxmax()
top_indicator = pivot_df.mean().idxmax()
overall_mean = pivot_df.values.mean()

col1, col2, col3 = st.columns(3)
col1.markdown(f'<div class="info-box">📅 Best Performing Year:<br><span>{best_year}</span></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="info-box">🏆 Most Influential Indicator:<br><span>{top_indicator}</span></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="info-box">📈 Overall Mean Value:<br><span>{overall_mean:.2f}</span></div>', unsafe_allow_html=True)

# --------------------
# Dynamic Charts
# --------------------
st.subheader("🔵 Line Chart: Indicator Trends Over Time")
line_chart = alt.Chart(filtered_df).mark_line(strokeWidth=3).encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Value:Q", title="Value"),
    color=alt.Color("Indicator:N", legend=alt.Legend(title="Indicator")),
    tooltip=["Year", "Indicator", "Value"]
).interactive().properties(width=700, height=400)
st.altair_chart(line_chart, use_container_width=True)

# --------------------
#  Stacked Bar Chart (Stacked for the selected indicators)
# --------------------
st.subheader("🔵 Stacked Bar Chart: Indicator Distribution by Year")
stacked_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Value:Q", stack="normalize", title="Proportion"),
    color=alt.Color("Indicator:N", legend=alt.Legend(title="Indicator")),
    tooltip=["Year", "Indicator", "Value"]
).properties(width=700, height=400)
st.altair_chart(stacked_chart, use_container_width=True)

# --------------------
# Scatter Plot with Detailed Tooltip
# --------------------
st.subheader("🔵 Scatter Plot: Indicator Values Across Time")
scatter_plot = alt.Chart(filtered_df).mark_circle(size=80, opacity=0.7).encode(
    x=alt.X("Year:O"),
    y=alt.Y("Value:Q"),
    color=alt.Color("Indicator:N"),
    tooltip=[
        "Year", "Indicator", "Value",
        alt.Tooltip("Value:Q", format=".2f"),
        alt.Tooltip("Value:Q", title="Percent Change", format=",.2%")  # Example to show percentage changes if applicable
    ]
).interactive().properties(width=700, height=400)
st.altair_chart(scatter_plot, use_container_width=True)

# --------------------
#  Heatmap: Correlation of Economic Indicators over Time
# --------------------
st.subheader("🔵 Heatmap: Correlation of Economic Indicators Over Time")
heatmap = alt.Chart(filtered_df).mark_rect().encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Indicator:N", title="Indicator"),
    color=alt.Color("Value:Q", scale=alt.Scale(scheme='viridis'), title="Value"),
    tooltip=["Year", "Indicator", "Value"]
).properties(width=700, height=400)
st.altair_chart(heatmap, use_container_width=True)

# --------------------
# 📋 Summary Table
# --------------------
st.subheader("📋 Indicator Summary Statistics")
summary = filtered_df.groupby("Indicator")["Value"].agg(['mean', 'min', 'max']).round(2)
st.dataframe(summary)
