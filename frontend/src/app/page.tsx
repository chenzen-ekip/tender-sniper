import { AlertBanner } from "@/components/alert-banner"
import { DashboardStats } from "@/components/dashboard-stats"
import { Header } from "@/components/header"
import { MarketList } from "@/components/market-list"
import { Sidebar } from "@/components/sidebar"

export default function Home() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-8 pt-6">
          <div className="mx-auto max-w-7xl space-y-8">
            <h2 className="text-3xl font-bold tracking-tight">Tender Sniper Dashboard</h2>
            <DashboardStats />
            <AlertBanner />
            <MarketList />
          </div>
        </main>
      </div>
    </div>
  )
}
