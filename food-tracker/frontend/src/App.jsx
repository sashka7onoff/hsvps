import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom'
import Wizard from './features/Wizard'
import History from './features/History'
import Stats from './features/Stats'
import { BowlFood, Clock, ChartBar } from '@phosphor-icons/react'

function Shell() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans flex flex-col">
      <header className="sticky top-0 z-10 bg-card border-b border-border px-4 py-3 flex items-center justify-between">
        <h1 className="font-serif text-xl font-semibold tracking-tight">Food Tracker</h1>
        <span className="text-sm text-muted-foreground">осознанное питание</span>
      </header>
      <main className="flex-1 pb-20">
        <Routes>
          <Route path="/" element={<Navigate to="/food-tracker/add" replace />} />
          <Route path="/food-tracker/add" element={<Wizard />} />
          <Route path="/food-tracker/history" element={<History />} />
          <Route path="/food-tracker/stats" element={<Stats />} />
        </Routes>
      </main>
      <nav className="fixed bottom-0 w-full bg-card border-t border-border flex justify-around py-2 safe-area-bottom shadow-lg">
        <NavLink to="/food-tracker/add" className={({isActive})=> `flex flex-col items-center gap-1 px-4 py-1 rounded-sm cursor-pointer transition-colors ${isActive?'text-primary':'text-muted-foreground'}`}><BowlFood size={24} weight="duotone" /><span className="text-xs">Добавить</span></NavLink>
        <NavLink to="/food-tracker/history" className={({isActive})=> `flex flex-col items-center gap-1 px-4 py-1 rounded-sm cursor-pointer transition-colors ${isActive?'text-primary':'text-muted-foreground'}`}><Clock size={24} /><span className="text-xs">История</span></NavLink>
        <NavLink to="/food-tracker/stats" className={({isActive})=> `flex flex-col items-center gap-1 px-4 py-1 rounded-sm cursor-pointer transition-colors ${isActive?'text-primary':'text-muted-foreground'}`}><ChartBar size={24} /><span className="text-xs">Статистика</span></NavLink>
      </nav>
    </div>
  )
}
export default function App(){ return <BrowserRouter><Shell/></BrowserRouter> }
