from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from monte_carlo import MonteCarloSimulation, UserInput, SimulationResult

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Personal Finance Monte Carlo API"}

@app.post("/simulate", response_model=SimulationResult)
async def run_simulation(user_input: UserInput):
    mc = MonteCarloSimulation(user_input)
    result = mc.run()
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}