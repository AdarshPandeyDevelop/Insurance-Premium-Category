import streamlit as st
import pickle
import pandas as pd
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsureIQ · Premium Predictor",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(236,72,153,0.12) 0%, transparent 55%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    font-size: 0.72rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    line-height: 1.1;
    color: #f1f5f9;
    margin: 0 0 0.8rem;
    letter-spacing: -0.03em;
}
.hero h1 span {
    background: linear-gradient(135deg, #818cf8 0%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: #94a3b8;
    font-size: 1rem;
    font-weight: 300;
    max-width: 440px;
    margin: 0 auto 2.5rem;
    line-height: 1.65;
}

/* ── Card ── */
.card {
    background: rgba(15,15,25,0.8);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 0 1px rgba(255,255,255,0.03), 0 24px 48px -12px rgba(0,0,0,0.6);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Streamlit widgets override ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stSelectbox"] > div > div:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #cbd5e1 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Toggle / checkbox */
div[data-testid="stToggle"] label {
    color: #cbd5e1 !important;
    font-size: 0.875rem !important;
}

/* ── Predict Button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.9rem 2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: all 0.25s;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35);
    margin-top: 0.5rem;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.5);
    filter: brightness(1.08);
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* ── Result cards ── */
.result-wrap {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
}
.result-card {
    border-radius: 20px;
    padding: 2rem 2.5rem;
    text-align: center;
    width: 100%;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    padding: 1px;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}
.result-card.low {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.35);
}
.result-card.medium {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.35);
}
.result-card.high {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.35);
}
.result-icon {
    font-size: 2.8rem;
    margin-bottom: 0.6rem;
    display: block;
}
.result-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.result-label.low  { color: #6ee7b7; }
.result-label.medium { color: #fcd34d; }
.result-label.high { color: #fca5a5; }

.result-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.02em;
    text-transform: capitalize;
    line-height: 1;
}
.result-value.low  { color: #10b981; }
.result-value.medium { color: #f59e0b; }
.result-value.high { color: #ef4444; }

.result-desc {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.8rem;
    line-height: 1.55;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.2rem;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.75rem;
    text-align: center;
}
.stat-chip .val {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #e2e8f0;
}
.stat-chip .lbl {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 0.15rem;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Slider ── */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #6366f1, #a855f7) !important;
}

/* ── Metric override ── */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
div[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────


@st.cache_resource
def load_model():
    model_path = "model.pkl"
    if not os.path.exists(model_path):
        # try sibling path
        model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)


try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ── City Data ─────────────────────────────────────────────────────────────────
TIER_1 = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune"]
TIER_2 = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi",
    "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat",
    "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun",
    "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Prayagraj", "Udaipur", "SambhajiNagar", "Hubli", "Belgaum", "Salem",
    "Vijayawada", "Tiruchirapalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly",
    "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur", "Bilaspur",
    "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri",
]
ALL_CITIES = sorted(TIER_1 + TIER_2 + ["Kolkata", "Ahmedabad", "Other"])

OCCUPATIONS = [
    "Engineer", "Business", "Doctor", "Farmer", "Driver",
    "Teacher", "Private Job", "Student", "Government Job", "Freelancer",
]

# ── Helper Functions ──────────────────────────────────────────────────────────


def compute_bmi(weight, height):
    return weight / (height ** 2)


def compute_lifestyle_risk(smoker, bmi):
    if smoker and bmi > 30:
        return "high"
    elif smoker or bmi > 27:
        return "medium"
    else:
        return "medium"


def compute_age_group(age):
    if age < 25:
        return "young"
    elif age < 45:
        return "adult"
    elif age < 60:
        return "middle_aged"
    return "senior"


def compute_city_tier(city):
    if city in TIER_1:
        return 1
    elif city in TIER_2:
        return 2
    return 3


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


RESULT_META = {
    "low":    ("🟢", "Low Premium",    "Great news! Your profile suggests a low-risk category. You're likely eligible for affordable insurance plans."),
    "medium": ("🟡", "Medium Premium", "Your profile falls in the moderate-risk range. Standard insurance plans are well-suited for you."),
    "high":   ("🔴", "High Premium",   "Your profile indicates elevated risk factors. Comprehensive coverage options are recommended."),
}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI-Powered Prediction</div>
    <h1>Know Your <span>Insurance Premium</span> Category</h1>
    <p>Enter your details below and our ML model will instantly classify your insurance risk profile.</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error(
        f"⚠️ Could not load model.pkl — make sure it's in the same directory as this script.\n\n`{model_error}`")
    st.stop()

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">👤 Personal Details</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", min_value=1,
                          max_value=119, value=30, step=1)
with col2:
    income_lpa = st.number_input("Annual Income (LPA ₹)", min_value=0.1,
                                 max_value=500.0, value=10.0, step=0.5, format="%.1f")

col3, col4 = st.columns(2)
with col3:
    city = st.selectbox("City", ALL_CITIES, index=ALL_CITIES.index("Mumbai"))
with col4:
    occupation = st.selectbox("Occupation", OCCUPATIONS)

st.markdown('</div>', unsafe_allow_html=True)

# ── Health ──
st.markdown('<div class="card"><div class="card-title">🏥 Health & Lifestyle</div>',
            unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    weight = st.number_input("Weight (kg)", min_value=1.0,
                             max_value=300.0, value=70.0, step=0.5, format="%.1f")
with col6:
    height = st.number_input("Height (m)", min_value=0.5,
                             max_value=2.49, value=1.70, step=0.01, format="%.2f")

smoker = st.toggle("🚬 I am a smoker", value=False)

# Live BMI preview
bmi_val = compute_bmi(weight, height)
bmi_cat = bmi_category(bmi_val)
bmi_color = {"Underweight": "#60a5fa", "Normal": "#10b981",
             "Overweight": "#f59e0b", "Obese": "#ef4444"}[bmi_cat]
st.markdown(f"""
<div style="margin-top:0.8rem; padding:0.8rem 1rem; background:rgba(255,255,255,0.03);
     border:1px solid rgba(255,255,255,0.07); border-radius:10px; display:flex; align-items:center; gap:1rem;">
  <span style="font-size:1.5rem;">⚖️</span>
  <span style="color:#94a3b8; font-size:0.85rem;">Calculated BMI</span>
  <span style="font-family:'Syne',sans-serif; font-weight:700; font-size:1.2rem; color:{bmi_color}; margin-left:auto;">
    {bmi_val:.1f} &nbsp;<span style="font-size:0.75rem; font-weight:500; color:{bmi_color}; opacity:0.8;">({bmi_cat})</span>
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
st.markdown("")
predict_btn = st.button("🔮 Predict My Premium Category")

if predict_btn:
    # Derived fields
    bmi = compute_bmi(weight, height)
    age_group = compute_age_group(age)
    lifestyle = compute_lifestyle_risk(smoker, bmi)
    city_tier = compute_city_tier(city)

    input_df = pd.DataFrame([{
        "bmi":            bmi,
        "age_group":      age_group,
        "lifestyle_risk": lifestyle,
        "city_tier":      city_tier,
        "income_lpa":     income_lpa,
        "occupation":     occupation,
    }])

    with st.spinner("Analyzing your profile…"):
        prediction = model.predict(input_df)[0].lower()

    icon, title, desc = RESULT_META.get(
        prediction, ("ℹ️", prediction.title(), ""))

    st.markdown(f"""
    <div class="card" style="margin-top:1.5rem;">
      <div class="card-title">🎯 Prediction Result</div>
      <div class="result-card {prediction}">
        <span class="result-icon">{icon}</span>
        <div class="result-label {prediction}">Insurance Premium Category</div>
        <div class="result-value {prediction}">{prediction} risk</div>
        <div class="result-desc">{desc}</div>
      </div>

      <div class="stats-row" style="margin-top:1.4rem;">
        <div class="stat-chip">
          <div class="val">{bmi:.1f}</div>
          <div class="lbl">BMI · {bmi_category(bmi)}</div>
        </div>
        <div class="stat-chip">
          <div class="val">{age_group.replace('_', ' ').title()}</div>
          <div class="lbl">Age Group</div>
        </div>
        <div class="stat-chip">
          <div class="val">Tier {city_tier}</div>
          <div class="lbl">City Tier</div>
        </div>
        <div class="stat-chip">
          <div class="val">{lifestyle.title()}</div>
          <div class="lbl">Lifestyle Risk</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.75rem; margin-top:3rem; padding-bottom:2rem;">
  InsureIQ &nbsp;·&nbsp; Powered by Scikit-learn &amp; FastAPI &nbsp;·&nbsp; For educational purposes only
</div>
""", unsafe_allow_html=True)
