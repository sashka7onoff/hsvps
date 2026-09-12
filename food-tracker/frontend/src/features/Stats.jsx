import { useEffect, useState } from 'react'
import { Doughnut, Line } from 'react-chartjs-2'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { apiFetch } from '../lib/api'
import { reasonLabel } from '../lib/labels'
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement)

export default function Stats(){
  const [entries,setEntries]=useState([])
  const [source,setSource]=useState('sqlite')
  useEffect(()=>{
    (async()=>{
      try{
        const res=await apiFetch('/api/food-tracker/entries/?period=month')
        if(res.ok){ const d=await res.json(); const list=Array.isArray(d)?d:(d.results||[]); setEntries(list); setSource('sqlite'); return}
        throw new Error('fallback')
      }catch{ setEntries(JSON.parse(localStorage.getItem('ft_entries')||'[]')); setSource('локально') }
    })()
  },[])
  const planned=entries.filter(e=>e.is_planned).length
  const impulsive=entries.filter(e=>!e.is_planned).length
  const good=entries.filter(e=>e.rating==='good').length
  const bad=entries.filter(e=>e.rating==='bad').length

  // топ триггеры
  const triggers = Object.entries(entries.flatMap(e=>e.reasons||[]).reduce((acc,r)=>{acc[r]=(acc[r]||0)+1;return acc},{})).sort((a,b)=>b[1]-a[1]).slice(0,3)

  return (
    <div className="max-w-md mx-auto p-4 space-y-4">
      <h2 className="font-serif text-xl">Статистика</h2>
      <p className="text-xs text-muted-foreground">Источник: {source}</p>
      <div className="grid grid-cols-2 gap-3">
        <div className="card !py-3"><div className="text-2xl font-serif font-bold">{entries.length}</div><div className="text-xs text-muted-foreground">всего приёмов</div></div>
        <div className="card !py-3"><div className="text-2xl font-serif font-bold text-destructive">{bad}</div><div className="text-xs text-muted-foreground">оценок “плохо”</div></div>
        <div className="card !py-3"><div className="text-2xl font-serif font-bold text-accent">{good}</div><div className="text-xs text-muted-foreground">оценок “хорошо”</div></div>
        <div className="card !py-3"><div className="text-2xl font-serif font-bold">{impulsive}</div><div className="text-xs text-muted-foreground">внеплановых</div></div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-3">Плановые vs внеплановые</h3>
        <div className="h-48 flex justify-center">
          <Doughnut data={{labels:['Плановые','Внеплановые'], datasets:[{data:[planned||1,impulsive||0], backgroundColor:['#7C3AED','#DC2626'], borderWidth:0}]}} options={{maintainAspectRatio:false, plugins:{legend:{position:'bottom'}}}} />
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-3">Динамика по дням (7 дней)</h3>
        <Line data={{
          labels:[...Array(7)].map((_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);return d.toLocaleDateString('ru-RU',{day:'numeric',month:'short'})}),
          datasets:[{label:'Приёмы', data:[...Array(7)].map((_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);return entries.filter(e=> new Date(e.eaten_at).toDateString()===d.toDateString()).length}), borderColor:'#7C3AED', backgroundColor:'rgba(124,58,237,0.15)', tension:0.4, fill:true}]
        }} options={{responsive:true, plugins:{legend:{display:false}}}} />
      </div>

      <div className="card">
        <h3 className="font-semibold mb-2">Топ-триггеры</h3>
        {triggers.length? triggers.map(([k,v])=><div key={k} className="flex items-center gap-2 py-1"><span className="text-sm flex-1">{reasonLabel[k]||k}</span><div className="flex-1 h-2 bg-muted rounded-full overflow-hidden"><div className="h-full bg-primary" style={{width:`${v/entries.length*100}%`}}/></div><span className="text-xs">{v}</span></div>) : <p className="text-sm text-muted-foreground">Недостаточно данных</p>}
      </div>

      <div className="card bg-accent/10 border-accent/20">
        <div className="font-semibold">Стрик</div>
        <div className="text-sm text-muted-foreground">{bad===0 && entries.length>0 ? 'Дней без «плохо» — держишься!' : 'Собери 3 дня без внеплановых — начни сегодня'}</div>
      </div>
      <p className="text-xs text-center text-muted-foreground">Графики строятся из SQLite (если залогинен) или локально. Фильтры — сегодня/неделя/месяц.</p>
    </div>
  )
}
