import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
from PIL import Image

st.set_page_config(page_title="EOSAS Dashboard", layout="centered")

st_autorefresh(interval=3000, key="eosas_refresh")

st.title("EOSAS Smart Skin Analyzer")
st.subheader("Live Scan Dashboard")

RESULT_FILE = "static/latest_result.json"

if not os.path.exists(RESULT_FILE):
    st.warning("Waiting for first scan...")
else:
    with open(RESULT_FILE, "r") as f:
        result = json.load(f)

    st.success("Latest EOSAS Scan")

    st.metric("Result", result.get("class", "Unknown"))
    st.metric("Confidence", f'{result.get("hazard_score", 0)}%')
    st.write(f"Scan Time: {result.get('time', 'Unknown')}")

    image_path = result.get("image_path", "").lstrip("/")

    if image_path and os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption="Latest scan image", use_container_width=True)
    else:
        st.info("Image not found yet.")