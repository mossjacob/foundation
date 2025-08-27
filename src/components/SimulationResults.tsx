import { useState } from "react"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  type ChartEvent,
  type ActiveElement,
} from "chart.js"
import { Line } from "react-chartjs-2"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { SimulationData, Trajectory } from "../types/simulation"

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

interface Props {
  data: SimulationData
  onNewSimulation: () => void
}

export default function SimulationResults({ data, onNewSimulation }: Props) {
  const [selectedTrajectory, setSelectedTrajectory] = useState<Trajectory | null>(null)

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency: "GBP",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }


  const generateColors = (count: number) => {
    const colors = []
    for (let i = 0; i < count; i++) {
      const hue = (i * 137.508) % 360
      colors.push(`hsla(${hue}, 70%, 50%, 0.6)`)
    }
    return colors
  }

  const chartData = {
    labels: data.trajectories[0]?.states.map((_, index) => `Year ${index}`) || [],
    datasets: data.trajectories.map((trajectory, index) => ({
      label: `Trajectory ${index + 1} (Final: ${formatCurrency(trajectory.final_wealth)})`,
      data: trajectory.states.map(state => state.wealth),
      borderColor: generateColors(data.trajectories.length)[index],
      backgroundColor: generateColors(data.trajectories.length)[index],
      borderWidth: 2,
      fill: false,
      pointRadius: 0,
      pointHoverRadius: 5,
      trajectoryIndex: index,
    })),
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
        display: false,
      },
      title: {
        display: true,
        text: "Wealth Trajectories Over Time",
      },
      tooltip: {
        mode: "nearest" as const,
        intersect: true,
        position: "nearest" as const,
        yAlign: "center" as const,
        xAlign: "right" as const,
        displayColors: false,
        bodySpacing: 0,
        titleSpacing: 0,
        footerSpacing: 0,
        cornerRadius: 4,
        caretPadding: 15,
        callbacks: {
          title: function() {
            return ""; // Remove title to make tooltip smaller
          },
          label: function(context: any) {
            return `${context.dataset.label}: ${formatCurrency(context.parsed.y)}`
          },
        }
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: "Years",
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: "Wealth (£)",
        },
        ticks: {
          callback: function(value: any) {
            return formatCurrency(value)
          },
        },
      },
    },
    onClick: (_event: ChartEvent, elements: ActiveElement[]) => {
      console.log(elements)
      if (elements.length > 0) {
        const datasetIndex = elements[0].datasetIndex
        setSelectedTrajectory(data.trajectories[datasetIndex])
      }
    },
    interaction: {
      mode: "dataset" as const,
//       axis: "x" as const,
      intersect: false,
    },
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Simulation Results</h2>
        <Button onClick={onNewSimulation} variant="outline">
          New Simulation
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Mean Wealth</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">
              {formatCurrency(data.summary_stats.mean_wealth)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Median Wealth</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-blue-600">
              {formatCurrency(data.summary_stats.median_wealth)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Best Case</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-emerald-600">
              {formatCurrency(data.summary_stats.max_wealth)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Worst Case</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-red-600">
              {formatCurrency(data.summary_stats.min_wealth)}
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Wealth Trajectories</CardTitle>
          <p className="text-sm text-gray-600">
            Click on any line to see the decisions made in that trajectory
          </p>
        </CardHeader>
        <CardContent>
          <div className="h-96 w-full">
            <Line data={chartData} options={chartOptions} />
          </div>
        </CardContent>
      </Card>

      {selectedTrajectory && (
        <Card>
          <CardHeader>
            <CardTitle>
              Selected Trajectory Details (Final Wealth: {formatCurrency(selectedTrajectory.final_wealth)})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2">Key Decisions Made:</h4>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {selectedTrajectory.decisions
                    .filter(decision => decision.type !== "do_nothing")
                    .map((decision, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span className="font-medium">Year {decision.year}:</span>
                        <span>{decision.description}</span>
                      </div>
                    ))}
                </div>
              </div>

              <div>
                <h4 className="text-lg font-semibold mb-2">Final State:</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {(() => {
                    const finalState = selectedTrajectory.states[selectedTrajectory.states.length - 1]
                    return (
                      <>
                        <div className="text-center">
                          <p className="text-sm text-gray-600">Age</p>
                          <p className="font-semibold">{finalState.age}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-gray-600">Income</p>
                          <p className="font-semibold">{formatCurrency(finalState.income)}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-gray-600">Property Value</p>
                          <p className="font-semibold">{formatCurrency(finalState.property_value)}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-gray-600">Children</p>
                          <p className="font-semibold">{finalState.num_children}</p>
                        </div>
                      </>
                    )
                  })()}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}