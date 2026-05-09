from fastapi.testclient import TestClient
from urllib.parse import quote


def test_root_redirect(client: TestClient):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (307, 308)
    assert resp.headers["location"].endswith("/static/index.html")


def test_get_activities(client: TestClient):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client: TestClient):
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")

    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate(client: TestClient):
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 400


def test_signup_nonexistent_activity(client: TestClient):
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": "x@x.com"})
    assert resp.status_code == 404


def test_unregister_success(client: TestClient):
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert resp.status_code == 200

    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_unregister_not_signed(client: TestClient):
    activity = "Basketball Team"
    email = "nonexistent@mergington.edu"
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert resp.status_code == 404
