import streamlit as st
import pandas as pd
import joblib
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Mission Control", page_icon="🚀", layout="wide")

# 2. HD BACKGROUND & CENTERED CHARCOAL BUTTON CSS
bg_img_url = "https://images.unsplash.com/photo-1517976487492-5750f3195933?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.95)), url("{bg_img_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
[data-testid="stSidebar"] {{ background-color: rgba(10, 10, 20, 0.85) !important; }}

/* Simple White Text */
h1, h2, h3, h4, h5, h6, p, span, label {{
    color: #ffffff !important;
    font-family: 'Arial', sans-serif;
}}

/* THE CENTERED SMALL CHARCOAL BUTTON */
div.stButton {{
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 20px;
}}

div.stButton > button {{
    background-color: #3a3a3a !important; 
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 6px !important;
    padding: 10px 35px !important;
    font-size: 16px !important;
    transition: 0.3s;
}}

div.stButton > button:hover {{
    background-color: #505050 !important;
    border-color: #ffffff !important;
}}

/* Clean input backgrounds */
.stNumberInput, .stSelectbox, .stSlider {{
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)


# 3. MODEL LOADER
@st.cache_resource
def load_model():
    base_path = os.path.dirname(__file__)
    root_path = os.path.abspath(os.path.join(base_path, ".."))
    files_in_root = os.listdir(root_path)
    target_file = None
    for f in files_in_root:
        if 'landing prediction' in f.lower() and f.endswith('.pkl'):
            target_file = f
            break
    if target_file:
        return joblib.load(os.path.join(root_path, target_file))
    return None


model = load_model()

# 4. MAIN INTERFACE
if model is not None:
    st.title("🚀 Rocket Landing Predictor")
    st.write("Fill in the details below to see if the landing will be successful.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("General Information")
        country = st.selectbox("Which country is launching?", ['USA', 'India', 'Russia', 'China', 'EU', 'SpaceX'])
        rocket = st.selectbox("Which rocket are you using?",
                              ['Starship', 'Falcon 9', 'GSLV Mk III', 'SLS', 'Long March 5'])
        planet = st.selectbox("Where are you landing?", ['Mars', 'Moon', 'Titan'])
        month = st.select_slider("Month of launch",
                                 options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
                                          'Dec'])

    with col2:
        st.subheader("Weather & Speed")
        payload = st.number_input("Weight of cargo (kg)", 500, 150000, 50000)
        rocket_velocity = st.number_input("Rocket speed (km/s)", 7.0, 15.0, 11.2)
        temp = st.slider("Outside Temperature (°C)", -20, 50, 25)
        humidity = st.slider("Air Humidity (%)", 10, 100, 50)
        rainfall = st.slider("Is it raining? (mm/h)", 0.0, 50.0, 0.0, step=0.1)

    st.markdown("---")

    # 5. PREDICTION BUTTON
    if st.button("Check Success Chance"):

        # --- SAFETY WARNINGS (SIMPLE LANGUAGE) ---
        if humidity >= 90:
            st.error("### 🛑 LAUNCH CANCELLED")
            st.warning(
                f"Warning: The air is too damp ({humidity}% humidity). High humidity can damage sensitive rocket electronics.")

        elif temp < 0:
            st.error("### 🛑 LAUNCH CANCELLED")
            st.warning(
                f"Warning: It is too cold ({temp}°C). Freezing temperatures can cause fuel leaks and engine failure.")

        elif rainfall > 0:
            st.error("### 🛑 LAUNCH CANCELLED")
            st.warning(
                f"Warning: Rain detected ({rainfall} mm/h). Rockets cannot launch in the rain due to lightning risks and wind safety.")

        # --- MACHINE LEARNING PREDICTION ---
        else:
            with st.spinner('Checking the math...'):
                input_df = pd.DataFrame({
                    'Country': [country], 'Rocket_Type': [rocket], 'Payload_kg': [payload],
                    'Velocity_km_s': [rocket_velocity], 'Launch_Angle': [45],
                    'Temp_C': [temp], 'Humidity': [humidity], 'Month': [month], 'Target_Planet': [planet]
                })

                prediction = model.predict(input_df)[0]
                prob = model.predict_proba(input_df)[0][1]

                if prediction == 1:
                    st.success(
                        f"### ✅ Rocket is good to go \nThe rocket has a **{prob:.2%}** chance of landing safely.")
                else:
                    st.error(f"### ❌ LANDING WILL LIKELY FAIL")
                    st.warning(
                        f"Reason: At a speed of {rocket_velocity} km/s, the rocket is moving too fast or too slow to land safely with this weight.")
else:
    st.error("🚨 Error: Could not find the brain file. Please check your folder.")