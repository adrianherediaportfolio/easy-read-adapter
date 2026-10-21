import type { Adaptation, AdaptationLevel, AdaptationSummary } from './types'

const API_BASE = '/api'

function apiHeaders(): HeadersInit {
  const apiKey = import.meta.env.VITE_API_KEY?.trim()
  return apiKey ? { 'X-API-Key': apiKey } : {}
}

async function readResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null
    throw new Error(payload?.detail ?? 'No se pudo completar la solicitud.')
  }
  return response.json() as Promise<T>
}

export async function createAdaptation(input: {
  text: string
  level: AdaptationLevel
  pictograms: boolean
}): Promise<Adaptation> {
  const response = await fetch(`${API_BASE}/adaptations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...apiHeaders() },
    body: JSON.stringify(input),
  })
  return readResponse<Adaptation>(response)
}

export async function uploadAdaptation(input: {
  file: File
  level: AdaptationLevel
  pictograms: boolean
}): Promise<Adaptation> {
  const body = new FormData()
  body.set('file', input.file)
  body.set('level', input.level)
  body.set('pictograms', String(input.pictograms))
  const response = await fetch(`${API_BASE}/adaptations/upload`, {
    method: 'POST',
    headers: apiHeaders(),
    body,
  })
  return readResponse<Adaptation>(response)
}

export async function listAdaptations(): Promise<AdaptationSummary[]> {
  const response = await fetch(`${API_BASE}/adaptations`, { headers: apiHeaders() })
  return readResponse<AdaptationSummary[]>(response)
}

export async function getAdaptation(id: string): Promise<Adaptation> {
  const response = await fetch(`${API_BASE}/adaptations/${id}`, {
    headers: apiHeaders(),
  })
  return readResponse<Adaptation>(response)
}

export async function deleteAdaptation(id: string): Promise<void> {
  const response = await fetch(`${API_BASE}/adaptations/${id}`, {
    method: 'DELETE',
    headers: apiHeaders(),
  })
  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null
    throw new Error(payload?.detail ?? 'No se pudo eliminar la adaptación.')
  }
}
