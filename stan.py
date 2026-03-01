import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sunderland Population Dashboard",
    page_icon="🏙️",
    layout="wide",
)

# ── Sample Data ───────────────────────────────────────────────────────────────
# Historical population estimates (Sunderland Metropolitan Borough)
pop_history = pd.DataFrame({
    "Year": [1981, 1991, 2001, 2011, 2021, 2023],
    "Population": [296_900, 289_000, 280_807, 275_506, 272_536, 270_200],
})

# Population by ward (2021 estimates)
ward_data = pd.DataFrame({
    "Ward": [
        "St Peter's", "Hendon", "Millfield", "Pallion", "Southwick",
        "Castletown", "Redhill", "Barnes", "Ryhope", "Silksworth",
        "Washington East", "Washington West", "Copt Hill", "Houghton",
        "Hetton",
    ],
    "Population": [
        11_820, 10_950, 12_340, 11_100, 10_560,
         9_870, 10_200, 13_450, 12_100, 11_780,
        14_200, 13_800, 12_600, 15_300, 10_466,
    ],
    "Area": [
        "City", "City", "City", "City", "City",
        "City", "City", "City", "South", "South",
        "Washington", "Washington", "North", "North", "North",
    ],
})

# Age distribution (2021 census, approximate %)
age_data = pd.DataFrame({
    "Age Group": ["0–15", "16–29", "30–44", "45–59", "60–74", "75+"],
    "Percentage": [18.2, 17.5, 19.1, 20.4, 15.8, 9.0],
})

# Population density comparison with nearby cities (people / km²)
density_data = pd.DataFrame({
    "City": ["Sunderland", "Newcastle", "Gateshead", "Durham", "Middlesbrough"],
    "Density (per km²)": [460, 680, 520, 190, 1_050],
})

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏙️ Sunderland Population Dashboard")
st.markdown("**Exploring population trends, ward breakdowns, and demographics for Sunderland, UK.**")
st.divider()

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Current Population (est.)", "270,200", delta="-2,336 vs 2021")
k2.metric("Area (km²)", "137.5")
k3.metric("Population Density", "~460 / km²")
k4.metric("Largest Ward", "Houghton (15,300)")

st.divider()

# ── Row 1: Historical trend + Ward bar chart ──────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Historical Population Trend")
    fig_hist = px.line(
        pop_history, x="Year", y="Population",
        markers=True,
        labels={"Population": "Population"},
        color_discrete_sequence=["#636EFA"],
    )
    fig_hist.update_traces(line_width=3, marker_size=8)
    fig_hist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_tickformat=",",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("🗺️ Population by Ward")
    fig_ward = px.bar(
        ward_data.sort_values("Population", ascending=True),
        x="Population", y="Ward",
        orientation="h",
        color="Area",
        color_discrete_map={
            "City": "#636EFA",
            "South": "#EF553B",
            "Washington": "#00CC96",
            "North": "#AB63FA",
        },
        labels={"Population": "Population"},
    )
    fig_ward.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_tickformat=",",
        legend_title_text="Area",
    )
    st.plotly_chart(fig_ward, use_container_width=True)

# ── Row 2: Age distribution + Density comparison ──────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("👥 Age Distribution (2021 Census)")
    fig_age = px.pie(
        age_data, names="Age Group", values="Percentage",
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.Plasma_r,
    )
    fig_age.update_traces(textinfo="percent+label")
    fig_age.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col4:
    st.subheader("📊 Density vs Nearby Cities")
    fig_den = px.bar(
        density_data.sort_values("Density (per km²)", ascending=False),
        x="City", y="Density (per km²)",
        color="City",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text="Density (per km²)",
    )
    fig_den.update_traces(textposition="outside")
    fig_den.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        yaxis_tickformat=",",
    )
    # Highlight Sunderland bar
    colors = ["#EF553B" if c == "Sunderland" else "#636EFA" for c in density_data.sort_values("Density (per km²)", ascending=False)["City"]]
    fig_den.update_traces(marker_color=colors)
    st.plotly_chart(fig_den, use_container_width=True)

# ── Raw Data Expander ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📋 View Raw Data"):
    tab1, tab2, tab3, tab4 = st.tabs(["Historical", "Wards", "Age Groups", "Density"])
    with tab1:
        st.dataframe(pop_history, use_container_width=True)
    with tab2:
        st.dataframe(ward_data, use_container_width=True)
    with tab3:
        st.dataframe(age_data, use_container_width=True)
    with tab4:
        st.dataframe(density_data, use_container_width=True)

st.caption("Data source: Sample data based on ONS population estimates and 2021 UK Census.")
