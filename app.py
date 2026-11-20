"""
Textile Carbon Footprint Estimator  (Streamlit, v2)
Dark 3D look, sage-green neon accents, animated visuals, fabric blends.

Run locally:   streamlit run app.py
Deploy:        push app.py and requirements.txt to GitHub, then deploy on Streamlit Community Cloud.
requirements.txt:
    streamlit
    matplotlib
"""

import json

import streamlit as st
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

st.set_page_config(
    page_title="Textile Carbon Footprint Estimator",
    page_icon="🌿",
    layout="wide",
)

# ------------------------------------------------------------------ #
# Palette
# ------------------------------------------------------------------ #
BG = "#0b0f0c"
PANEL = "#121915"
SAGE = "#9CAF88"
SAGE_SOFT = "#5F7253"
SAGE_NEON = "#B9F6A0"
TEXT = "#E4EBDF"
MUTED = "#8FA085"
WARN = "#F2C879"
DANGER = "#FF8F7A"

# ------------------------------------------------------------------ #
# Data: indicative cradle-to-gate factors (kg CO2e per kg fabric)
# Rounded, illustrative values for education and screening only.
# cat: plant / animal / synthetic (used for the animated icons)
# ------------------------------------------------------------------ #
FABRICS = {
    "Conventional Cotton": {"f": 5.9, "cat": "plant", "note": "Natural fibre; footprint driven by farming, fertiliser and energy."},
    "Organic Cotton": {"f": 3.8, "cat": "plant", "note": "Lower inputs than conventional cotton; yields and region matter."},
    "Linen (Flax)": {"f": 2.5, "cat": "plant", "note": "Low-input crop that grows on modest water and fertiliser."},
    "Hemp": {"f": 2.0, "cat": "plant", "note": "Fast-growing, low-input crop with a small farming footprint."},
    "Polyester (Virgin)": {"f": 9.5, "cat": "synthetic", "note": "Fossil-based synthetic with energy-heavy production."},
    "Recycled Polyester": {"f": 5.0, "cat": "synthetic", "note": "Made from recycled plastic; avoids virgin fossil extraction."},
    "Nylon": {"f": 12.0, "cat": "synthetic", "note": "Energy-intensive synthetic; process emissions can be high."},
    "Acrylic": {"f": 11.0, "cat": "synthetic", "note": "Fossil-based synthetic often used as a wool substitute."},
    "Wool": {"f": 13.0, "cat": "animal", "note": "Animal fibre; farm methane drives a high, variable footprint."},
    "Silk": {"f": 11.0, "cat": "animal", "note": "Labour- and energy-intensive natural protein fibre."},
    "Viscose (Rayon)": {"f": 5.5, "cat": "plant", "note": "Wood-pulp fibre; chemical processing and sourcing matter."},
    "Lyocell (Tencel)": {"f": 3.2, "cat": "plant", "note": "Closed-loop wood-pulp process lowers chemical impact."},
}

UNIT_TO_KG = {"kg": 1.0, "g": 0.001, "lb": 0.45359237}

KG_PER_CAR_KM = 0.192
KG_PER_TREE_YEAR = 21.0
KG_PER_PHONE_CHARGE = 0.008

# ------------------------------------------------------------------ #
# Global CSS (dark, 3D cards, neon, entrance animations, falling leaves)
# ------------------------------------------------------------------ #
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
.stApp {
  background: radial-gradient(1200px 600px at 10% -10%, rgba(156,175,136,0.14), transparent 60%),
              radial-gradient(900px 500px at 100% 0%, rgba(185,246,160,0.08), transparent 55%),
              linear-gradient(180deg, #0b0f0c 0%, #0d1310 100%);
  color: #E4EBDF;
  font-family: 'Poppins', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px; }
.stApp p, .stApp label, .stApp span, .stApp li, .stApp div { color: #E4EBDF; }
h1, h2, h3, h4 { color: #E4EBDF !important; font-family: 'Poppins', sans-serif !important; }
@keyframes fadeUp {
  from { opacity: 0; transform: perspective(900px) translateY(36px) rotateX(14deg); }
  to   { opacity: 1; transform: perspective(900px) translateY(0) rotateX(3deg); }
}
@keyframes borderGlow {
  0%, 100% { box-shadow: 0 22px 44px rgba(0,0,0,0.6), 0 0 0 1px rgba(185,246,160,0.35), 0 0 18px rgba(185,246,160,0.18); }
  50%      { box-shadow: 0 22px 44px rgba(0,0,0,0.6), 0 0 0 1px rgba(185,246,160,0.75), 0 0 34px rgba(185,246,160,0.38); }
}
@keyframes fall {
  0%   { transform: translate3d(0,-40px,0) rotate(0deg); }
  50%  { transform: translate3d(36px,55vh,0) rotate(180deg); }
  100% { transform: translate3d(-12px,112vh,0) rotate(360deg); }
}
.leaves { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; z-index: 0; }
.leaves i {
  position: absolute; top: -40px; width: 13px; height: 13px; opacity: 0.22;
  background: linear-gradient(135deg, #B9F6A0, #5F7253); border-radius: 0 100% 0 100%;
  animation: fall 16s linear infinite;
}
.leaves i:nth-child(1) { left: 6%;  animation-duration: 17s; animation-delay: 0s; }
.leaves i:nth-child(2) { left: 18%; animation-duration: 21s; animation-delay: 4s; width: 10px; height: 10px; }
.leaves i:nth-child(3) { left: 30%; animation-duration: 15s; animation-delay: 8s; }
.leaves i:nth-child(4) { left: 44%; animation-duration: 23s; animation-delay: 2s; width: 16px; height: 16px; }
.leaves i:nth-child(5) { left: 57%; animation-duration: 18s; animation-delay: 10s; }
.leaves i:nth-child(6) { left: 69%; animation-duration: 20s; animation-delay: 6s; width: 11px; height: 11px; }
.leaves i:nth-child(7) { left: 82%; animation-duration: 16s; animation-delay: 12s; }
.leaves i:nth-child(8) { left: 93%; animation-duration: 24s; animation-delay: 3s; width: 14px; height: 14px; }
.section-title {
  display: flex; align-items: center; gap: 0.7rem; margin: 2.2rem 0 0.9rem 0;
  animation: fadeUp 0.8s ease-out backwards;
}
.section-title .num {
  width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(145deg, #9CAF88, #5F7253); color: #0b0f0c !important; font-weight: 700;
  box-shadow: 0 6px 14px rgba(0,0,0,0.5), 0 0 14px rgba(185,246,160,0.35);
}
.section-title .txt { font-size: 1.35rem; font-weight: 600; color: #E4EBDF; }
.section-title .sub { font-size: 0.85rem; color: #8FA085; margin-left: 0.3rem; }
.card {
  position: relative; padding: 1.2rem 1.2rem; border-radius: 18px; height: 100%; margin-bottom: 0.6rem;
  background: linear-gradient(145deg, rgba(28,38,31,0.95), rgba(14,20,16,0.95));
  box-shadow: 0 20px 40px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.06), 0 0 0 1px rgba(156,175,136,0.2);
  transform: perspective(900px) rotateX(3deg);
  transition: transform 0.35s ease, box-shadow 0.35s ease;
  animation: fadeUp 0.85s ease-out backwards;
}
.card:hover {
  transform: perspective(900px) rotateX(0deg) translateY(-8px) scale(1.02);
  box-shadow: 0 30px 55px rgba(0,0,0,0.65), 0 0 0 1px rgba(185,246,160,0.7), 0 0 30px rgba(185,246,160,0.25);
}
.card.neon { animation: fadeUp 0.85s ease-out backwards, borderGlow 3.2s ease-in-out 1s infinite; }
.card .label { font-size: 0.74rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8FA085 !important; }
.card .value { font-size: 1.7rem; font-weight: 700; margin: 0.3rem 0 0.15rem 0; color: #B9F6A0 !important; }
.card .value.plain { color: #E4EBDF !important; }
.card .sub { font-size: 0.82rem; color: #8FA085 !important; }
.card .tip-title { font-weight: 600; color: #B9F6A0 !important; margin-bottom: 0.35rem; }
.card .tip-text { font-size: 0.86rem; color: #E4EBDF !important; }
.badge {
  display: inline-block; padding: 0.2rem 0.8rem; border-radius: 999px; font-weight: 600; font-size: 0.95rem;
  border: 1px solid currentColor; background: rgba(255,255,255,0.03);
}
.note-box {
  margin-top: 0.8rem; padding: 0.8rem 1rem; border-radius: 14px; font-size: 0.92rem;
  background: rgba(156,175,136,0.08); border-left: 3px solid #B9F6A0; color: #E4EBDF;
}
.verdict {
  margin-top: 1rem; padding: 1rem 1.2rem; border-radius: 16px; font-size: 0.98rem;
  background: linear-gradient(145deg, rgba(185,246,160,0.12), rgba(156,175,136,0.06));
  box-shadow: 0 0 0 1px rgba(185,246,160,0.35), 0 0 24px rgba(185,246,160,0.12);
  animation: fadeUp 0.9s ease-out backwards;
}
.table-scroll { overflow-x: auto; }
table.cmp { width: 100%; min-width: 560px; border-collapse: separate; border-spacing: 0 8px; }
table.cmp th {
  text-align: left; padding: 0.5rem 0.9rem; font-size: 0.74rem; letter-spacing: 0.12em;
  text-transform: uppercase; color: #8FA085 !important; font-weight: 500;
}
table.cmp td {
  padding: 0.75rem 0.9rem; background: rgba(22,31,25,0.95); color: #E4EBDF !important;
  border-top: 1px solid rgba(156,175,136,0.15); border-bottom: 1px solid rgba(156,175,136,0.15);
}
table.cmp td:first-child { border-left: 1px solid rgba(156,175,136,0.15); border-radius: 12px 0 0 12px; font-weight: 600; }
table.cmp td:last-child { border-right: 1px solid rgba(156,175,136,0.15); border-radius: 0 12px 12px 0; }
table.cmp tr.sel td { background: rgba(185,246,160,0.10); border-color: rgba(185,246,160,0.5); }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stNumberInput input {
  background-color: #121915 !important; color: #E4EBDF !important;
  border: 1px solid rgba(156,175,136,0.35) !important; border-radius: 12px !important;
}
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover {
  border-color: #B9F6A0 !important; box-shadow: 0 0 14px rgba(185,246,160,0.25);
}
div[data-baseweb="popover"] ul, ul[role="listbox"] { background-color: #121915 !important; }
ul[role="listbox"] li, div[data-baseweb="popover"] li { color: #E4EBDF !important; background-color: #121915 !important; }
ul[role="listbox"] li:hover { background-color: #1d2a21 !important; }
span[data-baseweb="tag"] { background-color: #5F7253 !important; border-radius: 8px !important; }
span[data-baseweb="tag"] span { color: #F2FBEA !important; }
.stNumberInput button { background-color: #1a241d !important; color: #B9F6A0 !important; border-color: rgba(156,175,136,0.35) !important; }
div[data-testid="stCode"] pre { background-color: #121915 !important; border: 1px solid rgba(156,175,136,0.3); border-radius: 12px; }
div[data-testid="stExpander"] {
  border-radius: 16px; overflow: hidden; margin-top: 2.5rem;
  background: linear-gradient(145deg, rgba(28,38,31,0.95), rgba(14,20,16,0.95));
  box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(156,175,136,0.25);
  animation: fadeUp 0.9s ease-out backwards;
}
div[data-testid="stExpander"] details { border: none !important; background: transparent !important; }
div[data-testid="stExpander"] summary { color: #B9F6A0 !important; font-weight: 600; }
div[data-testid="stExpander"] summary:hover { color: #E4EBDF !important; }
@media (prefers-reduced-motion: reduce) {
  .leaves i, .card, .card.neon, .section-title, .verdict, div[data-testid="stExpander"] { animation: none !important; }
  .card, .card:hover { transform: none !important; }
}
</style>
<div class="leaves"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Animated components (HTML/CSS/JS rendered in sandboxed iframes)
# ------------------------------------------------------------------ #
HERO_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body { margin: 0; height: 100%; background: transparent; font-family: 'Poppins', 'Segoe UI', system-ui, sans-serif; }
.hero { position: absolute; top: 6px; left: 6px; right: 6px; bottom: 6px; border-radius: 22px; overflow: hidden;
  background: linear-gradient(145deg, #16211a, #0b0f0c);
  box-shadow: 0 0 0 1px rgba(156,175,136,0.3), 0 0 40px rgba(185,246,160,0.12);
  animation: rise 0.9s ease-out both; }
@keyframes rise { from { opacity: 0; transform: translateY(22px); } to { opacity: 1; transform: none; } }
@keyframes glow { 0%,100% { text-shadow: 0 0 8px rgba(185,246,160,0.4); } 50% { text-shadow: 0 0 22px rgba(185,246,160,0.85); } }
canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.txt { position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; padding: 0 18px; }
.tag { font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: #B9F6A0;
  border: 1px solid rgba(185,246,160,0.45); border-radius: 999px; padding: 4px 14px; margin-bottom: 12px; background: rgba(11,15,12,0.6); }
h1 { margin: 0 0 8px 0; font-size: clamp(1.45rem, 4.6vw, 2.7rem); font-weight: 700; line-height: 1.15;
  background: linear-gradient(90deg, #9CAF88, #B9F6A0, #9CAF88); -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent; animation: glow 3.5s ease-in-out infinite; }
p { margin: 0; color: #A9BBA0; font-size: clamp(0.82rem, 2.2vw, 1rem); max-width: 560px; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
</style></head><body>
<div class="hero"><canvas id="c"></canvas>
<div class="txt"><span class="tag">Fibre to fabric</span>
<h1>Textile Carbon Footprint Estimator</h1>
<p>Pick fabrics, set the weight, and see the estimated climate impact of your product.</p></div></div>
<script>
(function () {
  var cv = document.getElementById('c'), ctx = cv.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var t = 0;
  function resize() {
    var r = cv.getBoundingClientRect(), d = window.devicePixelRatio || 1;
    cv.width = Math.max(1, r.width * d); cv.height = Math.max(1, r.height * d);
    ctx.setTransform(d, 0, 0, d, 0, 0);
  }
  function draw() {
    var w = cv.clientWidth, h = cv.clientHeight, i, j, x, y, rows = 16, cols = 38;
    ctx.clearRect(0, 0, w, h);
    ctx.lineWidth = 2;
    for (i = 0; i < rows; i++) {
      ctx.beginPath();
      var y0 = (i + 0.5) * h / rows;
      for (x = 0; x <= w; x += 8) {
        y = y0 + Math.sin(x * 0.012 + t + i * 0.5) * 7;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(156,175,136,' + (0.10 + 0.07 * (i % 3)) + ')';
      ctx.stroke();
    }
    ctx.lineWidth = 1.5;
    for (j = 0; j < cols; j++) {
      ctx.beginPath();
      var x0 = (j + 0.5) * w / cols;
      for (y = 0; y <= h; y += 8) {
        x = x0 + Math.sin(y * 0.015 + t * 0.9 + j * 0.4) * 5;
        if (y === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(185,246,160,0.07)';
      ctx.stroke();
    }
    ctx.save();
    ctx.shadowBlur = 14; ctx.shadowColor = '#B9F6A0';
    ctx.strokeStyle = '#B9F6A0'; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (x = 0; x <= w; x += 6) {
      y = h * 0.5 + Math.sin(x * 0.01 - t * 1.6) * h * 0.3;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.restore();
    if (!reduce) { t += 0.02; requestAnimationFrame(draw); }
  }
  resize(); draw();
  window.addEventListener('resize', function () { resize(); if (reduce) draw(); });
})();
</script></body></html>"""

GAUGE_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html, body { margin: 0; background: transparent; font-family: 'Segoe UI', system-ui, sans-serif; color: #E4EBDF; }
.box { margin: 6px; padding: 14px 10px 14px; border-radius: 20px; text-align: center;
  background: linear-gradient(145deg, #1e2921, #0f1511);
  box-shadow: 0 0 0 1px rgba(185,246,160,0.35), 0 0 28px rgba(185,246,160,0.14); animation: rise 0.9s ease-out both; }
@keyframes rise { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
svg { width: 100%; max-width: 380px; height: auto; filter: drop-shadow(0 0 6px rgba(185,246,160,0.25)); }
.num { font-size: 2.2rem; font-weight: 700; color: #B9F6A0; text-shadow: 0 0 14px rgba(185,246,160,0.5);
  margin-top: -4px; font-variant-numeric: tabular-nums; }
.cap { font-size: 0.74rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8FA085; }
.badge { display: inline-block; margin-top: 8px; padding: 3px 14px; border-radius: 999px; border: 1px solid;
  font-weight: 700; font-size: 0.9rem; color: __COLOR__; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
</style></head><body>
<div class="box">
<svg id="g" viewBox="0 0 300 178" role="img" aria-label="Carbon intensity gauge"></svg>
<div class="num" id="n">__TOTAL_STR__</div>
<div class="cap">kg CO&#8322;e total</div>
<div class="badge">__LABEL__ intensity</div>
</div>
<script>
(function () {
  var V = __V__, TOTAL = __TOTAL__, MAXV = 14;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var zones = [[0, 3.5, '#B9F6A0'], [3.5, 7, '#F2C879'], [7, 11, '#F0A068'], [11, 14, '#FF8F7A']];
  function pt(a, r) { return [150 + r * Math.cos(a), 150 - r * Math.sin(a)]; }
  function arc(v0, v1, r) {
    var a0 = Math.PI * (1 - v0 / MAXV), a1 = Math.PI * (1 - v1 / MAXV), p0 = pt(a0, r), p1 = pt(a1, r);
    return 'M' + p0[0].toFixed(2) + ' ' + p0[1].toFixed(2) + ' A' + r + ' ' + r + ' 0 0 1 ' + p1[0].toFixed(2) + ' ' + p1[1].toFixed(2);
  }
  var s = '';
  zones.forEach(function (z) {
    s += '<path d="' + arc(z[0] + 0.06, z[1] - 0.06, 110) + '" stroke="' + z[2] + '" stroke-width="16" fill="none" opacity="0.88"/>';
  });
  s += '<text x="34" y="170" fill="#8FA085" font-size="11" text-anchor="middle">0</text>';
  s += '<text x="150" y="24" fill="#8FA085" font-size="11" text-anchor="middle">7</text>';
  s += '<text x="266" y="170" fill="#8FA085" font-size="11" text-anchor="middle">14+</text>';
  s += '<g id="needle" style="transform-origin:150px 150px;transform:rotate(-90deg);transition:transform 1.6s cubic-bezier(.2,.9,.2,1)">' +
       '<line x1="150" y1="150" x2="150" y2="50" stroke="#E4EBDF" stroke-width="3" stroke-linecap="round"/></g>' +
       '<circle cx="150" cy="150" r="9" fill="#B9F6A0"/><circle cx="150" cy="150" r="3.5" fill="#0b0f0c"/>';
  document.getElementById('g').innerHTML = s;
  var needle = document.getElementById('needle');
  var target = -90 + 180 * Math.min(Math.max(V, 0), MAXV) / MAXV;
  if (reduce) { needle.style.transition = 'none'; needle.style.transform = 'rotate(' + target + 'deg)'; }
  else { setTimeout(function () { needle.style.transform = 'rotate(' + target + 'deg)'; }, 200); }
  var el = document.getElementById('n');
  function fmt(x) { return x.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  if (!reduce) {
    var start = null, dur = 1500;
    var step = function (now) {
      if (start === null) start = now;
      var p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(TOTAL * e);
      if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(TOTAL);
    };
    requestAnimationFrame(step);
  }
})();
</script></body></html>"""

TILE_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html, body { margin: 0; background: transparent; font-family: 'Segoe UI', system-ui, sans-serif; color: #E4EBDF; }
.tile { margin: 6px; padding: 14px 12px; border-radius: 18px; text-align: center;
  background: linear-gradient(145deg, #1e2921, #0f1511);
  box-shadow: 0 0 0 1px rgba(156,175,136,0.28), 0 14px 28px rgba(0,0,0,0.5); animation: rise 0.8s ease-out both; }
@keyframes rise { from { opacity: 0; transform: translateY(22px); } to { opacity: 1; transform: none; } }
@keyframes sway { from { transform: rotate(-7deg); } to { transform: rotate(7deg); } }
@keyframes puff { 0%,100% { transform: scale(1); } 50% { transform: scale(1.09); } }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.sway { transform-origin: 40px 70px; animation: sway 3s ease-in-out infinite alternate; }
.puff { transform-origin: 40px 46px; animation: puff 2.6s ease-in-out infinite; }
.spin { transform-origin: 40px 40px; animation: spi"""
