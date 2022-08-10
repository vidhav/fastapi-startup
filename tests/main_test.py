from fastapi.testclient import TestClient

from fastapi_startup.main import FastAPIStartup

DATA = {
    "name": "Test",
}

app = FastAPIStartup(
    static_dir="tests/static",
)


@app.get("/data")
async def read_data():
    return DATA


client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_static():
    response = client.get("/static/file.txt")
    assert response.status_code == 200
    assert response.text.startswith("content")


def test_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() == DATA


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "") == "application/json"


def test_swagger():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "") == "text/html; charset=utf-8"


def test_not_found():
    response = client.get("/not-a-page")
    assert response.status_code == 404
