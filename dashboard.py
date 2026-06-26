# dashboard.py
# EV Battery Security Live Dashboard
# Run with: streamlit run dashboard.py

import streamlit as st
import random
import hashlib
import json
import datetime
import time

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="EV Battery Security Dashboard",
    page_icon="🔋",
    layout="wide"
)

st.title("🔋 EV Battery Intelligence & Security Dashboard")
st.caption("Secure Telemetry Pipeline | ISO 21434 Aligned | Internship Project by Sai Vinesh")

# ── Helper Functions ──────────────────────────

def get_battery_data():
    return {
        "timestamp"     : datetime.datetime.utcnow().isoformat(),
        "battery_id"    : "EV-BATT-2207",
        "voltage_V"     : round(random.uniform(320.0, 400.0), 2),
        "current_A"     : round(random.uniform(-50.0, 50.0), 2),
        "temperature_C" : round(random.uniform(20.0, 45.0), 2),
        "soc_percent"   : round(random.uniform(10.0, 100.0), 2),
        "soh_percent"   : round(random.uniform(80.0, 100.0), 2),
        "cycle_count"   : random.randint(100, 1500),
        "cell_balance"  : round(random.uniform(0.0, 0.05), 4),
    }

def add_hash(data):
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()

def detect_anomaly(data):
    alerts = []
    if data["voltage_V"] > 420 or data["voltage_V"] < 250:
        alerts.append("⚡ Abnormal Voltage — Possible Spoofing!")
    if data["temperature_C"] > 60:
        alerts.append("🌡️ Overtemperature — Thermal Risk!")
    if data["soc_percent"] > 100 or data["soc_percent"] < 0:
        alerts.append("🚨 SOC Out of Range — Telemetry Injection Suspected!")
    if data["cell_balance"] > 0.1:
        alerts.append("⚠️ High Cell Imbalance — BMS Attack Possible!")
    return alerts

# ── Sidebar Controls ──────────────────────────
st.sidebar.header("⚙️ Controls")
auto_refresh = st.sidebar.toggle("Auto Refresh (2s)", value=False)
simulate_attack = st.sidebar.checkbox("🔴 Simulate Hacker Attack (SOC Injection)")

st.sidebar.markdown("---")
st.sidebar.markdown("**Tech Stack:**")
st.sidebar.markdown("- Python 3.12\n- Streamlit\n- SHA-256 Hashing\n- Rule-based Anomaly Detection")
st.sidebar.markdown("---")
st.sidebar.markdown("**Standards:** ISO/SAE 21434, OWASP API Top 10")

# ── Main Dashboard ─────────────────────────────

data = get_battery_data()

# Simulate attack if checkbox is on
if simulate_attack:
    data["soc_percent"] = 999
    st.error("🚨 ATTACK SIMULATED: Hacker injected SOC = 999% into telemetry!")

# Integrity Hash
integrity_hash = add_hash(data)

# ── Metrics Row ────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("🔋 Voltage (V)",      f"{data['voltage_V']} V",
            delta=f"{round(data['voltage_V'] - 360, 2)} from nominal")
col2.metric("⚡ Current (A)",      f"{data['current_A']} A")
col3.metric("🌡️ Temperature (°C)", f"{data['temperature_C']} °C",
            delta_color="inverse" if data['temperature_C'] > 40 else "normal",
            delta=f"{round(data['temperature_C'] - 30, 1)} from safe")
col4.metric("🔌 State of Charge",  f"{data['soc_percent']} %")

st.markdown("---")

col5, col6, col7 = st.columns(3)
col5.metric("💪 State of Health",  f"{data['soh_percent']} %")
col6.metric("🔄 Cycle Count",      data["cycle_count"])
col7.metric("⚖️ Cell Balance (V)", f"{data['cell_balance']} V")

st.markdown("---")

# ── Security Section ───────────────────────────
st.subheader("🔐 Cybersecurity Layer")

col_hash, col_status = st.columns([3, 1])
col_hash.code(f"SHA-256: {integrity_hash}", language="text")

if not simulate_attack:
    col_status.success("✅ Authentic")
else:
    col_status.error("❌ Tampered!")

# ── Anomaly Detection ──────────────────────────
st.subheader("🛡️ Anomaly Detection")
anomalies = detect_anomaly(data)

if anomalies:
    for alert in anomalies:
        st.error(alert)
else:
    st.success("✅ All parameters NORMAL — No threats detected.")

# ── Raw Data ───────────────────────────────────
with st.expander("📋 View Raw BMS Data (JSON)"):
    st.json(data)

# ── Footer ─────────────────────────────────────
st.markdown("---")
st.caption(f"Last updated: {data['timestamp']} UTC | Battery ID: {data['battery_id']}")

# Auto refresh
if auto_refresh:
    time.sleep(2)
    st.rerun()
