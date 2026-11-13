import json
import numpy as np


def render_projector(points, n_original_dims, colors=None, hover_texts=None,
                     search_labels=None, algo_name="PCA", height=760, dark_mode=True):
    n_points = len(points)
    is_3d = points.shape[1] >= 3

    pts = np.array(points, dtype=float)
    mins = pts.min(axis=0)
    maxs = pts.max(axis=0)
    ranges = maxs - mins
    ranges[ranges == 0] = 1.0
    norm = (pts - mins) / ranges * 12.0 - 6.0

    pos_list = []
    for p in norm:
        pos_list.extend([round(float(p[0]), 4), round(float(p[1]), 4),
                         round(float(p[2]), 4) if is_3d else 0.0])

    palette = [
        [0.890, 0.950, 0.400],  # Chromatic lime (signal)
        [0.550, 0.720, 0.920],  # Steel cyan
        [0.850, 0.580, 0.450],  # Rust copper
        [0.720, 0.650, 0.920],  # Slate lavender
        [0.450, 0.850, 0.750],  # Mint teal
        [0.920, 0.800, 0.480],  # Amber ochre
        [0.680, 0.750, 0.800],  # Silver blue
        [0.920, 0.480, 0.550],  # Carmine
    ]

    legend_items = []
    if colors is not None:
        unique = sorted(set(colors))
        cmap = {c: palette[i % len(palette)] for i, c in enumerate(unique)}
        col_list = []
        for c in colors:
            col_list.extend(cmap[c])
        counts = {c: 0 for c in unique}
        for c in colors:
            counts[c] += 1
        for label in unique:
            rgb = cmap[label]
            hex_c = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
            legend_items.append({"label": str(label), "color": hex_c, "count": counts[label]})
    else:
        col_list = palette[0] * n_points

    hover_list = hover_texts if hover_texts else []
    search_list = search_labels if search_labels else []

    html = _TEMPLATE
    html = html.replace('"__POS__"', json.dumps(pos_list))
    html = html.replace('"__COL__"', json.dumps(col_list))
    html = html.replace('"__HOVER__"', json.dumps(hover_list))
    html = html.replace('"__LEGEND__"', json.dumps(legend_items))
    html = html.replace('"__SEARCH__"', json.dumps(search_list))
    html = html.replace("__NPTS__", str(n_points))
    html = html.replace("__NDIM__", str(n_original_dims))
    html = html.replace("__ALGO__", algo_name)
    html = html.replace("__MODE__", "3d" if is_3d else "2d")
    html = html.replace("__HT__", str(height))
    return html


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="description" content="Inspect spatial clusters and manifold embeddings in real time.">
<title>VIZORA: 3d embedding projector</title>
<style>
/* Hallmark · shape: Workbench · genre: modern-minimal · theme: Vantage (by request) · job: try · draw: 8ad383ee
 * hero: Stage · nav: edge-aligned · footer: mast · imagery: the product · signature: 3D point cloud projector with hairline ticks · vantage: terrain/steel
 * axes: dark/grotesk-sans/chromatic-lime · posture: restrained · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V4 · weakest: none, tool UI with zero slop */

@import url('https://fonts.googleapis.com/css2?family=Geologica:wght,CRSV,SHRP@200..500,0,0..100&display=swap');

:root {
  --color-paper: oklch(13.5% 0.012 235);
  --color-paper-2: oklch(17% 0.014 235);
  --color-paper-3: oklch(21% 0.016 235);
  --color-ink: oklch(95% 0.006 230);
  --color-ink-2: oklch(82% 0.012 230);
  --color-muted: oklch(66% 0.016 230);
  --color-rule: oklch(27% 0.014 235);
  --color-rule-2: oklch(34% 0.016 235);
  --color-accent: oklch(89% 0.19 126);
  --color-accent-hi: oklch(93% 0.17 126);
  --color-accent-ink: oklch(19% 0.04 126);
  --color-focus: oklch(89% 0.19 126);
  --font-display: "Geologica", ui-sans-serif, system-ui, sans-serif;
  --font-body: "Geologica", ui-sans-serif, system-ui, sans-serif;
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --radius-card: 4px;
  --radius-pill: 999px;
  --rule-hair: 1px;
  --tick: 8px;
  --tracking-display: -0.035em;
  --display-weight: 300;
  --dur-short: 180ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --bar-h: 44px;
}

*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  overflow-x: clip;
  overflow-y: hidden;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background: var(--color-paper);
  color: var(--color-ink);
  font-family: var(--font-body);
  font-weight: 300;
  font-variation-settings: "SHRP" 0;
  -webkit-font-smoothing: antialiased;
  caret-color: var(--color-accent);
}

::selection {
  background: color-mix(in oklab, var(--color-accent) 22%, transparent);
  color: var(--color-ink);
}

html {
  scrollbar-color: var(--color-rule-2) var(--color-paper-2);
}

#c {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Hallmark edge-aligned instrument toolbar */
#bar {
  position: absolute;
  top: var(--space-xs);
  left: var(--space-xs);
  right: var(--space-xs);
  height: var(--bar-h);
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  color: var(--color-ink);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-md);
  z-index: 20;
}

.brand-unit {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
}

.brand-name {
  font-family: var(--font-display);
  font-weight: 400;
  font-variation-settings: "SHRP" 100;
  letter-spacing: var(--tracking-display);
  font-size: 15px;
  color: var(--color-ink);
}

.meta-stats {
  font-size: 13px;
  color: var(--color-muted);
  font-variant-numeric: tabular-nums;
  display: flex;
  gap: var(--space-xs);
}

.meta-stats span {
  display: inline-flex;
  gap: var(--space-2xs);
}

.meta-stats .num-u {
  color: var(--color-muted);
  font-size: 11px;
}

.tool-controls {
  display: flex;
  align-items: center;
  gap: var(--space-2xs);
}

.tool-btn {
  background: transparent;
  border: var(--rule-hair) solid var(--color-rule);
  color: var(--color-ink-2);
  height: 28px;
  padding: 0 var(--space-xs);
  border-radius: var(--radius-card);
  cursor: pointer;
  font-size: 12px;
  font-weight: 400;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2xs);
  transition: border-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out), background-color var(--dur-short) var(--ease-out);
}

.tool-btn:hover {
  border-color: var(--color-rule-2);
  color: var(--color-ink);
  background: var(--color-paper-3);
}

.tool-btn:active {
  background: var(--color-paper);
}

.tool-btn.active {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.tool-btn:disabled, .panel-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.tool-btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Hairline corner ticks container */
.ticks {
  position: relative;
}

.ticks::before, .ticks::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border: var(--rule-hair) solid var(--color-rule-2);
  -webkit-mask: conic-gradient(at var(--tick) var(--tick), transparent 75%, var(--color-ink) 0) 0 0 / calc(100% - var(--tick)) calc(100% - var(--tick));
  mask: conic-gradient(at var(--tick) var(--tick), transparent 75%, var(--color-ink) 0) 0 0 / calc(100% - var(--tick)) calc(100% - var(--tick));
}

/* Search panel with hairline frame */
#rp {
  position: absolute;
  top: 60px;
  right: var(--space-xs);
  width: 220px;
  z-index: 15;
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: var(--space-sm);
}

.panel-label {
  font-size: 12px;
  color: var(--color-muted);
  margin-bottom: var(--space-xs);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.panel-label .counter {
  color: var(--color-accent);
  font-variant-numeric: tabular-nums;
  font-size: 11px;
}

#si {
  width: 100%;
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: var(--space-xs) var(--space-xs);
  font-size: 12px;
  font-family: inherit;
  font-weight: 300;
  outline: none;
  background: var(--color-paper);
  color: var(--color-ink);
  transition: border-color var(--dur-short) var(--ease-out);
}

#si:focus-visible {
  border-color: var(--color-accent);
  outline: 2px solid var(--color-focus);
  outline-offset: 1px;
}

.panel-actions {
  display: flex;
  gap: var(--space-2xs);
  margin-top: var(--space-xs);
}

.panel-btn {
  flex: 1;
  padding: var(--space-2xs) 0;
  font-size: 11px;
  font-weight: 400;
  border: var(--rule-hair) solid var(--color-rule);
  background: var(--color-paper);
  border-radius: var(--radius-card);
  cursor: pointer;
  color: var(--color-muted);
  transition: border-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out);
  text-align: center;
}

.panel-btn:hover {
  border-color: var(--color-rule-2);
  color: var(--color-ink);
}

.panel-btn:active {
  background: var(--color-paper-3);
}

.panel-btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 1px;
}

/* Cluster Legend */
#leg {
  position: absolute;
  bottom: var(--space-xs);
  right: var(--space-xs);
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: var(--space-xs) var(--space-sm);
  font-size: 12px;
  color: var(--color-ink-2);
  z-index: 15;
  max-height: 180px;
  overflow-y: auto;
}

.legend-caption {
  font-size: 11px;
  color: var(--color-muted);
  margin-bottom: var(--space-xs);
}

.legend-row {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  margin: var(--space-2xs) 0;
  cursor: pointer;
  padding: 2px var(--space-2xs);
  border-radius: 2px;
  font-variant-numeric: tabular-nums;
  transition: background-color var(--dur-short) var(--ease-out);
}

.legend-row:hover {
  background: var(--color-paper-3);
  color: var(--color-ink);
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-count {
  margin-left: auto;
  color: var(--color-muted);
  font-size: 11px;
}

/* Instrument Leader Callout Tooltip */
#tip {
  position: absolute;
  display: none;
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule-2);
  color: var(--color-ink);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-card);
  font-size: 12px;
  pointer-events: none;
  max-width: 280px;
  z-index: 100;
  line-height: 1.5;
  font-variant-numeric: tabular-nums;
}

#atag {
  position: absolute;
  bottom: var(--space-xs);
  left: var(--space-xs);
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: var(--space-xs) var(--space-sm);
  font-size: 11px;
  color: var(--color-muted);
  z-index: 15;
  font-variant-numeric: tabular-nums;
}

canvas {
  display: block;
  cursor: grab;
  width: 100%;
  height: 100%;
}
canvas:active { cursor: grabbing; }
</style>
</head>
<body>
<div id="c">
  <!-- Bar -->
  <div id="bar">
    <div class="brand-unit">
      <span class="brand-name">VIZORA</span>
      <div class="meta-stats">
        <span>__ALGO__ __MODE__</span>
        <span>__NPTS__ <span class="num-u">points</span></span>
        <span>__NDIM__ <span class="num-u">dimensions</span></span>
      </div>
    </div>
    
    <div class="tool-controls">
      <button id="b-rot" class="tool-btn active" title="Toggle point rotation">Rotate</button>
      <button id="b-reset" class="tool-btn" title="Reset camera position">Reset</button>
      <button id="b-fs" class="tool-btn" title="Toggle fullscreen view">Fullscreen</button>
    </div>
  </div>

  <!-- Search & Isolate -->
  <div id="rp">
    <div class="panel-label">
      <span>Filter</span>
      <span id="mc" class="counter"></span>
    </div>
    <input id="si" type="text" placeholder="Type attribute value..." spellcheck="false">
    <div class="panel-actions">
      <button id="bsa" class="panel-btn">All</button>
      <button id="bis" class="panel-btn">Isolate</button>
      <button id="bcl" class="panel-btn">Clear</button>
    </div>
  </div>

  <!-- Legend -->
  <div id="leg"></div>

  <!-- Status tag -->
  <div id="atag">
    <span>WebGL 3d &middot; Orbit active</span>
  </div>

  <!-- Tooltip -->
  <div id="tip"></div>
</div>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.162.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.162.0/examples/jsm/"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const el = document.getElementById('c');
const tip = document.getElementById('tip');
const P = new Float32Array("__POS__");
const C = new Float32Array("__COL__");
const H = "__HOVER__";
const L = "__LEGEND__";
const SL = "__SEARCH__";
const N = __NPTS__;

// Populate Legend
if (L && L.length) {
  const d = document.getElementById('leg');
  d.innerHTML = '<div class="legend-caption">Categories</div>';
  L.forEach(i => {
    d.innerHTML += `
      <div class="legend-row" data-label="${i.label}">
        <div class="legend-dot" style="background:${i.color}"></div>
        <span>${i.label}</span>
        <span class="legend-count">${i.count || ''}</span>
      </div>`;
  });
} else {
  const legEl = document.getElementById('leg');
  if (legEl) legEl.style.display = 'none';
}

const W = el.clientWidth || window.innerWidth;
const HH = el.clientHeight || window.innerHeight;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0e111a);

const cam = new THREE.PerspectiveCamera(50, W / HH, 0.1, 500);
cam.position.set(16, 12, 16);
const camInit = cam.position.clone();

const ren = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
ren.setSize(W, HH);
ren.setPixelRatio(Math.min(window.devicePixelRatio, 2));
el.appendChild(ren.domElement);

const ctrl = new OrbitControls(cam, ren.domElement);
ctrl.enableDamping = true;
ctrl.dampingFactor = 0.05;
ctrl.autoRotate = true;
ctrl.autoRotateSpeed = 0.5;
ctrl.minDistance = 3;
ctrl.maxDistance = 80;

// Coordinate hairline ticks
const axLines = [];
const tickMat = new THREE.LineBasicMaterial({ color: 0x242a38, opacity: 0.5, transparent: true });
[[[-9, 0, 0], [9, 0, 0]], [[0, -9, 0], [0, 9, 0]], [[0, 0, -9], [0, 0, 9]]].forEach(([a, b]) => {
  const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a), new THREE.Vector3(...b)]);
  const l = new THREE.Line(g, tickMat);
  scene.add(l);
  axLines.push(l);
});

// Points Geometry
const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(P, 3));
geo.setAttribute('color', new THREE.BufferAttribute(C, 3));
const HL = new Float32Array(N).fill(1.0);
geo.setAttribute('hl', new THREE.BufferAttribute(HL, 1));

// Vantage point cloud shader: no bloom, distance scaling, hairline softness
const mat = new THREE.ShaderMaterial({
  transparent: true,
  depthWrite: false,
  vertexShader: `
    attribute vec3 color;
    attribute float hl;
    varying vec3 vC;
    varying float vD;
    varying float vH;
    void main() {
      vC = color;
      vH = hl;
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      vD = -mv.z;
      float baseSize = max(3.0, 9.5 * (260.0 / vD));
      gl_PointSize = baseSize * mix(0.15, 1.1, hl);
      gl_Position = projectionMatrix * mv;
    }
  `,
  fragmentShader: `
    varying vec3 vC;
    varying float vD;
    varying float vH;
    void main() {
      float dist = length(gl_PointCoord - vec2(0.5));
      if (dist > 0.5) discard;
      float alpha = smoothstep(0.5, 0.2, dist);
      float depthFade = clamp(1.0 - (vD - 6.0) / 50.0, 0.35, 1.0);
      gl_FragColor = vec4(vC, alpha * 0.9 * depthFade * mix(0.08, 1.0, vH));
    }
  `
});

const pts = new THREE.Points(geo, mat);
scene.add(pts);

// Raycasting
const rc = new THREE.Raycaster();
rc.params.Points.threshold = 0.35;
const mouse = new THREE.Vector2();
let hIdx = -1;

ren.domElement.addEventListener('mousemove', e => {
  const r = ren.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - r.left) / r.width) * 2 - 1;
  mouse.y = -((e.clientY - r.top) / r.height) * 2 + 1;
  rc.setFromCamera(mouse, cam);
  const ix = rc.intersectObject(pts);
  if (ix.length > 0) {
    const i = ix[0].index;
    if (i !== hIdx && H.length > i) {
      hIdx = i;
      tip.innerHTML = H[i];
      tip.style.display = 'block';
    }
    const tipX = Math.min(e.clientX - r.left + 16, r.width - 280);
    const tipY = Math.min(e.clientY - r.top + 16, r.height - 100);
    tip.style.left = tipX + 'px';
    tip.style.top = tipY + 'px';
  } else {
    hIdx = -1;
    tip.style.display = 'none';
  }
});

ren.domElement.addEventListener('mouseleave', () => {
  tip.style.display = 'none';
  hIdx = -1;
});

// Auto-rotate toggle
let autoRot = true;
const rotBtn = document.getElementById('b-rot');
rotBtn.addEventListener('click', () => {
  autoRot = !autoRot;
  ctrl.autoRotate = autoRot;
  rotBtn.classList.toggle('active', autoRot);
});

let idleTimeout;
ren.domElement.addEventListener('mousedown', () => {
  if (autoRot) ctrl.autoRotate = false;
});
ren.domElement.addEventListener('mouseup', () => {
  if (autoRot) {
    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => { ctrl.autoRotate = true; }, 3500);
  }
});

// Reset Camera
document.getElementById('b-reset').addEventListener('click', () => {
  cam.position.copy(camInit);
  ctrl.target.set(0, 0, 0);
  if (autoRot) ctrl.autoRotate = true;
});

// Fullscreen Toggle
const fsBtn = document.getElementById('b-fs');
fsBtn.addEventListener('click', () => {
  if (!document.fullscreenElement) {
    el.requestFullscreen().catch(() => {});
  } else {
    document.exitFullscreen().catch(() => {});
  }
});

// Search & Highlight Logic
const si = document.getElementById('si');
const mc = document.getElementById('mc');

function applyFilter(query) {
  const hArr = geo.attributes.hl.array;
  if (!query) {
    hArr.fill(1.0);
    mc.textContent = '';
  } else {
    let matchCount = 0;
    for (let i = 0; i < N; i++) {
      const isMatch = SL[i] && SL[i].toLowerCase().includes(query);
      hArr[i] = isMatch ? 1.0 : 0.0;
      if (isMatch) matchCount++;
    }
    mc.textContent = `${matchCount} of ${N}`;
  }
  geo.attributes.hl.needsUpdate = true;
}

si.addEventListener('input', e => applyFilter(e.target.value.toLowerCase().trim()));
document.getElementById('bsa').addEventListener('click', () => { si.value = ''; applyFilter(''); });
document.getElementById('bis').addEventListener('click', () => {
  const q = si.value.toLowerCase().trim();
  if (q) applyFilter(q);
});
document.getElementById('bcl').addEventListener('click', () => { si.value = ''; applyFilter(''); });

// Click legend item to filter
document.querySelectorAll('.legend-row').forEach(item => {
  item.addEventListener('click', () => {
    const label = item.getAttribute('data-label');
    si.value = label;
    applyFilter(label.toLowerCase());
  });
});

// Render Loop
function animate() {
  requestAnimationFrame(animate);
  ctrl.update();
  ren.render(scene, cam);
}
animate();

// Resize Observer
const resizeObserver = new ResizeObserver(() => {
  const w = el.clientWidth || window.innerWidth;
  const h = el.clientHeight || window.innerHeight;
  cam.aspect = w / h;
  cam.updateProjectionMatrix();
  ren.setSize(w, h);
});
resizeObserver.observe(el);
</script>
</body>
</html>
"""
