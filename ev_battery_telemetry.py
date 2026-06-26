# ev_battery_telemetry.py
# EV Battery Data Collection with Cybersecurity Layer
# Simulates: BMS Data → Secure Pipeline → Integrity Verification

import random
import hashlib
import json
import time
import datetime

# ─────────────────────────────────────────────
# STEP 1: Simulate EV Battery BMS Data
# (In real EV, this comes from OBD-II / CAN bus)
# ─────────────────────────────────────────────

def get_battery_data():
    """
    Simulates reading data from EV Battery Management System (BMS).
    In real world: read from CAN bus / OBD-II port using python-obd library.
    """
    data = {
        "timestamp"      : datetime.datetime.utcnow().isoformat(),
        "battery_id"     : "EV-BATT-2207",
        "voltage_V"      : round(random.uniform(320.0, 400.0), 2),
        "current_A"      : round(random.uniform(-50.0, 50.0), 2),
        "temperature_C"  : round(random.uniform(20.0, 45.0), 2),
        "soc_percent"    : round(random.uniform(10.0, 100.0), 2),
        "soh_percent"    : round(random.uniform(75.0, 100.0), 2),
        "cycle_count"    : random.randint(100, 1500),
        "cell_balance"   : round(random.uniform(0.0, 0.05), 4),
    }
    return data


# ─────────────────────────────────────────────
# STEP 2: Cybersecurity Layer
# Add SHA-256 hash to detect data tampering
# ─────────────────────────────────────────────

def add_integrity_hash(data: dict) -> dict:
    """
    Adds a SHA-256 hash to the battery data packet.
    Ensures data was NOT tampered during transmission.
    """
    data_string = json.dumps(data, sort_keys=True)
    hash_value = hashlib.sha256(data_string.encode()).hexdigest()
    data["integrity_hash"] = hash_value
    return data


def verify_integrity(received_data: dict) -> bool:
    """
    Verifies received battery data was NOT tampered.
    Extracts the hash, recalculates, and compares.
    """
    received_hash = received_data.pop("integrity_hash", None)

    if received_hash is None:
        print("[SECURITY ALERT] No integrity hash found! Data may be spoofed.")
        return False

    data_string = json.dumps(received_data, sort_keys=True)
    expected_hash = hashlib.sha256(data_string.encode()).hexdigest()

    if received_hash == expected_hash:
        print("[✓] Integrity Verified — Data is authentic.")
        return True
    else:
        print("[✗ ALERT] Data TAMPERED! Integrity check FAILED!")
        return False


# ─────────────────────────────────────────────
# STEP 3: Simulate Tampering Attack
# ─────────────────────────────────────────────

def simulate_tampering(data: dict) -> dict:
    """
    Simulates a hacker injecting a fake SOC value mid-transmission.
    This is a telemetry injection attack.
    """
    tampered = data.copy()
    tampered["soc_percent"] = 999  # Injected fake value
    print("[HACKER] Injecting fake SOC value: 999%")
    return tampered


# ─────────────────────────────────────────────
# STEP 4: Anomaly Detection (Basic Rule-Based)
# ─────────────────────────────────────────────

def detect_anomaly(data: dict) -> list:
    """
    Checks battery telemetry for suspicious values.
    In a real system, ML models (Scikit-learn/PyTorch) are used.
    """
    alerts = []

    if data["voltage_V"] > 420 or data["voltage_V"] < 250:
        alerts.append("CRITICAL: Abnormal voltage — possible spoofing!")

    if data["temperature_C"] > 60:
        alerts.append("WARNING: Overtemperature — thermal risk!")

    if data["soc_percent"] > 100 or data["soc_percent"] < 0:
        alerts.append("CRITICAL: SOC out of range — telemetry injection suspected!")

    if data["cell_balance"] > 0.1:
        alerts.append("WARNING: High cell imbalance — BMS calibration attack possible!")

    if not alerts:
        alerts.append("All parameters NORMAL.")

    return alerts


# ─────────────────────────────────────────────
# STEP 5: Save Log to JSON File
# ─────────────────────────────────────────────

def save_log(data: dict, filename="battery_log.json"):
    """Appends battery reading to a local JSON log file."""
    with open(filename, "a") as f:
        json.dump(data, f)
        f.write("\n")
    print(f"[Log] Data saved to {filename}")


# ─────────────────────────────────────────────
# STEP 6: Full Secure Telemetry Pipeline
# ─────────────────────────────────────────────

def run_telemetry_pipeline(num_readings=3, demo_attack=True):
    print("=" * 60)
    print("  EV BATTERY SECURE TELEMETRY PIPELINE")
    print("=" * 60)

    for i in range(1, num_readings + 1):
        print(f"\n--- Reading #{i} ---")

        # A: Collect BMS data
        battery_data = get_battery_data()
        print("\n[BMS Data Collected]")
        for key, val in battery_data.items():
            print(f"  {key:<20}: {val}")

        # B: Add integrity hash
        secured_data = add_integrity_hash(battery_data.copy())
        print(f"\n[Security] SHA-256 Hash: {secured_data['integrity_hash'][:32]}...")

        # C: Simulate transmission
        print("[Transmission] Sending to cloud broker... (simulated)")
        transmitted_data = secured_data.copy()

        # D: On last reading, simulate a hacker attack
        if demo_attack and i == num_readings:
            print("\n[!] Simulating Telemetry Injection Attack...")
            transmitted_data = simulate_tampering(transmitted_data)

        # E: Verify integrity on receiver side
        print("[Receiver] Verifying data integrity...")
        verify_integrity(transmitted_data)

        # F: Anomaly detection
        print("[Anomaly Detection] Scanning telemetry...")
        anomalies = detect_anomaly(battery_data)
        for alert in anomalies:
            print(f"  → {alert}")

        # G: Save to log
        save_log(battery_data)

        time.sleep(1)

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_telemetry_pipeline(num_readings=3, demo_attack=True)
