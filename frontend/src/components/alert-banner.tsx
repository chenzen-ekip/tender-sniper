import { AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"

export function AlertBanner() {
    return (
        <div className="flex w-full flex-col gap-4 rounded-lg border border-orange-200 bg-orange-50 p-4 text-orange-950 dark:border-orange-900/50 dark:bg-orange-900/20 dark:text-orange-100 md:flex-row md:items-center md:justify-between">
            <div className="flex gap-4">
                <div className="mt-1">
                    <AlertTriangle className="h-5 w-5 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="space-y-1">
                    <h3 className="font-bold text-orange-900 dark:text-orange-100">
                        Attention : Centre Pompidou - Visite J-1
                    </h3>
                    <p className="text-sm text-orange-800 dark:text-orange-200">
                        Paris (75) | 6.6 M€ | Deadline: 13/12/2025 - 12h
                    </p>
                </div>
            </div>
            <div className="flex gap-2">
                <Button
                    variant="outline"
                    className="border-orange-200 bg-white text-orange-900 hover:bg-orange-50 hover:text-orange-950 dark:border-orange-800 dark:bg-transparent dark:text-orange-100 dark:hover:bg-orange-900/40"
                >
                    Synthèse IA
                </Button>
                <Button className="bg-gray-900 text-white hover:bg-gray-800 dark:bg-orange-500 dark:text-white dark:hover:bg-orange-600">
                    Dossier DCE
                </Button>
            </div>
        </div>
    )
}
