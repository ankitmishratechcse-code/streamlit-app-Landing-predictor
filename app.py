import streamlit as st

st.set_page_config(page_title="Interplanetary Mission Intelligence", page_icon="🌌", layout="wide")

# Space Background CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stSidebar"] { background-color: rgba(10, 10, 20, 0.85) !important; }
h1, h2, h3, h4, h5, h6, p, li, span { color: #ffffff !important; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🌌 Interplanetary Mission Intelligence System")
st.markdown("---")

st.write("""
### Welcome to the Command Center
This project uses a **Stacked Ensemble ML Pipeline** (Random Forest, XGBoost, and KNN) 
to predict the success and landing coordinates of deep-space missions.

**Use the Sidebar to navigate:**
1. **🚀 Mission Control:** Predict landing success based on flight physics.
2. **📊 Global Analytics:** Explore historical data and rocket specifications.
3. **🪐 Planetary Descent:** View 3D landing trajectory and pole predictions.
""")

# UPDATED FILENAME
st.info("💡 Note: Ensure 'satellite_landing prediction.pkl' is in the project root folder.")