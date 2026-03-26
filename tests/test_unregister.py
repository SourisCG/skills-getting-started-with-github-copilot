"""Tests for unregister endpoint using AAA pattern."""
import pytest


class TestUnregisterEndpoint:
    """Test DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """
        ARRANGE: Reset activities with known participants
        ACT: Send unregister request for existing participant
        ASSERT: Verify participant removed and response successful
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Exists in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert f"Unregistered {email}" in response.json()["message"]
    
    def test_unregister_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        ARRANGE: Reset activities and prepare request for invalid activity
        ACT: Send unregister request for activity that doesn't exist
        ASSERT: Expect 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_fails_for_non_registered_participant(self, client, reset_activities):
        """
        ARRANGE: Reset activities and prepare request for non-registered student
        ACT: Send unregister request for participant not in activity
        ASSERT: Expect 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_updates_participant_count(self, client, reset_activities):
        """
        ARRANGE: Reset activities and fetch initial state
        ACT: Unregister participant and fetch activities again
        ASSERT: Verify participant count decreased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        
        # Assert
        assert unregister_response.status_code == 200
        assert final_count == initial_count - 1
        assert email not in final_response.json()[activity_name]["participants"]
    
    def test_unregister_then_signup_same_student(self, client, reset_activities):
        """
        ARRANGE: Reset activities, prepare to unregister and re-signup
        ACT: Unregister participant, then sign them up again
        ASSERT: Both operations succeed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        final_response = client.get("/activities")
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        assert email in final_response.json()[activity_name]["participants"]
