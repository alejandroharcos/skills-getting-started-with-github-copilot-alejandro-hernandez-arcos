from src.app import activities


def test_unregister_success_removes_participant(client):
    email = activities["Gym Class"]["participants"][0]

    response = client.delete(f"/activities/Gym Class/participants?email={email}")

    assert response.status_code == 200
    assert email not in activities["Gym Class"]["participants"]


def test_unregister_normalizes_email_before_lookup(client):
    existing_email = activities["Chess Club"]["participants"][0]
    raw_email = f"  {existing_email.upper()}  "

    response = client.delete(f"/activities/Chess Club/participants?email={raw_email}")

    assert response.status_code == 200
    assert existing_email not in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown Club/participants?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_400_for_empty_email(client):
    response = client.delete("/activities/Chess Club/participants?email=   ")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_unregister_returns_404_for_not_registered_participant(client):
    response = client.delete("/activities/Art Club/participants?email=missing@mergington.edu")

    assert response.status_code == 404
    assert "is not signed up" in response.json()["detail"]
