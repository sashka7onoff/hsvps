import { useState, useEffect } from 'react'
import { apiFetch } from '../lib/api'
import { mealTypeLabel, portionLabel, ratingLabel, reasonLabel, junkLabel, positiveLabel } from '../lib/labels'
export default function History(){
  const [period,setPeriod]=useState('today')
  const [entries,setEntries]=useState([])
  const [source,setSource]=useState('sqlite')
  const fetchEntries = async (p)=>{
    try{
      const res = await apiFetch(`/api/food-tracker/entries/?period=${p}`)
      if(res.ok){ const data=await res.json(); // DRF paginated? handle both
        const list = Array.isArray(data) ? data : (data.results || [])
        setEntries(list); setSource('sqlite'); return
      }
      throw new Error('fallback')
    }catch{
      // fallback localStorage
      const data=JSON.parse(localStorage.getItem('ft_entries')||'[]')
      const now=new Date()
      let filtered=data
      if(p==='today') filtered=data.filter(e=> new Date(e.eaten_at).toDateString()===now.toDateString())
      else if(p==='week') filtered=data.filter(e=> (now - new Date(e.eaten_at)) < 7*864e5)
      else if(p==='month') filtered=data.filter(e=> (now - new Date(e.eaten_at)) < 30*864e5)
      setEntries(filtered); setSource('локально')
    }
  }
  useEffect(()=>{ fetchEntries(period) },[period])
  const del= async (id)=>{
    try{
      const res = await apiFetch(`/api/food-tracker/entries/${id}/`, {method:'DELETE'})
      if(res.ok){ setEntries(e=>e.filter(x=>x.id!==id)); return }
      if(res.status===403||res.status===401) throw new Error('local')
    }catch{}
    const d=JSON.parse(localStorage.getItem('ft_entries')||'[]').filter(e=>e.id!==id); localStorage.setItem('ft_entries',JSON.stringify(d)); setEntries(e=>e.filter(x=>x.id!==id))
  }
  return (
    <div className="max-w-md mx-auto p-4 space-y-4">
      <h2 className="font-serif text-xl">История</h2>
      <p className="text-xs text-muted-foreground">Источник: {source} • {source==='локально' && 'войди в /admin/ для SQLite'}</p>
      <div className="flex gap-2 p-1 bg-muted rounded-full w-fit">
        {['today','week','month'].map(p=>(
          <button key={p} onClick={()=>setPeriod(p)} className={`px-4 py-2 rounded-full text-sm font-medium cursor-pointer transition-colors ${period===p?'bg-primary text-white':'text-muted-foreground'}`}>{p==='today'?'Сегодня':p==='week'?'Неделя':'Месяц'}</button>
        ))}
      </div>
      {entries.length===0 ? (
        <div className="card text-center py-8"><p className="text-muted-foreground">Пока нет записей</p><p className="text-xs mt-1">Добавь первый приём во вкладке “Добавить”</p></div>
      ) : entries.map(e=>(
        <div key={e.id} className="card space-y-2">
          <div className="flex justify-between items-start">
            <div><div className="font-semibold">{mealTypeLabel[e.meal_type]||e.meal_type} • {portionLabel[e.portion]||e.portion}</div><div className="text-xs text-muted-foreground">{new Date(e.eaten_at).toLocaleString('ru-RU')} • {e.is_planned?'плановый':'внеплановый'}</div></div>
            <span className={`px-2 py-1 rounded-full text-xs font-semibold ${e.rating==='good'?'bg-accent text-white':e.rating==='bad'?'bg-destructive text-white':'bg-muted'}`}>{ratingLabel[e.rating]||e.rating}</span>
          </div>
          <div className="flex flex-wrap gap-1 text-xs">
            {(e.reasons||[]).map(r=><span key={r} className="px-2 py-1 bg-muted rounded-full">{reasonLabel[r]||r}</span>)}
            {(e.junk_items||[]).map(j=><span key={j} className="px-2 py-1 bg-destructive/10 text-destructive rounded-full">{junkLabel[j]||j}</span>)}
            {(e.positive_items||[]).map(p=><span key={p} className="px-2 py-1 bg-accent/10 text-accent rounded-full">{positiveLabel[p]||p}</span>)}
            {e.hunger_level && <span className="px-2 py-1 bg-primary/10 text-primary rounded-full">{e.hunger_level}</span>}
          </div>
          {e.note && <p className="text-sm bg-muted p-2 rounded-sm">{e.note}</p>}
          <button onClick={()=>del(e.id)} className="text-xs text-destructive cursor-pointer">Удалить</button>
        </div>
      ))}
    </div>
  )
}
