import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────── PAGE CONFIG ────────────────────────────
st.set_page_config(
    page_title="ChurnSight Pro",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── CUSTOM CSS ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ─── Global ─── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #07080f;
    color: #e2e8f0;
}
.stApp { background: #07080f; }
.block-container { padding: 1.5rem 2rem 3rem 2rem; }

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0f1923 100%);
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #38bdf8;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 1.4rem;
    margin-bottom: 0.3rem;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 4px;
}

/* ─── Sliders & selects ─── */
div[data-baseweb="slider"] > div { background: #1e293b !important; }
div[data-baseweb="slider"] [data-testid="stThumbValue"] { color: #38bdf8; font-weight: 700; }
.stSelectbox > div > div { background: #131c2e; border: 1px solid #1e293b; border-radius: 8px; color: #e2e8f0; }

/* ─── Metric cards ─── */
div[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; font-size: 2rem !important; font-weight: 700; }
div[data-testid="stMetricLabel"] { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ─── Tab strip ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #0d1117;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #1e293b;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    color: #64748b;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 8px 18px;
    letter-spacing: 0.04em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0f4c81 0%, #1d6fa4 100%) !important;
    color: #e0f2fe !important;
}

/* ─── Hero banner ─── */
.hero-banner {
    background: linear-gradient(135deg, #0f2744 0%, #0a1f3d 50%, #091428 100%);
    border: 1px solid #1e3a5f;
    border-radius: 18px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.07);
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    color: #7dd3fc;
    font-size: 0.9rem;
    margin-top: 4px;
    letter-spacing: 0.03em;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-right: 6px;
}
.badge-gnb { background: #0c2a4a; color: #38bdf8; border: 1px solid #1e4a70; }
.badge-live { background: #052e16; color: #4ade80; border: 1px solid #15803d; }

/* ─── Metric tiles ─── */
.metric-tile {
    background: linear-gradient(135deg, #0d1117 0%, #111827 100%);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    transition: border-color 0.3s;
}
.metric-tile:hover { border-color: #38bdf8; }
.metric-tile .value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #38bdf8;
}
.metric-tile .label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ─── Risk card ─── */
.risk-card {
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-bottom: 20px;
}
.risk-card.high { background: linear-gradient(135deg, #3b0a0a 0%, #450f0f 100%); border: 1px solid #7f1d1d; }
.risk-card.medium { background: linear-gradient(135deg, #2d1b00 0%, #3b2000 100%); border: 1px solid #78350f; }
.risk-card.low { background: linear-gradient(135deg, #052e16 0%, #04271a 100%); border: 1px solid #14532d; }
.risk-card .risk-pct { font-family: 'Space Grotesk', sans-serif; font-size: 3.5rem; font-weight: 900; line-height: 1; }
.risk-card.high .risk-pct { color: #f87171; }
.risk-card.medium .risk-pct { color: #fb923c; }
.risk-card.low .risk-pct { color: #4ade80; }
.risk-card .risk-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

/* ─── Section headers ─── */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.04em;
    border-left: 3px solid #38bdf8;
    padding-left: 10px;
    margin-bottom: 14px;
    margin-top: 8px;
}

/* ─── Insight box ─── */
.insight-box {
    background: #0d1117;
    border: 1px solid #1e293b;
    border-left: 4px solid #818cf8;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.83rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin-top: 12px;
}

/* ─── Feature pills ─── */
.feat-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 3px;
}
.feat-pill.high-risk { background: #3b0a0a; color: #f87171; border: 1px solid #7f1d1d; }
.feat-pill.medium-risk { background: #2d1b00; color: #fb923c; border: 1px solid #78350f; }
.feat-pill.low-risk { background: #052e16; color: #4ade80; border: 1px solid #14532d; }

/* ─── Divider ─── */
hr { border-color: #1e293b !important; margin: 1rem 0; }

/* ─── Plotly ─── */
.js-plotly-plot .plotly { border-radius: 12px; overflow: hidden; }

/* ─── Buttons ─── */
.stButton > button {
    background: linear-gradient(135deg, #0f4c81 0%, #1d6fa4 100%);
    color: #e0f2fe;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 10px 24px;
    letter-spacing: 0.04em;
    transition: opacity 0.2s;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85; }

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── LOAD DATA ──────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("Coustomer_credit.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv("BankChurners.csv")
    nb_cols = [c for c in df.columns if c.startswith("Naive_Bayes")]
    df = df.drop(columns=nb_cols)
    return df

model = load_model()
df    = load_data()

FEATURE_NAMES = model.feature_names_in_
CAT_COLS      = ["Gender", "Education_Level", "Marital_Status", "Income_Category", "Card_Category"]

def prepare_input(row: dict) -> pd.DataFrame:
    """Convert a single-row dict to a model-ready DataFrame."""
    tmp = pd.DataFrame([row])
    tmp = pd.get_dummies(tmp, columns=CAT_COLS, drop_first=False)
    tmp = tmp.reindex(columns=FEATURE_NAMES, fill_value=0)
    return tmp

def predict_churn(row: dict):
    X   = prepare_input(row)
    prob = model.predict_proba(X)[0][1]
    pred = int(prob >= 0.5)
    return prob, pred

def get_dataset_proba(df_in):
    nb_cols = [c for c in df_in.columns if c.startswith("Naive_Bayes")]
    drop    = ["CLIENTNUM", "Attrition_Flag"] + nb_cols
    X = df_in.drop(columns=[c for c in drop if c in df_in.columns])
    X = pd.get_dummies(X, columns=CAT_COLS, drop_first=False)
    X = X.reindex(columns=FEATURE_NAMES, fill_value=0)
    return model.predict_proba(X)[:, 1]

# ─────────────────────────── PLOTLY THEME ───────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    margin=dict(l=10, r=10, t=36, b=10),
)
GRID = dict(showgrid=True, gridcolor="#1e293b", zeroline=False)

# ─────────────────────────── SIDEBAR INPUTS ─────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 16px;'>
        <div style='font-family: Space Grotesk; font-size:1.4rem; font-weight:900;
                    background: linear-gradient(90deg,#38bdf8,#818cf8);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            💳 ChurnSight
        </div>
        <div style='font-size:0.7rem; color:#64748b; margin-top:2px;'>Credit Card Attrition Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👤 Demographics")
    age       = st.slider("Customer Age", 18, 80, 45)
    gender    = st.selectbox("Gender", ["M", "F"])
    dep_count = st.slider("Dependents", 0, 5, 2)
    edu       = st.selectbox("Education", ["Graduate","High School","Uneducated","Unknown","College","Post-Graduate","Doctorate"])
    marital   = st.selectbox("Marital Status", ["Married","Single","Divorced","Unknown"])
    income    = st.selectbox("Income Category", ["Less than $40K","$40K - $60K","$60K - $80K","$80K - $120K","$120K +","Unknown"])
    card      = st.selectbox("Card Type", ["Blue","Silver","Gold","Platinum"])

    st.markdown("### 💰 Account Details")
    months_book  = st.slider("Months on Book", 1, 60, 36)
    rel_count    = st.slider("Total Relationships", 1, 6, 3)
    credit_limit = st.slider("Credit Limit ($)", 1000, 35000, 10000, step=500)
    revolving    = st.slider("Revolving Balance ($)", 0, 3000, 1200, step=50)
    open_to_buy  = credit_limit - revolving

    st.markdown("### 📊 Activity Signals")
    months_inactive = st.slider("Months Inactive (12mo)", 0, 6, 2)
    contacts        = st.slider("Contacts Count (12mo)", 0, 6, 2)
    trans_amt       = st.slider("Total Trans Amount ($)", 500, 20000, 4500, step=100)
    trans_ct        = st.slider("Total Trans Count", 1, 140, 55)
    amt_chng        = st.slider("Amt Change Q4/Q1", 0.0, 3.5, 0.76, step=0.01)
    ct_chng         = st.slider("Count Change Q4/Q1", 0.0, 3.5, 0.71, step=0.01)
    util_ratio      = st.slider("Avg Utilization Ratio", 0.0, 1.0, 0.27, step=0.01)

    predict_btn = st.button("⚡ Run Prediction")

# ─────────────────────────── CURRENT ROW ────────────────────────────
current_row = dict(
    Customer_Age=age,
    Dependent_count=dep_count,
    Months_on_book=months_book,
    Total_Relationship_Count=rel_count,
    Months_Inactive_12_mon=months_inactive,
    Contacts_Count_12_mon=contacts,
    Credit_Limit=credit_limit,
    Total_Revolving_Bal=revolving,
    Avg_Open_To_Buy=open_to_buy,
    Total_Amt_Chng_Q4_Q1=amt_chng,
    Total_Trans_Amt=trans_amt,
    Total_Trans_Ct=trans_ct,
    Total_Ct_Chng_Q4_Q1=ct_chng,
    Avg_Utilization_Ratio=util_ratio,
    Gender=gender,
    Education_Level=edu,
    Marital_Status=marital,
    Income_Category=income,
    Card_Category=card,
)

prob, pred = predict_churn(current_row)
risk_pct   = f"{prob*100:.1f}%"
risk_level = "high" if prob >= 0.65 else ("medium" if prob >= 0.35 else "low")
risk_label = {"high":"⚠️ High Risk", "medium":"🔶 Medium Risk", "low":"✅ Low Risk"}[risk_level]

# ─────────────────────────── HERO BANNER ────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <div style="font-size:3rem">💳</div>
  <div>
    <p class="hero-title">ChurnSight Pro</p>
    <p class="hero-sub">Real-time Credit Card Attrition Intelligence · Gaussian Naïve Bayes Engine</p>
    <span class="badge badge-gnb">GNB Model</span>
    <span class="badge badge-live">● Live Prediction</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── TOP KPI ROW ────────────────────────────
dataset_proba = get_dataset_proba(df)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="metric-tile">
        <div class="value">{prob*100:.1f}%</div>
        <div class="label">Churn Probability</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="metric-tile">
        <div class="value" style="color:#818cf8">{len(df):,}</div>
        <div class="label">Total Customers</div>
    </div>""", unsafe_allow_html=True)
with k3:
    actual_churn = (df["Attrition_Flag"] == "Attrited Customer").mean()
    st.markdown(f"""<div class="metric-tile">
        <div class="value" style="color:#f87171">{actual_churn*100:.1f}%</div>
        <div class="label">Actual Attrition Rate</div>
    </div>""", unsafe_allow_html=True)
with k4:
    high_risk_n = (dataset_proba >= 0.65).sum()
    st.markdown(f"""<div class="metric-tile">
        <div class="value" style="color:#fb923c">{high_risk_n:,}</div>
        <div class="label">High-Risk Customers</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────── MAIN TABS ──────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯  Prediction Engine",
    "📊  Portfolio Analytics",
    "🔬  What-If Simulator",
    "🗂️  Data Explorer",
])

# ════════════════════════════════════════════════════════════════════
# TAB 1 – PREDICTION ENGINE
# ════════════════════════════════════════════════════════════════════
with tab1:
    col_pred, col_gauge = st.columns([1, 1], gap="large")

    with col_pred:
        st.markdown(f'<div class="risk-card {risk_level}">'
                    f'<div class="risk-pct">{risk_pct}</div>'
                    f'<div class="risk-label">Churn Probability</div>'
                    f'<div style="font-size:1.2rem; margin-top:8px; font-weight:700">{risk_label}</div>'
                    f'</div>', unsafe_allow_html=True)

        # Insight text
        if risk_level == "high":
            insight = (f"🚨 This customer shows multiple high-risk signals. "
                       f"With {months_inactive} inactive months, {contacts} service contacts, "
                       f"and a utilization ratio of {util_ratio:.2f}, immediate retention outreach is recommended.")
        elif risk_level == "medium":
            insight = (f"🔶 This customer is on the fence. Transaction activity and revolving balance "
                       f"suggest moderate engagement, but elevated contacts ({contacts}) and "
                       f"utilization ({util_ratio:.2f}) warrant proactive monitoring.")
        else:
            insight = (f"✅ This customer appears loyal. Strong transaction count ({trans_ct}), "
                       f"healthy balance management, and low inactivity signal long-term retention.")

        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

        # Feature risk contributions
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Key Risk Signals</div>', unsafe_allow_html=True)

        signals = {
            "Months Inactive": (months_inactive, 0, 6, True),
            "Contacts Count":  (contacts, 0, 6, True),
            "Utilization Ratio": (util_ratio, 0, 1, True),
            "Trans Count":     (trans_ct, 10, 140, False),
            "Trans Amount":    (trans_amt, 500, 20000, False),
            "Relationships":   (rel_count, 1, 6, False),
        }
        pills_html = ""
        for name, (val, lo, hi, higher_is_riskier) in signals.items():
            norm = (val - lo) / (hi - lo)
            risk_score = norm if higher_is_riskier else 1 - norm
            cls = "high-risk" if risk_score > 0.65 else ("medium-risk" if risk_score > 0.35 else "low-risk")
            pills_html += f'<span class="feat-pill {cls}">{name}: {val}</span>'
        st.markdown(pills_html, unsafe_allow_html=True)

    with col_gauge:
        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={"text": "Attrition Risk Score", "font": {"size": 14, "color": "#94a3b8"}},
            number={"suffix": "%", "font": {"size": 40, "family": "Space Grotesk", "color": "#e2e8f0"}},
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=1, tickcolor="#1e293b", tickfont=dict(color="#64748b")),
                bar=dict(color="#38bdf8", thickness=0.22),
                bgcolor="#0d1117",
                borderwidth=0,
                steps=[
                    dict(range=[0, 35],  color="#052e16"),
                    dict(range=[35, 65], color="#2d1b00"),
                    dict(range=[65, 100],color="#3b0a0a"),
                ],
                threshold=dict(line=dict(color="#f87171", width=3), thickness=0.85, value=65),
            )
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#94a3b8"),
            height=280,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Model confidence bar
        fig_conf = go.Figure()
        fig_conf.add_trace(go.Bar(
            x=["Existing Customer", "Attrited Customer"],
            y=[(1-prob)*100, prob*100],
            marker=dict(color=["#4ade80", "#f87171"], line=dict(width=0)),
            text=[f"{(1-prob)*100:.1f}%", f"{prob*100:.1f}%"],
            textposition="outside",
            textfont=dict(size=13, color="#e2e8f0", family="Space Grotesk"),
        ))
        fig_conf.update_layout(
            title=dict(text="Model Confidence", font=dict(size=13, color="#94a3b8")),
            height=220, **PLOTLY_BASE,
            yaxis=dict(range=[0, 115], showticklabels=False, showgrid=False, zeroline=False),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    # Feature importance approximation via log-likelihood deltas
    st.markdown('<div class="section-header">Feature Contribution Radar</div>', unsafe_allow_html=True)
    numeric_features = {k: v for k, v in current_row.items() if isinstance(v, (int, float))}
    radar_labels = list(numeric_features.keys())
    radar_values = []
    for feat, val in numeric_features.items():
        base_row = current_row.copy()
        p_base, _ = predict_churn(base_row)
        base_row[feat] = 0
        p_zero, _ = predict_churn(base_row)
        radar_values.append(abs(p_base - p_zero) * 100)

    fig_radar = go.Figure(go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_labels + [radar_labels[0]],
        fill="toself",
        fillcolor="rgba(56,189,248,0.1)",
        line=dict(color="#38bdf8", width=2),
        name="Impact",
    ))
    fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            gridcolor="#1e293b",
            color="#64748b",
            linecolor="#1e293b"
        ),
        angularaxis=dict(
            gridcolor="#1e293b",
            linecolor="#1e293b",
            color="#94a3b8"
        ),
        bgcolor="rgba(0,0,0,0)",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    height=360,
    margin=dict(l=40, r=40, t=40, b=40),
    showlegend=False,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 2 – PORTFOLIO ANALYTICS
# ════════════════════════════════════════════════════════════════════
with tab2:
    df2 = df.copy()
    df2["churn_prob"] = dataset_proba
    df2["risk_tier"]  = pd.cut(df2["churn_prob"],
                                bins=[0,.35,.65,1],
                                labels=["Low Risk","Medium Risk","High Risk"])
    df2["churned"] = (df2["Attrition_Flag"] == "Attrited Customer").astype(int)

    row1c1, row1c2 = st.columns(2, gap="large")

    with row1c1:
        st.markdown('<div class="section-header">Risk Distribution Across Portfolio</div>', unsafe_allow_html=True)
        risk_counts = df2["risk_tier"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            hole=0.6,
            marker=dict(colors=["#4ade80","#fb923c","#f87171"]),
            textinfo="percent+label",
            textfont=dict(size=12, color="#e2e8f0"),
        ))
        fig_donut.add_annotation(text=f"{len(df2):,}<br>Total", x=0.5, y=0.5,
                                  font=dict(size=16, color="#e2e8f0", family="Space Grotesk"),
                                  showarrow=False)
        fig_donut.update_layout(height=300, **PLOTLY_BASE, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with row1c2:
        st.markdown('<div class="section-header">Churn Probability Distribution</div>', unsafe_allow_html=True)
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df2[df2["churned"]==0]["churn_prob"],
            name="Existing", nbinsx=30,
            marker=dict(color="rgba(74,222,128,0.7)", line=dict(color="#4ade80",width=0.5)),
        ))
        fig_hist.add_trace(go.Histogram(
            x=df2[df2["churned"]==1]["churn_prob"],
            name="Attrited", nbinsx=30,
            marker=dict(color="rgba(248,113,113,0.7)", line=dict(color="#f87171",width=0.5)),
        ))
        fig_hist.update_layout(
            barmode="overlay", height=300, **PLOTLY_BASE,
            xaxis=dict(title="Churn Probability", **GRID),
            yaxis=dict(title="Count", **GRID),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    row2c1, row2c2 = st.columns(2, gap="large")

    with row2c1:
        st.markdown('<div class="section-header">Attrition by Income Category</div>', unsafe_allow_html=True)
        inc_grp = (df2.groupby("Income_Category")["churned"].agg(["mean","count"])
                     .reset_index().rename(columns={"mean":"churn_rate","count":"n"}))
        inc_grp = inc_grp.sort_values("churn_rate", ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=inc_grp["churn_rate"]*100,
            y=inc_grp["Income_Category"],
            orientation="h",
            marker=dict(
                color=inc_grp["churn_rate"],
                colorscale=[[0,"#052e16"],[0.5,"#92400e"],[1,"#7f1d1d"]],
                line=dict(width=0),
            ),
            text=[f"{v:.1f}%" for v in inc_grp["churn_rate"]*100],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=11),
        ))
        fig_bar.update_layout(height=300, **PLOTLY_BASE,
                               xaxis=dict(title="Churn Rate (%)", **GRID),
                               yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar, use_container_width=True)

    with row2c2:
        st.markdown('<div class="section-header">Attrition by Card Category</div>', unsafe_allow_html=True)
        card_grp = (df2.groupby("Card_Category")["churned"].agg(["mean","count"])
                      .reset_index().rename(columns={"mean":"churn_rate","count":"n"}))
        fig_bubble = go.Figure(go.Scatter(
            x=card_grp["n"],
            y=card_grp["churn_rate"]*100,
            mode="markers+text",
            text=card_grp["Card_Category"],
            textposition="top center",
            textfont=dict(color="#e2e8f0", size=11),
            marker=dict(
                size=card_grp["n"]/40,
                color=card_grp["churn_rate"],
                colorscale=[[0,"#1d4ed8"],[1,"#dc2626"]],
                showscale=False,
                line=dict(color="#1e293b", width=1),
            ),
        ))
        fig_bubble.update_layout(height=300, **PLOTLY_BASE,
                                  xaxis=dict(title="Customer Count", **GRID),
                                  yaxis=dict(title="Churn Rate (%)", **GRID))
        st.plotly_chart(fig_bubble, use_container_width=True)

    # Heatmap: inactivity vs contacts
    st.markdown('<div class="section-header">Risk Heatmap · Inactivity vs Contacts</div>', unsafe_allow_html=True)
    hm = (df2.groupby(["Months_Inactive_12_mon","Contacts_Count_12_mon"])["churned"]
            .mean().unstack(fill_value=0) * 100)
    fig_hm = go.Figure(go.Heatmap(
        z=hm.values,
        x=[str(c) for c in hm.columns],
        y=[str(r) for r in hm.index],
        colorscale=[[0,"#052e16"],[0.4,"#1a3a2a"],[0.7,"#78350f"],[1,"#7f1d1d"]],
        text=np.round(hm.values, 1),
        texttemplate="%{text}%",
        textfont=dict(size=11, color="#e2e8f0"),
        colorbar=dict(tickfont=dict(color="#94a3b8"), outlinewidth=0),
    ))
    fig_hm.update_layout(
        height=280, **PLOTLY_BASE,
        xaxis=dict(title="Contacts Count (12 mo)", side="bottom"),
        yaxis=dict(title="Months Inactive (12 mo)"),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 3 – WHAT-IF SIMULATOR
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Sensitivity Analysis — Single Feature vs Churn Probability</div>', unsafe_allow_html=True)

    sim_feature = st.selectbox("Select feature to vary", [
        "Months_Inactive_12_mon", "Contacts_Count_12_mon",
        "Total_Trans_Ct", "Total_Trans_Amt",
        "Credit_Limit", "Avg_Utilization_Ratio",
        "Total_Revolving_Bal", "Total_Relationship_Count",
        "Customer_Age", "Months_on_book",
    ])

    feat_ranges = {
        "Months_Inactive_12_mon":   (0, 6, 1),
        "Contacts_Count_12_mon":    (0, 6, 1),
        "Total_Trans_Ct":           (10, 140, 1),
        "Total_Trans_Amt":          (500, 20000, 200),
        "Credit_Limit":             (1000, 35000, 500),
        "Avg_Utilization_Ratio":    (0.0, 1.0, 0.02),
        "Total_Revolving_Bal":      (0, 3000, 50),
        "Total_Relationship_Count": (1, 6, 1),
        "Customer_Age":             (18, 80, 1),
        "Months_on_book":           (1, 56, 1),
    }
    lo, hi, step_size = feat_ranges[sim_feature]
    sim_vals = np.arange(lo, hi + step_size, step_size)

    sim_probs = []
    for v in sim_vals:
        r = current_row.copy()
        r[sim_feature] = float(v)
        p, _ = predict_churn(r)
        sim_probs.append(p * 100)

    current_feat_val = current_row.get(sim_feature, lo)
    current_feat_prob = prob * 100

    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(
        x=sim_vals, y=sim_probs,
        mode="lines",
        line=dict(color="#38bdf8", width=3),
        fill="tozeroy",
        fillcolor="rgba(56,189,248,0.07)",
        name="Churn Probability",
    ))
    fig_sim.add_hline(y=65, line=dict(color="#f87171", width=1.5, dash="dash"),
                      annotation_text="High Risk Threshold (65%)",
                      annotation_font=dict(color="#f87171", size=10),
                      annotation_position="top right")
    fig_sim.add_vline(x=current_feat_val, line=dict(color="#818cf8", width=2, dash="dot"),
                      annotation_text=f"Current: {current_feat_val}",
                      annotation_font=dict(color="#818cf8", size=10),
                      annotation_position="top right")
    fig_sim.add_trace(go.Scatter(
        x=[current_feat_val], y=[current_feat_prob],
        mode="markers",
        marker=dict(color="#818cf8", size=12, symbol="circle",
                    line=dict(color="#e2e8f0", width=2)),
        name="Current Value",
    ))
    fig_sim.update_layout(
        height=380, **PLOTLY_BASE,
        xaxis=dict(title=sim_feature.replace("_"," "), **GRID),
        yaxis=dict(title="Churn Probability (%)", range=[0,105], **GRID),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    # Multi-feature comparison
    st.markdown('<div class="section-header">Scenario Comparison — Multi-Feature Impact</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("**Scenario A — Optimistic**")
        sc_a_trans = st.slider("Transactions ↑", 10, 140, min(trans_ct + 20, 140), key="sc_a_t")
        sc_a_inact = st.slider("Inactivity ↓", 0, 6, max(months_inactive - 1, 0), key="sc_a_i")
        sc_a_cont  = st.slider("Contacts ↓", 0, 6, max(contacts - 1, 0), key="sc_a_c")
    with sc2:
        st.markdown("**Scenario B — Pessimistic**")
        sc_b_trans = st.slider("Transactions ↓", 10, 140, max(trans_ct - 20, 10), key="sc_b_t")
        sc_b_inact = st.slider("Inactivity ↑", 0, 6, min(months_inactive + 2, 6), key="sc_b_i")
        sc_b_cont  = st.slider("Contacts ↑", 0, 6, min(contacts + 2, 6), key="sc_b_c")

    row_a = current_row.copy()
    row_a.update({"Total_Trans_Ct": sc_a_trans, "Months_Inactive_12_mon": sc_a_inact, "Contacts_Count_12_mon": sc_a_cont})
    row_b = current_row.copy()
    row_b.update({"Total_Trans_Ct": sc_b_trans, "Months_Inactive_12_mon": sc_b_inact, "Contacts_Count_12_mon": sc_b_cont})

    prob_a, _ = predict_churn(row_a)
    prob_b, _ = predict_churn(row_b)

    colors = ["#818cf8", "#4ade80", "#f87171"]
    fig_sc = go.Figure(go.Bar(
        x=["Baseline", "Scenario A (Optimistic)", "Scenario B (Pessimistic)"],
        y=[prob*100, prob_a*100, prob_b*100],
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in [prob*100, prob_a*100, prob_b*100]],
        textposition="outside",
        textfont=dict(size=14, color="#e2e8f0", family="Space Grotesk"),
    ))
    fig_sc.update_layout(
        height=300, **PLOTLY_BASE,
        yaxis=dict(range=[0, 115], showticklabels=False, showgrid=False, zeroline=False),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 4 – DATA EXPLORER
# ════════════════════════════════════════════════════════════════════
with tab4:
    df4 = df.copy()
    df4["churn_prob"] = dataset_proba
    df4["churned"]    = (df4["Attrition_Flag"] == "Attrited Customer").astype(int)

    ex1, ex2 = st.columns(2, gap="large")

    with ex1:
        st.markdown('<div class="section-header">Transaction Count vs Amount</div>', unsafe_allow_html=True)
        sample = df4.sample(min(1500, len(df4)), random_state=42)
        fig_scatter = go.Figure(go.Scatter(
            x=sample["Total_Trans_Ct"],
            y=sample["Total_Trans_Amt"],
            mode="markers",
            marker=dict(
                color=sample["churn_prob"],
                colorscale=[[0,"#052e16"],[0.35,"#1d4ed8"],[0.65,"#78350f"],[1,"#7f1d1d"]],
                size=5,
                opacity=0.75,
                colorbar=dict(title="Churn Prob", tickfont=dict(color="#94a3b8"), outlinewidth=0),
            ),
        ))
        fig_scatter.update_layout(
            height=320, **PLOTLY_BASE,
            xaxis=dict(title="Transaction Count", **GRID),
            yaxis=dict(title="Transaction Amount ($)", **GRID),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with ex2:
        st.markdown('<div class="section-header">Age Distribution by Attrition</div>', unsafe_allow_html=True)
        fig_age = go.Figure()
        for flag, color, name in [
            ("Existing Customer", "#4ade80", "Existing"),
            ("Attrited Customer", "#f87171", "Attrited"),
        ]:
            fill = "rgba(74, 222, 128, 0.25)" if name == "Existing" else "rgba(248, 113, 113, 0.25)"
            
            fig_age.add_trace(go.Violin(
                y=df4[df4["Attrition_Flag"] == flag]["Customer_Age"],
                name=name,
                fillcolor=fill,
                line_color=color,
                meanline_visible=True,
                box_visible=True,
            ))
        fig_age.update_layout(
            height=320, **PLOTLY_BASE,
            yaxis=dict(title="Customer Age", **GRID),
            xaxis=dict(showgrid=False),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
            violingap=0.3,
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # Credit limit boxplots
    st.markdown('<div class="section-header">Credit Limit by Education Level</div>', unsafe_allow_html=True)
    edu_order = ["Uneducated","High School","College","Graduate","Post-Graduate","Doctorate","Unknown"]
    fig_box = go.Figure()
    cmap = ["#38bdf8","#818cf8","#4ade80","#fb923c","#f87171","#a78bfa","#64748b"]
    for i, edu_val in enumerate(edu_order):
        sub = df4[df4["Education_Level"]==edu_val]["Credit_Limit"]
        if len(sub) == 0:
            continue



        box_fill_colors = [
        "rgba(56, 189, 248, 0.20)",   # blue
        "rgba(129, 140, 248, 0.20)",  # indigo
        "rgba(74, 222, 128, 0.20)",   # green
        "rgba(251, 146, 60, 0.20)",   # orange
        "rgba(248, 113, 113, 0.20)",  # red
        "rgba(167, 139, 250, 0.20)",  # purple
        "rgba(100, 116, 139, 0.20)"   # slate
    ]

    fig_box.add_trace(go.Box(
        y=sub,
        name=edu_val,
        marker=dict(color=cmap[i % len(cmap)]),
        line=dict(color=cmap[i % len(cmap)]),
        fillcolor=box_fill_colors[i % len(box_fill_colors)],
        boxmean=True,
    ))



    fig_box.update_layout(
        height=320, **PLOTLY_BASE,
        yaxis=dict(title="Credit Limit ($)", **GRID),
        xaxis=dict(showgrid=False),
        showlegend=False,
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Raw data preview
    st.markdown('<div class="section-header">Raw Data Preview</div>', unsafe_allow_html=True)
    n_show = st.slider("Rows to display", 5, 100, 20)
    show_df = df4[["CLIENTNUM","Customer_Age","Gender","Income_Category","Card_Category",
                    "Credit_Limit","Total_Trans_Amt","Total_Trans_Ct","Attrition_Flag","churn_prob"]].head(n_show)
    show_df["churn_prob"] = show_df["churn_prob"].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(show_df, use_container_width=True, hide_index=True)

# ─────────────────────────── FOOTER ─────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.72rem; margin-top:3rem; padding-top:1rem;
            border-top: 1px solid #1e293b;">
    ChurnSight Pro · Gaussian Naïve Bayes · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)