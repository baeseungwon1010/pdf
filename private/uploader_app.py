from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid, requests, os

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"
FRONT = BASE / "frontend"
INTERNAL = "http://127.0.0.1:5006"
ENV_PATH = BASE / "credit"

STORAGE.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(FRONT), static_url_path="/static")

def read_env_value(key: str):
    if not ENV_PATH.exists():
        return None
    for line in ENV_PATH.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == key:
            return v.strip().strip('"').strip("'")
    return None

@app.get("/")
def i():
    return send_from_directory(FRONT, "index.html")

@app.post("/upload")
def u():
    f = request.files.get("file")
    if not f or not f.filename.endswith(".pdf"):
        return jsonify({"error": "pdf only"}), 400
    name = f"{uuid.uuid4().hex}.pdf"
    f.save(STORAGE / secure_filename(name))
    return jsonify({"saved_as": name})

@app.post("/process/<n>")
def p(n):
    r = requests.post(f"{INTERNAL}/process/{secure_filename(n)}")
    return r.text, r.status_code, r.headers.items()

@app.get("/flag")
def flag():
    role = read_env_value("ROLE")
    if role != "admin":
        return jsonify({"ok": False, "error": "forbidden"}), 403

    flag_value = os.getenv("FLAG", "DH{FAKE-FLAG}")
    return jsonify({"ok": True, "flag": flag_value})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5005)
