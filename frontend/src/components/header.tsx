import { LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Header() {
    return (
        <header className="flex h-14 items-center justify-between border-b bg-background px-6">
            <h1 className="text-xl font-bold">Tender Sniper Dashboard</h1>
            <Button variant="ghost" size="icon">
                <LogOut className="h-5 w-5" />
                <span className="sr-only">Déconnexion</span>
            </Button>
        </header>
    )
}
