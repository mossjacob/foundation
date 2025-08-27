from flask import Flask, request, jsonify
from flask_cors import CORS
from api.lib.monte_carlo import MonteCarloSimulation, UserInput

app = Flask(__name__)
CORS(app)  # Allow all origins for deployment - restrict in production

@app.route("/")
def root():
    return {"message": "Personal Finance Monte Carlo API"}

@app.route("/api/simulate", methods=["POST"])
def run_simulation():
    try:
        data = request.get_json()
        user_input = UserInput(**data)
        mc = MonteCarloSimulation(user_input)
        result = mc.run()
        
        # Convert to dict for JSON serialization
        return {
            "trajectories": [
                {
                    "states": trajectory.states,
                    "decisions": trajectory.decisions,
                    "final_wealth": trajectory.final_wealth
                } for trajectory in result.trajectories
            ],
            "summary_stats": result.summary_stats
        }
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)