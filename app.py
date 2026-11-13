import os
os.environ["NUMBA_NUM_THREADS"] = "1"

import streamlit as st
import streamlit.components.v1 as components

# ── App Configuration matching FINOS Perspective dark theme ──
st.set_page_config(
    page_title="PERSPECTIVE / VIZORA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Zero-Chrome Edge-to-Edge Dark CSS ──
st.markdown("""
<style>
/* Remove standard Streamlit chrome completely */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }

html, body, #root, .stApp, [data-testid="stAppViewContainer"], section.main, .block-container {
    background-color: #111215 !important;
    background: #111215 !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    max-width: 100vw !important;
    overflow: hidden !important;
}

div.element-container, div.stCustomComponentV1 {
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

iframe[title="st.iframe"], iframe {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 999999 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Embed Real Local Perspective Web Server with Zero Margins ──
components.html(
    """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100vw; height:100vh; overflow:hidden; background:#111215; }
iframe { width:100vw; height:100vh; border:none; display:block; }
</style>
</head>
<body>
<iframe src="http://localhost:8080/"></iframe>
</body>
</html>""",
    height=1000,
    scrolling=False,
)
