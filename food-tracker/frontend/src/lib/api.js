function getCookie(name) {
  const m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return m ? decodeURIComponent(m[2]) : null
}

export async function apiFetch(url, opts = {}) {
  const headers = { 'Content-Type': 'application/json', ...(opts.headers || {}) }
  const csrftoken = getCookie('csrftoken')
  if (csrftoken) headers['X-CSRFToken'] = csrftoken
  const res = await fetch(url, { credentials: 'include', ...opts, headers })
  return res
}

export function toApiPayload(form) {
  // form.eaten_at is "YYYY-MM-DDTHH:mm" from input -> ISO
  let eaten_at = form.eaten_at
  try {
    eaten_at = new Date(form.eaten_at).toISOString()
  } catch {}
  return {
    eaten_at,
    meal_type: form.meal_type,
    is_planned: form.is_planned,
    reasons: form.reasons,
    hunger_level: form.hunger_level || null,
    portion: form.portion,
    junk_items: form.junk_items,
    positive_items: form.positive_items,
    rating: form.rating,
    note: form.note,
  }
}
