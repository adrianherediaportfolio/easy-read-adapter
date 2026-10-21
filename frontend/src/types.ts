export type AdaptationLevel = 'lectura_facil' | 'simplificado'

export interface Pictogram {
  keyword: string
  arasaac_id: number
  image_url: string
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
  attribution: string
}

export interface AdaptationSummary {
  id: string
  created_at: string
  level: AdaptationLevel
  preview: string
}
