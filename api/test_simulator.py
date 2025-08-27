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

def test_monte_carlo_simulation_basic():
    """Test basic Monte Carlo simulation with default parameters"""
    payload = {
        "current_age": 30,
        "current_income": 50000,
        "current_cash": 10000,
        "current_property_value": 0,
        "current_mortgage_debt": 0,
        "current_isa_balance": 0,
        "current_children": 0,
        "simulation_years": 10,
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
    
    # Check trajectories
    trajectories = data["trajectories"]
    assert isinstance(trajectories, list)
    assert len(trajectories) > 0
    
    # Check each trajectory structure
    for trajectory in trajectories:
        assert "states" in trajectory
        assert "decisions" in trajectory
        assert "final_wealth" in trajectory
        assert isinstance(trajectory["states"], list)
        assert isinstance(trajectory["decisions"], list)
        assert isinstance(trajectory["final_wealth"], (int, float))
        assert len(trajectory["states"]) == 10  # simulation_years
        assert len(trajectory["decisions"]) == 10
    
    # Check first trajectory state structure
    first_state = trajectories[0]["states"][0]
    required_state_fields = [
        "year", "age", "income", "cash", "property_value", 
        "mortgage_debt", "isa_balance", "num_children", 
        "living_expenses", "wealth"
    ]
    for field in required_state_fields:
        assert field in first_state
        assert isinstance(first_state[field], (int, float))
    
    # Check first decision structure
    first_decision = trajectories[0]["decisions"][0]
    required_decision_fields = ["year", "type", "amount", "description"]
    for field in required_decision_fields:
        assert field in first_decision
    
    # Check summary statistics
    summary_stats = data["summary_stats"]
    required_stats = [
        "mean_wealth", "median_wealth", "std_wealth",
        "min_wealth", "max_wealth", "p25_wealth", "p75_wealth"
    ]
    for stat in required_stats:
        assert stat in summary_stats
        assert isinstance(summary_stats[stat], (int, float))
    
    # Logical checks
    assert summary_stats["min_wealth"] <= summary_stats["p25_wealth"]
    assert summary_stats["p25_wealth"] <= summary_stats["median_wealth"]
    assert summary_stats["median_wealth"] <= summary_stats["p75_wealth"]
    assert summary_stats["p75_wealth"] <= summary_stats["max_wealth"]
    assert summary_stats["std_wealth"] >= 0

def test_monte_carlo_simulation_with_property():
    """Test simulation with existing property and mortgage"""
    payload = {
        "current_age": 35,
        "current_income": 75000,
        "current_cash": 20000,
        "current_property_value": 300000,
        "current_mortgage_debt": 240000,
        "current_isa_balance": 15000,
        "current_children": 1,
        "simulation_years": 20,
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
    # Wealth should be cash + property + isa - mortgage
    expected_initial_wealth = 20000 + 300000 + 15000 - 240000
    # Allow for some variance due to random factors
    assert abs(initial_state["wealth"] - expected_initial_wealth) < 10000

def test_monte_carlo_simulation_edge_cases():
    """Test simulation with edge case values"""
    payload = {
        "current_age": 60,  # Older age
        "current_income": 25000,  # Lower income
        "current_cash": 100000,  # High cash
        "current_property_value": 0,
        "current_mortgage_debt": 0,
        "current_isa_balance": 50000,
        "current_children": 3,  # Multiple children
        "simulation_years": 5,  # Shorter simulation
        "inflation_rate": 0.05,  # Higher inflation
        "income_growth_rate": 0.01,  # Lower growth
        "property_growth_rate": 0.02,
        "isa_return_rate": 0.04
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["trajectories"][0]["states"]) == 5
    assert data["trajectories"][0]["states"][0]["num_children"] == 3

def test_invalid_input_validation():
    """Test that invalid inputs are properly handled"""
    # Test with negative age
    invalid_payload = {
        "current_age": -5,
        "current_income": 50000,
        "current_cash": 10000,
        "simulation_years": 10,
        "inflation_rate": 0.025,
        "income_growth_rate": 0.03,
        "property_growth_rate": 0.04,
        "isa_return_rate": 0.07
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=invalid_payload)
    # Should either return 422 for validation error or handle gracefully
    assert response.status_code in [200, 422]

def test_non_trivial_decisions_are_made():
    """Test that the simulator makes non-trivial financial decisions"""
    payload = {
        "current_age": 25,  # Young age for more decision opportunities
        "current_income": 60000,  # Good income for decisions
        "current_cash": 50000,  # Enough cash for property/ISA decisions
        "current_property_value": 0,  # No property to start
        "current_mortgage_debt": 0,
        "current_isa_balance": 0,
        "current_children": 0,  # No children to start
        "simulation_years": 20,  # Longer simulation for more opportunities
        "inflation_rate": 0.025,
        "income_growth_rate": 0.03,
        "property_growth_rate": 0.04,
        "isa_return_rate": 0.07
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Count non-trivial decisions across all trajectories
    total_non_trivial_decisions = 0
    decision_types_found = set()
    
    for trajectory in data["trajectories"]:
        for decision in trajectory["decisions"]:
            if decision["type"] != "do_nothing":
                total_non_trivial_decisions += 1
                decision_types_found.add(decision["type"])
    
    # Assert that some non-trivial decisions were made
    assert total_non_trivial_decisions > 0, "No non-trivial decisions were made in any trajectory"
    
    print(f"\nDecision Analysis:")
    print(f"Total non-trivial decisions across all trajectories: {total_non_trivial_decisions}")
    print(f"Types of decisions found: {sorted(decision_types_found)}")
    
    # With good starting conditions, we should see various decision types
    expected_decisions = ["have_child", "buy_property", "get_pay_rise", "contribute_isa"]
    found_expected = [dt for dt in expected_decisions if dt in decision_types_found]
    
    print(f"Expected decision types found: {found_expected}")
    
    # At least some expected decision types should be present
    assert len(found_expected) > 0, f"None of the expected decision types {expected_decisions} were found"

def test_simulation_consistency():
    """Test that multiple runs with same parameters produce consistent results"""
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
    
    # Run simulation twice
    response1 = requests.post(f"{BASE_URL}/simulate", json=payload)
    response2 = requests.post(f"{BASE_URL}/simulate", json=payload)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    # Results should be different (due to randomness) but in similar ranges
    mean1 = data1["summary_stats"]["mean_wealth"]
    mean2 = data2["summary_stats"]["mean_wealth"]
    
    # Means should be within 20% of each other (allowing for Monte Carlo variance)
    assert abs(mean1 - mean2) / max(mean1, mean2) < 0.2

def print_sample_results():
    """Helper function to print a sample simulation result for inspection"""
    payload = {
        "current_age": 30,
        "current_income": 50000,
        "current_cash": 10000,
        "current_property_value": 0,
        "current_mortgage_debt": 0,
        "current_isa_balance": 0,
        "current_children": 0,
        "simulation_years": 10,
        "inflation_rate": 0.025,
        "income_growth_rate": 0.03,
        "property_growth_rate": 0.04,
        "isa_return_rate": 0.07
    }
    
    response = requests.post(f"{BASE_URL}/simulate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("\n=== SAMPLE SIMULATION RESULTS ===")
        print(f"Number of trajectories: {len(data['trajectories'])}")
        print(f"Mean final wealth: £{data['summary_stats']['mean_wealth']:,.0f}")
        print(f"Median final wealth: £{data['summary_stats']['median_wealth']:,.0f}")
        print(f"Best case: £{data['summary_stats']['max_wealth']:,.0f}")
        print(f"Worst case: £{data['summary_stats']['min_wealth']:,.0f}")
        
        # Show first trajectory decisions
        first_trajectory = data['trajectories'][0]
        print(f"\nFirst trajectory final wealth: £{first_trajectory['final_wealth']:,.0f}")
        print("Key decisions made:")
        for decision in first_trajectory['decisions']:
            if decision['type'] != 'do_nothing':
                print(f"  Year {decision['year']}: {decision['description']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Run a sample simulation and print results
    print("Testing Monte Carlo Personal Finance Simulator")
    print("=" * 50)
    
    try:
        print_sample_results()
        
        # Test for non-trivial decisions
        print("\n" + "=" * 50)
        print("Testing for non-trivial decisions...")
        test_non_trivial_decisions_are_made()
        
        print("\n" + "=" * 50)
        print("All manual tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: {e}")