from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "gastos.db"

CATEGORIAS = ["Alimentación", "Transporte", "Entretenimiento", "Salud", "Educación", "Ropa", "Servicios", "Otros"]

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK(tipo IN ('ingreso','gasto')),
                categoria TEXT NOT NULL,
                descripcion TEXT,
                monto REAL NOT NULL,
                fecha TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html", categorias=CATEGORIAS)

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.form
    with get_db() as conn:
        conn.execute(
            "INSERT INTO transacciones (tipo, categoria, descripcion, monto, fecha) VALUES (?,?,?,?,?)",
            (data["tipo"], data["categoria"], data.get("descripcion",""), float(data["monto"]), data["fecha"])
        )
        conn.commit()
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with get_db() as conn:
        conn.execute("DELETE FROM transacciones WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for("index"))

@app.route("/api/resumen")
def resumen():
    mes = request.args.get("mes", datetime.now().strftime("%Y-%m"))
    with get_db() as conn:
        # totales del mes
        rows = conn.execute(
            "SELECT tipo, SUM(monto) as total FROM transacciones WHERE fecha LIKE ? GROUP BY tipo",
            (f"{mes}%",)
        ).fetchall()
        totales = {r["tipo"]: r["total"] for r in rows}
        ingresos = totales.get("ingreso", 0)
        gastos_total = totales.get("gasto", 0)

        # gastos por categoria
        cats = conn.execute(
            "SELECT categoria, SUM(monto) as total FROM transacciones WHERE fecha LIKE ? AND tipo='gasto' GROUP BY categoria ORDER BY total DESC",
            (f"{mes}%",)
        ).fetchall()

        # historial diario del mes
        diario = conn.execute(
            "SELECT fecha, tipo, SUM(monto) as total FROM transacciones WHERE fecha LIKE ? GROUP BY fecha, tipo ORDER BY fecha",
            (f"{mes}%",)
        ).fetchall()

        # ultimas transacciones
        ultimas = conn.execute(
            "SELECT * FROM transacciones ORDER BY fecha DESC, id DESC LIMIT 10"
        ).fetchall()

    return jsonify({
        "ingresos": ingresos,
        "gastos": gastos_total,
        "balance": ingresos - gastos_total,
        "por_categoria": [{"categoria": r["categoria"], "total": r["total"]} for r in cats],
        "diario": [{"fecha": r["fecha"], "tipo": r["tipo"], "total": r["total"]} for r in diario],
        "ultimas": [dict(r) for r in ultimas]
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
