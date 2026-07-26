"""Leaderboard API — a small REST service backed by PostgreSQL."""

import os
import psycopg
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics  

def get_conn():
    # Connect to the database using the address in the DATABASE_URL environment
    # variable. We set that variable in Stage 2 (Compose provides the database).
    return psycopg.connect(os.environ["DATABASE_URL"])


def init_db():
    # Create the scores table the first time the app starts, if it isn't there.
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                player TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )

def create_app():
    app = Flask(__name__)
    PrometheusMetrics(app)   # it creates the /metrics endpoint
    init_db()

    @app.get("/healthz")
    def healthz():
        # Proves the app is up AND the database is reachable.
        with get_conn() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok")

    @app.post("/scores")
    def add_score():
        data = request.get_json(silent=True) or {}
        player = data.get("player")
        score = data.get("score")
        valid = (
            isinstance(player, str)
            and player.strip()
            and isinstance(score, int)
            and not isinstance(score, bool)
        )
        if not valid:
            return jsonify(error='send JSON: {"player": "name", "score": 10}'), 400
        with get_conn() as conn:
            row = conn.execute(
                "INSERT INTO scores (player, score) VALUES (%s, %s) RETURNING id",
                (player.strip(), score),
            ).fetchone()
        return jsonify(id=row[0], player=player.strip(), score=score), 201

    @app.get("/scores")
    def top_scores():
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT player, score FROM scores ORDER BY score DESC, created_at ASC LIMIT 10"
            ).fetchall()
        return jsonify([{"player": p, "score": s} for p, s in rows])

    return app