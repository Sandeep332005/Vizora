import json

def render_perspective_workbench(height: int = 1000) -> str:
    """Renders the exact FINOS Perspective / Vizora dark workbench interface
    matching uploaded_media_1794473944758.jpg with:
    - Fixed left sidebar (PERSPECTIVE wordmark, Import Data, telemetry indicators, Configure Agent)
    - 6-column gallery grid with all 24 visual cards (Superstore, Mandelbrot, Raycasting, NYPD, SF Evictions, Market, Webcam, etc.)
    - Live HTML5 Canvas renderers for each card
    - Interactive full workspace view on card click (Candlestick + Order Book + Blotter, Density Cam, Datagrid)
    - Dockable DUCKDB SQL console panel with live query engine
    - Bottom command bar with blue glow border (SELECT ... ⌘⏎ to run) and white Run button
    - Import Data and Configure Agent modals
    """
    return _HTML_CONTENT.replace("__HEIGHT__", str(height))


_HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PERSPECTIVE / VIZORA</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg-canvas: #111215;
  --bg-sidebar: #16171c;
  --bg-card: #16171c;
  --bg-card-canvas: #0e0f12;
  --border-rule: #282a33;
  --border-rule-subtle: #1f2128;
  --border-focus: #3b82f6;
  --text-primary: #e6e8ec;
  --text-secondary: #9da1ab;
  --text-muted: #6b707d;
  --status-ready: #3fb950;
  --status-notstarted: #6b707d;
  --accent-cyan: #58a6ff;
  --accent-lime: #e4f266;
  --accent-orange: #f0883e;
  --accent-purple: #bc8cff;
  --accent-coral: #f85149;
  --font-body: "Geologica", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background-color: var(--bg-canvas);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-weight: 400;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  user-select: none;
}

#app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: var(--bg-canvas);
}

/* ─── LEFT SIDEBAR ─── */
#sidebar {
  width: 250px;
  min-width: 250px;
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--border-rule);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px 16px;
  z-index: 10;
}

.sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.brand-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.brand-title {
  font-family: var(--font-body);
  font-size: 19px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--text-primary);
}

.brand-links {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.brand-links a {
  color: var(--text-muted);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.15s;
}

.brand-links a:hover {
  color: var(--text-primary);
}

.brand-icons {
  margin-left: auto;
  display: flex;
  gap: 6px;
  color: var(--text-muted);
  cursor: pointer;
}

.btn-import {
  background-color: transparent;
  border: 1px solid var(--border-rule);
  border-radius: 4px;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 400;
  padding: 8px 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
}

.btn-import:hover {
  background-color: #1f2128;
  border-color: #3e4250;
}

.status-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 6px;
}

.status-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-primary);
}

.status-dot-wrap {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-muted);
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.not-started { background-color: var(--status-notstarted); }
.status-dot.ready { background-color: var(--status-ready); }

.tag-sql {
  background-color: transparent;
  border: 1px solid var(--border-rule);
  border-radius: 3px;
  padding: 1px 4px;
  font-size: 9px;
  color: var(--text-secondary);
  margin-left: 4px;
}

.status-sub {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.sidebar-bottom {
  padding-top: 12px;
}

.btn-configure {
  background-color: transparent;
  border: 1px solid var(--border-rule);
  border-radius: 4px;
  color: var(--text-secondary);
  font-family: var(--font-body);
  font-size: 13px;
  padding: 8px 14px;
  text-align: center;
  cursor: pointer;
  width: 100%;
  transition: all 0.15s ease;
}

.btn-configure:hover {
  background-color: #1f2128;
  color: var(--text-primary);
  border-color: #3e4250;
}

/* ─── MAIN CONTENT AREA ─── */
#main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* ─── GALLERY GRID ─── */
#gallery-viewport {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 10px 14px 10px 14px;
  scrollbar-width: thin;
  scrollbar-color: var(--border-rule) var(--bg-canvas);
}

#gallery-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  width: 100%;
}

.gallery-card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-rule);
  border-radius: 3px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.12s ease, border-color 0.12s ease;
}

.gallery-card:hover {
  border-color: #434757;
  transform: translateY(-1px);
}

.card-canvas-box {
  width: 100%;
  aspect-ratio: 16 / 10.5;
  background-color: var(--bg-card-canvas);
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border-rule-subtle);
}

.card-canvas-box canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.card-caption {
  padding: 5px 8px 6px;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 400;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ─── TOOLTIP POPUP ─── */
#card-tooltip {
  position: fixed;
  background: rgba(18, 19, 24, 0.95);
  border: 1px solid var(--border-rule);
  border-radius: 4px;
  padding: 7px 11px;
  font-size: 11px;
  color: var(--text-primary);
  pointer-events: none;
  z-index: 1000;
  display: none;
  max-width: 260px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
  line-height: 1.4;
}

/* ─── DUCKDB SQL DRAWER ─── */
#duckdb-panel {
  background-color: #131418;
  border-top: 1px solid var(--border-rule);
  display: flex;
  flex-direction: column;
  max-height: 160px;
  min-height: 120px;
  transition: height 0.2s ease;
  overflow: hidden;
}

#duckdb-panel.collapsed {
  height: 26px !important;
  min-height: 26px !important;
}

.duckdb-header {
  height: 26px;
  padding: 0 12px;
  background-color: #17181f;
  border-bottom: 1px solid var(--border-rule-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
}

.duckdb-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 12px;
  padding: 2px 4px;
}

.btn-icon:hover { color: var(--text-primary); }

.duckdb-body {
  flex: 1;
  overflow: auto;
  padding: 6px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
}

table.sql-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}

table.sql-table th {
  text-align: left;
  padding: 4px 8px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-rule);
  font-weight: 500;
}

table.sql-table td {
  padding: 4px 8px;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-rule-subtle);
}

/* ─── BOTTOM COMMAND BAR ─── */
#command-bar {
  height: 48px;
  border-top: 1px solid var(--border-rule);
  background-color: var(--bg-sidebar);
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 10px;
  z-index: 20;
}

.prompt-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background-color: #131418;
  border: 1px solid var(--border-focus);
  box-shadow: 0 0 6px rgba(59, 130, 246, 0.35);
  border-radius: 4px;
  height: 34px;
  padding: 0 10px;
}

.prompt-input-wrapper input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 12px;
}

.prompt-input-wrapper input::placeholder {
  color: var(--text-muted);
}

.btn-run {
  background-color: #ffffff;
  color: #111215;
  border: none;
  border-radius: 4px;
  height: 34px;
  padding: 0 16px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.15s;
}

.btn-run:hover {
  background-color: #e5e7eb;
}

/* ─── WORKSPACE FULLSCREEN OVERLAY ─── */
#workspace-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-canvas);
  z-index: 50;
  display: none;
  flex-direction: column;
}

.workspace-topbar {
  height: 38px;
  background-color: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-rule);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  font-family: var(--font-mono);
  font-size: 12px;
}

.ws-tabs {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 100%;
}

.ws-tab {
  padding: 0 12px;
  height: 28px;
  display: flex;
  align-items: center;
  background: #1c1d24;
  border: 1px solid var(--border-rule);
  border-radius: 3px;
  color: var(--text-primary);
  font-size: 11px;
  cursor: pointer;
}

.ws-tab.active {
  border-color: var(--accent-cyan);
  color: var(--accent-cyan);
}

.ws-main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.ws-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px;
  overflow: hidden;
}

.ws-drawer {
  width: 280px;
  background-color: var(--bg-sidebar);
  border-left: 1px solid var(--border-rule);
  display: flex;
  flex-direction: column;
  padding: 12px;
  gap: 12px;
  overflow-y: auto;
  font-size: 11px;
}

.drawer-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-rule);
  gap: 12px;
  padding-bottom: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.drawer-tabs span.active {
  color: var(--text-primary);
  border-bottom: 2px solid var(--accent-cyan);
  padding-bottom: 4px;
}

.drawer-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.drawer-field label {
  color: var(--text-muted);
  font-size: 10px;
  font-family: var(--font-mono);
  text-transform: uppercase;
}

.drawer-field select, .drawer-field input {
  background: #111215;
  border: 1px solid var(--border-rule);
  border-radius: 3px;
  color: var(--text-primary);
  padding: 6px 8px;
  font-size: 11px;
  font-family: var(--font-mono);
}

/* Modals */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-box {
  width: 440px;
  background: var(--bg-sidebar);
  border: 1px solid var(--border-rule);
  border-radius: 4px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-primary);
}

.file-dropzone {
  border: 1px dashed var(--border-rule);
  border-radius: 4px;
  padding: 28px;
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
  cursor: pointer;
}

.file-dropzone:hover {
  border-color: var(--accent-cyan);
  color: var(--text-primary);
}
</style>
</head>
<body>

<div id="app-container">
  <!-- LEFT SIDEBAR -->
  <aside id="sidebar">
    <div class="sidebar-top">
      <div class="brand-header">
        <div class="brand-title">PERSPECTIVE</div>
        <div class="brand-links">
          <a>About</a>
          <a>Docs</a>
          <a>GitHub</a>
          <div class="brand-icons">
            <span>&#9788;</span>
            <span>&laquo;</span>
          </div>
        </div>
      </div>

      <button class="btn-import" onclick="openImportModal()">Import Data</button>

      <div class="status-section">
        <div class="status-block">
          <div class="status-header">
            <span>perspective-server</span>
            <span class="status-dot-wrap"><span class="status-dot not-started"></span> not started</span>
          </div>
          <div class="status-sub">No sources loaded</div>
        </div>

        <div class="status-block">
          <div class="status-header">
            <span>DuckDB-WASM <span class="tag-sql">SQL</span></span>
            <span class="status-dot-wrap"><span class="status-dot ready"></span> ready</span>
          </div>
          <div class="status-sub">No sources loaded</div>
        </div>
      </div>
    </div>

    <div class="sidebar-bottom">
      <button class="btn-configure" onclick="openAgentModal()">Configure Agent</button>
    </div>
  </aside>

  <!-- MAIN AREA -->
  <main id="main-area">
    <!-- 24-CARD GALLERY VIEWPORT -->
    <section id="gallery-viewport">
      <div id="gallery-grid">
        <!-- Row 1 -->
        <div class="gallery-card" data-idx="0" data-name="Superstore" data-tip="Full virtualized datagrid with sales, profits, and categories">
          <div class="card-canvas-box"><canvas id="c-0"></canvas></div>
          <div class="card-caption">Superstore</div>
        </div>
        <div class="gallery-card" data-idx="1" data-name="Superstore (Workspace)" data-tip="Multi-split analytics workspace with regional maps and pivot trees">
          <div class="card-canvas-box"><canvas id="c-1"></canvas></div>
          <div class="card-caption">Superstore (Workspace)</div>
        </div>
        <div class="gallery-card" data-idx="2" data-name="Mandelbrot" data-tip="Mathematical Mandelbrot fractal set rendered in realtime">
          <div class="card-canvas-box"><canvas id="c-2"></canvas></div>
          <div class="card-caption">Mandelbrot</div>
        </div>
        <div class="gallery-card" data-idx="3" data-name="Raycasting" data-tip="Interactive 3D shaded torus with real-time normal raycasting">
          <div class="card-canvas-box"><canvas id="c-3"></canvas></div>
          <div class="card-caption">Raycasting</div>
        </div>
        <div class="gallery-card" data-idx="4" data-name="NYPD CCRB" data-tip="Civilian complaints against NYPD officers with officer metadata">
          <div class="card-canvas-box"><canvas id="c-4"></canvas></div>
          <div class="card-caption">NYPD CCRB</div>
        </div>
        <div class="gallery-card" data-idx="5" data-name="NYPD CCRB" data-tip="Dense incident distribution scatter blotter">
          <div class="card-canvas-box"><canvas id="c-5"></canvas></div>
          <div class="card-caption">NYPD CCRB</div>
        </div>

        <!-- Row 2 -->
        <div class="gallery-card" data-idx="6" data-name="NYPD CCRB" data-tip="Stacked monthly incident counts and severity heatmaps">
          <div class="card-canvas-box"><canvas id="c-6"></canvas></div>
          <div class="card-caption">NYPD CCRB</div>
        </div>
        <div class="gallery-card" data-idx="7" data-name="NYPD CCRB" data-tip="Multi-line allegation trajectory series over time">
          <div class="card-canvas-box"><canvas id="c-7"></canvas></div>
          <div class="card-caption">NYPD CCRB</div>
        </div>
        <div class="gallery-card" data-idx="8" data-name="SF Evictions" data-tip="San Francisco eviction notice density and geographical contours">
          <div class="card-canvas-box"><canvas id="c-8"></canvas></div>
          <div class="card-caption">SF Evictions</div>
        </div>
        <div class="gallery-card" data-idx="9" data-name="SF Evictions" data-tip="Categorical dot scatter map of city property notices">
          <div class="card-canvas-box"><canvas id="c-9"></canvas></div>
          <div class="card-caption">SF Evictions</div>
        </div>
        <div class="gallery-card" data-idx="10" data-name="Movies" data-tip="Production budget vs worldwide gross with marginal density bars">
          <div class="card-canvas-box"><canvas id="c-10"></canvas></div>
          <div class="card-caption">Movies</div>
        </div>
        <div class="gallery-card" data-idx="11" data-name="Olympics" data-tip="Multi-sport athlete height vs weight clusters">
          <div class="card-canvas-box"><canvas id="c-11"></canvas></div>
          <div class="card-caption">Olympics</div>
        </div>

        <!-- Row 3 -->
        <div class="gallery-card" data-idx="12" data-name="Market" data-tip="Simulated real-time order flow and matching engine mirrored to the UI">
          <div class="card-canvas-box"><canvas id="c-12"></canvas></div>
          <div class="card-caption">Market</div>
        </div>
        <div class="gallery-card" data-idx="13" data-name="Market - Themed" data-tip="High-contrast candlestick price series with order book depth">
          <div class="card-canvas-box"><canvas id="c-13"></canvas></div>
          <div class="card-caption">Market - Themed</div>
        </div>
        <div class="gallery-card" data-idx="14" data-name="Market - Orders" data-tip="Depth over time, price-level heatmap and closed orders from the same feed">
          <div class="card-canvas-box"><canvas id="c-14"></canvas></div>
          <div class="card-caption">Market - Orders</div>
        </div>
        <div class="gallery-card" data-idx="15" data-name="Market - Orders Themed" data-tip="Themed depth timeseries with multi-tier bid/ask order volume">
          <div class="card-canvas-box"><canvas id="c-15"></canvas></div>
          <div class="card-caption">Market - Orders Themed</div>
        </div>
        <div class="gallery-card" data-idx="16" data-name="Webcam - Video Wall" data-tip="Realtime video wall stream with thermal colormap and histogram">
          <div class="card-canvas-box"><canvas id="c-16"></canvas></div>
          <div class="card-caption">Webcam - Video Wall</div>
        </div>
        <div class="gallery-card" data-idx="17" data-name="Webcam - Video Wall Them..." data-tip="Emerald night-vision thermal camera colormap projection">
          <div class="card-canvas-box"><canvas id="c-17"></canvas></div>
          <div class="card-caption">Webcam - Video Wall Them...</div>
        </div>

        <!-- Row 4 -->
        <div class="gallery-card" data-idx="18" data-name="Market - Heatmap" data-tip="Time-series bid/ask price level density heatmap">
          <div class="card-canvas-box"><canvas id="c-18"></canvas></div>
          <div class="card-caption">Market - Heatmap</div>
        </div>
        <div class="gallery-card" data-idx="19" data-name="Market - Heatmap (Closed)" data-tip="Completed and executed orders price level density">
          <div class="card-canvas-box"><canvas id="c-19"></canvas></div>
          <div class="card-caption">Market - Heatmap (Closed)</div>
        </div>
        <div class="gallery-card" data-idx="20" data-name="Closed Orders" data-tip="Scatter trajectory of closed execution ticks">
          <div class="card-canvas-box"><canvas id="c-20"></canvas></div>
          <div class="card-caption">Closed Orders</div>
        </div>
        <div class="gallery-card" data-idx="21" data-name="Market - Closed Orders" data-tip="Dual-cloud scatter points for market executions">
          <div class="card-canvas-box"><canvas id="c-21"></canvas></div>
          <div class="card-caption">Market - Closed Orders</div>
        </div>
        <div class="gallery-card" data-idx="22" data-name="Market - Mid Timeseries" data-tip="Continuous noisy mid-price timeseries band">
          <div class="card-canvas-box"><canvas id="c-22"></canvas></div>
          <div class="card-caption">Market - Mid Timeseries</div>
        </div>
        <div class="gallery-card" data-idx="23" data-name="Market - Depth Timeseries" data-tip="High-density vertical market depth timeseries columns">
          <div class="card-canvas-box"><canvas id="c-23"></canvas></div>
          <div class="card-caption">Market - Depth Timeseries</div>
        </div>
      </div>
    </section>

    <!-- DUCKDB SQL DRAWER -->
    <section id="duckdb-panel">
      <div class="duckdb-header">
        <span>DUCKDB SQL</span>
        <div class="duckdb-tools">
          <button class="btn-icon" onclick="toggleDuckPanel()">&times;</button>
        </div>
      </div>
      <div class="duckdb-body" id="duckdb-output">
        <table class="sql-table" id="sql-results-table">
          <thead>
            <tr><th>id</th><th>side</th><th>security</th><th>price</th><th>timestamp</th><th>status</th></tr>
          </thead>
          <tbody>
            <tr><td>11,820</td><td style="color:#58a6ff;">buy</td><td>Perspective Co</td><td>1.28</td><td>1/1/70, 7:17:37 AM</td><td style="color:#e4f266;">open</td></tr>
            <tr><td>11,821</td><td style="color:#f85149;">sell</td><td>Perspective Co</td><td>2.93</td><td>1/1/70, 7:17:37 AM</td><td style="color:#6b707d;">closed</td></tr>
            <tr><td>11,822</td><td style="color:#58a6ff;">buy</td><td>Perspective Co</td><td>4.99</td><td>1/1/70, 7:17:37 AM</td><td style="color:#6b707d;">closed</td></tr>
            <tr><td>11,823</td><td style="color:#f85149;">sell</td><td>Perspective Co</td><td>3.74</td><td>1/1/70, 7:17:37 AM</td><td style="color:#e4f266;">open</td></tr>
            <tr><td>11,824</td><td style="color:#58a6ff;">buy</td><td>Perspective Co</td><td>-2.14</td><td>1/1/70, 7:17:37 AM</td><td style="color:#e4f266;">open</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- BOTTOM COMMAND BAR -->
    <div id="command-bar">
      <div class="prompt-input-wrapper">
        <input type="text" id="sql-input" placeholder="SELECT ... &#8984;&#9166; to run" value="SELECT * FROM market_orders LIMIT 10">
      </div>
      <button class="btn-run" onclick="executeDuckSql()">Run</button>
    </div>

    <!-- WORKSPACE FULLSCREEN OVERLAY -->
    <div id="workspace-overlay">
      <div class="workspace-topbar">
        <div class="ws-tabs">
          <div class="ws-tab active" id="ws-tab-title">Market Trading Desk</div>
          <div class="ws-tab">Order Book</div>
          <div class="ws-tab">Blotter</div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="color:var(--text-muted); cursor:pointer;">&#9788;</span>
          <span style="color:var(--text-muted); cursor:pointer;">&#8635;</span>
          <span style="color:var(--text-muted); cursor:pointer;">&#8599;</span>
          <button class="btn-icon" style="font-size:14px; margin-left:8px;" onclick="closeWorkspaceOverlay()">&times;</button>
        </div>
      </div>
      <div class="ws-main">
        <div class="ws-content" id="ws-content-area">
          <canvas id="ws-large-canvas" style="width:100%; height:100%;"></canvas>
        </div>
        <div class="ws-drawer">
          <div class="drawer-tabs">
            <span class="active">QUERY</span>
            <span>PLUGIN</span>
            <span>JSON</span>
          </div>
          <div class="drawer-field">
            <label>Group By</label>
            <select><option>bucket("timestamp", 'm')</option><option>side</option><option>security</option></select>
          </div>
          <div class="drawer-field">
            <label>Split By</label>
            <select><option>None</option><option>side</option><option>status</option></select>
          </div>
          <div class="drawer-field">
            <label>Order By</label>
            <select><option>price DESC</option><option>timestamp ASC</option></select>
          </div>
          <div class="drawer-field">
            <label>Where</label>
            <input type="text" value="status == 'open'">
          </div>
          <div class="drawer-field">
            <label>X Axis</label>
            <input type="text" value="# timestamp">
          </div>
          <div class="drawer-field">
            <label>Y Axis</label>
            <input type="text" value="# price">
          </div>
          <div class="drawer-field">
            <label>Color</label>
            <input type="text" value="# side">
          </div>
        </div>
      </div>
    </div>
  </main>
</div>

<!-- FLOATING TOOLTIP -->
<div id="card-tooltip"></div>

<!-- IMPORT DATA MODAL -->
<div id="import-modal" class="modal-backdrop" onclick="closeImportModal(event)">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <span>IMPORT DATASET</span>
      <button class="btn-icon" onclick="document.getElementById('import-modal').style.display='none'">&times;</button>
    </div>
    <div class="file-dropzone" onclick="document.getElementById('file-upload').click()">
      <p style="font-weight:500; margin-bottom:4px;">Drag and drop or browse</p>
      <p style="font-size:11px;">Supports CSV, Parquet, JSON, Apache Arrow</p>
      <input type="file" id="file-upload" style="display:none;" onchange="handleFileSelected(event)">
    </div>
  </div>
</div>

<!-- CONFIGURE AGENT MODAL -->
<div id="agent-modal" class="modal-backdrop" onclick="closeAgentModal(event)">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <span>CONFIGURE AGENT &middot; STREAMING PIPELINES</span>
      <button class="btn-icon" onclick="document.getElementById('agent-modal').style.display='none'">&times;</button>
    </div>
    <div style="display:flex; flex-direction:column; gap:8px; font-size:12px; color:var(--text-secondary);">
      <label><input type="checkbox" checked> market-matching-engine (256 msg/sec)</label>
      <label><input type="checkbox" checked> duckdb-wasm-cache (In-memory columnar)</label>
      <label><input type="checkbox" checked> webcam-density-cam (WebGL shader)</label>
      <label><input type="checkbox" checked> eeg-connectome-agent (16-ch 256 Hz)</label>
    </div>
    <button class="btn-run" style="margin-top:8px;" onclick="document.getElementById('agent-modal').style.display='none'">Save Configuration</button>
  </div>
</div>

<script>
// ── CARD DRAWING ENGINES ──
function initCardCanvases() {
  for (let i = 0; i < 24; i++) {
    const canvas = document.getElementById('c-' + i);
    if (!canvas) continue;
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = (rect.width || 180) * dpr;
    canvas.height = (rect.height || 115) * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    const W = rect.width || 180;
    const H = rect.height || 115;
    
    drawCardGraphic(ctx, i, W, H);
  }
}

function drawCardGraphic(ctx, idx, W, H) {
  ctx.fillStyle = '#0e0f12';
  ctx.fillRect(0, 0, W, H);

  // Card 0: Superstore Datagrid
  if (idx === 0) {
    ctx.fillStyle = '#1c1e28';
    ctx.fillRect(0, 0, W, 14);
    ctx.fillStyle = '#58a6ff';
    ctx.font = '6px monospace';
    ctx.fillText('RowID  OrderDate  ShipMode   Customer      Sales', 6, 10);
    const rows = [
      ['CA-152', '11/8/16', 'Second', 'Claire Gute', '$261.96'],
      ['CA-108', '6/12/16', 'Standard', 'B. Hoffman', '$731.94'],
      ['US-104', '4/18/17', 'First', 'Alejandro G', '$14.62'],
      ['CA-143', '12/5/17', 'Standard', 'Z. Bonaldi', '$957.58'],
      ['CA-127', '8/27/15', 'Second', 'Ken Black', '$22.36'],
      ['US-161', '10/2/16', 'Standard', 'Sandra F', '$37.94'],
    ];
    for (let r = 0; r < rows.length; r++) {
      ctx.fillStyle = r % 2 === 0 ? '#111215' : '#14151a';
      ctx.fillRect(0, 15 + r * 15, W, 14);
      ctx.fillStyle = '#9da1ab';
      ctx.font = '5.5px monospace';
      ctx.fillText(rows[r].join('   '), 6, 25 + r * 15);
    }
  }

  // Card 1: Superstore (Workspace) 4-split
  else if (idx === 1) {
    // Quad 1: Bar chart
    ctx.fillStyle = '#58a6ff';
    const bars = [18, 35, 42, 28, 50, 22, 38];
    for (let b = 0; b < bars.length; b++) {
      ctx.fillRect(8 + b * 10, 52 - bars[b], 6, bars[b]);
    }
    // Quad 2: Map
    ctx.fillStyle = '#1f3454';
    ctx.fillRect(W/2 + 4, 8, W/2 - 8, 44);
    ctx.fillStyle = '#58a6ff';
    ctx.beginPath(); ctx.arc(W/2 + 25, 28, 4, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(W/2 + 55, 32, 6, 0, Math.PI*2); ctx.fill();
    // Quad 3: Treemap
    ctx.fillStyle = '#d99473'; ctx.fillRect(8, 62, 36, 44);
    ctx.fillStyle = '#8cb7eb'; ctx.fillRect(48, 62, 28, 20);
    ctx.fillStyle = '#ebcc7a'; ctx.fillRect(48, 86, 28, 20);
    // Quad 4: Small table
    ctx.fillStyle = '#1c1d24'; ctx.fillRect(W/2 + 4, 62, W/2 - 8, 44);
    ctx.fillStyle = '#6b707d'; ctx.font = '5px monospace';
    ctx.fillText('Central  $2,297k', W/2 + 8, 76);
    ctx.fillText('East     $678k', W/2 + 8, 88);
    ctx.fillText('West     $725k', W/2 + 8, 100);
  }

  // Card 2: Mandelbrot Fractal
  else if (idx === 2) {
    const imgData = ctx.createImageData(W, H);
    for (let py = 0; py < H; py++) {
      for (let px = 0; px < W; px++) {
        const x0 = (px - W/2) / (W/3) - 0.7;
        const y0 = (py - H/2) / (H/2);
        let x = 0, y = 0, iter = 0;
        while (x*x + y*y <= 4 && iter < 32) {
          const xt = x*x - y*y + x0;
          y = 2*x*y + y0;
          x = xt;
          iter++;
        }
        const pIdx = (py * W + px) * 4;
        if (iter === 32) {
          imgData.data[pIdx] = 10; imgData.data[pIdx+1] = 10; imgData.data[pIdx+2] = 15;
        } else {
          imgData.data[pIdx] = Math.min(255, iter * 9);
          imgData.data[pIdx+1] = Math.min(255, iter * 4);
          imgData.data[pIdx+2] = Math.min(255, iter * 2);
        }
        imgData.data[pIdx+3] = 255;
      }
    }
    ctx.putImageData(imgData, 0, 0);
  }

  // Card 3: Raycasting 3D Torus
  else if (idx === 3) {
    const cx = W / 2, cy = H / 2;
    ctx.strokeStyle = '#58a6ff';
    ctx.lineWidth = 1.2;
    for (let a = 0; a < Math.PI * 2; a += Math.PI / 10) {
      const rx = Math.cos(a) * 36;
      const ry = Math.sin(a) * 16;
      ctx.beginPath();
      ctx.ellipse(cx + rx, cy + ry, 12, 28, a, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.fillStyle = '#e4f266';
    ctx.beginPath(); ctx.arc(cx, cy, 3, 0, Math.PI*2); ctx.fill();
  }

  // Card 4: NYPD CCRB Datagrid
  else if (idx === 4) {
    ctx.fillStyle = '#1c1e28';
    ctx.fillRect(0, 0, W, 12);
    ctx.fillStyle = '#e6e8ec';
    ctx.font = '5.5px monospace';
    ctx.fillText('ID       IncidentDate  OfficerName      TaxID', 6, 9);
    for (let r = 0; r < 7; r++) {
      ctx.fillStyle = '#9da1ab';
      ctx.fillText(`4/28/23  2023-0${r+1}   Garrity, John    958,${r*111}`, 6, 22 + r * 13);
    }
  }

  // Card 5: NYPD CCRB Scatter
  else if (idx === 5) {
    ctx.fillStyle = 'rgba(230, 232, 236, 0.45)';
    for (let p = 0; p < 180; p++) {
      const rx = 10 + Math.random() * (W - 20);
      const ry = 10 + Math.random() * (H - 20);
      ctx.fillRect(rx, ry, 1.5, 1.5);
    }
  }

  // Card 6: NYPD CCRB Bar + Heatmap
  else if (idx === 6) {
    ctx.fillStyle = '#58a6ff';
    for (let b = 0; b < 14; b++) {
      const h = 10 + Math.sin(b * 0.5) * 20 + 20;
      ctx.fillRect(8 + b * 11, 55 - h, 7, h);
    }
    // Heatmap at bottom
    for (let hr = 0; hr < 4; hr++) {
      for (let hc = 0; hc < 14; hc++) {
        const v = (hr + hc * 3) % 10;
        ctx.fillStyle = `rgba(88, 166, 255, ${0.1 + v * 0.08})`;
        ctx.fillRect(8 + hc * 11, 62 + hr * 10, 9, 8);
      }
    }
  }

  // Card 7: NYPD CCRB Multi-lines
  else if (idx === 7) {
    const colors = ['#3fb950', '#58a6ff', '#bc8cff', '#f0883e'];
    colors.forEach((col, ci) => {
      ctx.strokeStyle = col;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      for (let x = 0; x < W; x += 6) {
        const y = 30 + ci * 18 + Math.sin(x * 0.1 + ci) * 14;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    });
  }

  // Card 8: SF Evictions Contour Heatmap
  else if (idx === 8) {
    const grad = ctx.createRadialGradient(W*0.45, H*0.5, 5, W*0.45, H*0.5, 45);
    grad.addColorStop(0, '#f85149');
    grad.addColorStop(0.3, '#f0883e');
    grad.addColorStop(0.6, '#bc8cff');
    grad.addColorStop(1, 'transparent');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
  }

  // Card 9: SF Evictions Dot Map
  else if (idx === 9) {
    const dotColors = ['#58a6ff', '#3fb950', '#f0883e', '#bc8cff'];
    for (let p = 0; p < 120; p++) {
      const rx = 20 + Math.random() * (W - 40);
      const ry = 15 + Math.random() * (H - 30);
      ctx.fillStyle = dotColors[p % dotColors.length];
      ctx.beginPath(); ctx.arc(rx, ry, 2, 0, Math.PI*2); ctx.fill();
    }
  }

  // Card 10: Movies Scatter
  else if (idx === 10) {
    ctx.fillStyle = '#58a6ff';
    for (let p = 0; p < 80; p++) {
      const rx = 20 + (p * 1.8);
      const ry = H - 15 - Math.log(p + 1) * 18 + (Math.random() * 12);
      ctx.fillRect(rx, ry, 2, 2);
    }
    // Marginal bars
    ctx.fillStyle = '#f85149';
    for (let m = 0; m < 8; m++) {
      ctx.fillRect(W - 25, 12 + m * 8, 4 + m * 2, 5);
    }
  }

  // Card 11: Olympics Scatter
  else if (idx === 11) {
    ctx.fillStyle = '#e4f266';
    for (let p = 0; p < 90; p++) {
      const rx = 30 + Math.sin(p) * 20 + p * 1.2;
      const ry = 25 + Math.cos(p) * 22 + (p % 25);
      ctx.fillRect(rx, ry, 2, 2);
    }
  }

  // Card 12: Market Candlestick + Order Book
  else if (idx === 12) {
    // Candlesticks
    for (let c = 0; c < 10; c++) {
      const x = 12 + c * 8;
      const isUp = c % 2 === 0;
      ctx.fillStyle = isUp ? '#58a6ff' : '#f85149';
      ctx.fillRect(x + 2, 20 + (c % 4) * 6, 1, 35);
      ctx.fillRect(x, 26 + (c % 4) * 6, 5, 20);
    }
    // Horizontal Order Book bars
    const midX = W * 0.75;
    for (let b = 0; b < 12; b++) {
      const y = 14 + b * 7;
      if (b < 6) {
        ctx.fillStyle = '#58a6ff';
        ctx.fillRect(midX - (b * 5 + 10), y, b * 5 + 10, 5);
      } else {
        ctx.fillStyle = '#f0883e';
        ctx.fillRect(midX, y, (12 - b) * 5 + 10, 5);
      }
    }
  }

  // Card 13: Market Themed
  else if (idx === 13) {
    for (let c = 0; c < 12; c++) {
      const x = 10 + c * 8;
      const isUp = (c * 3) % 4 !== 0;
      ctx.fillStyle = isUp ? '#3fb950' : '#bc8cff';
      ctx.fillRect(x, 30 + Math.sin(c) * 15, 5, 18);
    }
    ctx.fillStyle = '#58a6ff';
    for (let b = 0; b < 8; b++) {
      ctx.fillRect(W * 0.72, 20 + b * 9, 8 + b * 4, 6);
    }
  }

  // Card 14: Market Orders
  else if (idx === 14) {
    // Top depth timeseries bars
    for (let b = 0; b < 22; b++) {
      ctx.fillStyle = b % 2 === 0 ? '#58a6ff' : '#f0883e';
      ctx.fillRect(6 + b * 7, 8, 5, 30);
    }
    // Bottom order blotter lines
    ctx.strokeStyle = '#bc8cff';
    ctx.beginPath();
    for (let x = 6; x < W - 6; x += 4) {
      const y = 75 + Math.sin(x * 0.2) * 12;
      if (x === 6) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // Card 15: Market Orders Themed
  else if (idx === 15) {
    for (let b = 0; b < 22; b++) {
      ctx.fillStyle = b % 2 === 0 ? '#bc8cff' : '#58a6ff';
      ctx.fillRect(6 + b * 7, 8, 5, 28);
    }
    ctx.fillStyle = '#f85149';
    ctx.fillRect(W * 0.65, 55, 45, 38);
  }

  // Card 16: Webcam - Video Wall (Thermal Heatmap)
  else if (idx === 16) {
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, '#58a6ff');
    grad.addColorStop(0.3, '#3fb950');
    grad.addColorStop(0.7, '#e4f266');
    grad.addColorStop(1, '#f85149');
    ctx.fillStyle = grad;
    ctx.fillRect(8, 8, W * 0.65, H - 16);
    // Histogram at right
    ctx.fillStyle = '#58a6ff';
    for (let h = 0; h < 6; h++) {
      ctx.fillRect(W * 0.74, 20 + h * 12, 10 + h * 3, 8);
    }
  }

  // Card 17: Webcam - Video Wall Themed (Green)
  else if (idx === 17) {
    ctx.fillStyle = '#0f241a';
    ctx.fillRect(8, 8, W * 0.65, H - 16);
    ctx.fillStyle = '#3fb950';
    ctx.beginPath(); ctx.arc(W*0.35, H*0.45, 22, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#73d9bf';
    ctx.fillRect(W * 0.74, 18, 25, 60);
  }

  // Card 18: Market Heatmap
  else if (idx === 18) {
    for (let r = 0; r < 14; r++) {
      for (let c = 0; c < 22; c++) {
        const val = Math.sin(r * 0.4 + c * 0.3);
        ctx.fillStyle = val > 0.3 ? '#f85149' : (val > -0.2 ? '#f0883e' : '#1c1d24');
        ctx.fillRect(6 + c * 7, 10 + r * 6, 6, 5);
      }
    }
  }

  // Card 19: Market Heatmap (Closed)
  else if (idx === 19) {
    for (let r = 0; r < 14; r++) {
      for (let c = 0; c < 22; c++) {
        const val = Math.cos(r * 0.3 + c * 0.4);
        ctx.fillStyle = val > 0.4 ? '#58a6ff' : (val > 0 ? '#1f3454' : '#111215');
        ctx.fillRect(6 + c * 7, 10 + r * 6, 6, 5);
      }
    }
  }

  // Card 20: Closed Orders
  else if (idx === 20) {
    ctx.fillStyle = '#bc8cff';
    for (let p = 0; p < 140; p++) {
      const rx = 10 + p * 1.1;
      const ry = 60 + Math.sin(p * 0.15) * 25 + (Math.random() * 8);
      ctx.fillRect(rx, ry, 1.8, 1.8);
    }
  }

  // Card 21: Market - Closed Orders (Dual Cloud)
  else if (idx === 21) {
    for (let p = 0; p < 180; p++) {
      const rx = 10 + p * 0.9;
      if (p % 2 === 0) {
        ctx.fillStyle = '#f0883e';
        ctx.fillRect(rx, 40 + Math.sin(p*0.1)*16 + Math.random()*12, 1.5, 1.5);
      } else {
        ctx.fillStyle = '#58a6ff';
        ctx.fillRect(rx, 70 + Math.cos(p*0.1)*16 + Math.random()*12, 1.5, 1.5);
      }
    }
  }

  // Card 22: Market - Mid Timeseries
  else if (idx === 22) {
    ctx.strokeStyle = '#58a6ff';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (let x = 8; x < W - 8; x += 3) {
      const y = 55 + Math.sin(x * 0.1) * 22 + (Math.random() * 6 - 3);
      if (x === 8) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // Card 23: Market - Depth Timeseries
  else if (idx === 23) {
    for (let b = 0; b < 28; b++) {
      const x = 6 + b * 6;
      ctx.fillStyle = '#f0883e';
      ctx.fillRect(x, 15, 4.5, 35);
      ctx.fillStyle = '#58a6ff';
      ctx.fillRect(x, 52, 4.5, 40);
    }
  }
}

// ── TOOLTIP HOVER BEHAVIOR ──
const tooltip = document.getElementById('card-tooltip');
document.querySelectorAll('.gallery-card').forEach(card => {
  card.addEventListener('mouseenter', e => {
    const tip = card.getAttribute('data-tip');
    if (!tip) return;
    tooltip.textContent = tip;
    tooltip.style.display = 'block';
  });
  card.addEventListener('mousemove', e => {
    tooltip.style.left = (e.clientX + 14) + 'px';
    tooltip.style.top = (e.clientY + 14) + 'px';
  });
  card.addEventListener('mouseleave', () => {
    tooltip.style.display = 'none';
  });

  // CLICK OPENS WORKSPACE
  card.addEventListener('click', () => {
    const name = card.getAttribute('data-name');
    openWorkspaceOverlay(name);
  });
});

// ── WORKSPACE OVERLAY LOGIC ──
function openWorkspaceOverlay(name) {
  const overlay = document.getElementById('workspace-overlay');
  const title = document.getElementById('ws-tab-title');
  title.textContent = name;
  overlay.style.display = 'flex';

  const container = document.getElementById('ws-content-area');
  
  if (name === 'Raycasting') {
    container.innerHTML = '<div id="three-container" style="width:100%; height:100%;"></div>';
    const tBox = document.getElementById('three-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0e0f12);
    const camera = new THREE.PerspectiveCamera(45, tBox.clientWidth / (tBox.clientHeight || 500), 0.1, 1000);
    camera.position.z = 45;
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(tBox.clientWidth, tBox.clientHeight || 500);
    tBox.appendChild(renderer.domElement);

    const geometry = new THREE.TorusGeometry(14, 4.2, 30, 100);
    const material = new THREE.MeshStandardMaterial({
      color: 0x58a6ff,
      roughness: 0.25,
      metalness: 0.75,
      wireframe: false
    });
    const torus = new THREE.Mesh(geometry, material);
    scene.add(torus);

    const wireMat = new THREE.MeshBasicMaterial({ color: 0x1f3454, wireframe: true, transparent: true, opacity: 0.4 });
    const wireTorus = new THREE.Mesh(geometry, wireMat);
    scene.add(wireTorus);

    const light1 = new THREE.DirectionalLight(0xe4f266, 1.4);
    light1.position.set(20, 30, 40);
    scene.add(light1);
    const light2 = new THREE.AmbientLight(0x334466);
    scene.add(light2);

    let animId;
    function animate() {
      animId = requestAnimationFrame(animate);
      torus.rotation.x += 0.01;
      torus.rotation.y += 0.015;
      wireTorus.rotation.x += 0.01;
      wireTorus.rotation.y += 0.015;
      renderer.render(scene, camera);
    }
    animate();
    window.currentThreeAnim = animId;
    return;
  }

  // Restore canvas if not Three.js
  container.innerHTML = '<canvas id="ws-large-canvas" style="width:100%; height:100%;"></canvas>';
  const canvas = document.getElementById('ws-large-canvas');
  const dpr = window.devicePixelRatio || 1;
  const rect = container.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const W = rect.width;
  const H = rect.height;

  // Render high-res version of the clicked instrument
  ctx.fillStyle = '#0e0f12';
  ctx.fillRect(0, 0, W, H);

  if (name.includes('Market')) {
    // 3-Split workspace: Candlestick, Order Book, Blotter
    for (let c = 0; c < 30; c++) {
      const x = 20 + c * (W * 0.55 / 32);
      const isUp = (c * 7) % 3 === 0;
      ctx.fillStyle = isUp ? '#58a6ff' : '#f85149';
      ctx.fillRect(x + 4, 30 + (c % 6) * 15, 2, H * 0.45);
      ctx.fillRect(x, 60 + (c % 6) * 15, 10, H * 0.25);
    }
    const midX = W * 0.78;
    for (let b = 0; b < 24; b++) {
      const y = 30 + b * (H * 0.45 / 25);
      if (b < 12) {
        ctx.fillStyle = '#58a6ff';
        ctx.fillRect(midX - (b * 12 + 20), y, b * 12 + 20, 10);
      } else {
        ctx.fillStyle = '#f0883e';
        ctx.fillRect(midX, y, (24 - b) * 12 + 20, 10);
      }
    }
    ctx.strokeStyle = '#282a33';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, H * 0.6); ctx.lineTo(W, H * 0.6); ctx.stroke();
    ctx.fillStyle = '#6b707d';
    ctx.font = '11px monospace';
    ctx.fillText('BLOTTER FEED · 20,000 TICKS · REALTIME ARROW BUFFER', 20, H * 0.64);
  } else if (name.includes('Webcam')) {
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, '#58a6ff');
    grad.addColorStop(0.25, '#3fb950');
    grad.addColorStop(0.5, '#e4f266');
    grad.addColorStop(0.85, '#f85149');
    ctx.fillStyle = grad;
    ctx.fillRect(30, 30, W - 60, H - 60);
  } else {
    ctx.fillStyle = '#1c1e28';
    ctx.fillRect(20, 20, W - 40, 24);
    ctx.fillStyle = '#e6e8ec';
    ctx.font = '11px monospace';
    ctx.fillText('RowID     OrderDate    ShipMode     CustomerName         City           State       Sales     Profit', 30, 36);
    for (let r = 0; r < 24; r++) {
      ctx.fillStyle = r % 2 === 0 ? '#111215' : '#14151a';
      ctx.fillRect(20, 48 + r * 22, W - 40, 20);
      ctx.fillStyle = '#9da1ab';
      ctx.fillText(`CA-2016-${1000+r}  11/${r+1}/16    Second Class  Customer ${r+1}        Los Angeles    CA          $${(r*87+14.5).toFixed(2)}    $${(r*12).toFixed(2)}`, 30, 62 + r * 22);
    }
  }
}

function closeWorkspaceOverlay() {
  if (window.currentThreeAnim) {
    cancelAnimationFrame(window.currentThreeAnim);
    window.currentThreeAnim = null;
  }
  document.getElementById('workspace-overlay').style.display = 'none';
}

function toggleDuckPanel() {
  const panel = document.getElementById('duckdb-panel');
  panel.classList.toggle('collapsed');
}

function executeDuckSql() {
  const query = document.getElementById('sql-input').value.trim();
  const panel = document.getElementById('duckdb-panel');
  panel.classList.remove('collapsed');
  const thead = document.querySelector('#sql-results-table thead');
  const tbody = document.querySelector('#sql-results-table tbody');
  
  tbody.innerHTML = '';
  
  if (query.toLowerCase().includes('superstore')) {
    thead.innerHTML = '<tr><th>RowID</th><th>OrderDate</th><th>Customer</th><th>City</th><th>Sales</th><th>Profit</th></tr>';
    const storeData = [
      ['CA-102', '11/8/16', 'Claire Gute', 'Los Angeles', '$261.96', '$41.91'],
      ['CA-108', '6/12/16', 'B. Hoffman', 'Chicago', '$731.94', '$219.58'],
      ['US-104', '4/18/17', 'Alejandro G', 'Seattle', '$14.62', '$6.87'],
      ['CA-143', '12/5/17', 'Z. Bonaldi', 'San Francisco', '$957.58', '-$383.03'],
      ['CA-127', '8/27/15', 'Ken Black', 'Denver', '$22.36', '$10.95'],
      ['US-161', '10/2/16', 'Sandra F', 'New York', '$37.94', '$14.22']
    ];
    storeData.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3]}</td><td style="color:#58a6ff;">${row[4]}</td><td style="color:${row[5].startsWith('-') ? '#f85149' : '#3fb950'}">${row[5]}</td>`;
      tbody.appendChild(tr);
    });
  } else if (query.toLowerCase().includes('eeg') || query.toLowerCase().includes('band')) {
    thead.innerHTML = '<tr><th>Channel</th><th>Delta</th><th>Theta</th><th>Alpha</th><th>Beta</th><th>Gamma</th></tr>';
    const chans = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4'];
    chans.forEach(ch => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${ch}</td><td>0.12</td><td>0.18</td><td style="color:#e4f266; font-weight:600;">0.48</td><td>0.15</td><td>0.07</td>`;
      tbody.appendChild(tr);
    });
  } else {
    thead.innerHTML = '<tr><th>id</th><th>side</th><th>security</th><th>price</th><th>timestamp</th><th>status</th></tr>';
    for (let i = 0; i < 6; i++) {
      const tr = document.createElement('tr');
      const isBuy = i % 2 === 0;
      tr.innerHTML = `
        <td>${12840 + i}</td>
        <td style="color:${isBuy ? '#58a6ff' : '#f85149'};">${isBuy ? 'buy' : 'sell'}</td>
        <td>Perspective Co</td>
        <td>${(1.45 + i * 0.72).toFixed(2)}</td>
        <td>${new Date().toLocaleTimeString()}</td>
        <td style="color:${i < 3 ? '#e4f266' : '#6b707d'};">${i < 3 ? 'open' : 'closed'}</td>
      `;
      tbody.appendChild(tr);
    }
  }
}

// Enter key runs SQL
document.getElementById('sql-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    executeDuckSql();
  }
});

// Modals
function openImportModal() { document.getElementById('import-modal').style.display = 'flex'; }
function closeImportModal(e) { document.getElementById('import-modal').style.display = 'none'; }
function openAgentModal() { document.getElementById('agent-modal').style.display = 'flex'; }
function closeAgentModal(e) { document.getElementById('agent-modal').style.display = 'none'; }

function handleFileSelected(e) {
  if (e.target.files.length > 0) {
    alert('Loaded dataset: ' + e.target.files[0].name + ' into DuckDB in-memory buffer.');
    document.getElementById('import-modal').style.display = 'none';
  }
}

// Window resize re-renders canvases
window.addEventListener('resize', initCardCanvases);
window.addEventListener('DOMContentLoaded', initCardCanvases);
setTimeout(initCardCanvases, 100);
</script>
</body>
</html>
"""
