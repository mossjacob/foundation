from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
import random
from enum import Enum
from dataclasses import dataclass

class DecisionType(str, Enum):
    HAVE_CHILD = "have_child"
    BUY_PROPERTY = "buy_property"
    TAKE_MORTGAGE = "take_mortgage"
    GET_PAY_RISE = "get_pay_rise"
    CONTRIBUTE_ISA = "contribute_isa"
    CHANGE_JOB = "change_job"
    SELL_PROPERTY = "sell_property"
    DO_NOTHING = "do_nothing"

@dataclass
class Decision:
    year: int
    type: DecisionType
    amount: float = 0.0
    description: str = ""

@dataclass
class FinancialState:
    year: int
    age: int
    income: float
    cash: float
    property_value: float
    mortgage_debt: float
    isa_balance: float
    num_children: int
    living_expenses: float
    wealth: float

class UserInput(BaseModel):
    current_age: int
    current_income: float
    current_cash: float
    current_property_value: float = 0.0
    current_mortgage_debt: float = 0.0
    current_isa_balance: float = 0.0
    current_children: int = 0
    simulation_years: int = 30
    inflation_rate: float = 0.025
    income_growth_rate: float = 0.03
    property_growth_rate: float = 0.04
    isa_return_rate: float = 0.07

class Trajectory(BaseModel):
    states: List[Dict[str, Any]]
    decisions: List[Dict[str, Any]]
    final_wealth: float

class SimulationResult(BaseModel):
    trajectories: List[Trajectory]
    summary_stats: Dict[str, float]

class MonteCarloSimulation:
    def __init__(self, user_input: UserInput):
        self.user_input = user_input
        self.num_simulations = 1000
        self.max_depth = user_input.simulation_years
        
    def run(self) -> SimulationResult:
        trajectories = []
        
        for _ in range(self.num_simulations):
            trajectory = self._run_single_simulation()
            trajectories.append(trajectory)
        
        final_wealths = [t.final_wealth for t in trajectories]
        
        summary_stats = {
            "mean_wealth": float(np.mean(final_wealths)),
            "median_wealth": float(np.median(final_wealths)),
            "std_wealth": float(np.std(final_wealths)),
            "min_wealth": float(np.min(final_wealths)),
            "max_wealth": float(np.max(final_wealths)),
            "p25_wealth": float(np.percentile(final_wealths, 25)),
            "p75_wealth": float(np.percentile(final_wealths, 75))
        }
        
        sorted_trajectories = sorted(trajectories, key=lambda x: x.final_wealth, reverse=True)
        selected_trajectories = self._select_representative_trajectories(sorted_trajectories)
        
        return SimulationResult(
            trajectories=selected_trajectories,
            summary_stats=summary_stats
        )
    
    def _select_representative_trajectories(self, sorted_trajectories: List[Trajectory]) -> List[Trajectory]:
        n = len(sorted_trajectories)
        indices = [
            0,  # Best case
            n // 4,  # 75th percentile
            n // 2,  # Median
            3 * n // 4,  # 25th percentile
            n - 1  # Worst case
        ]
        
        selected = [sorted_trajectories[i] for i in indices if i < n]
        
        random_sample = random.sample(sorted_trajectories[n//10:9*n//10], 
                                    min(15, len(sorted_trajectories[n//10:9*n//10])))
        selected.extend(random_sample)
        
        return selected
    
    def _run_single_simulation(self) -> Trajectory:
        state = FinancialState(
            year=0,
            age=self.user_input.current_age,
            income=self.user_input.current_income,
            cash=self.user_input.current_cash,
            property_value=self.user_input.current_property_value,
            mortgage_debt=self.user_input.current_mortgage_debt,
            isa_balance=self.user_input.current_isa_balance,
            num_children=self.user_input.current_children,
            living_expenses=self._calculate_living_expenses(self.user_input.current_income, self.user_input.current_children),
            wealth=0
        )
        
        states = []
        decisions = []
        
        for year in range(self.max_depth):
            state.year = year
            state.age = self.user_input.current_age + year
            
            decision = self._make_decision(state)
            decisions.append({
                "year": year,
                "type": decision.type.value,
                "amount": decision.amount,
                "description": decision.description
            })
            
            state = self._apply_decision(state, decision)
            state = self._apply_yearly_changes(state)
            
            state.wealth = state.cash + state.property_value + state.isa_balance - state.mortgage_debt
            
            states.append({
                "year": year,
                "age": state.age,
                "income": state.income,
                "cash": state.cash,
                "property_value": state.property_value,
                "mortgage_debt": state.mortgage_debt,
                "isa_balance": state.isa_balance,
                "num_children": state.num_children,
                "living_expenses": state.living_expenses,
                "wealth": state.wealth
            })
        
        return Trajectory(
            states=states,
            decisions=decisions,
            final_wealth=state.wealth
        )
    
    def _make_decision(self, state: FinancialState) -> Decision:
        possible_decisions = self._get_possible_decisions(state)
        decision_types = list(possible_decisions.keys())
        probabilities = list(possible_decisions.values())
        
        # Convert enum keys to indices for np.random.choice
        choice_idx = np.random.choice(len(decision_types), p=probabilities)
        decision_type = decision_types[choice_idx]
        
        if decision_type == DecisionType.HAVE_CHILD:
            return Decision(state.year, decision_type, 0, "Have a child")
        elif decision_type == DecisionType.BUY_PROPERTY:
            property_price = np.random.normal(300000, 50000)
            return Decision(state.year, decision_type, property_price, f"Buy property for £{property_price:,.0f}")
        elif decision_type == DecisionType.TAKE_MORTGAGE:
            mortgage_amount = min(state.cash * 0.8, state.income * 4.5)
            return Decision(state.year, decision_type, mortgage_amount, f"Take mortgage of £{mortgage_amount:,.0f}")
        elif decision_type == DecisionType.GET_PAY_RISE:
            raise_amount = np.random.normal(0.05, 0.02)
            return Decision(state.year, decision_type, raise_amount, f"Get {raise_amount:.1%} pay rise")
        elif decision_type == DecisionType.CONTRIBUTE_ISA:
            max_contribution = min(20000, state.cash * 0.3)
            contribution = np.random.uniform(0.5, 1.0) * max_contribution
            return Decision(state.year, decision_type, contribution, f"Contribute £{contribution:,.0f} to ISA")
        else:
            return Decision(state.year, DecisionType.DO_NOTHING, 0, "No major financial decision")
    
    def _get_possible_decisions(self, state: FinancialState) -> Dict[DecisionType, float]:
        decisions = {DecisionType.DO_NOTHING: 0.4}
        
        if state.age < 45 and state.num_children < 3:
            decisions[DecisionType.HAVE_CHILD] = 0.1
        
        if state.property_value == 0 and state.cash > 50000:
            decisions[DecisionType.BUY_PROPERTY] = 0.2
        
        if state.property_value > 0 and state.mortgage_debt == 0:
            decisions[DecisionType.TAKE_MORTGAGE] = 0.05
        
        if state.year % 3 == 0:
            decisions[DecisionType.GET_PAY_RISE] = 0.15
        
        if state.cash > 5000:
            decisions[DecisionType.CONTRIBUTE_ISA] = 0.3
        
        total = sum(decisions.values())
        return {k: v/total for k, v in decisions.items()}
    
    def _apply_decision(self, state: FinancialState, decision: Decision) -> FinancialState:
        if decision.type == DecisionType.HAVE_CHILD:
            state.num_children += 1
            state.living_expenses = self._calculate_living_expenses(state.income, state.num_children)
        elif decision.type == DecisionType.BUY_PROPERTY:
            state.property_value = decision.amount
            state.cash -= decision.amount * 0.2  # 20% deposit
            state.mortgage_debt += decision.amount * 0.8
        elif decision.type == DecisionType.TAKE_MORTGAGE:
            state.mortgage_debt += decision.amount
            state.cash += decision.amount
        elif decision.type == DecisionType.GET_PAY_RISE:
            state.income *= (1 + decision.amount)
        elif decision.type == DecisionType.CONTRIBUTE_ISA:
            state.cash -= decision.amount
            state.isa_balance += decision.amount
        
        return state
    
    def _apply_yearly_changes(self, state: FinancialState) -> FinancialState:
        inflation = np.random.normal(self.user_input.inflation_rate, 0.01)
        income_growth = np.random.normal(self.user_input.income_growth_rate, 0.02)
        property_growth = np.random.normal(self.user_input.property_growth_rate, 0.03)
        isa_return = np.random.normal(self.user_input.isa_return_rate, 0.05)
        
        state.income *= (1 + income_growth)
        state.property_value *= (1 + property_growth)
        state.isa_balance *= (1 + isa_return)
        state.living_expenses *= (1 + inflation)
        
        mortgage_payment = state.mortgage_debt * 0.05 if state.mortgage_debt > 0 else 0
        annual_savings = state.income - state.living_expenses - mortgage_payment
        state.cash += annual_savings
        
        if mortgage_payment > 0:
            principal_payment = mortgage_payment * 0.6
            state.mortgage_debt = max(0, state.mortgage_debt - principal_payment)
        
        state.cash = max(0, state.cash)
        
        return state
    
    def _calculate_living_expenses(self, income: float, num_children: int) -> float:
        base_expenses = income * 0.6
        child_expenses = num_children * 12000
        return base_expenses + child_expenses