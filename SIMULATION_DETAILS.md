# Monte Carlo Simulation: Events and Assumptions

This document details all the financial events, decisions, and assumptions used in the Personal Finance Monte Carlo simulation.

## Financial Decisions Modeled

### 1. Having Children (`have_child`)
- **Trigger**: Age < 45 and current children < 3
- **Probability**: 15% (when conditions are met)
- **Effect**: 
  - Increases number of children by 1
  - Adds £12,000 per year in living expenses per child
  - Recalculates total living expenses

### 2. Buying Property (`buy_property`)
- **Trigger**: No current property and cash > £30,000
- **Probability**: 25% (when conditions are met)
- **Property Price**: Normal distribution (mean: £300,000, std: £50,000)
- **Effect**:
  - Sets property value to purchase price
  - Reduces cash by 20% (deposit)
  - Increases mortgage debt by 80% of property price

### 3. Taking a Mortgage (`take_mortgage`)
- **Trigger**: Own property and no existing mortgage debt
- **Probability**: 10% (when conditions are met)
- **Mortgage Amount**: Lesser of 80% of cash or 4.5× annual income
- **Effect**:
  - Increases mortgage debt
  - Increases available cash

### 4. Getting Pay Rise (`get_pay_rise`)
- **Trigger**: Every 2 years (when year % 2 == 0)
- **Probability**: 20% (when triggered)
- **Raise Amount**: Normal distribution (mean: 5%, std: 2%)
- **Effect**: Multiplies annual income by (1 + raise_amount)

### 5. Contributing to ISA (`contribute_isa`)
- **Trigger**: Cash > £2,000
- **Probability**: 40% (when conditions are met)
- **Contribution Amount**: 
  - Maximum: Lesser of £20,000 or 30% of current cash
  - Actual: Random between 50% and 100% of maximum
- **Effect**:
  - Reduces cash by contribution amount
  - Increases ISA balance by contribution amount

### 6. Do Nothing (`do_nothing`)
- **Probability**: 20% base probability
- **Effect**: No financial changes made in that year

## Economic Assumptions

### Annual Growth Rates
- **Inflation Rate**: Default 2.5% (user configurable)
- **Income Growth Rate**: Default 3% (user configurable)
- **Property Growth Rate**: Default 4% (user configurable)
- **ISA Return Rate**: Default 7% (user configurable)

### Variability
All economic factors include random variation:
- **Income Growth**: Normal distribution (mean: user setting, std: 2%)
- **Property Growth**: Normal distribution (mean: user setting, std: 3%)
- **ISA Returns**: Normal distribution (mean: user setting, std: 5%)
- **Inflation**: Normal distribution (mean: user setting, std: 1%)

## Financial Calculations

### Living Expenses
- **Base Expenses**: 60% of annual income
- **Child Expenses**: £12,000 per child per year
- **Inflation Adjustment**: Applied annually
- **Formula**: `(income × 0.6) + (children × £12,000)` × inflation adjustment

### Mortgage Payments
- **Annual Payment**: 5% of outstanding mortgage debt
- **Principal vs Interest**: 60% goes to principal, 40% to interest
- **Effect**: Reduces mortgage debt and available cash

### Annual Savings Calculation
```
Annual Savings = Income - Living Expenses - Mortgage Payment
```
- If positive: Added to cash reserves
- If negative: May result in financial stress (cash cannot go below £0)

### Wealth Calculation
```
Total Wealth = Cash + Property Value + ISA Balance - Mortgage Debt
```

## Decision Probability System

The simulation uses a weighted probability system where multiple decisions can be possible in any given year:

1. **Base Probabilities**: Each decision type has a base probability
2. **Condition Checking**: Only decisions meeting trigger conditions are included
3. **Normalization**: All possible probabilities are normalized to sum to 1.0
4. **Random Selection**: One decision is randomly selected based on normalized probabilities

### Example Probability Calculation
If in a given year:
- Do Nothing: 20% base
- Contribute ISA: 40% (cash > £2,000)
- Get Pay Rise: 20% (even year)

Normalized probabilities:
- Do Nothing: 20/80 = 25%
- Contribute ISA: 40/80 = 50%  
- Get Pay Rise: 20/80 = 25%

## Simulation Parameters

### User Configurable Inputs
- **Personal**: Age, income, current children
- **Financial**: Cash, property value, mortgage debt, ISA balance
- **Simulation**: Number of years to simulate
- **Economic**: All growth rates and inflation assumptions

### Fixed Parameters
- **Property Deposit**: 20% of property price
- **Mortgage Lending**: Maximum 4.5× income or 80% of cash
- **ISA Annual Limit**: £20,000
- **Maximum Children**: 3 (for simulation purposes)
- **Child-bearing Age**: Up to 45 years old
- **Mortgage Interest Rate**: 5% annually (payment rate)

## Limitations and Simplifications

### What's Not Modeled
- **Unemployment**: Income is assumed to continue
- **Market Crashes**: Property and ISA values don't account for major downturns
- **Pension Contributions**: Not included in current model
- **Healthcare Costs**: Beyond basic child expenses
- **Divorce/Relationship Changes**: Single-person financial model
- **Inheritance**: No windfall events
- **Career Changes**: No major income disruptions
- **Student Loans**: Not factored into debt calculations
- **Other Investments**: Only ISAs are modeled

### Simplifications
- **Linear Expenses**: Child costs are fixed per year
- **Perfect Information**: All decisions made with complete knowledge
- **No Behavioral Economics**: No irrational financial behavior
- **Single Property**: Only one property ownership modeled
- **Fixed Mortgage Terms**: No remortgaging or rate changes
- **No Emergency Fund**: No separate emergency savings strategy

## Statistical Output

The simulation runs 1,000 iterations and provides:
- **Mean Wealth**: Average final wealth across all simulations
- **Median Wealth**: 50th percentile outcome
- **Standard Deviation**: Measure of outcome variability
- **Percentiles**: 25th and 75th percentile outcomes
- **Range**: Minimum and maximum outcomes observed
- **Individual Trajectories**: Sample paths showing decision sequences

This allows users to understand both the expected outcome and the range of possible financial futures based on probabilistic decision-making and economic uncertainty.