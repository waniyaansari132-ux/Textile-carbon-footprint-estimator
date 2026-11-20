import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Textile Carbon Footprint Estimator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS STYLING (Eco-Friendly Sage Green & Charcoal Palette) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global Typography & Base Background */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #2B302C;
}

.stApp {
    background-color: #F6F8F5;
}

/* Main Container Spacing */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1120px;
}

/* Headers */
h1 {
    color: #1E2420;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}

h2, h3 {
    color: #2D4234;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin-top: 1.5rem;
}

.subtitle {
    color: #556358;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* Enhanced Metric Cards */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3DA;
    border-left: 5px solid #4F7759;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 6px rgba(43, 48, 44, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(43, 48, 44, 0.08);
}

div[data-testid="stMetricLabel"] > div {
    color: #556358;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

div[data-testid="stMetricValue"] > div {
    color: #1E2420;
    font-weight: 700;
    font-size: 1.85rem;
}

/* Input Containers & Expanders */
div[data-testid="stForm"], div.stDataFrame {
    background-color: #FFFFFF;
    border: 1px solid #DCE3DA;
    border-radius: 10px;
    padding: 1.25rem;
}

/* Multiselect Tags */
span[data-baseweb="tag"] {
    background-color: #4F7759 !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

/* Callout Box for Savings */
.savings-banner {
    background-color: #E7F0E8;
    border: 1px solid #B8D1BC;
    border-left: 5px solid #3D6347;
    color: #1E3323;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    font-weight: 500;
    margin: 1.25rem 0;
}

/* Prominently Styled Limitations & Responsible Use Note */
.limitations-card {
    background-color: #FFFFFF;
    border: 1px solid #CBD5C8;
    border-top: 4px solid #36453B;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    margin-top: 2rem;
    box-shadow: 0 2px 8px rgba(43, 48, 44, 0.05);
}

.limitations-title {
    color: #1E2420;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.limitations-card ul {
    margin-bottom: 0;
    padding-left: 1.25rem;
    color: #3B443D;
    line-height: 1.6;
}

.limitations-card li {
    margin-bottom: 0.45rem;
}
</style>
""", unsafe_allow_html=True)

# --- EMISSION FACTOR DATASET (kg CO2e per kg of fabric) ---
EMISSION_FACTORS = {
    "Wool": 13.8,
    "Acrylic": 11.5,
    "Silk": 11.0,
    "Nylon": 10.2,
    "Cotton (Conventional)": 8.3,
    "Polyester (Virgin)": 6.4,
    "Viscose (Rayon)": 4.0,
    "Organic Cotton": 3.8,
    "Recycled Polyester": 3.5,
    "Linen (Flax)": 2.3,
    "Hemp": 2.1,
}

# --- HEADER ---
st.title("Textile Carbon Footprint Estimator")
st.markdown(
    '<p class="subtitle">Cradle-to-gate greenhouse gas emission estimation and sustainable material comparison tool.</p>',
    unsafe_allow_html=True
)

# --- SECTION 1: INPUT PARAMETERS ---
st.subheader("1. Material & Weight Specification")

col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1.2])

with col1:
    selected_fabric = st.selectbox(
        "Primary Fabric Type",
        options=list(EMISSION_FACTORS.keys()),
        index=4
    )

with col2:
    unit = st.selectbox(
        "Weight Unit",
        options=["Kilograms (kg)", "Grams (g)"],
        index=0
    )

with col3:
    weight_input = st.number_input(
        "Unit Weight",
        min_value=0.01,
        value=0.25 if unit == "Kilograms (kg)" else 250.0,
        step=0.05 if unit == "Kilograms (kg)" else 10.0
    )

with col4:
    quantity = st.number_input(
        "Quantity (Units)",
        min_value=1,
        value=1,
        step=1
    )

# Convert total weight to kg
unit_weight_kg = weight_input if unit == "Kilograms (kg)" else weight_input / 1000.0
total_weight_kg = unit_weight_kg * quantity
factor = EMISSION_FACTORS[selected_fabric]
total_emissions = total_weight_kg * factor

st.markdown("---")

# --- SECTION 2: ESTIMATION SUMMARY METRICS ---
st.subheader("2. Estimated Carbon Footprint")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(
        label="Total Fabric Weight",
        value=f"{total_weight_kg:.2f} kg",
        delta=f"{quantity} unit(s) @ {unit_weight_kg:.3f} kg"
    )
with m2:
    st.metric(
        label="Emission Factor",
        value=f"{factor:.1f} kg CO₂e/kg",
        delta=selected_fabric,
        delta_color="off"
    )
with m3:
    st.metric(
        label="Total Cradle-to-Gate Emissions",
        value=f"{total_emissions:.2f} kg CO₂e"
    )

st.markdown("---")

# --- SECTION 3: EMISSION FACTOR BENCHMARK CHART ---
st.subheader("3. Emission Factor by Fabric Type")

df_factors = pd.DataFrame({
    "Fabric": list(EMISSION_FACTORS.keys()),
    "Emission Factor (kg CO2e/kg)": list(EMISSION_FACTORS.values())
}).sort_values(by="Emission Factor (kg CO2e/kg)", ascending=True)

fig1, ax1 = plt.subplots(figsize=(9, 4.2))
fig1.patch.set_facecolor("#FFFFFF")
ax1.set_facecolor("#FFFFFF")

bar_colors = [
    "#3D6347" if f == selected_fabric else "#A3B8A8"
    for f in df_factors["Fabric"]
]

bars1 = ax1.barh(
    df_factors["Fabric"],
    df_factors["Emission Factor (kg CO2e/kg)"],
    color=bar_colors,
    height=0.65
)

ax1.set_xlabel("kg CO₂e per kg of fabric", color="#3B443D", fontsize=10, fontweight="600")
ax1.tick_params(axis="both", colors="#2B302C", labelsize=9.5)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color("#CBD5C8")
ax1.spines["bottom"].set_color("#CBD5C8")
ax1.xaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5C8")
ax1.set_axisbelow(True)

for bar in bars1:
    width = bar.get_width()
    ax1.text(
        width + 0.25,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.1f}",
        va="center",
        ha="left",
        fontsize=9,
        color="#2B302C",
        fontweight="600"
    )

ax1.set_xlim(0, max(df_factors["Emission Factor (kg CO2e/kg)"]) * 1.12)
plt.tight_layout()
st.pyplot(fig1)

st.markdown("---")

# --- SECTION 4: FABRIC COMPARISON ---
st.subheader("4. Fabric Comparison with Alternatives")

available_alternatives = [f for f in EMISSION_FACTORS.keys() if f != selected_fabric]
default_alts = [f for f in ["Organic Cotton", "Recycled Polyester", "Hemp"] if f in available_alternatives]

alternatives = st.multiselect(
    "Select alternative fabrics to compare (same total weight):",
    options=available_alternatives,
    default=default_alts
)

comparison_fabrics = [selected_fabric] + alternatives
comparison_rows = []

for fab in comparison_fabrics:
    ef = EMISSION_FACTORS[fab]
    em = total_weight_kg * ef
    diff = em - total_emissions
    pct = ((em - total_emissions) / total_emissions * 100) if total_emissions > 0 else 0.0
    label = f"{fab} (Selected)" if fab == selected_fabric else fab
    comparison_rows.append({
        "Fabric": label,
        "Raw_Name": fab,
        "Emission Factor (kg CO₂e/kg)": ef,
        "Total Emissions (kg CO₂e)": round(em, 2),
        "Difference vs. Selected (kg CO₂e)": round(diff, 2),
        "Change (%)": round(pct, 1)
    })

df_comp = pd.DataFrame(comparison_rows)

comp_col1, comp_col2 = st.columns([1.2, 1])

with comp_col1:
    fig2, ax2 = plt.subplots(figsize=(6.5, 4))
    fig2.patch.set_facecolor("#FFFFFF")
    ax2.set_facecolor("#FFFFFF")

    comp_colors = [
        "#36453B" if r == selected_fabric else "#5C8A67"
        for r in df_comp["Raw_Name"]
    ]

    bars2 = ax2.bar(
        df_comp["Fabric"],
        df_comp["Total Emissions (kg CO₂e)"],
        color=comp_colors,
        width=0.52
    )

    ax2.set_ylabel("Total kg CO₂e", color="#3B443D", fontsize=10, fontweight="600")
    ax2.set_title("Footprint Comparison (Same Weight & Quantity)", color="#1E2420", fontsize=11, fontweight="600", pad=12)
    ax2.tick_params(axis="x", rotation=18, colors="#2B302C", labelsize=9)
    ax2.tick_params(axis="y", colors="#2B302C", labelsize=9.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#CBD5C8")
    ax2.spines["bottom"].set_color("#CBD5C8")
    ax2.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5C8")
    ax2.set_axisbelow(True)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max(df_comp["Total Emissions (kg CO₂e)"]) * 0.025),
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#2B302C",
            fontweight="600"
        )

    ax2.set_ylim(0, max(df_comp["Total Emissions (kg CO₂e)"]) * 1.18 if max(df_comp["Total Emissions (kg CO₂e)"]) > 0 else 1)
    plt.tight_layout()
    st.pyplot(fig2)

with comp_col2:
    display_df = df_comp.drop(columns=["Raw_Name"])
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if alternatives:
        best_alt = df_comp.iloc[1:].sort_values(by="Total Emissions (kg CO₂e)").iloc[0]
        saved_kg = total_emissions - best_alt["Total Emissions (kg CO₂e)"]
        saved_pct = -best_alt["Change (%)"]
        if saved_kg > 0:
            st.markdown(
                f'<div class="savings-banner">'
                f'Switching from <strong>{selected_fabric}</strong> to <strong>{best_alt["Raw_Name"]}</strong> '
                f'could reduce emissions by <strong>{saved_kg:.2f} kg CO₂e ({saved_pct:.0f}% lower)</strong> for the same weight.'
                f'</div>',
                unsafe_allow_html=True
            )
        elif saved_kg < 0:
            st.markdown(
                f'<div class="savings-banner">'
                f'<strong>{selected_fabric}</strong> already has a lower carbon footprint than the selected alternatives '
                f'by at least <strong>{abs(saved_kg):.2f} kg CO₂e</strong>.'
                f'</div>',
                unsafe_allow_html=True
            )

# --- SECTION 5: PROMINENT LIMITATIONS & RESPONSIBLE USE ---
st.markdown("""
<div class="limitations-card">
    <div class="limitations-title">Limitations & Responsible Use</div>
    <p style="color:#3B443D; margin-bottom:0.75rem;">
        <strong>What this tool does:</strong> Provides a quick, indicative estimate of cradle-to-gate emissions by multiplying fabric weight by an average emission factor.
    </p>
    <ul>
        <li><strong>Approximate factors:</strong> Values are rounded industry averages for educational comparison. Real figures vary by country, energy grid, farming method, dyeing, finishing, and mill efficiency.</li>
        <li><strong>Limited scope:</strong> Estimates exclude transport, packaging, garment assembly, consumer washing/drying, and end-of-life disposal.</li>
        <li><strong>Single fiber only:</strong> Blended fabrics (e.g., cotton-polyester) are not modeled directly. Use the dominant fiber or calculate a weighted average manually.</li>
        <li><strong>Carbon metric only:</strong> Water consumption, land use, chemical pollution, and microplastic release are not measured, though essential for holistic sustainability assessment.</li>
        <li><strong>Responsible use:</strong> Treat results as an indicative guide rather than certified Life Cycle Assessment (LCA) data for regulatory reporting or marketing claims.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
