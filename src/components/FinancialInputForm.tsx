import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { SimulationData, UserInput } from "../types/simulation"

const formSchema = z.object({
  current_age: z.number().min(18).max(80),
  current_income: z.number().min(0),
  current_cash: z.number().min(0),
  current_property_value: z.number().min(0).optional(),
  current_mortgage_debt: z.number().min(0).optional(),
  current_isa_balance: z.number().min(0).optional(),
  current_children: z.number().min(0).max(10),
  simulation_years: z.number().min(5).max(50),
  inflation_rate: z.number().min(0).max(0.2),
  income_growth_rate: z.number().min(0).max(0.2),
  property_growth_rate: z.number().min(0).max(0.2),
  isa_return_rate: z.number().min(0).max(0.3),
})

type FormData = z.infer<typeof formSchema>

interface Props {
  onSimulationComplete: (data: SimulationData) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export default function FinancialInputForm({ onSimulationComplete, isLoading, setIsLoading }: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      current_age: 30,
      current_income: 50000,
      current_cash: 10000,
      current_property_value: 0,
      current_mortgage_debt: 0,
      current_isa_balance: 0,
      current_children: 0,
      simulation_years: 30,
      inflation_rate: 0.025,
      income_growth_rate: 0.03,
      property_growth_rate: 0.04,
      isa_return_rate: 0.07,
    }
  })

  const onSubmit = async (data: FormData) => {
    setIsLoading(true)
    try {
      const userInput: UserInput = {
        ...data,
        current_property_value: data.current_property_value || 0,
        current_mortgage_debt: data.current_mortgage_debt || 0,
        current_isa_balance: data.current_isa_balance || 0,
      }

      const apiUrl = import.meta.env.PROD ? "/api/simulate" : "http://localhost:8000/simulate"
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userInput),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result: SimulationData = await response.json()
      onSimulationComplete(result)
    } catch (error) {
      console.error("Simulation failed:", error)
      alert("Simulation failed. Please make sure the Python backend is running on localhost:8000")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>Enter Your Financial Information</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Personal Information</h3>
              
              <div>
                <Label htmlFor="current_age">Current Age</Label>
                <Input
                  id="current_age"
                  type="number"
                  {...register("current_age", { valueAsNumber: true })}
                />
                {errors.current_age && (
                  <p className="text-red-500 text-sm mt-1">{errors.current_age.message}</p>
                )}
              </div>

              <div>
                <Label htmlFor="current_income">Annual Income (£)</Label>
                <Input
                  id="current_income"
                  type="number"
                  {...register("current_income", { valueAsNumber: true })}
                />
                {errors.current_income && (
                  <p className="text-red-500 text-sm mt-1">{errors.current_income.message}</p>
                )}
              </div>

              <div>
                <Label htmlFor="current_children">Number of Children</Label>
                <Input
                  id="current_children"
                  type="number"
                  {...register("current_children", { valueAsNumber: true })}
                />
                {errors.current_children && (
                  <p className="text-red-500 text-sm mt-1">{errors.current_children.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Financial Assets</h3>
              
              <div>
                <Label htmlFor="current_cash">Cash Savings (£)</Label>
                <Input
                  id="current_cash"
                  type="number"
                  {...register("current_cash", { valueAsNumber: true })}
                />
                {errors.current_cash && (
                  <p className="text-red-500 text-sm mt-1">{errors.current_cash.message}</p>
                )}
              </div>

              <div>
                <Label htmlFor="current_property_value">Property Value (£)</Label>
                <Input
                  id="current_property_value"
                  type="number"
                  {...register("current_property_value", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="current_mortgage_debt">Mortgage Debt (£)</Label>
                <Input
                  id="current_mortgage_debt"
                  type="number"
                  {...register("current_mortgage_debt", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="current_isa_balance">ISA Balance (£)</Label>
                <Input
                  id="current_isa_balance"
                  type="number"
                  {...register("current_isa_balance", { valueAsNumber: true })}
                />
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Simulation Parameters</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="simulation_years">Simulation Years</Label>
                <Input
                  id="simulation_years"
                  type="number"
                  {...register("simulation_years", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="inflation_rate">Inflation Rate (0.025 = 2.5%)</Label>
                <Input
                  id="inflation_rate"
                  type="number"
                  step="0.001"
                  {...register("inflation_rate", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="income_growth_rate">Income Growth Rate (0.03 = 3%)</Label>
                <Input
                  id="income_growth_rate"
                  type="number"
                  step="0.001"
                  {...register("income_growth_rate", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="property_growth_rate">Property Growth Rate (0.04 = 4%)</Label>
                <Input
                  id="property_growth_rate"
                  type="number"
                  step="0.001"
                  {...register("property_growth_rate", { valueAsNumber: true })}
                />
              </div>

              <div>
                <Label htmlFor="isa_return_rate">ISA Return Rate (0.07 = 7%)</Label>
                <Input
                  id="isa_return_rate"
                  type="number"
                  step="0.001"
                  {...register("isa_return_rate", { valueAsNumber: true })}
                />
              </div>
            </div>
          </div>

          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? "Running Simulation..." : "Run Monte Carlo Simulation"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}