import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Global Analytics", page_icon="📊", layout="wide")


# --- CUSTOM NASA BACKGROUND ---
# --- UPDATED BACKGROUND LOGIC ---
def set_bg():
    st.markdown(
        f"""
        <style>
        /* 1. Apply background to the entire app */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                        url("https://svs.gsfc.nasa.gov/vis/a010000/a014800/a014866/NGC_1929_from_Spitzer_Chandra_ESO_desktop.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* 2. Make the Top Header Bar transparent */
        header, [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}

        /* 3. Force the Sidebar to stay solid (Opaque) */
        [data-testid="stSidebar"] {{
            background-color: #111111 !important; /* Dark solid color */
            background-image: none !important;
        }}

        /* 4. Fix text visibility for dark theme */
        h1, h2, h3, p, span, .stMetric {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg()


# 2. DATA LOADER
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    root_path = os.path.abspath(os.path.join(base_path, ".."))
    file_path = os.path.join(root_path, 'satellite_landing_data.csv')
    return pd.read_csv(file_path)


try:
    df = load_data()
    target_col = "Landing_Status"

    # --- 3. THE STICKY STATE FIX ---
    if 'sel_country' not in st.session_state:
        st.session_state['sel_country'] = "India"
    if 'sel_rocket' not in st.session_state:
        st.session_state['sel_rocket'] = "Starship"
    if 'sel_planet' not in st.session_state:
        st.session_state['sel_planet'] = "Mars"

    # --- 4. SIDEBAR WITH MANUAL SYNC ---
    st.sidebar.header("Mission Settings")

    countries = sorted(df['Country'].unique().tolist())
    rockets = sorted(df['Rocket_Type'].unique().tolist())
    planets = sorted(df['Target_Planet'].unique().tolist())

    c_idx = countries.index(st.session_state['sel_country'])
    r_idx = rockets.index(st.session_state['sel_rocket'])
    p_idx = planets.index(st.session_state['sel_planet'])

    new_country = st.sidebar.selectbox("Select Country", countries, index=c_idx)
    new_rocket = st.sidebar.selectbox("Select Rocket", rockets, index=r_idx)
    new_planet = st.sidebar.selectbox("Select Planet", planets, index=p_idx)

    st.session_state['sel_country'] = new_country
    st.session_state['sel_rocket'] = new_rocket
    st.session_state['sel_planet'] = new_planet

    # --- 5. UI CONTENT ---
    st.title("📊 Mission Data Analytics")
    st.write(f"Showing performance for: **{st.session_state['sel_rocket']}** to **{st.session_state['sel_planet']}**")
    st.markdown("---")

    filtered_df = df[(df['Target_Planet'] == st.session_state['sel_planet']) &
                     (df['Rocket_Type'] == st.session_state['sel_rocket'])]

    total_m = len(filtered_df)
    if total_m > 0:
        succ_rate = (filtered_df[target_col].sum() / total_m) * 100
        avg_v = filtered_df['Velocity_km_s'].mean()
    else:
        succ_rate, avg_v = 0, 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Missions", f"{total_m:,}")
    col2.metric("Success Rate", f"{succ_rate:.1f}%")
    col3.metric("Avg Speed", f"{avg_v:.2f} km/s")

    st.markdown("---")

    # Custom Chart for better visibility against the background
    st.subheader("Global Success vs Failure")
    fig_pie = px.pie(
        df,
        names=target_col,
        hole=0.4,
        color_discrete_sequence=['#ef553b', '#348ea9'],
        template="plotly_dark"  # Matches the dark theme perfectly
    )
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Error: {e}")