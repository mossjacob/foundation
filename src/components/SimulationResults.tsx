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
          <div className="h-96 w-full overflow-x-auto">
            <div className="min-w-[800px] h-96">
              <Line data={chartData} options={chartOptions} />
            </div>
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

      <Card>
        <CardHeader>
          <CardTitle>Simulation Details: Events & Assumptions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h4 className="text-lg font-semibold mb-3">Financial Decisions Modeled</h4>
              <div className="grid gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h5 className="font-semibold text-blue-900">Having Children</h5>
                  <p className="text-sm text-gray-700 mt-1">15% chance if age &lt; 45 and children &lt; 3</p>
                  <p className="text-sm text-gray-600">Adds £12,000/year in expenses per child</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <h5 className="font-semibold text-green-900">Buying Property</h5>
                  <p className="text-sm text-gray-700 mt-1">25% chance if no property and cash &gt; £30,000</p>
                  <p className="text-sm text-gray-600">Average price £300,000 (±£50k), 20% deposit required</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <h5 className="font-semibold text-purple-900">Getting Pay Rise</h5>
                  <p className="text-sm text-gray-700 mt-1">20% chance every 2 years</p>
                  <p className="text-sm text-gray-600">Average 5% increase (±2%)</p>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg">
                  <h5 className="font-semibold text-orange-900">ISA Contributions</h5>
                  <p className="text-sm text-gray-700 mt-1">40% chance if cash &gt; £2,000</p>
                  <p className="text-sm text-gray-600">Up to £20,000/year, 50-100% of available amount</p>
                </div>
                <div className="p-4 bg-red-50 rounded-lg">
                  <h5 className="font-semibold text-red-900">Taking Mortgage</h5>
                  <p className="text-sm text-gray-700 mt-1">10% chance if own property with no mortgage</p>
                  <p className="text-sm text-gray-600">Max 4.5× income or 80% of cash</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h5 className="font-semibold text-gray-900">Do Nothing</h5>
                  <p className="text-sm text-gray-700 mt-1">20% base probability each year</p>
                  <p className="text-sm text-gray-600">No major financial decisions made</p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-3">Economic Assumptions</h4>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h5 className="font-medium mb-2">Annual Growth Rates</h5>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Inflation: 2.5% ±1%</li>
                    <li>• Income Growth: 3% ±2%</li>
                    <li>• Property Growth: 4% ±3%</li>
                    <li>• ISA Returns: 7% ±5%</li>
                  </ul>
                </div>
                <div>
                  <h5 className="font-medium mb-2">Fixed Parameters</h5>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Property Deposit: 20%</li>
                    <li>• Mortgage Rate: 5%/year</li>
                    <li>• Base Living Costs: 60% of income</li>
                    <li>• Max Children: 3</li>
                  </ul>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-3">Wealth Calculation</h4>
              <div className="p-4 bg-gray-100 rounded-lg">
                <code className="text-sm">
                  Total Wealth = Cash + Property Value + ISA Balance - Mortgage Debt
                </code>
              </div>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-3">What's Not Modeled</h4>
              <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
                <ul className="space-y-1">
                  <li>• Unemployment or career breaks</li>
                  <li>• Market crashes or recessions</li>
                  <li>• Pension contributions</li>
                  <li>• Healthcare costs</li>
                  <li>• Relationship changes</li>
                </ul>
                <ul className="space-y-1">
                  <li>• Inheritance or windfalls</li>
                  <li>• Student loan repayments</li>
                  <li>• Other investments beyond ISAs</li>
                  <li>• Emergency fund strategies</li>
                  <li>• Behavioral spending patterns</li>
                </ul>
              </div>
            </div>

            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h5 className="font-semibold text-yellow-900 mb-2">Important Note</h5>
              <p className="text-sm text-yellow-800">
                This simulation provides illustrative scenarios based on probabilistic modeling. 
                Real financial outcomes depend on many factors not captured in this model. 
                Always consult with qualified financial advisors for personal financial planning.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}