import os
import psycopg
import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    # start each test from an empty table
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("TRUNCATE scores")
    return app.test_client()


def test_healthz_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_scores_start_empty(client):
    assert client.get("/scores").get_json() == []


def test_add_and_rank(client):
    for player, score in [("amal", 40), ("badr", 90), ("celine", 70)]:
        client.post("/scores", json={"player": player, "score": score})
    ranked = client.get("/scores").get_json()
    assert [r["player"] for r in ranked] == ["badr", "celine", "amal"]


def test_rejects_bad_input(client):
    resp = client.post("/scores", json={"player": "amal", "score": "ten"})
    assert resp.status_code == 400
