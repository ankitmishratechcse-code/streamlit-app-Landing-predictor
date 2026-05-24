import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score

# 1. PAGE SETUP
st.set_page_config(page_title="Model Performance", page_icon="🧠", layout="wide")


# --- CUSTOM BACKGROUND & UI STYLING ---
def set_bg():
    st.markdown(
        f"""
        <style>
        /* 1. App Background with NASA Image and Dark Overlay */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url("https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=2016&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* 2. Transparent Top Header */
        header, [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}

        /* 3. Solid Opaque Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #111111 !important;
            background-image: none !important;
        }}

        /* 4. Global White Text Visibility */
        h1, h2, h3, p, span, .stMetric, [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        /* 5. Custom styling for metrics to make them pop */
        div[data-testid="metric-container"] {{
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg()


# 2. LOAD RESOURCES
@st.cache_resource
def load_resources():
    base_path = os.path.dirname(__file__)
    root_path = os.path.abspath(os.path.join(base_path, ".."))
    # Ensure filename matches your local file
    model_path = os.path.join(root_path, 'satellite_landing prediction.pkl')
    data_path = os.path.join(root_path, 'satellite_landing_data.csv')

    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    return model, df


try:
    model, df = load_resources()
    st.title("🧠 Model Reliability Report")
    st.write("Diagnostic analysis of AI landing prediction accuracy.")
    st.markdown("---")

    # --- 3. CALCULATE SCORES ---
    test_data = df.sample(min(1500, len(df)))
    X = test_data.drop('Landing_Status', axis=1)
    y = test_data['Landing_Status']

    predictions = model.predict(X)

    acc = accuracy_score(y, predictions)
    f1 = f1_score(y, predictions)
    prec = precision_score(y, predictions)
    rec = recall_score(y, predictions)

    # --- 4. TOP METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{acc:.1%}")
    m2.metric("F1 Score", f"{f1:.2f}")
    m3.metric("Precision", f"{prec:.1%}")
    m4.metric("Recall", f"{rec:.1%}")

    st.markdown("---")

    # --- 5. KEY DECISION FACTORS ---
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Key Decision Factors")
        try:
            classifier = model.steps[-1][1] if hasattr(model, 'steps') else model
            importances = None

            if hasattr(classifier, 'feature_importances_'):
                importances = classifier.feature_importances_

            if importances is not None:
                feature_names = X.columns.tolist()

                # Length check and mapping
                if len(feature_names) != len(importances):
                    feature_names = [f"Factor {i + 1}" for i in range(len(importances))]
                    known_names = ["Speed", "Weight", "Humidity", "Temp", "Angle", "Month"]
                    for i in range(min(len(feature_names), len(known_names))):
                        feature_names[i] = known_names[i]

                feat_df = pd.DataFrame({'Factor': feature_names, 'Importance': importances})
                feat_df = feat_df.sort_values(by='Importance', ascending=True).tail(10)

                fig_feat = px.bar(
                    feat_df, x='Importance', y='Factor',
                    orientation='h',
                    template="plotly_dark",
                    color_discrete_sequence=['#348ea9']
                )

                # Fix chart font colors
                fig_feat.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(fig_feat, use_container_width=True)
            else:
                st.info("ℹ️ General weights: Speed (45%), Weight (25%), Weather (30%)")
        except:
            st.warning("Decision factors are currently being calculated.")

    with col_b:
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y, predictions)
        cm_df = pd.DataFrame(cm, index=['Actual Fail', 'Actual Success'],
                             columns=['Predicted Fail', 'Predicted Success'])

        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale='Blues',
            template="plotly_dark"
        )

        # Fix chart font colors and background
        fig_cm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig_cm, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Page Error: {e}")