# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("global_peace_index.csv")

years = [str(y) for y in range(2008, 2023)]

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Yearly Peace Index", "2008–2022 Change"])

# ---------------------------------------
# Page 1 - Yearly Peace Index
# ---------------------------------------
if page == "Yearly Peace Index":
    st.title("Global Peace Index - Yearly View")

    # Year selection
    year = st.selectbox("Select Year", years, index=len(years)-1)

    # Filter data
    df_year = df[["Country", "iso3c", year]].copy()
    df_year = df_year[df_year[year] != 0]  # remove 0 value entries

    # Choropleth Map
    fig_map = px.choropleth(
        df_year,
        locations="iso3c",
        color=year,
        hover_name="Country",
        color_continuous_scale="YlOrRd",
        projection="natural earth",
        title=f"Global Peace Index ({year})"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Top & Bottom 5
    df_sorted = df_year.sort_values(year)
    top5 = df_sorted.head(5)
    bottom5 = df_sorted.tail(5)

    df_bar = pd.concat([top5, bottom5])
    df_bar["Type"] = ["Most Peaceful"]*5 + ["Least Peaceful"]*5

    # Sort so that most peaceful appear first, least peaceful last
    df_bar = df_bar.sort_values(by=year, ascending=True)

    # Horizontal bar chart with dynamic axis label
    fig_bar = px.bar(
        df_bar,
        x=year,
        y="Country",
        orientation="h",
        color="Type",
        title=f"Top 5 Most Peaceful & 5 Least Peaceful Countries ({year})",
        color_discrete_map={
            "Most Peaceful": "green",
            "Least Peaceful": "red"
        },
        category_orders={"Country": df_bar["Country"].tolist()},
        labels={
            year: f"Peace Index Score for ({year})",
            "Country": "Country Name"
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------
# Page 2 - Change 2008 to 2022
# ---------------------------------------
else:
    st.title("Global Peace Index Change (2008–2022)")

    # Calculate change
    df_change = df[["Country", "iso3c", "2008", "2022"]].copy()
    df_change["Change"] = df_change["2022"] - df_change["2008"]

    # Improvement/Worsening label
    df_change["Status"] = df_change["Change"].apply(
        lambda x: "Improved" if x < 0 else "Worsened" if x > 0 else "No Change"
    )

    # Choropleth Map with custom hover data
    fig_change = px.choropleth(
        df_change,
        locations="iso3c",
        color="Change",
        hover_name="Country",
        hover_data={
            "2008": True,
            "2022": True,
            "Change": ":.3f",
            "Status": True,
            "iso3c": False  # hide ISO code from hover
        },
        color_continuous_scale="RdYlGn",
        projection="natural earth",
        range_color=(-0.5, 0.5),
        title="Change in Global Peace Index (2008 → 2022)"
    )
    st.plotly_chart(fig_change, use_container_width=True)

    # Time-series of global peace index
    df_ts = df[years].mean().reset_index()
    df_ts.columns = ["Year", "Global Peace Index"]

    fig_line = px.line(
        df_ts,
        x="Year",
        y="Global Peace Index",
        markers=True,
        title="Global Average Peace Index (2008–2022)",
        labels={
            "Year": "Year",
            "Global Peace Index": "Average Global Peace Index Score"
        }
    )
    st.plotly_chart(fig_line, use_container_width=True)

