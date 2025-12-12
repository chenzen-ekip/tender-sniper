import { ArrowRight } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function DashboardStats() {
    return (
        <div className="grid gap-4 md:grid-cols-2">
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">
                        Marchés Identifiés:
                    </CardTitle>
                    <button className="text-primary hover:text-primary/80">
                        <ArrowRight className="h-5 w-5" />
                    </button>
                </CardHeader>
                <CardContent>
                    <div className="text-4xl font-bold">12 <span className="text-lg font-normal text-muted-foreground">(+4 today)</span></div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">
                        Potentiel Total:
                    </CardTitle>
                    <button className="text-amber-500 hover:text-amber-600">
                        <ArrowRight className="h-5 w-5" />
                    </button>
                </CardHeader>
                <CardContent>
                    <div className="text-4xl font-bold">15.4 M€</div>
                </CardContent>
            </Card>
        </div>
    )
}
