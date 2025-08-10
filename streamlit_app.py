# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config for wide layout and custom styling
st.set_page_config(
    page_title="Global Peace Index Dashboard",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for funky styling
st.markdown("""
<style>
    /* Main background and theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Floating card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        margin: 10px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress bar container */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Country ranking cards */
    .ranking-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    
    .ranking-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Search box styling */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("global_peace_index.csv")

df = load_data()
years = [str(y) for y in range(2008, 2023)]

# Custom function for floating metric cards
def create_metric_card(value, label, color="#ffffff"):
    return f"""
    <div class="metric-card">
        <div class="metric-value" style="color: {color}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

# Custom function for country ranking display using Streamlit components
def display_rankings(df_ranked, year, rank_type="peaceful"):
    color = "#4CAF50" if rank_type == "peaceful" else "#f44336"
    emoji = "🕊️" if rank_type == "peaceful" else "⚠️"
    title = f"{emoji} {'Most' if rank_type == 'peaceful' else 'Least'} Peaceful Countries"
    
    # Create header
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin: 10px 0;">
        <h3 style="color: white; text-align: center; margin-bottom: 20px;">{title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each country with consistent layout
    for i, (_, row) in enumerate(df_ranked.iterrows(), 1):
        score = row[year] if year in row else row['Change']
        country = row['Country']
        
        # Create container with fixed height and consistent spacing
        with st.container():
            # Create three columns with specific width ratios
            col1, col2, col3 = st.columns([3, 4, 2])
            
            with col1:
                # Truncate long country names and add tooltip
                display_name = country if len(country) <= 25 else country[:22] + "..."
                st.markdown(f"**#{i}** {display_name}")
            
            with col2:
                # Create progress bar based on score
                if year == 'Change':
                    # For change values, use absolute value and normalize
                    abs_score = abs(score)
                    if rank_type == "peaceful":  # Improvements (negative changes)
                        progress_value = min(1.0, abs_score / 2.0)  # Scale to max expected change
                    else:  # Worsenings (positive changes)
                        progress_value = min(1.0, abs_score / 2.0)
                else:
                    # For peace index scores (typically 1-4 range)
                    if rank_type == "peaceful":
                        progress_value = max(0.1, min(1.0, (4 - score) / 3))  # Lower scores = higher progress
                    else:
                        progress_value = min(1.0, max(0.1, (score - 1) / 3))  # Higher scores = higher progress
                
                st.progress(progress_value)
            
            with col3:
                st.markdown(f"**{score:.3f}**")
            
            # Add consistent spacing between entries
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Sidebar for navigation with custom styling
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>🕊️ Navigation</h2>", unsafe_allow_html=True)
    page = st.radio("", ["Yearly Peace Index", "2008–2022 Change"], label_visibility="collapsed")
    
    # Add some stats in sidebar
    total_countries = len(df[df['2022'] != 0])
    most_peaceful = df[df['2022'] != 0].loc[df['2022'].idxmin(), 'Country']
    least_peaceful = df[df['2022'] != 0].loc[df['2022'].idxmax(), 'Country']
    
    st.markdown("---")
    st.markdown(f"**📊 Total Countries:** {total_countries}")
    st.markdown(f"**🏆 Most Peaceful (2022):** {most_peaceful}")
    st.markdown(f"**⚡ Least Peaceful (2022):** {least_peaceful}")

# ---------------------------------------
# Page 1 - Yearly Peace Index
# ---------------------------------------
if page == "Yearly Peace Index":
    st.markdown("<h1 class='main-title'>🕊️ Global Peace Index Dashboard</h1>", unsafe_allow_html=True)

    # Year selection with search functionality
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        year = st.selectbox("🗓️ Select Year", years, index=len(years)-1)

    # Filter data
    df_year = df[["Country", "iso3c", year]].copy()
    df_year = df_year[df_year[year] != 0]  # remove 0 value entries

    # Calculate statistics for floating cards
    avg_score = df_year[year].mean()
    most_peaceful_country = df_year.loc[df_year[year].idxmin(), 'Country']
    least_peaceful_country = df_year.loc[df_year[year].idxmax(), 'Country']
    most_peaceful_score = df_year[year].min()
    least_peaceful_score = df_year[year].max()

    # Floating metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card(f"{avg_score:.3f}", "Global Average", "#4CAF50"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card(f"{most_peaceful_score:.3f}", "Best Score", "#2196F3"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card(f"{least_peaceful_score:.3f}", "Worst Score", "#FF9800"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card(str(len(df_year)), "Countries", "#9C27B0"), unsafe_allow_html=True)

    # Search functionality with autocomplete
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        search_country = st.selectbox(
            "🔍 Search for a specific country:",
            [""] + sorted(df_year['Country'].tolist()),
            format_func=lambda x: "Select a country..." if x == "" else x
        )
    
    # Display searched country info
    if search_country:
        country_score = df_year[df_year['Country'] == search_country][year].iloc[0]
        country_rank = df_year.sort_values(year)['Country'].tolist().index(search_country) + 1
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #4CAF50, #2196F3); border-radius: 15px; padding: 20px; margin: 20px 0;">
            <h3 style="color: white; margin-bottom: 15px;">🔍 {search_country} Details</h3>
            <div style="display: flex; justify-content: space-around;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: white; font-weight: bold;">{country_score:.3f}</div>
                    <div style="color: rgba(255,255,255,0.8);">Peace Score</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: white; font-weight: bold;">#{country_rank}</div>
                    <div style="color: rgba(255,255,255,0.8);">Global Rank</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Choropleth Map with enhanced styling
    fig_map = px.choropleth(
        df_year,
        locations="iso3c",
        color=year,
        hover_name="Country",
        color_continuous_scale="Viridis",
        projection="natural earth",
        title=f"Global Peace Index Map ({year})"
    )
    fig_map.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        title_font_size=20
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Country rankings with slider and bar chart
    num_countries = st.slider(
        "📊 Number of countries to display in rankings", 
        min_value=3, 
        max_value=15, 
        value=5, 
        step=1
    )

    df_sorted = df_year.sort_values(year)
    top_n = df_sorted.head(num_countries)
    bottom_n = df_sorted.tail(num_countries)

    # Enhanced horizontal bar chart (moved above rankings)
    df_bar = pd.concat([top_n, bottom_n])
    df_bar["Type"] = ["Most Peaceful"]*num_countries + ["Least Peaceful"]*num_countries
    df_bar = df_bar.sort_values(by=year, ascending=True)

    fig_bar = px.bar(
        df_bar,
        x=year,
        y="Country",
        orientation="h",
        color="Type",
        title=f"Peace Index Rankings Comparison ({year})",
        color_discrete_map={
            "Most Peaceful": "#4CAF50",
            "Least Peaceful": "#f44336"
        },
        category_orders={"Country": df_bar["Country"].tolist()}
    )
    
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        title_font_size=18,
        height=max(400, num_countries * 35)  # Dynamic height based on number of countries
    )
    
    fig_bar.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                      "%{fullData.name}<br>" +
                      "Peace Index Score: %{x}<extra></extra>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Display rankings side by side with fixed width
    col1, col2 = st.columns(2)
    with col1:
        display_rankings(top_n, year, "peaceful")
    with col2:
        display_rankings(bottom_n[::-1], year, "conflict")

# ---------------------------------------
# Page 2 - Change 2008 to 2022
# ---------------------------------------
else:
    st.markdown("<h1 class='main-title'>📈 Peace Index Evolution (2008–2022)</h1>", unsafe_allow_html=True)

    # Calculate change
    df_change = df[["Country", "iso3c", "2008", "2022"]].copy()
    df_change = df_change[(df_change["2008"] != 0) & (df_change["2022"] != 0)]
    df_change["Change"] = df_change["2022"] - df_change["2008"]
    df_change["Status"] = df_change["Change"].apply(
        lambda x: "Improved" if x < 0 else "Worsened" if x > 0 else "No Change"
    )

    # Statistics for floating cards
    avg_change = df_change["Change"].mean()
    improved_count = len(df_change[df_change["Change"] < 0])
    worsened_count = len(df_change[df_change["Change"] > 0])
    biggest_improvement = df_change["Change"].min()
    biggest_decline = df_change["Change"].max()

    # Floating metric cards for change page
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card(f"{avg_change:+.3f}", "Avg Change", "#FF9800"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card(str(improved_count), "Improved", "#4CAF50"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card(str(worsened_count), "Worsened", "#f44336"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card(f"{biggest_improvement:.3f}", "Best Improvement", "#2196F3"), unsafe_allow_html=True)

    st.markdown("---")

    # Enhanced choropleth map for changes
    fig_change = px.choropleth(
        df_change,
        locations="iso3c",
        color="Change",
        hover_name="Country",
        hover_data={
            "2008": ":.3f",
            "2022": ":.3f",
            "Change": ":.3f",
            "Status": True,
            "iso3c": False
        },
        color_continuous_scale="RdYlGn_r",
        projection="natural earth",
        range_color=(-0.8, 0.8),
        title="Peace Index Change: Green = Improved, Red = Worsened"
    )
    fig_change.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        title_font_size=18
    )
    st.plotly_chart(fig_change, use_container_width=True)

    # Enhanced time series
    df_ts = df[years].mean().reset_index()
    df_ts.columns = ["Year", "Global Peace Index"]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_ts["Year"],
        y=df_ts["Global Peace Index"],
        mode='lines+markers',
        line=dict(color='#4CAF50', width=4),
        marker=dict(size=10, color='#2196F3'),
        hovertemplate="<b>%{x}</b><br>Global Average: %{y:.3f}<extra></extra>"
    ))
    
    fig_line.update_layout(
        title="Global Peace Trends Over Time",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        title_font_size=18,
        xaxis_title="Year",
        yaxis_title="Average Peace Index Score"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Top improvers and decliners
    st.markdown("### 🏆 Biggest Changes (2008-2022)")
    col1, col2 = st.columns(2)
    
    with col1:
        top_improvers = df_change.nsmallest(5, 'Change')
        display_rankings(top_improvers, 'Change', 'peaceful')
    
    with col2:
        top_decliners = df_change.nlargest(5, 'Change')
        display_rankings(top_decliners, 'Change', 'conflict')