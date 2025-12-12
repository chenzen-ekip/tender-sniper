"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
    LayoutDashboard,
    Globe,
    FolderOpen,
    Bell,
    Settings,
    Send
} from "lucide-react"

import { cn } from "@/lib/utils"

const navigation = [
    { name: "Tableau de Bord", href: "/", icon: LayoutDashboard },
    { name: "Marchés", href: "/marches", icon: Globe },
    { name: "Dossiers", href: "/dossiers", icon: FolderOpen },
    { name: "Alertes", href: "/alertes", icon: Bell },
    { name: "Paramètres", href: "/parametres", icon: Settings },
]

export function Sidebar() {
    const pathname = usePathname()

    return (
        <div className="flex h-screen w-64 flex-col border-r bg-sidebar dark:bg-card">
            <div className="flex h-14 items-center gap-2 border-b px-6">
                <Send className="h-6 w-6 text-primary rotate-[-45deg]" />
                <span className="font-bold text-lg">Tender Sniper</span>
            </div>
            <div className="flex-1 overflow-y-auto py-4">
                <nav className="grid gap-1 px-2">
                    {navigation.map((item, index) => {
                        const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href)
                        return (
                            <Link
                                key={index}
                                href="#"
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:text-primary",
                                    isActive
                                        ? "bg-secondary text-primary"
                                        : "text-muted-foreground hover:bg-secondary/50"
                                )}
                            >
                                <item.icon className="h-4 w-4" />
                                {item.name}
                            </Link>
                        )
                    })}
                </nav>
            </div>
        </div>
    )
}
