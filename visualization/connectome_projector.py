import json
from typing import Dict, List, Any


def render_connectome_projector(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    manifold_points: List[List[float]],
    manifold_labels: List[str],
    current_state: str = "Alpha Rest",
    height: int = 760,
) -> str:
    """Renders a synchronized dual-space WebGL visualizer in VIZORA dark theme.
    Left: 3D Anatomical Scalp Connectome Graph (Electrodes & Coherence Arcs)
    Right: 3D Latent Cognitive State Manifold (UMAP State Trajectory)
    """

    # Community palette aligned with Vantage theme
    palette = [
        "#e4f266",  # Chromatic lime (signal)
        "#8cb7eb",  # Steel cyan
        "#d99473",  # Copper ochre
        "#b8a6eb",  # Slate lavender
        "#73d9bf",  # Mint teal
        "#ebcc7a",  # Amber gold
    ]

    html = _TEMPLATE
    html = html.replace('"__NODES__"', json.dumps(nodes))
    html = html.replace('"__EDGES__"', json.dumps(edges))
    html = html.replace('"__MANIFOLD__"', json.dumps(manifold_points))
    html = html.replace('"__MLABELS__"', json.dumps(manifold_labels))
    html = html.replace("__STATE__", current_state)
    html = html.replace("__HT__", str(height))
    html = html.replace('"__PALETTE__"', json.dumps(palette))
    return html


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="description" content="VIZORA high-density 3D connectome and manifold visualizer.">
<title>VIZORA: Connectome & Manifold Studio</title>
<style>
/* Hallmark · shape: Workbench · genre: modern-minimal · theme: Vantage (by request) · job: try · draw: 8ad383ee
 * hero: Stage · nav: edge-aligned · footer: mast · imagery: the product · signature: dual-space connectome visualizer · vantage: terrain/steel
 * axes: dark/grotesk-sans/chromatic-lime · posture: restrained · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V4 · weakest: none, tool UI with zero slop */

@import url('https://fonts.googleapis.com/css2?family=Geologica:wght,CRSV,SHRP@200..500,0,0..100&family=JetBrains+Mono:wght@400;500&display=swap');

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
  --font-mono: "JetBrains Mono", monospace;
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --radius-card: 4px;
  --rule-hair: 1px;
  --tick: 8px;
  --dur-short: 180ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --bar-h: 40px;
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
  -webkit-font-smoothing: antialiased;
}

#viewport-container {
  display: flex;
  width: 100%;
  height: calc(100% - var(--bar-h));
  position: relative;
}

.sub-viewport {
  flex: 1;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.sub-viewport:first-child {
  border-right: var(--rule-hair) solid var(--color-rule);
}

.viewport-tag {
  position: absolute;
  top: var(--space-xs);
  left: var(--space-xs);
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: var(--space-2xs) var(--space-xs);
  font-size: 11px;
  color: var(--color-muted);
  font-variant-numeric: tabular-nums;
  z-index: 10;
  pointer-events: none;
}

.viewport-tag .tag-signal {
  color: var(--color-accent);
}

/* Perspective top bar */
#hud-bar {
  height: var(--bar-h);
  background: var(--color-paper-2);
  border-bottom: var(--rule-hair) solid var(--color-rule);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-md);
  font-size: 12px;
}

.hud-title {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 12px;
  color: var(--color-ink);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.hud-pill {
  border: var(--rule-hair) solid var(--color-rule);
  border-radius: var(--radius-card);
  padding: 2px 8px;
  font-size: 11px;
  color: var(--color-muted);
}

.hud-pill.signal {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.hud-tools {
  display: flex;
  gap: var(--space-2xs);
}

.hud-btn {
  background: var(--color-paper-3);
  border: var(--rule-hair) solid var(--color-rule-2);
  color: var(--color-ink);
  font-size: 11px;
  padding: 3px 8px;
  border-radius: var(--radius-card);
  cursor: pointer;
  transition: border-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out);
}

.hud-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.hud-btn.active {
  background: var(--color-accent);
  color: var(--color-accent-ink);
}

#tooltip {
  position: absolute;
  display: none;
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule-2);
  color: var(--color-ink);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-card);
  font-size: 11px;
  font-family: var(--font-mono);
  pointer-events: none;
  z-index: 100;
  line-height: 1.4;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
  cursor: grab;
}
canvas:active { cursor: grabbing; }
</style>
</head>
<body>

<div id="hud-bar">
  <div class="hud-title">
    <span>VIZORA / DUAL-SPACE 3D INSTRUMENT</span>
    <span class="hud-pill signal">Cognitive State: __STATE__</span>
    <span class="hud-pill">16 Electrodes &middot; 256 Hz</span>
  </div>
  <div class="hud-tools">
    <button id="btn-rot" class="hud-btn active">Auto-Rotate</button>
    <button id="btn-reset" class="hud-btn">Reset Views</button>
    <button id="btn-fs" class="hud-btn">Fullscreen</button>
  </div>
</div>

<div id="viewport-container">
  <!-- Viewport A: Scalp Connectome -->
  <div id="vp-connectome" class="sub-viewport">
    <div class="viewport-tag">
      <span>Viewport A: <span class="tag-signal">3D Scalp Connectome (PLV Coherence)</span></span>
    </div>
  </div>

  <!-- Viewport B: Cognitive Manifold -->
  <div id="vp-manifold" class="sub-viewport">
    <div class="viewport-tag">
      <span>Viewport B: <span class="tag-signal">3D Latent Manifold (State Trajectory)</span></span>
    </div>
  </div>
</div>

<div id="tooltip"></div>

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

const nodes = "__NODES__";
const edges = "__EDGES__";
const manifold = "__MANIFOLD__";
const mlabels = "__MLABELS__";
const palette = "__PALETTE__";

const vpConn = document.getElementById('vp-connectome');
const vpMani = document.getElementById('vp-manifold');
const tip = document.getElementById('tooltip');

// ── SETUP SCENE A: CONNECTOME ──
const sceneA = new THREE.Scene();
sceneA.background = new THREE.Color(0x0e111a);
const camA = new THREE.PerspectiveCamera(45, vpConn.clientWidth / vpConn.clientHeight, 0.1, 100);
camA.position.set(0, 1.8, 3.2);

const renA = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renA.setSize(vpConn.clientWidth, vpConn.clientHeight);
renA.setPixelRatio(Math.min(window.devicePixelRatio, 2));
vpConn.appendChild(renA.domElement);

const ctrlA = new OrbitControls(camA, renA.domElement);
ctrlA.enableDamping = true;
ctrlA.dampingFactor = 0.05;
ctrlA.autoRotate = true;
ctrlA.autoRotateSpeed = 0.6;

// Translucent head model wireframe
const headGeo = new THREE.SphereGeometry(1.0, 24, 20);
const headMat = new THREE.MeshBasicMaterial({
  color: 0x1f2638,
  wireframe: true,
  transparent: true,
  opacity: 0.18
});
sceneA.add(new THREE.Mesh(headGeo, headMat));

// Nodes (Electrodes)
const nodeMeshes = [];
nodes.forEach(n => {
  const geo = new THREE.SphereGeometry(0.045, 16, 16);
  const colorHex = palette[n.community % palette.length];
  const mat = new THREE.MeshBasicMaterial({ color: colorHex });
  const m = new THREE.Mesh(geo, mat);
  m.position.set(n.x, n.z, -n.y); // Transform 10-20 to 3D Cartesian head coordinate
  m.userData = n;
  sceneA.add(m);
  nodeMeshes.push(m);
});

// Coherence Arcs (Edges)
const arcLines = [];
edges.forEach(e => {
  const p1 = new THREE.Vector3(e.pos_source[0], e.pos_source[2], -e.pos_source[1]);
  const p2 = new THREE.Vector3(e.pos_target[0], e.pos_target[2], -e.pos_target[1]);
  const mid = p1.clone().add(p2).multiplyScalar(0.5);
  mid.multiplyScalar(1.25); // Lift arc outward above scalp

  const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
  const pts = curve.getPoints(20);
  const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
  const lineMat = new THREE.LineBasicMaterial({
    color: 0xe4f266, // Chromatic lime signal
    transparent: true,
    opacity: Math.max(0.2, (e.weight - 0.4) * 1.5)
  });
  const arc = new THREE.Line(lineGeo, lineMat);
  sceneA.add(arc);
  arcLines.push(arc);
});


// ── SETUP SCENE B: MANIFOLD ──
const sceneB = new THREE.Scene();
sceneB.background = new THREE.Color(0x0e111a);
const camB = new THREE.PerspectiveCamera(45, vpMani.clientWidth / vpMani.clientHeight, 0.1, 100);
camB.position.set(4, 3, 5);

const renB = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renB.setSize(vpMani.clientWidth, vpMani.clientHeight);
renB.setPixelRatio(Math.min(window.devicePixelRatio, 2));
vpMani.appendChild(renB.domElement);

const ctrlB = new OrbitControls(camB, renB.domElement);
ctrlB.enableDamping = true;
ctrlB.dampingFactor = 0.05;
ctrlB.autoRotate = true;
ctrlB.autoRotateSpeed = 0.6;

// Manifold Grid & Trajectory Points
const mPos = [];
const mCol = [];
manifold.forEach((pt, idx) => {
  mPos.push(pt[0], pt[1], pt[2]);
  const label = mlabels[idx] || "Rest";
  if (label.includes("Focus")) {
    mCol.push(0.55, 0.72, 0.92); // Steel blue
  } else if (label.includes("Fatigue")) {
    mCol.push(0.85, 0.58, 0.45); // Copper
  } else if (label.includes("Spike")) {
    mCol.push(0.92, 0.48, 0.55); // Red
  } else {
    mCol.push(0.89, 0.95, 0.40); // Lime (Rest)
  }
});

const mGeo = new THREE.BufferGeometry();
mGeo.setAttribute('position', new THREE.Float32BufferAttribute(mPos, 3));
mGeo.setAttribute('color', new THREE.Float32BufferAttribute(mCol, 3));

const mMat = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  transparent: true,
  opacity: 0.85
});
sceneB.add(new THREE.Points(mGeo, mMat));

// Current state pulse indicator in Manifold
if (manifold.length > 0) {
  const lastPt = manifold[manifold.length - 1];
  const pulseGeo = new THREE.SphereGeometry(0.18, 16, 16);
  const pulseMat = new THREE.MeshBasicMaterial({ color: 0xe4f266, wireframe: true });
  const pulseMesh = new THREE.Mesh(pulseGeo, pulseMat);
  pulseMesh.position.set(lastPt[0], lastPt[1], lastPt[2]);
  sceneB.add(pulseMesh);
}


// ── RAYCASTING & HOVER ON SCENE A ──
const rayA = new THREE.Raycaster();
const mouseA = new THREE.Vector2();

renA.domElement.addEventListener('mousemove', e => {
  const rect = renA.domElement.getBoundingClientRect();
  mouseA.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  mouseA.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  rayA.setFromCamera(mouseA, camA);
  const hits = rayA.intersectObjects(nodeMeshes);
  if (hits.length > 0) {
    const d = hits[0].object.userData;
    tip.innerHTML = `Electrode: <strong>${d.name}</strong><br>Community: Network #${d.community + 1}<br>Degree: ${d.degree} connections`;
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top = (e.clientY + 14) + 'px';
    tip.style.display = 'block';
  } else {
    tip.style.display = 'none';
  }
});
renA.domElement.addEventListener('mouseleave', () => { tip.style.display = 'none'; });


// ── CONTROLS & RESIZE ──
let autoRot = true;
const btnRot = document.getElementById('btn-rot');
btnRot.addEventListener('click', () => {
  autoRot = !autoRot;
  ctrlA.autoRotate = autoRot;
  ctrlB.autoRotate = autoRot;
  btnRot.classList.toggle('active', autoRot);
});

document.getElementById('btn-reset').addEventListener('click', () => {
  camA.position.set(0, 1.8, 3.2);
  ctrlA.target.set(0, 0, 0);
  camB.position.set(4, 3, 5);
  ctrlB.target.set(0, 0, 0);
});

document.getElementById('btn-fs').addEventListener('click', () => {
  const c = document.getElementById('viewport-container');
  if (!document.fullscreenElement) c.requestFullscreen().catch(() => {});
  else document.exitFullscreen().catch(() => {});
});

function animate() {
  requestAnimationFrame(animate);
  ctrlA.update();
  ctrlB.update();
  renA.render(sceneA, camA);
  renB.render(sceneB, camB);
}
animate();

window.addEventListener('resize', () => {
  const wA = vpConn.clientWidth, hA = vpConn.clientHeight;
  camA.aspect = wA / hA;
  camA.updateProjectionMatrix();
  renA.setSize(wA, hA);

  const wB = vpMani.clientWidth, hB = vpMani.clientHeight;
  camB.aspect = wB / hB;
  camB.updateProjectionMatrix();
  renB.setSize(wB, hB);
});
</script>
</body>
</html>
"""
