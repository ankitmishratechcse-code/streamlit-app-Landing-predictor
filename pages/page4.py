import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Planetary Descent", page_icon="🪐", layout="wide")


# --- CUSTOM BACKGROUND LOGIC ---
def set_bg():
    st.markdown(
        f"""
        <style>
        /* 1. App Background with your starry image */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                        url("https://images.unsplash.com/photo-1457364887197-9150188c107b?q=80&w=1170&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* 2. Make Top Bar transparent */
        header, [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}

        /* 3. Keep Sidebar solid */
        [data-testid="stSidebar"] {{
            background-color: #111111 !important;
            background-image: none !important;
        }}

        /* 4. Ensure text visibility */
        h1, h2, h3, p, span, .stMetric, [data-testid="stMetricValue"] {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg()
# 2. SESSION STATE CONNECTION (Retrieving choices from Page 2)
# If the user hasn't visited Page 2, we set default values so it doesn't crash
if 'sel_planet' not in st.session_state:
    st.session_state['sel_planet'] = "Mars"
    st.session_state['sel_country'] = "India"
    st.session_state['sel_rocket'] = "Starship"

planet = st.session_state.sel_planet
country = st.session_state.sel_country
rocket = st.session_state.sel_rocket

# --- HEADER SECTION ---
st.title(f"🪐 Mission Destination: {planet}")
st.write(f"Telemetry Active for **{rocket}** | Launch Agency: **{country}**")
st.markdown("---")

# 3. TOP SECTION: 3D PLANET & LANDING RADAR
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"3D Interactive {planet} Surface")

    # NASA GLTF Embeds
    planet_urls = {
        "Mars": "https://solarsystem.nasa.gov/gltf_embed/2372",
        "Moon": "https://solarsystem.nasa.gov/gltf_embed/2366",
        "Titan": "https://solarsystem.nasa.gov/gltf_embed/2391"
    }
    url = planet_urls.get(planet, "https://solarsystem.nasa.gov/gltf_embed/2366")

    # Displaying the High-Quality NASA Model
    st.components.v1.iframe(url, height=550)
    st.write("🖱️ *Click and drag to rotate the planet; scroll to zoom into the topography.*")

with col2:
    st.subheader("📍 Mission Site Radar")

    # Landing Logic: India/SpaceX target South Pole, others North Pole
    pole_name = "South Pole" if country in ["India", "SpaceX"] else "North Pole"
    st.success(f"**Landing Target:** {planet} {pole_name}")
    st.write(
        f"The descent trajectory for {rocket} is locked onto the {pole_name} region for high-priority ice-sampling.")

    # --- EARTH SPACE CENTRE MAP ---
    spaceport_data = {
        "USA": {"name": "Kennedy Space Center, FL", "lat": 28.57, "lon": -80.64},
        "India": {"name": "Satish Dhawan Space Centre, SHAR", "lat": 13.72, "lon": 80.23},
        "Russia": {"name": "Baikonur Cosmodrome, KZ", "lat": 45.96, "lon": 63.30},
        "China": {"name": "Jiuquan Launch Center, CN", "lat": 40.96, "lon": 100.29},
        "EU": {"name": "Guiana Space Centre, FR", "lat": 5.23, "lon": -52.76},
        "SpaceX": {"name": "Starbase, Boca Chica, TX", "lat": 25.99, "lon": -97.15}
    }
    port = spaceport_data.get(country, spaceport_data["India"])

    st.write(f"**Tracking Signal:** {port['name']}")

    # Native Streamlit Map (Reliable)
    map_df = pd.DataFrame({'lat': [port['lat']], 'lon': [port['lon']]})
    st.map(map_df, zoom=2)

# --- 4. ROCKET ENCYCLOPEDIA (HISTORY, SPECS & IMAGES) ---
st.markdown("---")
st.header(f"🚀 Launch Vehicle: {rocket}")

# Detailed Rocket Database
rocket_db = {
    "Starship": {
        "img": "https://wallpapercave.com/wp/wp8215690.jpg?w=1000",
        "tagline": "The Gateway to Multi-Planetary Life",
        "history": """Developed by SpaceX in Boca Chica, Texas, Starship is the most powerful launch vehicle ever built. 
        It is a fully reusable transportation system designed to carry both crew and cargo to Earth orbit, the Moon, and Mars. 
        **Key Milestone:** Its successful Integrated Flight Tests (IFT) proved that methane-powered Raptor engines could successfully lift massive payloads beyond Earth's gravity.""",
        "stats": {"Height": "121m", "Thrust": "17M Lbs", "Capacity": "150t", "Reusable": "100%"},
        "engine_info": "Utilizes 33 Raptor engines on the Super Heavy booster and 6 Raptors on the Starship spacecraft, burning Methane and Liquid Oxygen."
    },
    "Falcon 9": {
        "img": "https://wallpapercave.com/wp/wp2376723.jpg?w=1000",
        "tagline": "The Reusable Workhorse of Modern Space",
        "history": """Falcon 9 is the first orbital-class rocket capable of reflight. First launched in 2010, it made history in 2015 by landing its first stage booster vertically. 
        **Key Milestone:** It has since become the most-flown rocket in the US, drastically reducing the cost of access to space by landing boosters on drone ships in the Atlantic.""",
        "stats": {"Height": "70m", "Diameter": "3.7m", "Reliability": "99%+", "Recovery": "Drone Ship"},
        "engine_info": "Powered by 9 Merlin 1D engines in the first stage and a single Merlin Vacuum engine in the second stage, burning kerosene (RP-1)."
    },
    "GSLV Mk III": {
        "img": "https://wallpapercave.com/wp/wp10474819.jpg?w=600",
        "tagline": "The Pride of ISRO: India's Heavy Lifter",
        "history": """The Geosynchronous Satellite Launch Vehicle Mark III (now LVM3) is the 'Fat Boy' of the Indian Space Research Organisation. 
        It was built to give India self-reliance in launching heavy communication satellites.
        **Key Milestone:** It gained global fame during the **Chandrayaan-3** mission in 2023, where it successfully launched the spacecraft that made India the first nation to land near the Lunar South Pole.""",
        "stats": {"Height": "43.4m", "Mass": "640t", "Stages": "3-Stage", "Payload": "8,000kg"},
        "engine_info": "Powered by two S200 solid rocket boosters, a L110 liquid core stage with Vikas engines, and a C25 cryogenic upper stage."
    },"SLS": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Soyuz_TMA-9_launch.jpg/500px-Soyuz_TMA-9_launch.jpg",
        "tagline": "NASA's Artemis Chariot: Returning to the Moon",
        "history": """The Space Launch System (SLS) is NASA's foundational rocket for deep space exploration. Built to be the successor to the Saturn V, it is the backbone of the Artemis program.
        **Major Milestone:** The 2022 Artemis I mission proved the SLS could send the Orion capsule around the Moon and back, clearing the way for human lunar return.""",
        "stats": {"Height": "98m", "Thrust": "8.8M Lbs", "Capacity": "95t", "Type": "Expendable"},
        "engine_info": "Powered by 4 RS-25 engines (derived from the Space Shuttle) and two 5-segment solid rocket boosters."
    },
    "Long March 5": {
        "img": "https://substackcdn.com/image/fetch/$s_!edpm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc86ea9a5-04e2-49cb-a8fe-b884e133ac3c_1440x759.jpeg",
        "tagline": "China's Heavy-Lift Gateway to Mars",
        "history": """The Long March 5 (Changzheng 5) is the heavy-lift workhorse of the Chinese Space Agency (CNSA). It is essential for China's most ambitious missions.
        **Major Milestone:** It successfully launched the Tianwen-1 Mars mission and the Chang'e-5 lunar sample return mission, establishing China as a major power in planetary exploration.""",
        "stats": {"Height": "57m", "Thrust": "2.4M Lbs", "Capacity": "25t", "Region": "Wenchang, CN"},
        "engine_info": "Utilizes a high-performance cryogenic core with YF-77 engines and four liquid-fueled boosters."
    }
}

# Fetch data or use fallback
info = rocket_db.get(rocket, rocket_db["Starship"])

# Big Hero Image
st.image(info['img'], caption=f"The {rocket} Launch Profile", use_container_width=True)

# Interactive Museum Tabs
tab1, tab2, tab3 = st.tabs(["📖 Historical Legacy", "⚙️ Technical Specifications", "🧬 Propulsion Physics"])

with tab1:
    st.subheader(f"The Story of {rocket}")
    st.markdown(f"**_{info['tagline']}_**")
    st.write(info['history'])
    st.info(f"📍 Vehicle Status: Confirmed for {st.session_state.sel_planet} atmospheric entry.")

with tab2:
    st.subheader("Vehicle Data Sheet")
    # Metric Columns for a High-Tech look
    cols = st.columns(len(info['stats']))
    for i, (label, val) in enumerate(info['stats'].items()):
        cols[i].metric(label, val)

    st.markdown("---")
    st.write("Current payload configuration is optimized for long-duration deep space stability.")

with tab3:
    st.subheader("Engine & Fuel Configuration")
    st.write(info['engine_info'])
    st.success("✅ Engine synchronization check: All systems nominal.")
    st.progress(100, text="Navigation Sync: Complete")