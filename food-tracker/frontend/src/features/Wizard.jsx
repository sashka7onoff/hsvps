import { useState } from 'react'
import { apiFetch, toApiPayload } from '../lib/api'

const REASONS = [
  {id:'hunger', label:'Голоден'},
  {id:'boredom', label:'Скука'},
  {id:'stress', label:'Стресс'},
  {id:'fatigue', label:'Усталость'},
  {id:'social', label:'За компанию'},
  {id:'craving', label:'Захотелось'},
  {id:'habit', label:'Привычка'},
]
const MEAL_TYPES = [
  {id:'breakfast', label:'Завтрак'}, {id:'lunch', label:'Обед'}, {id:'dinner', label:'Ужин'},
  {id:'snack', label:'Перекус'}, {id:'impulsive', label:'Импульсивный'},
]
const JUNK = [
  {id:'sweet',label:'Сладкое'},{id:'bakery',label:'Выпечка'},{id:'fastfood',label:'Фастфуд'},{id:'snacks',label:'Чипсы'},{id:'soda_alco',label:'Газировка/алк.'},
]
const POSITIVE = [
  {id:'veggies',label:'Овощи/зелень'},{id:'protein',label:'Белок'},{id:'fiber',label:'Клетчатка'},{id:'water',label:'Вода'},{id:'no_overeat',label:'Без переедания'},
]

export default function Wizard(){
  const [step, setStep] = useState(0)
  const [form, setForm] = useState({
    reasons:[], hunger_level:null, meal_type:'', is_planned:true, portion:'moderate',
    junk_items:[], positive_items:[], rating:'normal', note:'', eaten_at: new Date().toISOString().slice(0,16)
  })
  const total=5
  const toggle = (key, id, max=2) => setForm(f=>{
    const arr=f[key].includes(id)? f[key].filter(x=>x!==id) : [...f[key], id]
    if(arr.length>max) return f
    return {...f,[key]:arr}
  })

  const next = ()=> setStep(s=> Math.min(s+1, total-1))
  const back = ()=> setStep(s=> Math.max(s-1,0))
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')
  const save = async ()=>{
    if (!form.meal_type) { setMsg('Выбери тип приёма (завтрак/обед/и т.д.)'); return }
    setSaving(true); setMsg('')
    const payload = toApiPayload(form)
    try {
      const res = await apiFetch('/api/food-tracker/entries/', { method:'POST', body: JSON.stringify(payload) })
      if (res.ok) {
        setMsg('Сохранено ✓')
        setStep(0)
        setForm({ reasons:[], hunger_level:null, meal_type:'', is_planned:true, portion:'moderate', junk_items:[], positive_items:[], rating:'normal', note:'', eaten_at: new Date().toISOString().slice(0,16) })
        return
      }
      if (res.status===403 || res.status===401) {
        setMsg('Войди в аккаунт, чтобы сохранить')
        setTimeout(()=>{ window.location.href='/accounts/login/?next='+encodeURIComponent('/food-tracker/add') }, 800)
        return
      }
      const err = await res.text()
      setMsg('Ошибка: '+err.slice(0,120))
    } catch(e){ setMsg('Ошибка сети: '+e.message) }
    finally{ setSaving(false) }
  }

  return (
    <div className="max-w-md mx-auto p-4 space-y-4">
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>Шаг {step+1} из {total}</span>
        <span className="text-xs">{Math.round((step+1)/total*100)}%</span>
      </div>
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div className="h-full bg-primary transition-all" style={{width:`${(step+1)/total*100}%`}} />
      </div>

      {step===0 && (
        <div className="space-y-3">
          <h2 className="font-serif text-xl">Почему ты ешь?</h2>
          <p className="text-sm text-muted-foreground">Выбери до 2 причин</p>
          <div className="grid grid-cols-2 gap-2">
            {REASONS.map(r=> (
              <button key={r.id} onClick={()=>toggle('reasons',r.id)} className={`chip ${form.reasons.includes(r.id)?'chip-active':''}`}>{r.label}</button>
            ))}
          </div>
          {form.reasons.includes('hunger') && (
            <div className="flex gap-2 pt-2">
              {[{id:'slightly',l:'Слегка'},{id:'hungry',l:'Голоден'},{id:'very',l:'Очень'}].map(o=>(
                <button key={o.id} onClick={()=>setForm({...form, hunger_level:o.id})} className={`flex-1 py-3 rounded-sm border text-sm cursor-pointer ${form.hunger_level===o.id?'bg-primary text-white border-primary':'bg-card border-border'}`}>{o.l}</button>
              ))}
            </div>
          )}
          <input type="datetime-local" value={form.eaten_at} onChange={e=>setForm({...form,eaten_at:e.target.value})} className="input w-full mt-2" />
        </div>
      )}
      {step===1 && (
        <div className="space-y-3">
          <h2 className="font-serif text-xl">Что это был за приём?</h2>
          <div className="grid grid-cols-2 gap-2">
            {MEAL_TYPES.map(m=>(
              <button key={m.id} onClick={()=>setForm({...form, meal_type:m.id})} className={`p-4 rounded-md border text-center cursor-pointer transition-all ${form.meal_type===m.id?'bg-primary text-white border-primary shadow-md':'bg-card border-border hover:shadow-sm'}`}>{m.label}</button>
            ))}
          </div>
          <label className="flex items-center gap-3 p-3 bg-card rounded-md border border-border cursor-pointer">
            <input type="checkbox" checked={form.is_planned} onChange={e=>setForm({...form,is_planned:e.target.checked})} className="w-5 h-5 accent-primary" />
            <span className="text-sm font-medium">Плановый приём</span>
            <span className="ml-auto text-xs text-muted-foreground">{form.is_planned?'завтрак/обед/ужин':'внеплановый'}</span>
          </label>
        </div>
      )}
      {step===2 && (
        <div className="space-y-3">
          <h2 className="font-serif text-xl">Размер порции</h2>
          <div className="grid grid-cols-1 gap-2">
            {[{id:'small',l:'Маленькая',d:'легкий перекус'},{id:'moderate',l:'Умеренная',d:'обычная порция'},{id:'large',l:'Большая',d:'плотно поел'}].map(p=>(
              <button key={p.id} onClick={()=>setForm({...form,portion:p.id})} className={`p-4 rounded-md border text-left cursor-pointer ${form.portion===p.id?'bg-primary text-white border-primary':'bg-card border-border'}`}>
                <div className="font-semibold">{p.l}</div><div className="text-sm opacity-80">{p.d}</div>
              </button>
            ))}
          </div>
        </div>
      )}
      {step===3 && (
        <div className="space-y-4">
          <h2 className="font-serif text-xl">Детали</h2>
          <div>
            <div className="text-sm font-medium mb-2">Мусорные калории</div>
            <div className="flex flex-wrap gap-2">
              {JUNK.map(j=>(
                <button key={j.id} onClick={()=>toggle('junk_items',j.id,5)} className={`chip !min-h-0 py-2 text-sm ${form.junk_items.includes(j.id)?'bg-destructive text-white border-destructive':'bg-card'}`}>{j.label}</button>
              ))}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium mb-2">Позитивные моменты</div>
            <div className="flex flex-wrap gap-2">
              {POSITIVE.map(p=>(
                <button key={p.id} onClick={()=>toggle('positive_items',p.id,5)} className={`chip !min-h-0 py-2 text-sm ${form.positive_items.includes(p.id)?'bg-accent text-white border-accent':'bg-card'}`}>{p.label}</button>
              ))}
            </div>
          </div>
        </div>
      )}
      {step===4 && (
        <div className="space-y-3">
          <h2 className="font-serif text-xl">Оценка</h2>
          <div className="grid grid-cols-3 gap-2">
            {[{id:'good',l:'Хорошо',c:'bg-accent'},{id:'normal',l:'Норм',c:'bg-muted'},{id:'bad',l:'Плохо',c:'bg-destructive'}].map(r=>(
              <button key={r.id} onClick={()=>setForm({...form,rating:r.id})} className={`p-4 rounded-md border text-center font-semibold cursor-pointer ${form.rating===r.id? r.c+' text-white border-transparent':'bg-card border-border'}`}>{r.l}</button>
            ))}
          </div>
          <textarea placeholder="Заметка (необязательно)" value={form.note} onChange={e=>setForm({...form,note:e.target.value})} className="input w-full h-24 resize-none" maxLength={500} />
        </div>
      )}

      {msg && <p className="text-sm text-center p-2 bg-muted rounded-sm">{msg}</p>}
      <div className="flex gap-2 pt-2">
        {step>0 && <button onClick={back} className="btn-secondary flex-1">Назад</button>}
        {step<total-1 ? <button onClick={next} className="btn-primary flex-1 bg-primary">Далее</button> : <button onClick={save} disabled={saving} className="btn-primary flex-1 !bg-accent disabled:opacity-50">{saving?'Сохранение...':'Добавить'}</button>}
      </div>
      <p className="text-xs text-center text-muted-foreground">Требуется вход в аккаунт. Время можно править.</p>
    </div>
  )
}
