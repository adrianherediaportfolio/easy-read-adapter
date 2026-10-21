export type AdaptationLevel = 'lectura_facil' | 'simplificado'

export interface Pictogram {
  keyword: string
  source: 'own' | 'mulberry' | 'openmoji' | 'arasaac'
  id: string
  image_url: string
  license: 'proprietary' | 'CC BY-SA 4.0' | 'CC BY-NC-SA 4.0'
  commercial_use: boolean
}

export interface AdaptedSentence {
  text: string
  pictograms: Pictogram[]
}

export interface ReadabilityScore {
  score: number
  label: string
}

export interface Adaptation {
  id: string
  created_at: string
  level: AdaptationLevel
  source: string | null
  original_text: string
  adapted_text: string
  sentences: AdaptedSentence[]
  readability: {
    original: ReadabilityScore
    adapted: ReadabilityScore
  }
  engine: 'openai' | 'rules'
  attributions: string[]
  attribution: string
}

export interface AdaptationSummary {
  id: string
  created_at: string
  level: AdaptationLevel
  preview: string
}
