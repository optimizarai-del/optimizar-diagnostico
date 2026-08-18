import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export async function crearDiagnostico(payload) {
  const { data } = await api.post('/diagnostico', payload)
  return data
}

export async function obtenerDiagnostico(token) {
  const { data } = await api.get(`/diagnostico/${token}`)
  return data
}

export async function registrarClickCta(token) {
  try {
    await api.post(`/diagnostico/${token}/cta`)
  } catch {
    /* el tracking nunca puede frenar al usuario */
  }
}

export async function registrarEvento(tipo, variante, datos = {}, token = null) {
  try {
    await api.post('/eventos', { tipo, variante, datos, token })
  } catch {
    /* idem */
  }
}

/** Lee los utm_* de la URL para poder cruzar los leads con Meta Ads. */
export function leerUtm() {
  const params = new URLSearchParams(window.location.search)
  const utm = {}
  for (const clave of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']) {
    const valor = params.get(clave)
    if (valor) utm[clave] = valor
  }
  return utm
}

/**
 * Resuelve la variante del test A/B.
 * `?v=a` o `?v=b` desde el anuncio; si no viene, se sortea 50/50 y se guarda
 * para que un refresh no cambie de rama a mitad del formulario.
 */
export function resolverVariante() {
  const params = new URLSearchParams(window.location.search)
  const pedida = params.get('v')
  if (pedida === 'a' || pedida === 'b') {
    sessionStorage.setItem('variante', pedida)
    return pedida
  }
  const guardada = sessionStorage.getItem('variante')
  if (guardada === 'a' || guardada === 'b') return guardada
  const sorteada = Math.random() < 0.5 ? 'a' : 'b'
  sessionStorage.setItem('variante', sorteada)
  return sorteada
}
