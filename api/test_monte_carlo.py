from api.lib.monte_carlo import MonteCarloSimulation, UserInput, DecisionType
import numpy as np

def test_monte_carlo_initialization():
    """Test that Monte Carlo simulation initializes correctly"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        current_property_value=0,
        current_mortgage_debt=0,
        current_isa_balance=0,
        current_children=0,
        simulation_years=10,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    assert mc.user_input == user_input
    assert mc.num_simulations == 1000
    assert mc.max_depth == 10

def test_monte_carlo_single_simulation():
    """Test running a single simulation trajectory"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        simulation_years=5,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    trajectory = mc._run_single_simulation()
    
    # Check trajectory structure
    assert hasattr(trajectory, 'states')
    assert hasattr(trajectory, 'decisions')
    assert hasattr(trajectory, 'final_wealth')
    
    # Check correct number of states and decisions
    assert len(trajectory.states) == 5
    assert len(trajectory.decisions) == 5
    
    # Check state progression
    for i, state in enumerate(trajectory.states):
        assert state['year'] == i
        assert state['age'] == 30 + i
        assert state['wealth'] >= 0  # Wealth should be non-negative

def test_decision_types_are_available():
    """Test that different decision types can be made"""
    user_input = UserInput(
        current_age=25,  # Young age for more opportunities
        current_income=60000,
        current_cash=50000,  # Good cash for decisions
        current_property_value=0,
        current_mortgage_debt=0,
        current_isa_balance=0,
        current_children=0,
        simulation_years=20,  # Longer simulation
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    
    # Run multiple simulations to increase chance of different decisions
    decision_types_found = set()
    non_trivial_decisions = 0
    
    for _ in range(50):  # Run 50 trajectories
        trajectory = mc._run_single_simulation()
        for decision in trajectory.decisions:
            decision_types_found.add(decision['type'])
            if decision['type'] != 'do_nothing':
                non_trivial_decisions += 1
    
    print(f"\nDecision Types Found: {sorted(decision_types_found)}")
    print(f"Total non-trivial decisions across 50 trajectories: {non_trivial_decisions}")
    
    # Should have at least some variety in decisions
    assert len(decision_types_found) > 1, "Only one type of decision was made"
    assert non_trivial_decisions > 0, "No non-trivial decisions were made"

def test_financial_state_progression():
    """Test that financial state progresses logically"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        simulation_years=10,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    trajectory = mc._run_single_simulation()
    
    # Check that age progresses correctly
    for i, state in enumerate(trajectory.states):
        assert state['age'] == 30 + i
        assert state['year'] == i
    
    # Check that income generally trends upward (allowing for some variance)
    initial_income = trajectory.states[0]['income']
    final_income = trajectory.states[-1]['income']
    # With 3% growth over 10 years, should be at least 20% higher
    assert final_income > initial_income * 1.2

def test_wealth_calculation():
    """Test that wealth is calculated correctly"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        current_property_value=100000,
        current_mortgage_debt=80000,
        current_isa_balance=5000,
        simulation_years=1,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    trajectory = mc._run_single_simulation()
    
    initial_state = trajectory.states[0]
    
    # Wealth = cash + property + ISA - mortgage
    expected_wealth = (initial_state['cash'] + 
                      initial_state['property_value'] + 
                      initial_state['isa_balance'] - 
                      initial_state['mortgage_debt'])
    
    assert abs(initial_state['wealth'] - expected_wealth) < 1, "Wealth calculation incorrect"

def test_decision_probabilities():
    """Test that decision probabilities work as expected"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        simulation_years=5,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    
    # Create a test state
    from api.lib.monte_carlo import FinancialState
    test_state = FinancialState(
        year=0,
        age=30,
        income=50000,
        cash=60000,  # High cash to enable property purchase
        property_value=0,
        mortgage_debt=0,
        isa_balance=0,
        num_children=0,
        living_expenses=30000,
        wealth=60000
    )
    
    # Get possible decisions
    decisions = mc._get_possible_decisions(test_state)
    
    # Should include multiple decision types
    assert DecisionType.DO_NOTHING in decisions
    assert DecisionType.CONTRIBUTE_ISA in decisions  # Should be possible with high cash
    
    # Probabilities should sum to 1
    total_prob = sum(decisions.values())
    assert abs(total_prob - 1.0) < 0.001

def test_full_simulation():
    """Test running the full Monte Carlo simulation"""
    user_input = UserInput(
        current_age=30,
        current_income=50000,
        current_cash=10000,
        simulation_years=5,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    # Reduce number of simulations for faster testing
    mc = MonteCarloSimulation(user_input)
    mc.num_simulations = 100  # Reduce for testing
    
    result = mc.run()
    
    # Check result structure
    assert hasattr(result, 'trajectories')
    assert hasattr(result, 'summary_stats')
    
    # Should have selected representative trajectories
    assert len(result.trajectories) <= 100
    assert len(result.trajectories) > 0
    
    # Check summary statistics
    stats = result.summary_stats
    required_stats = ['mean_wealth', 'median_wealth', 'std_wealth', 
                     'min_wealth', 'max_wealth', 'p25_wealth', 'p75_wealth']
    
    for stat in required_stats:
        assert stat in stats
        assert isinstance(stats[stat], (int, float))

def print_decision_analysis():
    """Analyze decision-making patterns"""
    user_input = UserInput(
        current_age=25,
        current_income=60000,
        current_cash=50000,
        current_property_value=0,
        current_mortgage_debt=0,
        current_isa_balance=0,
        current_children=0,
        simulation_years=15,
        inflation_rate=0.025,
        income_growth_rate=0.03,
        property_growth_rate=0.04,
        isa_return_rate=0.07
    )
    
    mc = MonteCarloSimulation(user_input)
    
    # Collect decision statistics
    decision_counts = {}
    total_decisions = 0
    
    print("\n=== DECISION ANALYSIS ===")
    print("Running 100 trajectories to analyze decision patterns...")
    
    for _ in range(100):
        trajectory = mc._run_single_simulation()
        for decision in trajectory.decisions:
            decision_type = decision['type']
            decision_counts[decision_type] = decision_counts.get(decision_type, 0) + 1
            total_decisions += 1
    
    print(f"\nDecision Statistics (out of {total_decisions} total decisions):")
    for decision_type, count in sorted(decision_counts.items()):
        percentage = (count / total_decisions) * 100
        print(f"  {decision_type}: {count} ({percentage:.1f}%)")
    
    non_trivial = total_decisions - decision_counts.get('do_nothing', 0)
    print(f"\nNon-trivial decisions: {non_trivial} ({(non_trivial/total_decisions)*100:.1f}%)")

if __name__ == "__main__":
    print("Testing Monte Carlo Simulation Algorithm")
    print("=" * 50)
    
    try:
        print("Testing initialization...")
        test_monte_carlo_initialization()
        print("✓ Initialization working")
        
        print("\nTesting single simulation...")
        test_monte_carlo_single_simulation()
        print("✓ Single simulation working")
        
        print("\nTesting financial state progression...")
        test_financial_state_progression()
        print("✓ State progression working")
        
        print("\nTesting wealth calculation...")
        test_wealth_calculation()
        print("✓ Wealth calculation working")
        
        print("\nTesting decision probabilities...")
        test_decision_probabilities()
        print("✓ Decision probabilities working")
        
        print("\nTesting decision variety...")
        test_decision_types_are_available()
        print("✓ Decision variety working")
        
        print("\nTesting full simulation...")
        test_full_simulation()
        print("✓ Full simulation working")
        
        # Print decision analysis
        print_decision_analysis()
        
        print("\n" + "=" * 50)
        print("All Monte Carlo algorithm tests completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()