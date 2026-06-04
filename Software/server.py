from flask import Flask, request, jsonify, render_template_string
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os
from datetime import datetime
import json

app = Flask(__name__)

MODEL_PATH = "models/eosas_hazard_model.keras"
model = load_model(MODEL_PATH)

with open("models/hazard_class_names.txt", "r") as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

latest_result = {
    "class": "Waiting...",
    "confidence": 0,
    "hazard_score": 0,
    "time": "No scans yet",
    "image_path": "",
    "esp32_ip": "192.168.1.182"
}

scan_requested = False

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>EOSAS Dashboard</title>
    <meta http-equiv="refresh" content="3">

    <style>
        body {
            margin: 0;
            background: radial-gradient(circle at top, #1e293b, #020617);
            color: white;
            font-family: Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .dashboard {
            width: 90%;
            max-width: 1100px;
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 28px;
            padding: 35px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.45);
        }

        .header {
            margin-bottom: 35px;
        }

        .title {
            font-size: 52px;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #22c55e);
            -webkit-background-clip: text;
            color: transparent;
        }

        .subtitle {
            margin-top: 10px;
            color: #94a3b8;
            font-size: 18px;
        }

        .status {
            display: inline-block;
            margin-top: 18px;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            font-weight: bold;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 28px;
        }

        .card {
            background: #0f172a;
            border-radius: 22px;
            padding: 28px;
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        .label {
            color: #94a3b8;
            font-size: 14px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .result {
            margin-top: 18px;
            font-size: 42px;
            font-weight: bold;
        }

        .score {
            margin-top: 22px;
            font-size: 72px;
            font-weight: 800;
            color: #38bdf8;
        }

        .confidence {
            margin-top: 12px;
            color: #cbd5e1;
            font-size: 18px;
        }

        .time {
            margin-top: 25px;
            color: #94a3b8;
        }

        img {
            width: 100%;
            max-height: 420px;
            object-fit: cover;
            border-radius: 18px;
            margin-top: 20px;
        }

        .button {
            display: inline-block;
            margin-top: 25px;
            padding: 14px 22px;
            border-radius: 14px;
            background: linear-gradient(90deg, #2563eb, #06b6d4);
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: 0.2s;
        }

        .button:hover {
            opacity: 0.9;
        }

        .preview-title {
            margin-top: 10px;
            font-size: 24px;
            font-weight: bold;
        }

        .small-text {
            color: #94a3b8;
            margin-top: 8px;
        }

        @media (max-width: 850px) {
            .grid {
                grid-template-columns: 1fr;
            }

            .title {
                font-size: 40px;
            }

            .score {
                font-size: 58px;
            }
        }
    </style>
</head>

<body>
<div class="dashboard">

    <div class="header">
        <div class="title">EOSAS</div>
        <div class="subtitle">Embedded Optical Skin Analysis System</div>
        <div class="status">System Online</div>
    </div>

    <div class="grid">

        <div class="card">
            <div class="label">Latest Scan Result</div>

            <div class="result">
                {{ result["class"] }}
            </div>

            <div class="score">
                {{ result["hazard_score"] }}%
            </div>

            <div class="confidence">
                Confidence: {{ result["confidence"] }}
            </div>

            <div class="time">
                Last Scan: {{ result["time"] }}
            </div>

            <a class="button"
               href="http://{{ result["esp32_ip"] }}"
               target="_blank">
               Open Camera Stream
            </a>
        </div>

        <div class="card">
            <div class="label">Live Scan Preview</div>

            <div class="preview-title">
                Latest Captured Image
            </div>

            <div class="small-text">
                Most recent frame processed by EOSAS
            </div>

            {% if result["image_path"] %}
                <img src="{{ result["image_path"] }}">
            {% else %}
                <p style="color:#94a3b8;">Waiting for first scan...</p>
            {% endif %}
        </div>

    </div>

</div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(HTML_PAGE, result=latest_result)


@app.route("/start_scan", methods=["GET"])
def start_scan():
    global scan_requested
    scan_requested = True
    print("Scan requested by Argon.")
    return jsonify({
        "message": "Scan requested",
        "scan_requested": True
    })


@app.route("/get_command", methods=["GET"])
def get_command():
    global scan_requested

    if scan_requested:
        scan_requested = False
        return jsonify({"scan": True})

    return jsonify({"scan": False})


@app.route("/latest_result", methods=["GET"])
def get_latest_result():
    return jsonify(latest_result)


@app.route("/predict", methods=["POST"])
def predict():
    global latest_result

    if "image" not in request.files:
        return jsonify({"error": "No image received"}), 400

    file = request.files["image"]
    image_bytes = file.read()

    os.makedirs("static/eosas_captures", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_{timestamp}.jpg"

    save_path = f"static/eosas_captures/{filename}"
    browser_path = f"/static/eosas_captures/{filename}"

    with open(save_path, "wb") as f:
        f.write(image_bytes)

    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]

    class_index = int(np.argmax(preds))
    confidence = float(preds[class_index])
    predicted_class = CLASS_NAMES[class_index]

    hazard_score = round(confidence * 100, 2)

    latest_result = {
        "class": predicted_class,
        "confidence": round(confidence, 4),
        "hazard_score": hazard_score,
        "time": datetime.now().strftime("%I:%M:%S %p"),
        "image_path": browser_path,
        "esp32_ip": request.remote_addr
    }

    os.makedirs("static", exist_ok=True)

    with open("static/latest_result.json", "w") as f:
        json.dump(latest_result, f)

    print("\nEOSAS Prediction:")
    print(latest_result)

    return jsonify(latest_result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)