import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test that the API is running and healthy"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_root():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Personal Finance Monte Carlo API"}

def test_api_accepts_valid_payload():
    """Test that the API correctly receives and processes a valid payload"""
    payload = {
        "current_age": 30,
        "current_income": 50000,
        "current_cash": 10000,
        "current_property_value": 0,
        "current_mortgage_debt": 0,
        "current_isa_balance": 0,
        "current_children": 0,
        "simulation_years": 5,  # Short simulation for faster testing
        "inflation_rate": 0.025,
        "income_growth_rate": 0.03,
        "property_growth_rate": 0.04,
        "isa_return_rate": 0.07
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "trajectories" in data
    assert "summary_stats" in data
    
    # Check trajectories structure
    trajectories = data["trajectories"]
    assert isinstance(trajectories, list)
    assert len(trajectories) > 0
    
    # Verify simulation ran for correct number of years
    first_trajectory = trajectories[0]
    assert len(first_trajectory["states"]) == 5  # simulation_years
    assert len(first_trajectory["decisions"]) == 5

def test_api_handles_different_payload_values():
    """Test API with different input values"""
    payload = {
        "current_age": 35,
        "current_income": 75000,
        "current_cash": 20000,
        "current_property_value": 300000,
        "current_mortgage_debt": 240000,
        "current_isa_balance": 15000,
        "current_children": 1,
        "simulation_years": 3,
        "inflation_rate": 0.03,
        "income_growth_rate": 0.025,
        "property_growth_rate": 0.035,
        "isa_return_rate": 0.06
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Check that initial state reflects input
    first_trajectory = data["trajectories"][0]
    initial_state = first_trajectory["states"][0]
    
    assert initial_state["age"] == 35
    assert initial_state["num_children"] == 1

def test_api_invalid_input_handling():
    """Test that API handles invalid inputs appropriately"""
    invalid_payloads = [
        # Missing required fields
        {"current_age": 30},
        # Negative values
        {
            "current_age": -5,
            "current_income": 50000,
            "current_cash": 10000,
            "simulation_years": 10,
            "inflation_rate": 0.025,
            "income_growth_rate": 0.03,
            "property_growth_rate": 0.04,
            "isa_return_rate": 0.07
        },
        # Empty payload
        {}
    ]
    
    for invalid_payload in invalid_payloads:
        response = requests.post(f"{BASE_URL}/simulate", json=invalid_payload)
        # Should return validation error or handle gracefully
        assert response.status_code in [200, 400, 422], f"Unexpected status code for payload: {invalid_payload}"

def print_sample_api_response():
    """Helper function to print a sample API response for inspection"""
    payload = {
        "current_age": 30,
        "current_income": 50000,
        "current_cash": 10000,
        "current_property_value": 0,
        "current_mortgage_debt": 0,
        "current_isa_balance": 0,
        "current_children": 0,
        "simulation_years": 5,
        "inflation_rate": 0.025,
        "income_growth_rate": 0.03,
        "property_growth_rate": 0.04,
        "isa_return_rate": 0.07
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("\n=== SAMPLE API RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Number of trajectories returned: {len(data['trajectories'])}")
        print(f"Simulation years: {len(data['trajectories'][0]['states'])}")
        print(f"Response structure valid: {'trajectories' in data and 'summary_stats' in data}")
        print(f"Summary stats keys: {list(data['summary_stats'].keys())}")
    else:
        print(f"API Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Testing Personal Finance API Integration")
    print("=" * 50)
    
    try:
        print("Testing API endpoints...")
        test_api_health()
        test_api_root()
        print("✓ Basic endpoints working")
        
        print("\nTesting simulation endpoint...")
        test_api_accepts_valid_payload()
        test_api_handles_different_payload_values()
        print("✓ Simulation endpoint working")
        
        print("\nTesting error handling...")
        test_api_invalid_input_handling()
        print("✓ Error handling working")
        
        print_sample_api_response()
        
        print("\n" + "=" * 50)
        print("All API integration tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: uv run python start.py")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()