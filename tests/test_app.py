def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert payload[expected_activity]["description"]


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    updated_activities = activities_response.json()
    assert email in updated_activities[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "already-registered@example.com"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    updated_activities = activities_response.json()
    assert email not in updated_activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
