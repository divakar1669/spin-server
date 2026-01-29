from fastapi.testclient import TestClient
from rules_app.app import app


client = TestClient(app)


def test_validate_valid_claim():
    payload = {
        "claims": [
            {
                "claim_id": "CLM-001",
                "member_id": "MBR-123",
                "provider_id": "PRV-001",
                "submission_date": "2025-09-15T00:00:00",
                "service_date": "2025-09-14T00:00:00",
                "diagnosis_codes": ["M54.2"],
                "procedure_codes": ["99214"]
            }
        ]
    }
    r = client.post("/validate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["status"] == "valid"


def test_validate_invalid_claim_and_ai_suggestion():
    payload = {
        "claims": [
            {
                "claim_id": "CLM-002",
                "member_id": "MBR-456",
                "provider_id": "PRV-999",
                "submission_date": "2025-09-15T00:00:00",
                "service_date": "2025-09-16T00:00:00",
                "diagnosis_codes": ["R51"],
                "procedure_codes": ["99214"]
            }
        ]
    }
    r = client.post("/validate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data[0]["status"] == "invalid"
    assert len(data[0]["errors"]) >= 1
    assert "ai_suggestion" in data[0]
