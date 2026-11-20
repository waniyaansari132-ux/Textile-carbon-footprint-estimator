<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fiberprint Carbon Estimator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
Layout: headline, then controls beside a 3D fabric roll, then 3D comparison bars beside a ranked list. Single dark digital theme by choice
:root {
  --bg: #050912;
  --panel: rgba(13, 22, 44, 0.78);
  --line: rgba(120, 170, 255, 0.22);
  --text: #e8f0ff;
  --muted: #93a8cc;
  --accent: #22e0ff;
  --accent-2: #b26bff;
  --warn: #ff5c8a;
  --good: #5cf2a6;
  --display: "Chakra Petch", "Segoe UI", sans-serif;
  --body: "Manrope", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  color-scheme: dark;
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
html, body { margin: 0; }
body {
  background:
    radial-gradient(900px 500px at 85% -5%, rgba(178, 107, 255, 0.18), transparent 60%),
    radial-gradient(800px 500px at -5% 10%, rgba(34, 224, 255, 0.14), transparent 60%),
    linear-gradient(rgba(120, 170, 255, 0.05) 1px, transparent 1px) 0 0 / 44px 44px,
    linear-gradient(90deg, rgba(120, 170, 255, 0.05) 1px, transparent 1px) 0 0 / 44px 44px,
    var(--bg);
  color: var(--text);
  font-family: var(--body);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 20px 56px; }
header.top { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 18px 0; }
.brand { font-family: var(--display); font-weight: 700; letter-spacing: 0.16em; font-size: 15px; display: flex; align-items: center; gap: 10px; }
.brand i { width: 12px; height: 12px; background: var(--accent); box-shadow: 0 0 14px var(--accent); transform: rotate(45deg); display: block; }
.status { font-family: var(--mono); font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 8px; }
.status b { width: 8px; height: 8px; border-radius: 50%; background: var(--good); box-shadow: 0 0 10px var(--good); display: block; animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 50% { opacity: 0.35; } }

h1 { font-family: var(--display); font-weight: 700; font-size: clamp(30px, 5.2vw, 54px); line-height: 1.05; margin: 14px 0 12px; max-width: 18ch; text-wrap: balance; }
h1 span { color: var(--accent); text-shadow: 0 0 24px rgba(34, 224, 255, 0.45); }
.lede { color: var(--muted); max-width: 62ch; margin: 0 0 26px; font-size: 17px; }

.stage { display: grid; grid-template-columns: minmax(300px, 420px) 1fr; gap: 20px; align-items: stretch; }
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
.controls { padding: 20px; display: flex; flex-direction: column; gap: 20px; }
.label { font-family: var(--mono); font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin: 0 0 10px; padding: 0; display: block; }
fieldset { border: 0; margin: 0; padding: 0; min-width: 0; }

.seg { display: inline-grid; grid-auto-flow: column; gap: 2px; border: 1px solid var(--line); border-radius: 10px; padding: 3px; background: rgba(8, 14, 30, 0.8); }
.seg label { position: relative; display: block; }
.seg input { position: absolute; opacity: 0; inset: 0; width: 100%; height: 100%; margin: 0; cursor: pointer; }
.seg span { display: block; padding: 7px 14px; border-radius: 7px; font-family: var(--mono); font-size: 12px; color: var(--muted); transition: all 0.15s; white-space: nowrap; }
.seg input:checked + span { background: rgba(34, 224, 255, 0.16); color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
.seg input:focus-visible + span { outline: 2px solid var(--accent); outline-offset: 1px; }
.seg.full { display: grid; grid-auto-flow: row; grid-template-columns: 1fr 1fr; }
.seg.full span { text-align: center; }
.rowhead { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 10px; }
.rowhead .label { margin: 0; }

.fibers { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.fiber { position: relative; display: block; }
.fiber input { position: absolute; opacity: 0; inset: 0; width: 100%; height: 100%; margin: 0; cursor: pointer; }
.fiber .face {
  display: grid; grid-template-columns: 20px 1fr; gap: 10px; align-items: center; height: 100%;
  padding: 10px 11px; border-radius: 10px; border: 1px solid var(--line);
  background: rgba(8, 14, 30, 0.7); transition: border-color 0.15s, background 0.15s, box-shadow 0.15s, transform 0.15s;
}
.fiber:hover .face { border-color: rgba(34, 224, 255, 0.5); transform: translateY(-1px); }
.fiber input:focus-visible + .face { outline: 2px solid var(--accent); outline-offset: 2px; }
.fiber input:checked + .face { border-color: var(--accent); background: rgba(34, 224, 255, 0.09); box-shadow: 0 0 0 1px var(--accent), 0 0 26px rgba(34, 224, 255, 0.18); }
.sw { width: 20px; height: 20px; border-radius: 6px; box-shadow: inset 0 -6px 10px rgba(0, 0, 0, 0.3), 0 0 12px var(--c); background: var(--c); }
.fname { font-weight: 600; font-size: 13.5px; line-height: 1.25; }
.fnote { display: block; font-family: var(--mono); font-size: 11px; color: var(--muted); font-weight: 400; margin-top: 2px; }
.about { font-size: 13px; color: var(--muted); margin: 12px 0 0; min-height: 3em; }
.about strong { color: var(--text); }

.blend { display: grid; gap: 10px; padding: 14px; border: 1px dashed rgba(34, 224, 255, 0.45); border-radius: 12px; background: rgba(34, 224, 255, 0.04); }
select { width: 100%; background: rgba(8, 14, 30, 0.9); color: var(--text); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; font-family: var(--body); font-size: 15px; }
select:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.pctrow { display: flex; justify-content: space-between; align-items: baseline; }
.pctrow .label { margin: 0; }
.pctrow output { font-family: var(--mono); color: var(--text); font-size: 14px; }

.numwrap { display: flex; align-items: center; background: rgba(8, 14, 30, 0.8); border: 1px solid var(--line); border-radius: 10px; padding: 0 12px; }
.numwrap:focus-within { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.numwrap input { width: 100%; background: transparent; border: 0; color: var(--text); font-family: var(--mono); font-size: 26px; font-weight: 500; padding: 10px 0; outline: none; font-variant-numeric: tabular-nums; }
.numwrap span { font-family: var(--mono); color: var(--muted); }
input[type="range"] { -webkit-appearance: none; appearance: none; width: 100%; height: 28px; background: transparent; margin: 10px 0 0; cursor: pointer; }
input[type="range"]::-webkit-slider-runnable-track { height: 6px; border-radius: 6px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); box-shadow: 0 0 14px rgba(34, 224, 255, 0.35); }
input[type="range"]::-moz-range-track { height: 6px; border-radius: 6px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }
input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%; background: #fff; border: 3px solid var(--accent); margin-top: -8px; box-shadow: 0 0 16px var(--accent); }
input[type="range"]::-moz-range-thumb { width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 3px solid var(--accent); }
input[type="range"]:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 6px; }
.ticks { position: relative; height: 18px; font-family: var(--mono); font-size: 11px; color: var(--muted); margin: 0 11px; }
.ticks span { position: absolute; top: 0; transform: translateX(-50%); white-space: nowrap; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.chip { font-family: var(--mono); font-size: 12px; color: var(--text); background: rgba(8, 14, 30, 0.8); border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px; cursor: pointer; transition: all 0.15s; }
.chip:hover { border-color: var(--accent); color: var(--accent); }
.chip:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.viewport { position: relative; min-height: 480px; overflow: hidden; }
.viewport::before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 120px; background: linear-gradient(180deg, transparent, rgba(34, 224, 255, 0.07), transparent); animation: sweep 6s linear infinite; pointer-events: none; }
@keyframes sweep { from { transform: translateY(-120px); } to { transform: translateY(560px); } }
.viewport::after { content: ""; position: absolute; inset: 0; pointer-events: none; background: repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.022) 0 1px, transparent 1px 3px); }
.viewport canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; touch-action: pan-y; cursor: grab; }
.viewport canvas:active { cursor: grabbing; }
.hud { position: absolute; left: 22px; top: 20px; right: 22px; pointer-events: none; z-index: 2; }
.hud .k { font-family: var(--mono); font-size: 12px; letter-spacing: 0.14em; color: var(--accent); text-transform: uppercase; }
.hud .big { font-family: var(--display); font-weight: 700; font-size: clamp(44px, 7vw, 76px); line-height: 1; font-variant-numeric: tabular-nums; text-shadow: 0 0 30px rgba(34, 224, 255, 0.5); margin-top: 6px; }
.hud .unit { font-family: var(--mono); font-size: 14px; color: var(--muted); margin-top: 6px; }
.hud .for { font-size: 13px; color: var(--muted); margin-top: 2px; max-width: 34ch; }
.corner { position: absolute; width: 22px; height: 22px; border: 2px solid var(--accent); opacity: 0.7; pointer-events: none; z-index: 2; }
.corner.tl { top: 10px; left: 10px; border-right: 0; border-bottom: 0; }
.corner.tr { top: 10px; right: 10px; border-left: 0; border-bottom: 0; }
.corner.bl { bottom: 10px; left: 10px; border-right: 0; border-top: 0; }
.corner.br { bottom: 10px; right: 10px; border-left: 0; border-top: 0; }
.hint { position: absolute; right: 22px; bottom: 18px; font-family: var(--mono); font-size: 11px; color: var(--muted); pointer-events: none; z-index: 2; }
.nogl { display: none; position: absolute; inset: 0; align-items: center; justify-content: center; text-align: center; padding: 24px; color: var(--muted); font-size: 14px; z-index: 2; }
.viewport.fallback .nogl { display: flex; }
.viewport.fallback canvas, .viewport.fallback .hint { display: none; }

.compare { display: grid; grid-template-columns: 1fr minmax(320px, 470px); gap: 20px; margin-top: 20px; align-items: stretch; }
.compare .viewport { min-height: 440px; }
.tag { position: absolute; transform: translate(-50%, -50%); font-family: var(--mono); font-size: 12px; white-space: nowrap; pointer-events: none; z-index: 2; }
.tag.val { background: rgba(5, 9, 18, 0.82); border: 1px solid var(--line); border-radius: 6px; padding: 2px 7px; color: var(--text); }
.tag.val.on { border-color: var(--accent); color: var(--accent); box-shadow: 0 0 14px rgba(34, 224, 255, 0.3); }
.tag.nm { color: var(--muted); letter-spacing: 0.06em; font-size: 11px; }
.tag.nm.on { color: var(--accent); }

.results { padding: 20px; display: flex; flex-direction: column; gap: 18px; }
.rows { display: grid; gap: 7px; }
.row { display: grid; grid-template-columns: 14px 1fr auto; gap: 3px 12px; align-items: center; text-align: left; width: 100%; font: inherit; color: inherit; background: rgba(8, 14, 30, 0.7); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; cursor: pointer; transition: border-color 0.15s; }
.row:hover { border-color: rgba(34, 224, 255, 0.5); }
.row:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.row.on { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.row .dot { width: 12px; height: 12px; border-radius: 3px; background: var(--c); box-shadow: 0 0 10px var(--c); }
.row .rn { font-size: 14px; font-weight: 600; }
.row .rv { font-family: var(--mono); font-size: 14px; font-variant-numeric: tabular-nums; text-align: right; }
.meter { grid-column: 2 / 4; height: 5px; background: rgba(120, 170, 255, 0.12); border-radius: 6px; overflow: hidden; }
.meter i { display: block; height: 100%; background: var(--c); border-radius: 6px; box-shadow: 0 0 10px var(--c); transition: width 0.5s cubic-bezier(.2, .8, .2, 1); }
.delta { grid-column: 2 / 4; font-family: var(--mono); font-size: 11.5px; color: var(--muted); }
.delta.up { color: var(--warn); }
.delta.down { color: var(--good); }

.save { border: 1px solid rgba(92, 242, 166, 0.45); background: rgba(92, 242, 166, 0.08); border-radius: 12px; padding: 14px 16px; font-size: 15px; }
.save strong { color: var(--good); font-family: var(--display); font-size: 17px; }
.save p { margin: 0; }
.save p + p { margin-top: 8px; font-size: 13.5px; color: var(--muted); }
.eq { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.eq div { border: 1px solid var(--line); border-radius: 12px; padding: 12px; background: rgba(8, 14, 30, 0.6); }
.eq b { display: block; font-family: var(--display); font-size: 22px; font-variant-numeric: tabular-nums; }
.eq span { font-size: 12px; color: var(--muted); line-height: 1.35; display: block; margin-top: 2px; }
.actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.btn { font-family: var(--display); font-weight: 600; font-size: 14px; letter-spacing: 0.04em; color: #03121a; background: linear-gradient(90deg, var(--accent), #7de9ff); border: 0; border-radius: 10px; padding: 11px 18px; cursor: pointer; box-shadow: 0 0 22px rgba(34, 224, 255, 0.4); }
.btn:hover { filter: brightness(1.1); }
.btn:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
#copyMsg { font-family: var(--mono); font-size: 12px; color: var(--good); }
textarea { width: 100%; background: rgba(8, 14, 30, 0.9); color: var(--text); border: 1px solid var(--line); border-radius: 10px; padding: 10px; font-family: var(--mono); font-size: 12px; resize: none; }

.method { margin-top: 20px; padding: 22px; }
.method h2 { font-family: var(--display); font-size: 22px; margin: 0 0 8px; }
.method p { color: var(--muted); max-width: 80ch; margin: 0 0 10px; }
.method p strong { color: var(--text); }
footer { color: var(--muted); font-size: 12.5px; font-family: var(--mono); margin-top: 22px; }

@media (max-width: 900px) {
  .stage, .compare { grid-template-columns: 1fr; }
  .viewport { min-height: 420px; }
  .compare .viewport { min-height: 400px; }
}
@media (max-width: 600px) {
  .tag.val:not(.on) { display: none; }
}
@media (max-width: 480px) {
  .wrap { padding: 0 16px 40px; }
  .eq { grid-template-columns: 1fr; }
  .eq div { display: flex; align-items: baseline; gap: 12px; }
  .eq b { min-width: 90px; }
  .hud { left: 16px; top: 16px; }
}
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand"><i></i>FIBERPRINT</div>
    <div class="status"><b></b>Live estimate</div>
  </header>

  <h1>Textile Carbon <span>Footprint</span> Estimator</h1>
  <p class="lede">Select fiber type and fabric weight (kg) to estimate approximate CO₂ emissions and compare cotton, polyester and recycled fibers.</p>

  <section class="stage" aria-label="Estimator">
    <div class="card controls">
      <div>
        <p class="label" id="modeLabel">Mode</p>
        <div class="seg full" role="radiogroup" aria-labelledby="modeLabel">
          <label><input type="radio" name="mode" value="single" checked><span>Single fiber</span></label>
          <label><input type="radio" name="mode" value="blend"><span>Blend two fibers</span></label>
        </div>
      </div>

      <fieldset>
        <legend class="label" id="fiberLegend">01 · Fiber type</legend>
        <div class="fibers" id="fibers" role="radiogroup" aria-labelledby="fiberLegend"></div>
        <p class="about" id="about"></p>
      </fieldset>

      <div class="blend" id="blendBox" hidden>
        <div>
          <label class="label" for="fiber2">Blend with</label>
          <select id="fiber2"></select>
        </div>
        <div>
          <div class="pctrow"><label class="label" for="pct">Share of second fiber</label><output id="pctOut" for="pct">35%</output></div>
          <input id="pct" type="range" min="5" max="95" step="5" value="35">
        </div>
      </div>

      <div>
        <div class="rowhead">
          <p class="label" id="wlabel">02 · Fabric weight</p>
          <div class="seg" role="radiogroup" aria-label="Weight unit">
            <label><input type="radio" name="unit" value="kg" checked><span>kg</span></label>
            <label><input type="radio" name="unit" value="lb"><span>lb</span></label>
          </div>
        </div>
        <div class="numwrap">
          <input id="weight" type="number" inputmode="decimal" min="0.1" max="10000" step="any" value="25" aria-labelledby="wlabel">
          <span id="unitTag">kg</span>
        </div>
        <input id="slider" type="range" min="0" max="1000" step="1" aria-label="Fabric weight slider, logarithmic scale">
        <div class="ticks" id="ticks" aria-hidden="true"></div>
        <div class="chips" id="chips" aria-label="Weight presets"></div>
      </div>
    </div>

    <div class="card viewport" id="heroVp">
      <canvas id="heroCanvas" aria-label="3D fabric roll that changes size and color with your selection"></canvas>
      <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
      <div class="hud" aria-live="polite">
        <div class="k">Estimated emissions</div>
        <div class="big" id="bigNum">0</div>
        <div class="unit">kg CO₂e <span id="tonnes"></span></div>
        <div class="for" id="forText"></div>
      </div>
      <div class="hint">DRAG TO ROTATE</div>
      <div class="nogl">The 3D view is not available in this browser. The numbers still work.</div>
    </div>
  </section>

  <section class="compare" aria-label="Fiber comparison">
    <div class="card viewport" id="barVp">
      <canvas id="barCanvas" aria-label="3D bar chart comparing emissions for each fiber at the chosen weight"></canvas>
      <div id="barLabels" aria-hidden="true"></div>
      <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
      <div class="hint">SAME WEIGHT · DRAG TO ROTATE</div>
      <div class="nogl">The 3D chart is not available in this browser. Use the list on the right.</div>
    </div>
    <div class="card results">
      <div>
        <p class="label">03 · Compare at <span id="cmpW">25 kg</span> · lowest first</p>
        <div class="rows" id="rows"></div>
      </div>
      <div class="save" id="save"></div>
      <div>
        <p class="label">What this equals</p>
        <div class="eq" id="eq"></div>
      </div>
      <div>
        <div class="actions">
          <button class="btn" id="copyBtn" type="button">Copy summary</button>
          <span id="copyMsg" role="status"></span>
        </div>
        <textarea id="sumTa" rows="4" readonly hidden aria-label="Summary text"></textarea>
      </div>
    </div>
  </section>

  <section class="card method">
    <h2>How the estimate works</h2>
    <p><strong>Emissions = fabric weight (kg) × emission factor (kg CO₂e per kg of fabric).</strong> Each fiber has one factor, shown on its card. A blend uses the weighted average of its two factors. CO₂e means carbon dioxide equivalent, which puts every greenhouse gas on one scale.<
