"""Tests for root and activities endpoints using AAA pattern."""
import pytest


class TestRootEndpoint:
    """Test GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        ARRANGE: Setup test client
        ACT: Make GET request to root
        ASSERT: Expect redirect status to /static/index.html
        """
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert expected_redirect_url in response.headers.get("location", "")


class TestActivitiesEndpoint:
    """Test GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        ARRANGE: Reset activities to known state
        ACT: Make GET request to /activities
        ASSERT: Verify all activities returned with correct structure
        """
        # Arrange
        expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert set(data.keys()) == expected_activity_names
        
    def test_activities_have_correct_structure(self, client, reset_activities):
        """
        ARRANGE: Reset activities to known state
        ACT: Make GET request to /activities
        ASSERT: Verify each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert set(activity_details.keys()) == required_fields
            
    def test_activities_have_correct_participant_counts(self, client, reset_activities):
        """
        ARRANGE: Reset activities to known state with specific participant counts
        ACT: Make GET request to /activities
        ASSERT: Verify participant counts match initial data
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, expected_count in expected_counts.items():
            actual_count = len(data[activity_name]["participants"])
            assert actual_count == expected_count
