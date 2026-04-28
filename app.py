import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="House Haven | Estate Valuation",
    page_icon="🏠",
    layout="wide"
)

# -------------------- PREMIUM THEME CSS --------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* ── ROOT VARIABLES ── */
    :root {
        --cream:    #F4EFE6;
        --ink:      #1B1B1F;
        --ink-soft: #3A3A42;
        --gold:     #C9A84C;
        --gold-lt:  #E2C77A;
        --brick:    #9E5B3B;
        --sage:     #6B7F6E;
        --mist:     #E8E3DA;
        --white:    #FDFCFA;
    }

    /* ── GLOBAL ── */
    html, body, .stApp {
        background-color: var(--cream) !important;
        color: var(--ink) !important;
        font-family: 'DM Sans', sans-serif;
    }

    /* Remove Streamlit default top padding */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    /* ── HERO HEADER ── */
    .hero-wrap {
        position: relative;
        width: 100%;
        padding: 70px 60px 55px;
        overflow: hidden;
        background:
            radial-gradient(ellipse 80% 60% at 10% -10%, rgba(201,168,76,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 80% at 95% 110%, rgba(158,91,59,0.14) 0%, transparent 60%),
            linear-gradient(160deg, #1B1B1F 0%, #272730 60%, #1B1B1F 100%);
    }

    /* Grain overlay */
    .hero-wrap::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
        opacity: 0.45;
        pointer-events: none;
    }

    /* Decorative arc */
    .hero-wrap::after {
        content: '';
        position: absolute;
        right: -120px;
        top: -120px;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        border: 1px solid rgba(201,168,76,0.20);
        pointer-events: none;
    }

    .hero-inner {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .eyebrow {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.72rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 20px;
    }

    .hero-title {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 300;
        font-size: clamp(3rem, 6vw, 5.5rem);
        color: #FDFCFA;
        letter-spacing: -1px;
        line-height: 1;
        text-align: center;
        margin: 0 0 6px;
    }

    .hero-title em {
        font-style: italic;
        color: var(--gold-lt);
    }

    .hero-rule {
        width: 80px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        margin: 22px auto;
    }

    .hero-sub {
        font-family: 'DM Sans', sans-serif;
        font-weight: 300;
        font-size: 0.95rem;
        color: rgba(253,252,250,0.5);
        letter-spacing: 2px;
        text-align: center;
        text-transform: uppercase;
        font-size: 0.75rem;
    }

    /* ── BADGE STATS STRIP ── */
    .stats-strip {
        display: flex;
        justify-content: center;
        gap: 48px;
        padding: 28px 60px;
        background: var(--white);
        border-bottom: 1px solid var(--mist);
    }
    .stat-item {
        text-align: center;
    }
    .stat-num {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 600;
        color: var(--ink);
        line-height: 1;
    }
    .stat-label {
        font-size: 0.65rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--sage);
        margin-top: 4px;
        font-weight: 500;
    }
    .stat-sep {
        width: 1px;
        background: var(--mist);
        align-self: stretch;
    }

    /* ── MAIN CONTENT AREA ── */
    .main-area {
        padding: 48px 60px;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* ── SECTION HEADING ── */
    .section-heading {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 400;
        color: var(--ink);
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--sage);
        margin-bottom: 28px;
        font-weight: 500;
    }

    /* ── INPUT CARD ── */
    .input-card {
        background: var(--white);
        border: 1px solid var(--mist);
        border-radius: 2px;
        padding: 40px 44px;
        box-shadow: 0 2px 24px rgba(27,27,31,0.04), 0 0 0 1px rgba(201,168,76,0.06);
        position: relative;
        overflow: hidden;
    }

    .input-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--gold), var(--gold-lt), var(--gold));
    }

    /* ── LABELS ── */
    div[data-testid="stWidgetLabel"] p,
    .stSelectbox label, .stNumberInput label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.7rem !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        color: var(--sage) !important;
        margin-bottom: 8px !important;
    }

    /* ── INPUTS ── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: var(--cream) !important;
        border: 1px solid #DEDAD3 !important;
        border-radius: 2px !important;
        color: var(--ink) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.3s ease !important;
    }
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    }

    /* ── CTA BUTTON ── */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        background: var(--ink) !important;
        color: var(--gold) !important;
        border: 1px solid var(--gold) !important;
        border-radius: 2px !important;
        padding: 14px 24px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        transition: all 0.35s ease !important;
        cursor: pointer !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: var(--gold) !important;
        color: var(--ink) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(201,168,76,0.25) !important;
    }

    /* ── VALUATION RESULT ── */
    .result-outer {
        background: var(--ink);
        border-radius: 2px;
        padding: 2px;
        background: linear-gradient(135deg, var(--gold) 0%, var(--gold-lt) 50%, var(--gold) 100%);
        margin: 36px 0 28px;
    }

    .result-inner {
        background: var(--ink);
        border-radius: 1px;
        padding: 52px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .result-inner::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 60% 50% at 50% 0%, rgba(201,168,76,0.12) 0%, transparent 70%);
    }

    .result-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 16px;
        position: relative;
    }

    .result-price {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(3rem, 5vw, 4.8rem);
        font-weight: 300;
        color: #FDFCFA;
        letter-spacing: -1px;
        line-height: 1;
        position: relative;
    }

    .result-price span {
        font-size: 0.45em;
        font-weight: 400;
        color: var(--gold-lt);
        vertical-align: super;
        margin-right: 6px;
    }

    .result-note {
        font-size: 0.7rem;
        letter-spacing: 1px;
        color: rgba(253,252,250,0.35);
        margin-top: 14px;
        position: relative;
    }

    /* ── INSIGHT CARDS ── */
    .insight-card {
        background: var(--white);
        border: 1px solid var(--mist);
        border-left: 3px solid var(--gold);
        border-radius: 2px;
        padding: 28px 28px 24px;
    }
    .insight-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 10px;
    }
    .insight-body {
        font-size: 0.875rem;
        color: var(--ink-soft);
        line-height: 1.7;
    }
    .insight-metric {
        display: inline-block;
        background: var(--cream);
        border: 1px solid var(--mist);
        border-radius: 2px;
        padding: 6px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--ink);
        margin-top: 12px;
        letter-spacing: 0.5px;
    }
    .insight-metric.above { border-left: 3px solid var(--sage); }
    .insight-metric.below { border-left: 3px solid var(--brick); }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: var(--ink) !important;
        border-right: 1px solid rgba(201,168,76,0.15) !important;
    }
    [data-testid="stSidebar"] * {
        color: rgba(253,252,250,0.75) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--gold) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(201,168,76,0.15) !important;
    }
    [data-testid="stSidebar"] .stCaption {
        color: rgba(253,252,250,0.35) !important;
        font-size: 0.7rem !important;
    }

    /* Sidebar logo area */
    .logo-block {
        text-align: center;
        padding: 8px 0 20px;
    }
    .logo-symbol {
        font-size: 3rem;
        line-height: 1;
    }
    .logo-name {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.4rem !important;
        color: #FDFCFA !important;
        letter-spacing: 2px;
        margin: 6px 0 2px;
    }
    .logo-tagline {
        font-size: 0.6rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase;
        color: var(--gold) !important;
    }

    /* ── FOOTER ── */
    .footer-bar {
        background: var(--ink);
        padding: 22px 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 60px;
    }
    .footer-left {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        color: rgba(253,252,250,0.5);
        letter-spacing: 1px;
    }
    .footer-right {
        font-size: 0.65rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--gold);
        font-weight: 500;
    }

    /* ── MISC ── */
    .stMarkdown hr {
        border: none;
        height: 1px;
        background: var(--mist);
        margin: 32px 0;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    </style>
""", unsafe_allow_html=True)


# -------------------- ASSET LOADING --------------------
@st.cache_resource
def load_data():
    model = joblib.load("rf_model.joblib")
    model_features = joblib.load("model_columnn.joblib")
    df = pd.read_csv("cleaned_df.csv")
    return model, model_features, df

model, model_features, df = load_data()
locations = sorted([col.replace("location_", "") for col in model_features if col.startswith("location_")])


# -------------------- HERO --------------------
st.markdown("""
    <div class="hero-wrap">
        <div class="hero-inner">
            <div class="eyebrow">✦ Bengaluru Division &nbsp;·&nbsp; Est. 2024 ✦</div>
            <h1 class="hero-title">House <em>Haven</em></h1>
            <div class="hero-rule"></div>
            <p class="hero-sub">Automated Property Appraisal &nbsp;·&nbsp; AI-Powered Intelligence</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------- STATS STRIP --------------------
st.markdown(f"""
    <div class="stats-strip">
        <div class="stat-item">
            <div class="stat-num">{len(df):,}</div>
            <div class="stat-label">Verified Listings</div>
        </div>
        <div class="stat-sep"></div>
        <div class="stat-item">
            <div class="stat-num">{len(locations)}</div>
            <div class="stat-label">Locations Mapped</div>
        </div>
        <div class="stat-sep"></div>
        <div class="stat-item">
            <div class="stat-num">₹{df['price'].mean()*1e5/1e6:.1f}M</div>
            <div class="stat-label">Avg. Market Value</div>
        </div>
        <div class="stat-sep"></div>
        <div class="stat-item">
            <div class="stat-num">RF</div>
            <div class="stat-label">Model Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("""
        <div class="logo-block">
            <div class="logo-symbol">🏛</div>
            <div class="logo-name">House Haven</div>
            <div class="logo-tagline">Estate Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### About This Tool")
    st.write("A machine-learning valuation engine trained on Bengaluru's residential property market. Input architectural variables for a high-fidelity market estimate.")
    st.markdown("---")
    st.markdown("### Model Highlights")
    st.write("• Random Forest Regressor")
    st.write("• One-hot encoded locations")
    st.write("• Sqft, BHK, Bath features")
    st.markdown("---")
    st.caption("Curated by Mohammed Owais Qureshi")
    st.caption("© 2024 House Haven Analytics")


# -------------------- MAIN CONTENT --------------------
st.markdown('<div class="main-area">', unsafe_allow_html=True)

st.markdown("""
    <div class="section-heading">Property Configuration</div>
    <div class="section-sub">Enter the architectural variables below to generate your valuation</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
with c1:
    location = st.selectbox("Geographic Location", locations)
with c2:
    sqft = st.number_input("Square Footage (sq ft)", min_value=300, step=100)
with c3:
    bath = st.selectbox("Bathrooms", sorted(df["bath"].unique()))
with c4:
    bhk = st.selectbox("BHK Configuration", sorted(df["bhk"].unique()))

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 3, 2])
with btn_col:
    generate = st.button("⊹ GENERATE VALUATION REPORT ⊹")

st.markdown('</div>', unsafe_allow_html=True)


# -------------------- RESULT --------------------
if generate:
    input_dict = {col: 0 for col in model_features}
    input_dict['total_sqft'] = sqft
    input_dict['bath'] = bath
    input_dict['bhk'] = bhk
    loc_col = f"location_{location}"
    if loc_col in input_dict:
        input_dict[loc_col] = 1

    prediction = model.predict(pd.DataFrame([input_dict]))[0]
    final_val = prediction * 100000

    # Format price nicely
    if final_val >= 1e7:
        display_price = f"{final_val/1e7:.2f} Cr"
    else:
        display_price = f"{final_val/1e5:.2f} L"

    st.markdown(f"""
        <div class="result-outer">
            <div class="result-inner">
                <div class="result-label">✦ Official Market Estimate ✦</div>
                <div class="result-price"><span>₹</span>{display_price}</div>
                <div class="result-note">({final_val:,.0f} · Bengaluru Residential Market)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── INSIGHTS ──────────────────────────────────────────────────
    similar = df[(df["total_sqft"].between(sqft * 0.8, sqft * 1.2)) & (df["bhk"] == bhk)]

    st.markdown("""
        <div class="section-heading" style="margin-top:8px;">Market Analysis</div>
        <div class="section-sub">Contextual intelligence drawn from comparable regional listings</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.4], gap="large")

    with col_left:
        if not similar.empty:
            avg = similar["price"].mean()
            diff = ((prediction - avg) / avg) * 100
            status = "above" if diff > 0 else "below"
            badge_class = "above" if diff > 0 else "below"
            arrow = "↑" if diff > 0 else "↓"

            st.markdown(f"""
                <div class="insight-card">
                    <div class="insight-title">Comparative Positioning</div>
                    <div class="insight-body">
                        This property is valued relative to <strong>{len(similar)}</strong> comparable
                        listings within ±20% of your specified square footage and matching BHK configuration.
                    </div>
                    <div class="insight-metric {badge_class}">
                        {arrow} {abs(diff):.1f}% {status.title()} Market Average
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            avg_sqft_price = (similar["price"].mean() * 1e5) / similar["total_sqft"].mean() if "total_sqft" in similar.columns else 0
            your_sqft_price = final_val / sqft if sqft > 0 else 0

            st.markdown(f"""
                <div class="insight-card">
                    <div class="insight-title">Price Per Square Foot</div>
                    <div class="insight-body">
                        Your estimate works out to <strong>₹{your_sqft_price:,.0f}/sqft</strong>,
                        compared to a segment average of ₹{avg_sqft_price:,.0f}/sqft.
                    </div>
                    <div class="insight-metric">
                        ₹{your_sqft_price:,.0f} / sq ft
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">Insufficient Comparables</div>
                    <div class="insight-body">
                        No comparable listings found matching this exact configuration.
                        The valuation is based on broader market patterns.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        if not similar.empty:
            # ── PREMIUM CHART ──────────────────────────────────────
            fig, ax = plt.subplots(figsize=(7, 4))
            fig.patch.set_facecolor('#FDFCFA')
            ax.set_facecolor('#FDFCFA')

            prices = similar["price"].values
            n, bins, patches = ax.hist(
                prices, bins=18,
                color='#272730', alpha=0.85, rwidth=0.85, zorder=2
            )

            # Colour the bar that contains the prediction
            for patch, left_edge, right_edge in zip(patches, bins[:-1], bins[1:]):
                if left_edge <= prediction <= right_edge:
                    patch.set_facecolor('#C9A84C')
                    patch.set_alpha(1.0)

            ax.axvline(prediction, color='#C9A84C', linewidth=2, linestyle='--', zorder=3, alpha=0.9)

            ax.set_xlabel("Price (Lakhs)", fontsize=8, color='#6B7F6E',
                          fontfamily='DejaVu Sans', labelpad=8)
            ax.set_ylabel("Listings", fontsize=8, color='#6B7F6E',
                          fontfamily='DejaVu Sans', labelpad=8)
            ax.set_title("Regional Price Distribution", fontsize=11, color='#1B1B1F',
                         fontfamily='DejaVu Sans', fontweight='normal', pad=14)

            ax.tick_params(axis='both', labelsize=7, colors='#6B7F6E', length=0)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E8E3DA')
            ax.spines['bottom'].set_color('#E8E3DA')
            ax.yaxis.grid(True, color='#E8E3DA', linewidth=0.5, zorder=0)
            ax.set_axisbelow(True)

            legend_patches = [
                mpatches.Patch(color='#272730', label='Market Listings'),
                mpatches.Patch(color='#C9A84C', label='Your Valuation')
            ]
            ax.legend(handles=legend_patches, fontsize=7.5, frameon=False,
                      labelcolor='#3A3A42', loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

            # ── MINI METRICS ROW ──────────────────────────────────
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Min (Segment)", f"₹{similar['price'].min()*1e5/1e5:.1f}L")
            with m2:
                st.metric("Median", f"₹{similar['price'].median()*1e5/1e5:.1f}L")
            with m3:
                st.metric("Max (Segment)", f"₹{similar['price'].max()*1e5/1e5:.1f}L")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("""
    <div class="footer-bar">
        <div class="footer-left">House Haven · Estate Intelligence</div>
        <div class="footer-right">Curated by Mohammed Owais Qureshi &nbsp;·&nbsp; Bengaluru Division 2024</div>
    </div>
""", unsafe_allow_html=True)