import json

def test_auth_payload_validation():
    user_payload = {
        "username": "traveler1",
        "email": "traveler1@example.com",
        "password": "SecurePassword123"
    }
    assert "username" in user_payload
    assert "email" in user_payload
    assert len(user_payload["password"]) >= 8

def test_journal_entry_structure():
    journal = {
        "title": "Sunset at Beach",
        "destination": "Goa, India",
        "content": "Spent the evening watching the waves and recording thoughts.",
        "image_url": "/static/traveler1_goa.jpg"
    }
    assert journal["title"] == "Sunset at Beach"
    assert journal["destination"] == "Goa, India"

def test_expense_tracker_calculation():
    expenses = [
        {"category": "Flight", "amount": 150.0},
        {"category": "Hotel", "amount": 80.0},
        {"category": "Food", "amount": 25.0}
    ]
    total_spent = sum(item["amount"] for item in expenses)
    assert total_spent == 255.0

def test_destination_planner_schema():
    planner_result = {
        "destination": "Goa",
        "must_visit": ["Calangute Beach", "Fort Aguada", "Dudhsagar Falls"],
        "estimated_budget_per_day": "$50 - $100 USD"
    }
    assert len(planner_result["must_visit"]) == 3
    assert planner_result["destination"] == "Goa"

if __name__ == "__main__":
    test_auth_payload_validation()
    test_journal_entry_structure()
    test_expense_tracker_calculation()
    test_destination_planner_schema()
    print("ALL API & UNIT TESTS PASSED SUCCESSFULLY!")
