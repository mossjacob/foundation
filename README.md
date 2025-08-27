# Personal Finance Monte Carlo Simulator

A comprehensive personal finance application that uses Monte Carlo Tree Search to simulate various financial trajectories over time. The application helps users understand potential wealth outcomes based on different financial decisions.

## Features

- **Monte Carlo Simulation**: Runs 1000+ simulations to explore different financial paths
- **Interactive Visualization**: Chart.js powered charts showing wealth trajectories
- **Decision Analysis**: Click on any trajectory to see the financial decisions that led to that outcome
- **Comprehensive Input**: Account for income, properties, mortgages, ISAs, children, and economic assumptions
- **Statistical Summary**: View mean, median, best/worst case scenarios

## Architecture

- **Frontend**: React + TypeScript + Vite + shadcn/ui + Chart.js
- **Backend**: FastAPI + Python with NumPy for Monte Carlo simulations
- **Simulation Engine**: Custom Monte Carlo Tree Search algorithm considering inflation, income growth, and various financial decisions

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.8+)
- pip

### Installation

1. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Python Backend**
   ```bash
   cd backend
   python start.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the React Frontend**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## How It Works

### Monte Carlo Simulation
The application runs 1000 simulations, each exploring a different path through financial decisions over the specified time period. Each simulation:

1. Starts with your current financial state
2. Makes probabilistic decisions each year (having children, buying property, getting pay rises, etc.)
3. Applies economic factors (inflation, income growth, property appreciation)
4. Tracks wealth progression over time

### Financial Decisions Modeled
- Having children (affects living expenses)
- Buying property (deposit, mortgage)
- Taking mortgages
- Getting pay rises
- Contributing to ISAs
- Economic factors (inflation, property growth, investment returns)

### Visualization
- Interactive line chart showing multiple wealth trajectories
- Click any line to see the specific decisions that led to that outcome
- Summary statistics showing distribution of outcomes

## Configuration

You can adjust simulation parameters including:
- Simulation duration (years)
- Inflation rate assumptions
- Income growth rate
- Property growth rate
- ISA return assumptions

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint

The application uses shadcn/ui for components and Tailwind CSS for styling.
