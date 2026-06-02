from src.app import activities


def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_normalizes_email(client):
    raw_email = "  NEW.USER@MERGINGTON.EDU  "

    response = client.post(f"/activities/Art Club/signup?email={raw_email}")

    assert response.status_code == 200
    assert "new.user@mergington.edu" in activities["Art Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_empty_email(client):
    response = client.post("/activities/Chess Club/signup?email=   ")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_signup_returns_409_for_duplicate_participant(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess Club/signup?email={existing_email}")

    assert response.status_code == 409
    assert "already signed up" in response.json()["detail"]


def test_signup_returns_400_when_activity_is_full(client):
    club = activities["Programming Class"]
    club["max_participants"] = len(club["participants"])

    response = client.post("/activities/Programming Class/signup?email=extra@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Programming Class is full"
