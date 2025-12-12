import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const markets = [
    {
        name: "Campus Audencia (St Ouen)",
        details: "250k€/an, 15/01",
    },
    {
        name: "Mairie de Lyon (Nettoyage)",
        details: "400k€, 20/01",
    },
    {
        name: "Hôpital Nord Marseille",
        details: "1.2 M€, 05/02",
    },
]

export function MarketList() {
    return (
        <div className="grid gap-4">
            {markets.map((market, index) => (
                <Card key={index}>
                    <CardContent className="flex items-center justify-between p-4">
                        <div className="font-medium">
                            {market.name} - <span className="text-muted-foreground">{market.details}</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <Badge variant="secondary" className="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-gray-700">
                                Avis IA
                            </Badge>
                            <Button variant="outline" size="sm">
                                Voir
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}
