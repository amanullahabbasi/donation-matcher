
import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# ---------------------------
# Config / App
# ---------------------------
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Donation Matcher API is running!"

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS victims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            need_type TEXT,
            urgency TEXT,
            income INTEGER,
            has_home INTEGER,
            amount_needed INTEGER
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            resource_type TEXT,
            donation_amount INTEGER
        );
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Helpers
# ---------------------------

URGENCY_MAP = {"High": 3, "Medium": 2, "Low": 1}

def safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default

def calculate_need_score(urgency: str, income: int, has_home: int, amount_needed: int) -> float:
    # urgency -> weight (3/2/1)
    u = URGENCY_MAP.get(urgency, 1)
    # avoid division by zero
    income_factor = 1.0 / max(income, 1)
    # if no home -> +1
    asset_bonus = 1.0 if has_home == 0 else 0.0
    money_factor = amount_needed / 10000.0
    score = (u * income_factor * 10000.0) + asset_bonus + money_factor
    return round(score, 3)

# ---------------------------
# Routes
# ---------------------------

@app.route("/api/victims", methods=["POST"])
def add_victim():
    data = request.get_json(force=True)
    name = data.get("name", "")
    location = data.get("location", "")
    need_type = data.get("need_type", "")
    urgency = data.get("urgency", "Low")
    income = safe_int(data.get("income", 0))
    has_home = 0 if str(data.get("has_home", "No")).lower() in ["no", "0", "false", "f"] else 1
    amount_needed = safe_int(data.get("amount_needed", 0))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO victims (name, location, need_type, urgency, income, has_home, amount_needed) VALUES (?, ?, ?, ?, ?, ?, ?);",
        (name, location, need_type, urgency, income, has_home, amount_needed),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "ok": True})

@app.route("/api/donors", methods=["POST"])
def add_donor():
    data = request.get_json(force=True)
    name = data.get("name", "")
    location = data.get("location", "")
    resource_type = data.get("resource_type", "")
    donation_amount = safe_int(data.get("donation_amount", 0))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO donors (name, location, resource_type, donation_amount) VALUES (?, ?, ?, ?);",
        (name, location, resource_type, donation_amount),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "ok": True})

@app.route("/api/victims", methods=["GET"])
def list_victims():
    conn = get_db()
    rows = conn.execute("SELECT * FROM victims ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/donors", methods=["GET"])
def list_donors():
    conn = get_db()
    rows = conn.execute("SELECT * FROM donors ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/reset", methods=["DELETE"])
def reset_all():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM victims;")
    cur.execute("DELETE FROM donors;")
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/matches", methods=["GET"])
def compute_matches():
    conn = get_db()
    victims = conn.execute("SELECT * FROM victims").fetchall()
    donors = conn.execute("SELECT * FROM donors").fetchall()
    conn.close()

    # Build simple matching: resource type must match, donor must afford
    donors_by_type = {}
    for d in donors:
        donors_by_type.setdefault(d["resource_type"].lower(), []).append(dict(d))

    matches = []
    for v in victims:
        vdict = dict(v)
        v_need_type = (vdict["need_type"] or "").lower()
        compatible = donors_by_type.get(v_need_type, [])
        if not compatible:
            continue
        # pick first donor with enough budget
        for d in compatible:
            if d["donation_amount"] >= vdict["amount_needed"]:
                score = calculate_need_score(
                    vdict["urgency"],
                    safe_int(vdict["income"]),
                    safe_int(vdict["has_home"]),
                    safe_int(vdict["amount_needed"]),
                )
                matches.append({
                    "victim": {
                        "id": vdict["id"],
                        "name": vdict["name"],
                        "location": vdict["location"],
                        "need_type": vdict["need_type"],
                        "urgency": vdict["urgency"],
                        "income": vdict["income"],
                        "has_home": bool(vdict["has_home"]),
                        "amount_needed": vdict["amount_needed"],
                        "need_score": score,
                    },
                    "donor": {
                        "id": d["id"],
                        "name": d["name"],
                        "location": d["location"],
                        "resource_type": d["resource_type"],
                        "donation_amount": d["donation_amount"],
                    }
                })
                break  # one donor per victim in this simple demo

    # Sort by highest need score first
    matches.sort(key=lambda m: m["victim"]["need_score"], reverse=True)
    return jsonify(matches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # use Render-assigned port
    app.run(host='0.0.0.0', port=port, debug=False)