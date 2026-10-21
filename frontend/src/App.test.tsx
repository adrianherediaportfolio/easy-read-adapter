import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import App from './App'
import { createAdaptation } from './api'

vi.mock('./api', () => ({
  createAdaptation: vi.fn(),
  deleteAdaptation: vi.fn(),
  getAdaptation: vi.fn(),
  listAdaptations: vi.fn(),
  uploadAdaptation: vi.fn(),
}))

const adaptation = {
  id: 'adaptation-1',
  created_at: '2026-01-15T10:00:00+00:00',
  level: 'lectura_facil' as const,
  source: null,
  original_text: 'El grupo participa en la actividad.',
  adapted_text: 'El grupo participa en la actividad.',
  sentences: [
    {
      text: 'El grupo participa en la actividad.',
      pictograms: [
        {
          keyword: 'grupo',
          source: 'arasaac' as const,
          id: '42',
          image_url: 'https://static.arasaac.org/pictograms/42/42_300.png',
          license: 'CC BY-NC-SA 4.0' as const,
          commercial_use: false,
        },
      ],
    },
  ],
  readability: {
    original: { score: 71.4, label: 'bastante fácil' },
    adapted: { score: 78.2, label: 'bastante fácil' },
  },
  engine: 'rules' as const,
  attributions: [
    'Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)',
  ],
  attribution:
    'Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)',
}

describe('Easy Read Adapter', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows the Spanish text-entry form and reading options after adaptation', async () => {
    vi.mocked(createAdaptation).mockResolvedValue(adaptation)
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Nueva adaptación' })).toBeInTheDocument()
    fireEvent.change(screen.getByLabelText('Pega el texto que quieres adaptar'), {
      target: { value: 'El grupo participa en la actividad.' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Adaptar texto' }))

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Texto listo para compartir' })).toBeInTheDocument()
    })
    expect(
      screen.getAllByText('El grupo participa en la actividad.'),
    ).toHaveLength(2)
    expect(screen.getAllByText('bastante fácil')).toHaveLength(2)
    expect(screen.getByText(/Propiedad: Gobierno de Aragón/)).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Opciones de lectura' }))
    expect(screen.getByRole('dialog', { name: 'Opciones de lectura' })).toBeInTheDocument()
    expect(screen.getByLabelText('Tipo de letra')).toHaveValue('atkinson')
  })

  it('explains when neither text nor a file has been selected', async () => {
    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: 'Adaptar texto' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Escribe un texto o selecciona un archivo.',
    )
    expect(createAdaptation).not.toHaveBeenCalled()
  })
})
