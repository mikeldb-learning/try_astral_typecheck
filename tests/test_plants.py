from fastapi.testclient import TestClient

from app.plants.domain import WateringFrequency, LightRequirement


def test_create_plant(test_client: TestClient):
    """Test creating a new plant."""
    plant_data = {
        "name": "Test Plant",
        "species": "Test Species",
        "description": "A test plant",
        "watering_frequency": WateringFrequency.WEEKLY.value,
        "light_requirement": LightRequirement.MEDIUM.value,
    }

    response = test_client.post("/plants/", json=plant_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["species"] == plant_data["species"]
    assert data["description"] == plant_data["description"]
    assert data["watering_frequency"] == plant_data["watering_frequency"]
    assert data["light_requirement"] == plant_data["light_requirement"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert data["care_logs"] == []
