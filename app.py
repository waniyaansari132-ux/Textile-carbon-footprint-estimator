"""
Textile Carbon Footprint Estimator
Run with:  streamlit run textile_carbon_estimator.py
Requires:  streamlit, matplotlib, pandas
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Textile Carbon Footprint Estimator",
    page_icon="🧵",
    layout="wide",
)

# ----------------------------------------------------------------------------
# Data: indicative cradle-to-gate emission factors (kg CO2e per kg of fabric).
# These are approximate, rounded values compiled for educational estimation.
# Real values vary by region, energy mix, dyeing and finishing processes.
# ----------------------------------------------------------------------------
FABRICS = {
    "Hemp": {"factor": 2.1, "note": "Low-input crop, little irrigation"},
    "Linen (Flax)": {"factor": 2.5, "note": "Rain-fed crop, low chemical use"},
    "Recycled Polyester": {"factor": 3.5, "note": "Made from PET waste"},
    "Organic Cotton": {"factor": 3.8, "note": "No synthetic fertilizers"},
    "Viscose (Rayon)": {"factor": 6.0, "note": "Wood pulp, chemical processing"},
    "Cotton (Conventional)": {"factor": 8.3, "note": "Irrigation and fertilizer heavy"},
    "Polyester": {"factor": 9.5, "note": "Fossil-based, energy intensive"},
    "Nylon": {"factor": 10.2, "note": "Fossil-based, N2O emissions"},
    "Silk": {"factor": 11.0, "note": "Sericulture and reeling energy"},
    "Acrylic": {"factor": 11.5, "note": "Fossil-based synthetic"},
    "Wool": {"factor": 13.0, "note": "Livestock methane emissions"},
}

# Everyday equivalents (approximate)
CAR_KG_PER_KM = 0.192        # average petrol car, kg CO2e per km
TREE_KG_PER_YEAR = 21.0      # CO2 absorbed by one mature tree per year
PHONE_KG_PER_CHARGE = 0.008  # one smartphone full charge

# Neon palette
NEON_CYAN = "#00f5ff"
NEON_PINK = "#ff2bd6"
NEON_GREEN = "#39ff14"
NEON_PURPLE = "#9d4edd"
BG_DARK = "#0b0b1a"
PANEL_DARK = "#14142b"
TEXT_LIGHT = "#e6e6ff"

# ----------------------------------------------------------------------------
# Custom CSS: dark theme, neon accents, 3D-style cards
# ----------------------------------------------------------------------------
CUSTOM_CSS = f"""
<style>
.stApp {{
    background: radial-gradient(circle at 20% 10%, #1b1040 0%, {BG_DARK} 45%, #05050d 100%);
    color: {TEXT_LIGHT};
}}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }}

h1, h2, h3, h4, label, p, span, div {{ color: {TEXT_LIGHT}; }}

.hero {{
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(145deg, #1a1a3d, #0e0e24);
    border: 1px solid rgba(0, 245, 255, 0.35);
    box-shadow:
        0 0 25px rgba(0, 245, 255, 0.25),
        12px 12px 30px rgba(0, 0, 0, 0.7),
        -6px -6px 18px rgba(80, 80, 160, 0.15);
    margin-bottom: 26px;
    transform: perspective(900px) rotateX(2deg);
}}
.hero h1 {{
    margin: 0;
    font-size: 2.3rem;
    font-weight: 800;
    color: {NEON_CYAN};
    text-shadow: 0 0 8px {NEON_CYAN}, 0 0 22px rgba(0, 245, 255, 0.6);
}}
.hero p {{ margin: 8px 0 0 0; color: #b9b9e6; font-size: 1.02rem; }}

.section-title {{
    margin: 34px 0 14px 0;
    font-size: 1.45rem;
    font-weight: 700;
    color: {NEON_PINK};
    text-shadow: 0 0 8px rgba(255, 43, 214, 0.7);
    border-left: 4px solid {NEON_PINK};
    padding-left: 12px;
}}

.card {{
    padding: 20px 22px;
    border-radius: 18px;
    background: linear-gradient(145deg, #191937, #0f0f25);
    border: 1px solid rgba(157, 78, 221, 0.4);
    box-shadow: 8px 8px 22px rgba(0, 0, 0, 0.65),
                -4px -4px 14px rgba(70, 70, 140, 0.18);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    margin-bottom: 14px;
}}
.card:hover {{
    transform: translateY(-6px) scale(1.015);
    box-shadow: 0 0 22px rgba(0, 245, 255, 0.45),
                10px 14px 28px rgba(0, 0, 0, 0.75);
}}
.card .label {{
    font-size: 0.82rem;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #9a9ad0;
}}
.card .value {{
    font-size: 1.9rem;
    font-weight: 800;
    margin-top: 4px;
}}
.card .sub {{ font-size: 0.85rem; color: #8f8fc4; margin-top: 2px; }}
.neon-cyan  {{ color: {NEON_CYAN};  text-shadow: 0 0 10px rgba(0, 245, 255, 0.7); }}
.neon-pink  {{ color: {NEON_PINK};  text-shadow: 0 0 10px rgba(255, 43, 214, 0.7); }}
.neon-green {{ color: {NEON_GREEN}; text-shadow: 0 0 10px rgba(57, 255, 20, 0.6); }}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #12122b, #08081a);
    border-right: 1px solid rgba(0, 245, 255, 0.25);
}}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stNumberInput input {{
    background-color: {PANEL_DARK} !important;
    color: {TEXT_LIGHT} !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0, 245, 255, 0.35) !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, {NEON_PURPLE}, {NEON_PINK});
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 700;
    box-shadow: 0 6px 0 #4b1d73, 0 0 18px rgba(255, 43, 214, 0.5);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    color: white;
    box-shadow: 0 8px 0 #4b1d73, 0 0 26px rgba(255, 43, 214, 0.8);
}}
.stButton > button:active {{
    transform: translateY(4px);
    box-shadow: 0 2px 0 #4b1d73;
}}

[data-testid="stExpander"] {{
    background: linear-gradient(145deg, #181838, #0e0e24);
    border: 1px solid rgba(57, 255, 20, 0.45);
    border-radius: 16px;
    box-shadow: 0 0 18px rgba(57, 255, 20, 0.18);
}}
[data-testid="stExpander"] summary p {{
    color: {NEON_GREEN};
    font-weight: 700;
}}

.insight {{
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(57, 255, 20, 0.07);
    border: 1px solid rgba(57, 255, 20, 0.4);
    color: {TEXT_LIGHT};
    margin-top: 10px;
}}
.footer {{ text-align: center; color: #6e6ea8; font-size: 0.8rem; margin-top: 30px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------
def to_kg(value: float, unit: str) -> float:
    """Convert the entered weight to kilograms."""
    return value / 1000.0 if unit == "Grams (g)" else value


def calc_footprint(weight_kg: float, quantity: int, fabric: str) -> float:
    """Total emissions in kg CO2e for the given fabric, weight and quantity."""
    return weight_kg * quantity * FABRICS[fabric]["factor"]


def metric_card(label: str, value: str, sub: str, css_class: str) -> str:
    return (
        f'<div class="card"><div class="label">{label}</div>'
        f'<div class="value {css_class}">{value}</div>'
        f'<div class="sub">{sub}</div></div>'
    )


def style_axes(fig, ax):
    """Apply the dark neon look to a Matplotlib figure."""
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(PANEL_DARK)
    for spine in ax.spines.values():
        spine.set_color("#3a3a7a")
    ax.tick_params(colors=TEXT_LIGHT, labelsize=10)
    ax.xaxis.label.set_color(TEXT_LIGHT)
    ax.yaxis.label.set_color(TEXT_LIGHT)
    ax.title.set_color(NEON_CYAN)
    ax.grid(axis="x", color="#2a2a5a", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)


def glow_bars(ax, names, values, colors, horizontal=True):
    """Draw bars with a soft neon glow effect behind them."""
    for width, alpha in ((0.95, 0.10), (0.85, 0.18)):
        if horizontal:
            ax.barh(names, values, height=width, color=colors, alpha=alpha, zorder=2)
        else:
            ax.bar(names, values, width=width, color=colors, alpha=alpha, zorder=2)
    if horizontal:
        bars = ax.barh(names, values, height=0.6, color=colors,
                       edgecolor="white", linewidth=0.6, zorder=3)
    else:
        bars = ax.bar(names, values, width=0.55, color=colors,
                      edgecolor="white", linewidth=0.6, zorder=3)
    return bars


def factor_chart(selected: str):
    """Bar chart of emission factors for every fabric, selected one highlighted."""
    ordered = sorted(FABRICS.items(), key=lambda kv: kv[1]["factor"])
    names = [n for n, _ in ordered]
    values = [d["factor"] for _, d in ordered]
    colors = [NEON_CYAN if n == selected else NEON_PURPLE for n in names]

    fig, ax = plt.subplots(figsize=(9, 5.2))
    style_axes(fig, ax)
    bars = glow_bars(ax, names, values, colors, horizontal=True)

    for bar, val, name in zip(bars, values, names):
        txt = ax.text(
            val + 0.2, bar.get_y() + bar.get_height() / 2, f"{val:.1f}",
            va="center", ha="left", fontsize=10, fontweight="bold",
            color=NEON_CYAN if name == selected else TEXT_LIGHT,
        )
        txt.set_path_effects([pe.withStroke(linewidth=2, foreground=BG_DARK)])

    ax.set_xlim(0, max(values) * 1.18)
    ax.set_xlabel("kg CO2e per kg of fabric")
    ax.set_title("Emission Factor by Fabric Type", fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig


def comparison_chart(names, totals, selected: str):
    """Vertical bar chart comparing total footprint of chosen fabrics."""
    colors = []
    for n in names:
        if n == selected:
            colors.append(NEON_CYAN)
        else:
            colors.append(NEON_GREEN if totals[n] < totals[selected] else NEON_PINK)

    values = [totals[n] for n in names]
    fig, ax = plt.subplots(figsize=(9, 5))
    style_axes(fig, ax)
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", color="#2a2a5a", linestyle="--", linewidth=0.7, alpha=0.7)
    bars = glow_bars(ax, names, values, colors, horizontal=False)

    top = max(values) if values else 1
    for bar, val in zip(bars, values):
        txt = ax.text(
            bar.get_x() + bar.get_width() / 2, val + top * 0.02, f"{val:.2f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT_LIGHT,
        )
        txt.set_path_effects([pe.withStroke(linewidth=2, foreground=BG_DARK)])

    ax.set_ylim(0, top * 1.18)
    ax.set_ylabel("Total kg CO2e")
    ax.set_title("Footprint Comparison (same weight and quantity)",
                 fontsize=14, fontweight="bold", pad=12)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    fig.tight_layout()
    return fig


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🧵 Textile Carbon Footprint Estimator</h1>
        <p>Estimate the greenhouse gas emissions of your fabric choice and compare
        it with greener alternatives.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Section 1: Inputs
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">1. Fabric and Weight Input</div>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d = st.columns([2, 1.3, 1, 1])

with col_a:
    fabric = st.selectbox(
        "Select fabric",
        options=list(FABRICS.keys()),
        index=list(FABRICS.keys()).index("Cotton (Conventional)"),
        help="Choose the main fiber of your textile product.",
    )
with col_b:
    unit = st.radio("Weight unit", ["Kilograms (kg)", "Grams (g)"], horizontal=True)
with col_c:
    if unit == "Grams (g)":
        weight = st.number_input("Weight per item", min_value=1.0, max_value=100000.0,
                                 value=250.0, step=10.0)
    else:
        weight = st.number_input("Weight per item", min_value=0.01, max_value=1000.0,
                                 value=0.25, step=0.05, format="%.2f")
with col_d:
    quantity = st.number_input("Quantity", min_value=1, max_value=1000000,
                               value=1, step=1)

weight_kg = to_kg(float(weight), unit)
total_weight_kg = weight_kg * int(quantity)
factor = FABRICS[fabric]["factor"]
total_co2 = calc_footprint(weight_kg, int(quantity), fabric)

st.caption(f"Fabric note: {FABRICS[fabric]['note']}  |  Emission factor: {factor} kg CO2e per kg")

# ----------------------------------------------------------------------------
# Section 2: Results
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">2. Your Estimated Footprint</div>', unsafe_allow_html=True)

car_km = total_co2 / CAR_KG_PER_KM
tree_years = total_co2 / TREE_KG_PER_YEAR
phone_charges = total_co2 / PHONE_KG_PER_CHARGE

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(metric_card("Total emissions", f"{total_co2:,.2f} kg",
                            "kg CO2e (cradle-to-gate)", "neon-cyan"),
                unsafe_allow_html=True)
with m2:
    st.markdown(metric_card("Total fabric weight", f"{total_weight_kg:,.2f} kg",
                            f"{int(quantity):,} item(s)", "neon-pink"),
                unsafe_allow_html=True)
with m3:
    st.markdown(metric_card("Car travel equivalent", f"{car_km:,.1f} km",
                            "average petrol car", "neon-green"),
                unsafe_allow_html=True)
with m4:
    st.markdown(metric_card("Tree absorption", f"{tree_years:,.2f} yrs",
                            "of one mature tree", "neon-cyan"),
                unsafe_allow_html=True)

st.markdown(
    f'<div class="insight">This equals roughly <b>{phone_charges:,.0f}</b> smartphone '
    f'charges worth of emissions.</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Section 3: Chart
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">3. Emission Factor Chart</div>', unsafe_allow_html=True)

fig1 = factor_chart(fabric)
st.pyplot(fig1)
plt.close(fig1)

# ----------------------------------------------------------------------------
# Section 4: Comparison
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">4. Fabric Comparison</div>', unsafe_allow_html=True)

all_fabrics = list(FABRICS.keys())
default_compare = [f for f in ["Organic Cotton", "Recycled Polyester", "Hemp"] if f != fabric]

compare_choice = st.multiselect(
    "Compare your fabric with alternatives",
    options=[f for f in all_fabrics if f != fabric],
    default=default_compare,
    help="Totals use the same weight and quantity you entered above.",
)

if not compare_choice:
    st.info("Select at least one alternative fabric to see the comparison.")
else:
    names = [fabric] + compare_choice
    totals = {n: calc_footprint(weight_kg, int(quantity), n) for n in names}

    chart_col, table_col = st.columns([1.5, 1])

    with chart_col:
        fig2 = comparison_chart(names, totals, fabric)
        st.pyplot(fig2)
        plt.close(fig2)

    with table_col:
        rows = []
        for n in names:
            diff = totals[n] - total_co2
            pct = (diff / total_co2 * 100) if total_co2 > 0 else 0.0
            rows.append({
                "Fabric": n + (" (selected)" if n == fabric else ""),
                "kg CO2e/kg": FABRICS[n]["factor"],
                "Total kg CO2e": round(totals[n], 2),
                "Change vs selected": f"{pct:+.0f}%",
            })
        df = pd.DataFrame(rows).sort_values("Total kg CO2e").reset_index(drop=True)
        st.dataframe(df, hide_index=True)

    best = min(totals, key=totals.get)
    if best != fabric and total_co2 > 0:
        saving = total_co2 - totals[best]
        pct_saving = saving / total_co2 * 100
        st.markdown(
            f'<div class="insight">Switching from <b>{fabric}</b> to <b>{best}</b> '
            f'could cut about <b>{saving:,.2f} kg CO2e</b> ({pct_saving:.0f}% lower) '
            f'for the same weight.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="insight"><b>{fabric}</b> already has the lowest footprint '
            f'among the fabrics you selected.</div>',
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Section 5: Limitations and Responsible Use (always at the bottom)
# ----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("Limitations and Responsible Use"):
    st.markdown(
        """
**What this tool does.** It gives a quick, indicative estimate of cradle-to-gate
emissions by multiplying fabric weight by an average emission factor.

**Key limitations**

- **Approximate factors.** Values are rounded averages for education and
  comparison. Real figures change with country, energy grid, farming method,
  dyeing, finishing and mill efficiency.
- **Limited scope.** The estimate excludes transport, packaging, garment
  assembly, consumer washing and drying, and end-of-life disposal.
- **Single fiber only.** Blended fabrics (for example cotton-polyester) are not
  modeled. Use the closest dominant fiber or average the values yourself.
- **Carbon only.** Water use, land use, chemical pollution and microplastic
  release are not measured, yet they matter for a full sustainability view.

**Responsible use**

- Treat results as a rough guide, not as certified data or an audit.
- Do not use them for regulatory reporting, carbon claims or marketing
  statements. Use verified Life Cycle Assessment data (for example, from your
  suppliers or recognized databases) for that.
- Use the comparison to start better conversations about material choice, and
  remember that wearing a garment longer is often the biggest saving.
        """
    )

st.markdown(
    '<div class="footer">Built with Streamlit and Matplotlib. Estimates are indicative only.</div>',
    unsafe_allow_html=True,
)
