export interface UserInput {
  current_age: number;
  current_income: number;
  current_cash: number;
  current_property_value: number;
  current_mortgage_debt: number;
  current_isa_balance: number;
  current_children: number;
  simulation_years: number;
  inflation_rate: number;
  income_growth_rate: number;
  property_growth_rate: number;
  isa_return_rate: number;
}

export interface FinancialState {
  year: number;
  age: number;
  income: number;
  cash: number;
  property_value: number;
  mortgage_debt: number;
  isa_balance: number;
  num_children: number;
  living_expenses: number;
  wealth: number;
}

export interface Decision {
  year: number;
  type: string;
  amount: number;
  description: string;
}

export interface Trajectory {
  states: FinancialState[];
  decisions: Decision[];
  final_wealth: number;
}

export interface SummaryStats {
  mean_wealth: number;
  median_wealth: number;
  std_wealth: number;
  min_wealth: number;
  max_wealth: number;
  p25_wealth: number;
  p75_wealth: number;
}

export interface SimulationData {
  trajectories: Trajectory[];
  summary_stats: SummaryStats;
}