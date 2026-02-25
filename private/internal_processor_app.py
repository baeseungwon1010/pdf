from flask import Flask, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename
import subprocess

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"
BOT = BASE / "backend" / "bot.py"

app = Flask(__name__)

@app.post("/process/<n>")
def p(n):
    pdf = STORAGE / secure_filename(n)
    if not pdf.exists():
        return jsonify({"error": "not found"}), 404
    r = subprocess.run(
        ["python", str(BOT), str(pdf)],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        return jsonify({"error": r.stderr}), 500
    return r.stdout, 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(port=5006)
