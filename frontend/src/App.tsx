import {
  BookOpenCheck,
  Check,
  Clock3,
  FileText,
  History,
  LoaderCircle,
  Printer,
  Settings2,
  ShieldCheck,
  Sparkles,
  Trash2,
  Upload,
  Volume2,
} from 'lucide-react'
import { useEffect, useState, type FormEvent } from 'react'

import {
  createAdaptation,
  deleteAdaptation,
  getAdaptation,
  listAdaptations,
  uploadAdaptation,
} from './api'
import type { Adaptation, AdaptationLevel, AdaptationSummary } from './types'

type Page = 'new' | 'history'
type ReadingFont = 'system' | 'atkinson'

const ATTRIBUTION =
  'Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)'

function ReadabilityBadge({
  title,
  result,
  kind,
}: {
  title: string
  result: { score: number; label: string }
  kind: 'before' | 'after'
}) {
  return (
    <div className={`score-card score-card-${kind}`}>
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-bold text-slate-600">{title}</p>
        <span className="text-xs font-semibold text-slate-500">INFLESZ</span>
      </div>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-3xl font-bold tracking-tight text-ink">{result.score}</span>
        <span className="text-xs text-slate-500">/ 100</span>
      </div>
      <span className="mt-2 inline-flex rounded-full bg-white/80 px-3 py-1 text-sm font-bold text-moss">
        {result.label}
      </span>
    </div>
  )
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('es-ES', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export default function App() {
  const [page, setPage] = useState<Page>('new')
  const [text, setText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [level, setLevel] = useState<AdaptationLevel>('lectura_facil')
  const [withPictograms, setWithPictograms] = useState(true)
  const [result, setResult] = useState<Adaptation | null>(null)
  const [history, setHistory] = useState<AdaptationSummary[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [font, setFont] = useState<ReadingFont>('atkinson')
  const [fontSize, setFontSize] = useState(22)
  const [lineSpacing, setLineSpacing] = useState(1.7)
  const [letterSpacing, setLetterSpacing] = useState(0.2)

  useEffect(() => {
    if (page !== 'history') return
    let active = true
    listAdaptations()
      .then((items) => {
        if (active) setHistory(items)
      })
      .catch((cause: unknown) => {
        if (active) {
          setError(cause instanceof Error ? cause.message : 'No se pudo cargar el historial.')
        }
      })
    return () => {
      active = false
    }
  }, [page])

  async function submitAdaptation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    if (!file && !text.trim()) {
      setError('Escribe un texto o selecciona un archivo.')
      return
    }

    setLoading(true)
    try {
      const adaptation = file
        ? await uploadAdaptation({ file, level, pictograms: withPictograms })
        : await createAdaptation({ text, level, pictograms: withPictograms })
      setResult(adaptation)
      setPage('new')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo adaptar el texto.')
    } finally {
      setLoading(false)
    }
  }

  async function openHistoryItem(id: string) {
    setError('')
    try {
      setResult(await getAdaptation(id))
      setPage('new')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo abrir la adaptación.')
    }
  }

  async function removeHistoryItem(id: string) {
    setError('')
    try {
      await deleteAdaptation(id)
      setHistory((items) => items.filter((item) => item.id !== id))
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo eliminar la adaptación.')
    }
  }

  function startNewAdaptation() {
    setResult(null)
    setText('')
    setFile(null)
    setError('')
    setPage('new')
  }

  return (
    <div className="min-h-screen bg-cream text-ink">
      <header className="border-b border-[#dfe4d9] bg-[#fbfaf6]">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-5 px-5 py-4 md:px-10">
          <a href="/" className="flex items-center gap-3" aria-label="Lectura Clara, inicio">
            <span className="grid h-11 w-11 place-items-center rounded-2xl bg-ink text-white">
              <BookOpenCheck size={23} aria-hidden="true" />
            </span>
            <span>
              <span className="block text-lg font-bold leading-tight">Lectura Clara</span>
              <span className="block text-xs font-semibold tracking-wide text-slate-500">
                EASY READ ADAPTER
              </span>
            </span>
          </a>
          <nav className="flex items-center gap-2" aria-label="Secciones principales">
            <button
              className={`nav-button ${page === 'new' ? 'nav-button-active' : ''}`}
              onClick={startNewAdaptation}
              type="button"
            >
              <Sparkles size={16} aria-hidden="true" />
              Nueva adaptación
            </button>
            <button
              className={`nav-button ${page === 'history' ? 'nav-button-active' : ''}`}
              onClick={() => {
                setError('')
                setPage('history')
              }}
              type="button"
            >
              <History size={16} aria-hidden="true" />
              Historial
            </button>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-[1440px] px-5 pb-14 pt-8 md:px-10 md:pt-12">
        <div className="print-hidden mb-8 flex flex-col justify-between gap-5 lg:flex-row lg:items-end">
          <div className="max-w-3xl">
            <p className="mb-3 inline-flex items-center gap-2 text-sm font-bold uppercase tracking-[0.13em] text-moss">
              <span className="h-2 w-2 rounded-full bg-coral" />
              Lectura inclusiva, paso a paso
            </p>
            <h1 className="max-w-3xl text-4xl font-bold leading-[1.08] tracking-tight text-ink md:text-5xl">
              Las ideas claras abren puertas.
            </h1>
            <p className="mt-4 max-w-2xl text-lg leading-7 text-slate-600">
              Adapta textos para que cada estudiante pueda leer, comprender y participar.
            </p>
          </div>
          <div className="flex w-fit items-center gap-3 rounded-2xl border border-[#dce5da] bg-white px-4 py-3 shadow-sm">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-[#eaf2e9] text-moss">
              <ShieldCheck size={19} aria-hidden="true" />
            </span>
            <span>
              <span className="block text-sm font-bold">Privado y sencillo</span>
              <span className="block text-xs text-slate-500">Sin cuenta de estudiante</span>
            </span>
          </div>
        </div>

        {error && (
          <div
            className="print-hidden mb-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-800"
            role="alert"
          >
            <span className="mt-0.5">!</span>
            <span>{error}</span>
          </div>
        )}

        {page === 'new' ? (
          <div className="grid gap-6 xl:grid-cols-[minmax(350px,0.83fr)_minmax(0,1.17fr)]">
            <section className="panel print-hidden h-fit">
              <div className="mb-5 flex items-start justify-between gap-4">
                <div>
                  <p className="eyebrow">PREPARA EL TEXTO</p>
                  <h2 className="mt-1 text-2xl font-bold">Nueva adaptación</h2>
                </div>
                <span className="grid h-11 w-11 place-items-center rounded-2xl bg-[#edf2e9] text-moss">
                  <FileText size={20} aria-hidden="true" />
                </span>
              </div>

              <form onSubmit={submitAdaptation} className="space-y-5">
                <label htmlFor="source-text" className="label">
                  Pega el texto que quieres adaptar
                </label>
                <textarea
                  id="source-text"
                  className="text-area"
                  maxLength={20_000}
                  onChange={(event) => {
                    setText(event.target.value)
                    if (file) setFile(null)
                  }}
                  placeholder="Pega aquí una explicación, una actividad o un texto escolar..."
                  rows={9}
                  value={text}
                />
                <div className="-mt-4 flex justify-between text-xs text-slate-500">
                  <span>Máximo 20.000 caracteres</span>
                  <span>{text.length.toLocaleString('es-ES')} / 20.000</span>
                </div>

                <div className="file-drop">
                  <label htmlFor="source-file" className="flex cursor-pointer items-center gap-3">
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white text-moss">
                      <Upload size={19} aria-hidden="true" />
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block font-bold">
                        {file ? file.name : 'O sube un archivo PDF o TXT'}
                      </span>
                      <span className="block text-xs text-slate-500">Hasta 5 MB</span>
                    </span>
                    {file && <Check size={18} className="text-moss" aria-label="Archivo seleccionado" />}
                  </label>
                  <input
                    id="source-file"
                    className="sr-only"
                    accept=".pdf,.txt,application/pdf,text/plain"
                    onChange={(event) => {
                      const selected = event.target.files?.[0] ?? null
                      setFile(selected)
                      if (selected) setText('')
                    }}
                    type="file"
                  />
                </div>

                <div>
                  <label htmlFor="adaptation-level" className="label">
                    Nivel de adaptación
                  </label>
                  <select
                    id="adaptation-level"
                    className="select-field mt-2"
                    onChange={(event) => setLevel(event.target.value as AdaptationLevel)}
                    value={level}
                  >
                    <option value="lectura_facil">Lectura Fácil</option>
                    <option value="simplificado">Texto simplificado</option>
                  </select>
                </div>

                <label className="toggle-row">
                  <span>
                    <span className="block font-bold">Añadir pictogramas</span>
                    <span className="block text-xs text-slate-500">Busca apoyos visuales en ARASAAC</span>
                  </span>
                  <input
                    checked={withPictograms}
                    className="toggle-input"
                    onChange={(event) => setWithPictograms(event.target.checked)}
                    type="checkbox"
                  />
                </label>

                <button className="primary-button w-full" disabled={loading} type="submit">
                  {loading ? (
                    <>
                      <LoaderCircle size={18} className="animate-spin" aria-hidden="true" />
                      Preparando adaptación...
                    </>
                  ) : (
                    <>
                      <Sparkles size={18} aria-hidden="true" />
                      Adaptar texto
                    </>
                  )}
                </button>
                <p className="text-center text-xs leading-5 text-slate-500">
                  El modo local funciona sin conexión a OpenAI. Los pictogramas necesitan internet.
                </p>
              </form>
            </section>

            <section className="min-w-0">
              {result ? (
                <div className="panel result-panel">
                  <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
                    <div>
                      <p className="eyebrow">RESULTADO</p>
                      <h2 className="mt-1 text-2xl font-bold">Texto listo para compartir</h2>
                      <p className="mt-1 text-sm text-slate-500">
                        {result.level === 'lectura_facil' ? 'Lectura Fácil' : 'Texto simplificado'}
                        {' · '}
                        {result.engine === 'openai' ? 'OpenAI' : 'Modo local'}
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <button className="secondary-button" onClick={() => window.print()} type="button">
                        <Printer size={16} aria-hidden="true" />
                        Guardar en PDF
                      </button>
                      <button className="icon-button" onClick={startNewAdaptation} type="button">
                        <FileText size={16} aria-hidden="true" />
                        Nuevo
                      </button>
                    </div>
                  </div>

                  <div className="mt-6 grid gap-3 sm:grid-cols-2">
                    <ReadabilityBadge
                      title="Texto original"
                      result={result.readability.original}
                      kind="before"
                    />
                    <ReadabilityBadge
                      title="Texto adaptado"
                      result={result.readability.adapted}
                      kind="after"
                    />
                  </div>

                  <details className="reading-settings mt-5">
                    <summary>
                      <Settings2 size={17} aria-hidden="true" />
                      Opciones de lectura
                    </summary>
                    <div className="grid gap-4 pt-4 sm:grid-cols-2">
                      <label className="setting-control">
                        <span>Tipo de letra</span>
                        <select
                          className="select-field"
                          onChange={(event) => setFont(event.target.value as ReadingFont)}
                          value={font}
                        >
                          <option value="atkinson">Atkinson Hyperlegible</option>
                          <option value="system">Sistema</option>
                        </select>
                      </label>
                      <label className="setting-control">
                        <span>Tamaño: {fontSize} px</span>
                        <input
                          max="32"
                          min="18"
                          onChange={(event) => setFontSize(Number(event.target.value))}
                          type="range"
                          value={fontSize}
                        />
                      </label>
                      <label className="setting-control">
                        <span>Espacio entre líneas: {lineSpacing.toFixed(1)}</span>
                        <input
                          max="2.1"
                          min="1.3"
                          onChange={(event) => setLineSpacing(Number(event.target.value))}
                          step="0.1"
                          type="range"
                          value={lineSpacing}
                        />
                      </label>
                      <label className="setting-control">
                        <span>Espacio entre letras: {letterSpacing.toFixed(1)} px</span>
                        <input
                          max="1.2"
                          min="0"
                          onChange={(event) => setLetterSpacing(Number(event.target.value))}
                          step="0.1"
                          type="range"
                          value={letterSpacing}
                        />
                      </label>
                    </div>
                  </details>

                  <div className="mt-6 space-y-3" id="adaptation-result">
                    {result.sentences.map((sentence, index) => (
                      <article className="sentence-card" key={`${result.id}-${index}`}>
                        {sentence.pictograms.length > 0 && (
                          <div className="mb-3 flex flex-wrap gap-3" aria-label="Pictogramas de la frase">
                            {sentence.pictograms.map((pictogram) => (
                              <figure
                                className="m-0 grid justify-items-center gap-1"
                                key={`${pictogram.arasaac_id}-${pictogram.keyword}`}
                              >
                                <img
                                  alt={`Pictograma: ${pictogram.keyword}`}
                                  className="h-16 w-16 rounded-xl object-contain"
                                  loading="lazy"
                                  src={pictogram.image_url}
                                />
                                <figcaption className="text-xs font-semibold text-slate-500">
                                  {pictogram.keyword}
                                </figcaption>
                              </figure>
                            ))}
                          </div>
                        )}
                        <p
                          className={font === 'atkinson' ? 'reading-text reading-atkinson' : 'reading-text'}
                          style={{
                            fontSize: `${fontSize}px`,
                            letterSpacing: `${letterSpacing}px`,
                            lineHeight: lineSpacing,
                          }}
                        >
                          <span className="mr-3 inline-block text-sm font-bold text-coral">
                            {String(index + 1).padStart(2, '0')}
                          </span>
                          {sentence.text}
                        </p>
                      </article>
                    ))}
                  </div>

                  {withPictograms && (
                    <p className="attribution mt-5">
                      {result.attribution || ATTRIBUTION}
                    </p>
                  )}
                  <div className="mt-5 flex items-center gap-2 rounded-xl bg-[#f1f4ef] px-4 py-3 text-xs text-slate-600">
                    <Volume2 size={16} className="shrink-0 text-moss" aria-hidden="true" />
                    <span>
                      Puedes cambiar el tamaño, el tipo de letra y los espacios antes de imprimir.
                    </span>
                  </div>
                </div>
              ) : (
                <div className="empty-result">
                  <div className="empty-art" aria-hidden="true">
                    <span className="art-card art-card-back" />
                    <span className="art-card art-card-front">
                      <BookOpenCheck size={38} />
                    </span>
                    <span className="art-spark art-spark-one">✳</span>
                    <span className="art-spark art-spark-two">✦</span>
                  </div>
                  <p className="eyebrow">TU ESPACIO DE TRABAJO</p>
                  <h2 className="mt-2 text-2xl font-bold">Un texto más claro empieza aquí.</h2>
                  <p className="mx-auto mt-3 max-w-md leading-7 text-slate-600">
                    Pega un texto o carga un archivo. Verás frases breves, apoyos visuales y una
                    medida de legibilidad para comparar.
                  </p>
                  <div className="mt-8 grid gap-3 sm:grid-cols-3">
                    <div className="step-card">
                      <span>01</span>
                      <strong>Añade</strong>
                      <small>un texto o archivo</small>
                    </div>
                    <div className="step-card">
                      <span>02</span>
                      <strong>Adapta</strong>
                      <small>con un clic</small>
                    </div>
                    <div className="step-card">
                      <span>03</span>
                      <strong>Comparte</strong>
                      <small>o guarda en PDF</small>
                    </div>
                  </div>
                  <div className="mt-7 flex items-center justify-center gap-2 text-xs font-semibold text-moss">
                    <Clock3 size={15} aria-hidden="true" />
                    El historial se guarda en tu dispositivo de trabajo.
                  </div>
                </div>
              )}
            </section>
          </div>
        ) : (
          <section className="panel">
            <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
              <div>
                <p className="eyebrow">TUS ADAPTACIONES</p>
                <h2 className="mt-1 text-2xl font-bold">Historial</h2>
                <p className="mt-2 text-sm text-slate-500">
                  Abre un resultado o elimina una adaptación que ya no necesites.
                </p>
              </div>
              <button className="primary-button" onClick={startNewAdaptation} type="button">
                <Sparkles size={17} aria-hidden="true" />
                Crear adaptación
              </button>
            </div>
            {history.length === 0 ? (
              <div className="my-12 grid justify-items-center text-center">
                <span className="grid h-14 w-14 place-items-center rounded-2xl bg-[#edf2e9] text-moss">
                  <History size={24} aria-hidden="true" />
                </span>
                <h3 className="mt-4 text-lg font-bold">Todavía no hay adaptaciones</h3>
                <p className="mt-1 text-sm text-slate-500">Tus resultados aparecerán aquí.</p>
              </div>
            ) : (
              <div className="mt-6 grid gap-3">
                {history.map((item) => (
                  <article className="history-row" key={item.id}>
                    <button
                      className="min-w-0 flex-1 text-left"
                      onClick={() => void openHistoryItem(item.id)}
                      type="button"
                    >
                      <span className="mb-1 flex flex-wrap items-center gap-2">
                        <span className="font-bold">
                          {item.level === 'lectura_facil' ? 'Lectura Fácil' : 'Texto simplificado'}
                        </span>
                        <span className="text-xs text-slate-400">·</span>
                        <span className="text-xs text-slate-500">{formatDate(item.created_at)}</span>
                      </span>
                      <span className="block truncate text-sm text-slate-600">{item.preview}</span>
                    </button>
                    <button
                      aria-label="Eliminar adaptación"
                      className="delete-button"
                      onClick={() => void removeHistoryItem(item.id)}
                      type="button"
                    >
                      <Trash2 size={17} aria-hidden="true" />
                    </button>
                  </article>
                ))}
              </div>
            )}
          </section>
        )}

        <footer className="mt-9 flex flex-col justify-between gap-2 border-t border-[#dfe4d9] pt-5 text-xs text-slate-500 sm:flex-row">
          <span>Una herramienta de apoyo para la práctica pedagógica.</span>
          <span>Los pictogramas de ARASAAC son para uso no comercial.</span>
        </footer>
      </main>
    </div>
  )
}
