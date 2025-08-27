import { useState } from 'react'
import FinancialInputForm from './components/FinancialInputForm'
import SimulationResults from './components/SimulationResults'
import type { SimulationData } from './types/simulation'
import './App.css'

function App() {
  const [simulationData, setSimulationData] = useState<SimulationData | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSimulationComplete = (data: SimulationData) => {
    setSimulationData(data)
  }

  const handleNewSimulation = () => {
    setSimulationData(null)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-900">
          Personal Finance Monte Carlo Simulator
        </h1>
        
        {!simulationData ? (
          <FinancialInputForm
            onSimulationComplete={handleSimulationComplete}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        ) : (
          <SimulationResults
            data={simulationData}
            onNewSimulation={handleNewSimulation}
          />
        )}
      </div>
    </div>
  )
}

export default App
