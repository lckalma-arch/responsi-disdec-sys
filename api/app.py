from flask import Flask, jsonify, abort
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "yugabyte",
    "user": "yugabyte",
    "password": "yugabyte",
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_all(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=None):
    rows = fetch_all(query, params)
    return rows[0] if rows else None

@app.route("/")
def index():
    return jsonify({
        "message": "REST API - Responsi DisDec Sys",
        "endpoints": ["/mahasiswa", "/mahasiswa/<id>", "/produk", "/produk/<id>"]
    })

@app.route("/mahasiswa", methods=["GET"])
def get_all_mahasiswa():
    data = fetch_all("SELECT * FROM mahasiswa ORDER BY id;")
    return jsonify(data)

@app.route("/mahasiswa/<int:id>", methods=["GET"])
def get_mahasiswa(id):
    data = fetch_one("SELECT * FROM mahasiswa WHERE id = %s;", (id,))
    if not data:
        abort(404, description="Mahasiswa tidak ditemukan")
    return jsonify(data)

@app.route("/produk", methods=["GET"])
def get_all_produk():
    data = fetch_all("SELECT * FROM produk ORDER BY id;")
    return jsonify(data)

@app.route("/produk/<int:id>", methods=["GET"])
def get_produk(id):
    data = fetch_one("SELECT * FROM produk WHERE id = %s;", (id,))
    if not data:
        abort(404, description="Produk tidak ditemukan")
    return jsonify(data)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
