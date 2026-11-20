import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Textile Carbon Footprint Estimator",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stApp {
        background-color: #0d0f12;
        color: #e0e6ed;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #00ffcc, #0099ff);
        border: none;
        color: #000;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 255, 204, 0.8);
    }
    
    .main-container {
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00ffcc;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }
    
    .css-card {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .css-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
        box-shadow: 0 15px 35px rgba(0, 255, 204, 0.2), inset 0 1px 0 rgba(255,255,255,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🧵 Textile Carbon Footprint Estimator")
st.markdown('<div class="css-card">Cradle-to-gate greenhouse gas emission estimation and sustainable material comparison tool.</div>', unsafe_allow_html=True)

FABRICS = {
    "Hemp": {"factor": 2.1, "note": "Low-input crop, little irrigation"},
    "Linen (Flax)": {"factor": 2.5, "note": "Rain-fed crop, low chemical use"},
    "Recycled Polyester": {"factor": 3.5, "note": "Made from PET waste"},
    "Organic Cotton": {"factor": 3.8, "note": "No synthetic fertilizers"},
    "Viscose (Rayon)": {"factor": 6.0, "note": "Wood pulp, chemical processing"},
    "Cotton (Conventional)": {"factor": 8.3, "note": "Irrigation and fertilizer heavy"},
    "Polyester (Virgin)": {"factor": 9.5, "note": "Fossil-based, energy intensive"},
    "Nylon": {"factor": 10.2, "note": "Fossil-based, N2O emissions"},
    "Silk": {"factor": 11.0, "note": "Sericulture and reeling energy"},
    "Acrylic": {"factor": 11.5, "note": "Fossil-based synthetic"},
    "Wool": {"factor": 13.0, "note": "Livestock methane emissions"}
}

CAR_KG_PER_KM = 0.192
TREE_KG_PER_YEAR = 21.0
PHONE_KG_PER_CHARGE = 0.008

st.subheader("1. Material & Weight Specification")
col1, col2 = st.columns([2, 1])
with col1:
    selected_fabric = st.selectbox("Primary Fabric Type", list(FABRICS.keys()))
with col2:
    unit = st.radio("Weight Unit", ["Kilograms (kg)", "Grams (g)"], horizontal=True)

unit_weight = st.number_input("Unit Weight", min_value=0.01, value=0.25, step=0.01)
quantity = st.number_input("Quantity (Units)", min_value=1, value=1, step=1)

if unit == "Grams (g)":
    total_weight_kg = (unit_weight * quantity) / 1000.0
else:
    total_weight_kg = unit_weight * quantity

emission_factor = FABRICS[selected_fabric]["factor"]
total_emissions = total_weight_kg * emission_factor

st.markdown("---")
st.subheader("2. Estimated Carbon Footprint")
m1, m2, m3 = st.columns(3)
m1.metric("Total Fabric Weight", f"{total_weight_kg:.2f} kg")
m2.metric("Emission Factor", f"{emission_factor} kg CO₂e/kg")
m3.metric("Total Cradle-to-Gate Emissions", f"{total_emissions:.2f} kg CO₂e")

phone_charges = total_emissions / PHONE_KG_PER_CHARGE

st.info(f"This equals roughly {int(phone_charges):,} smartphone charges worth of emissions.")

st.markdown("---")
st.subheader("3. Emission Factor Chart")
df_factors = pd.DataFrame.from_dict(FABRICS, orient='index').sort_values('factor', ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df_factors.index, df_factors['factor'], color='#2B302C')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, f'{width}', va='center', ha='left', color='#2B302C', fontweight='600')
ax.set_xlabel("kg CO₂e per kg of fabric")
ax.set_title("Emission Factor by Fabric Type", fontsize=14, color='#2B302C', fontweight='bold')
st.pyplot(fig)

st.markdown("---")
st.subheader("4. Fabric Comparison with Alternatives")
available_alternatives = [f for f in FABRICS.keys() if f != selected_fabric]
default_alts = ["Organic Cotton", "Recycled Polyester", "Hemp"]
alternatives = st.multiselect("Select alternative fabrics to compare (same total weight):", options=available_alternatives, default=default_alts)

if alternatives:
    comp_data = {"Fabric": [selected_fabric] + alternatives, "Emissions (kg CO₂e)": [total_emissions] + [total_weight_kg * FABRICS[alt]["factor"] for alt in alternatives]}
    df_comp = pd.DataFrame(comp_data)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    bars2 = ax2.bar(df_comp["Fabric"], df_comp["Emissions (kg CO₂e)"], color=['#2B302C' if f == selected_fabric else '#36453B' for f in df_comp["Fabric"]])
    ax2.set_ylabel("Total kg CO₂e")
    ax2.set_title("Footprint Comparison (Same Weight)", fontsize=14, color='#2B302C', fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    st.pyplot(fig2)
    
    best_alt = df_comp.sort_values("Emissions (kg CO₂e)").iloc[0]
    if best_alt["Fabric"] != selected_fabric:
        saved = total_emissions - best_alt["Emissions (kg CO₂e)"]
        st.success(f"Switching from {selected_fabric} to {best_alt['Fabric']} could reduce emissions by {saved:.2f} kg CO₂e ({saved/total_emissions*100:.1f}% lower) for the same weight.")

st.markdown("---")
with st.expander("✨ Limitations & Responsible Use"):
    st.write("""
    - **Approximate factors:** Values are rounded industry averages for educational comparison. Real figures vary by country, energy grid, farming method, dyeing, finishing, and mill efficiency.
    - **Limited scope:** Estimates exclude transport, packaging, garment assembly, consumer washing/drying, and end-of-life disposal.
    - **Single fiber only:** Blended fabrics (e.g., cotton-polyester) are not modeled directly. Use the dominant fiber or calculate a weighted average manually.
    - **Carbon metric only:** Water consumption, land use, chemical pollution, and microplastic release are not measured, though essential for holistic sustainability assessment.
    - **Responsible use:** Treat results as an indicative guide rather than certified Life Cycle Assessment (LCA) data for reporting or marketing claims.
    """)
st.markdown('</div>', unsafe_allow_html=True)
