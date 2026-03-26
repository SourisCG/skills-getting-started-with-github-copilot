"""Tests for signup endpoint using AAA pattern."""
import pytest


class TestSignupEndpoint:
    """Test POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """
        ARRANGE: Reset activities and prepare new participant
        ACT: Send signup request with email and activity name
        ASSERT: Verify participant added and response successful
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert f"Signed up {email} for {activity_name}" in response.json()["message"]
    
    def test_signup_prevents_duplicate_registration(self, client, reset_activities):
        """
        ARRANGE: Reset activities with existing participant
        ACT: Try to sign up same participant twice
        ASSERT: Second signup fails with 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        ARRANGE: Reset activities and prepare request for invalid activity
        ACT: Send signup request for activity that doesn't exist
        ASSERT: Expect 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_updates_participant_count(self, client, reset_activities):
        """
        ARRANGE: Reset activities and fetch initial state
        ACT: Sign up new participant and fetch activities again
        ASSERT: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newcomer@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        
        # Assert
        assert signup_response.status_code == 200
        assert final_count == initial_count + 1
        assert email in final_response.json()[activity_name]["participants"]
    
    @pytest.mark.parametrize("email", [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ])
    def test_multiple_signups_for_different_students(self, client, reset_activities, email):
        """
        ARRANGE: Reset activities and prepare different emails
        ACT: Sign up each student for an empty activity
        ASSERT: All signups succeed
        """
        # Arrange
        activity_name = "Gym Class"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
