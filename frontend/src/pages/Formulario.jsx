import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import Logo from '../components/Logo'
import { crearDiagnostico, leerUtm, registrarEvento, resolverVariante } from '../api'
import { preguntasVisibles } from '../data/questions'

// El progreso se guarda en sessionStorage. Son 13 o 14 pantallas y el tráfico
// viene de anuncios, o sea casi todo mobile: un F5 sin querer, rotar el
// teléfono o perder señal no puede costar el formulario entero.
const CLAVE = 'optimizar_diagnostico_form'

function leerGuardado(variante) {
  try {
    const crudo = sessionStorage.getItem(CLAVE)
    if (!crudo) return null
    const datos = JSON.parse(crudo)
    // Un borrador de la otra rama no sirve: si alguien entra por los dos
    // anuncios en la misma pestaña, arrastraría respuestas de una variante a
    // la otra y contaminaría el test.
    return datos?.variante === variante ? datos : null
  } catch {
    return null // modo privado o storage bloqueado: se sigue sin persistencia
  }
}

export default function Formulario() {
  const navigate = useNavigate()
  const variante = resolverVariante()
  const utm = useMemo(leerUtm, [])
  const guardado = useMemo(() => leerGuardado(variante), [variante])

  const [respuestas, setRespuestas] = useState(() => guardado?.respuestas ?? {})
  const [paso, setPaso] = useState(() => guardado?.paso ?? 0)
  const [nombre, setNombre] = useState(() => guardado?.nombre ?? '')
  const [contacto, setContacto] = useState(() => guardado?.contacto ?? '')
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState(null)
  const [resultado, setResultado] = useState(null) // solo variante B
  const [finalizado, setFinalizado] = useState(false)

  const visibles = useMemo(() => preguntasVisibles(respuestas), [respuestas])
  const enCaptura = paso >= visibles.length
  const pregunta = enCaptura ? null : visibles[paso]
  const progreso = Math.round((paso / (visibles.length + 1)) * 100)

  useEffect(() => {
    // Solo en el arranque real. Si venimos de un refresh no es un form_start
    // nuevo: contarlo otra vez inflaría el embudo del test A/B.
    if (!guardado) registrarEvento('form_start', variante, utm)
  }, [guardado, variante, utm])

  useEffect(() => {
    // Una vez enviado no se guarda más. Si no, un "atrás" mueve el paso, este
    // efecto se vuelve a disparar y reescribe el borrador que ya borramos —
    // dejando revivir un formulario ya mandado y pagando otro diagnóstico.
    if (finalizado) return
    try {
      sessionStorage.setItem(
        CLAVE,
        JSON.stringify({ variante, respuestas, paso, nombre, contacto }),
      )
    } catch {
      // sin storage disponible, el formulario funciona igual
    }
  }, [finalizado, variante, respuestas, paso, nombre, contacto])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [paso])

  // El "atrás" del navegador tiene que retroceder una pregunta, no expulsar del
  // formulario — en mobile es un gesto constante. Mantenemos una entrada de
  // historial de sobra y la reponemos en cada pop.
  const estadoRef = useRef({ paso, finalizado })
  useEffect(() => {
    estadoRef.current = { paso, finalizado }
  }, [paso, finalizado])

  useEffect(() => {
    window.history.pushState(null, '')
    const alVolver = () => {
      const { paso: actual, finalizado: cerrado } = estadoRef.current
      // Ya enviado: el formulario terminó, atrás lleva a la landing y no
      // devuelve a las preguntas.
      if (cerrado || actual === 0) {
        navigate('/')
        return
      }
      window.history.pushState(null, '')
      setPaso((p) => Math.max(0, p - 1))
    }
    window.addEventListener('popstate', alVolver)
    return () => window.removeEventListener('popstate', alVolver)
  }, [navigate])

  // --- Interacción con las preguntas -------------------------------------

  const avanzar = () => setPaso((p) => p + 1)
  const volver = () => setPaso((p) => Math.max(0, p - 1))

  const elegirUnica = (valor) => {
    setRespuestas((r) => ({ ...r, [pregunta.id]: valor }))
    registrarEvento('form_step', variante, { pregunta: pregunta.id })
    // Pausa mínima para que se vea la selección antes de pasar.
    setTimeout(avanzar, 180)
  }

  const alternarMultiple = (valor) => {
    setRespuestas((r) => {
      const actuales = r[pregunta.id] || []
      if (actuales.includes(valor)) {
        return { ...r, [pregunta.id]: actuales.filter((v) => v !== valor) }
      }
      if (pregunta.maximo && actuales.length >= pregunta.maximo) return r
      return { ...r, [pregunta.id]: [...actuales, valor] }
    })
  }

  const puedeContinuar = () => {
    if (!pregunta) return false
    const valor = respuestas[pregunta.id]
    if (pregunta.multiple) return Array.isArray(valor) && valor.length > 0
    if (pregunta.abierta) return typeof valor === 'string' && valor.trim().length >= 3
    return Boolean(valor)
  }

  // --- Envío --------------------------------------------------------------

  const contactoValido = () => {
    if (!nombre.trim()) return false
    if (variante === 'a') return /^\S+@\S+\.\S+$/.test(contacto.trim())
    return contacto.replace(/\D/g, '').length >= 8
  }

  const enviar = async () => {
    setEnviando(true)
    setError(null)
    try {
      const data = await crearDiagnostico({
        variante,
        respuestas,
        nombre: nombre.trim(),
        email: variante === 'a' ? contacto.trim() : null,
        telefono: variante === 'b' ? contacto.trim() : null,
        utm,
      })
      // Enviado: el borrador ya no sirve y no queremos que un "atrás" lo reviva.
      setFinalizado(true)
      try {
        sessionStorage.removeItem(CLAVE)
      } catch {
        /* sin storage, no hay nada que limpiar */
      }
      if (variante === 'a') {
        navigate(`/d/${data.token}`)
      } else {
        // Variante B: no abrimos WhatsApp solos (los navegadores bloquean el
        // popup si no viene de un click directo). Mostramos el botón y el
        // prospecto abre la conversación él — eso además abre la ventana de
        // 24 h que nos deja responderle sin plantilla de Meta.
        setResultado(data)
      }
    } catch (e) {
      setError(
        e?.response?.data?.detail ||
          'No pudimos guardar tus respuestas. Probá de nuevo en un momento.',
      )
    } finally {
      setEnviando(false)
    }
  }

  // --- Pantalla final de la variante B ------------------------------------

  if (resultado) {
    return (
      <main className="contenedor flex min-h-screen flex-col justify-center py-16">
        <Logo className="mb-12" />
        <div className="tarjeta animate-aparecer">
          <p className="etiqueta mb-4">Último paso</p>
          <h1 className="text-2xl sm:text-3xl">
            {nombre.split(' ')[0]}, abrí WhatsApp y te mandamos el diagnóstico
          </h1>
          <p className="mt-4 text-[15px] leading-relaxed text-texto-suave">
            El mensaje ya viene escrito. Tocá enviar y en un par de minutos lo
            tenés en el chat.
          </p>
          <a
            href={resultado.whatsapp_url}
            target="_blank"
            rel="noopener noreferrer"
            className="boton mt-8 w-full sm:w-auto"
          >
            Abrir WhatsApp
          </a>
          <p className="mt-6 text-sm text-texto-tenue">
            ¿Preferís leerlo acá?{' '}
            <button
              onClick={() => navigate(`/d/${resultado.token}`)}
              className="text-marca-acento underline underline-offset-4"
            >
              Ver el diagnóstico en la web
            </button>
          </p>
        </div>
      </main>
    )
  }

  // --- Pantalla de captura -------------------------------------------------

  if (enCaptura) {
    const esEmail = variante === 'a'
    return (
      <main className="contenedor flex min-h-screen flex-col justify-center py-16">
        <Barra progreso={95} />
        <Logo className="mb-12" />

        <div className="animate-aparecer">
          <p className="etiqueta mb-4">Ya está</p>
          <h1 className="text-2xl leading-snug sm:text-3xl">
            ¿A dónde te mandamos el diagnóstico?
          </h1>
          <p className="mt-4 text-[15px] leading-relaxed text-texto-suave">
            Lo generamos con tus respuestas y te llega en un par de minutos.
          </p>

          <div className="mt-8 space-y-4">
            <Campo
              etiqueta="Tu nombre"
              valor={nombre}
              onChange={setNombre}
              placeholder="Cómo te llamamos"
              autoFocus
            />
            <Campo
              etiqueta={esEmail ? 'Tu email' : 'Tu WhatsApp'}
              valor={contacto}
              onChange={setContacto}
              placeholder={esEmail ? 'nombre@empresa.com' : '2954 12 3456'}
              tipo={esEmail ? 'email' : 'tel'}
            />
          </div>

          {error && <p className="mt-5 text-sm text-marca-magenta">{error}</p>}

          <button
            onClick={enviar}
            disabled={!contactoValido() || enviando}
            className="boton mt-8 w-full sm:w-auto"
          >
            {enviando ? 'Generando…' : esEmail ? 'Recibir por email' : 'Recibir por WhatsApp'}
          </button>

          <p className="mt-4 text-xs leading-relaxed text-texto-tenue">
            Usamos tus datos solo para mandarte este diagnóstico. Nada de spam.
          </p>

          <button onClick={volver} className="mt-8 text-sm text-texto-tenue hover:text-texto-suave">
            ← Volver
          </button>
        </div>
      </main>
    )
  }

  // --- Pantalla de pregunta ------------------------------------------------

  const valor = respuestas[pregunta.id]

  return (
    <main className="contenedor flex min-h-screen flex-col justify-center py-16">
      <Barra progreso={progreso} />
      <Logo className="mb-12" />

      <div key={pregunta.id} className="animate-aparecer">
        <p className="etiqueta mb-4">{pregunta.bloque}</p>
        <h1 className="text-2xl leading-snug sm:text-[1.75rem]">{pregunta.texto}</h1>
        {pregunta.ayuda && (
          <p className="mt-2.5 text-sm text-texto-tenue">{pregunta.ayuda}</p>
        )}

        {pregunta.abierta ? (
          <textarea
            value={valor || ''}
            onChange={(e) => setRespuestas((r) => ({ ...r, [pregunta.id]: e.target.value }))}
            placeholder={pregunta.placeholder}
            rows={4}
            autoFocus
            className="mt-7 w-full resize-none rounded-xl border border-borde bg-superficie px-5 py-4
                       text-[15px] leading-relaxed text-texto-fuerte placeholder:text-texto-tenue
                       focus:border-marca-acento focus:outline-none"
          />
        ) : (
          <div className="mt-7 space-y-2.5">
            {pregunta.opciones.map((opcion) => {
              const activa = pregunta.multiple
                ? (valor || []).includes(opcion.valor)
                : valor === opcion.valor
              return (
                <button
                  key={opcion.valor}
                  onClick={() =>
                    pregunta.multiple
                      ? alternarMultiple(opcion.valor)
                      : elegirUnica(opcion.valor)
                  }
                  className={`opcion ${activa ? 'opcion-activa' : ''}`}
                >
                  <span className="flex items-center justify-between gap-3">
                    {opcion.texto}
                    {activa && <span className="text-marca-acento">✓</span>}
                  </span>
                </button>
              )
            })}
          </div>
        )}

        {(pregunta.multiple || pregunta.abierta) && (
          <>
            <button
              onClick={avanzar}
              disabled={!puedeContinuar()}
              className="boton mt-8 w-full sm:w-auto"
            >
              Continuar
            </button>
            {/* Un botón apagado sin explicación se lee como que algo falló. */}
            {!puedeContinuar() && (
              <p className="mt-3 text-sm text-texto-tenue">
                {pregunta.multiple
                  ? 'Elegí al menos una opción para continuar.'
                  : 'Escribí unas palabras para continuar.'}
              </p>
            )}
          </>
        )}

        {paso > 0 && (
          <button onClick={volver} className="mt-8 block text-sm text-texto-tenue hover:text-texto-suave">
            ← Volver
          </button>
        )}
      </div>
    </main>
  )
}

// --- Piezas chicas ---------------------------------------------------------

function Barra({ progreso }) {
  return (
    <div className="fixed inset-x-0 top-0 z-20 h-1 bg-superficie">
      <div
        className="h-full bg-marca-gradiente transition-[width] duration-300 ease-out"
        style={{ width: `${progreso}%` }}
      />
    </div>
  )
}

function Campo({ etiqueta, valor, onChange, placeholder, tipo = 'text', autoFocus = false }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm text-texto-suave">{etiqueta}</span>
      <input
        type={tipo}
        value={valor}
        autoFocus={autoFocus}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-borde bg-superficie px-5 py-4 text-[15px]
                   text-texto-fuerte placeholder:text-texto-tenue
                   focus:border-marca-acento focus:outline-none"
      />
    </label>
  )
}
