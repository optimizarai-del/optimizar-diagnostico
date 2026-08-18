import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'

import Logo from '../components/Logo'
import { obtenerDiagnostico, registrarClickCta } from '../api'

const INTERVALO_MS = 3000
const INTENTOS_MAX = 60 // ~3 minutos

/** El titular viene como oración suelta, pero acá va detrás del nombre:
 *  "Gabriel, Más de 20 horas…" se lee mal. Bajamos la inicial, salvo que sea
 *  una sigla o un nombre propio (ahí la segunda letra también es mayúscula). */
function enMinuscula(texto) {
  if (!texto) return texto
  const [inicial, siguiente] = [texto[0], texto[1]]
  const esOracionNormal =
    inicial !== inicial.toLowerCase() && siguiente && siguiente === siguiente.toLowerCase()
  return esOracionNormal ? inicial.toLowerCase() + texto.slice(1) : texto
}

export default function Diagnostico() {
  const { token } = useParams()
  const [datos, setDatos] = useState(null)
  const [fallo, setFallo] = useState(null)
  const intentos = useRef(0)

  useEffect(() => {
    let vivo = true
    let timer

    const consultar = async () => {
      try {
        const d = await obtenerDiagnostico(token)
        if (!vivo) return
        setDatos(d)

        if (d.estado === 'listo') return
        if (d.estado === 'error') {
          setFallo('No pudimos generar tu diagnóstico.')
          return
        }
        if (++intentos.current >= INTENTOS_MAX) {
          setFallo('Está tardando más de lo normal.')
          return
        }
        timer = setTimeout(consultar, INTERVALO_MS)
      } catch {
        if (vivo) setFallo('No encontramos ese diagnóstico.')
      }
    }

    consultar()
    return () => {
      vivo = false
      clearTimeout(timer)
    }
  }, [token])

  const abrirWhatsapp = () => registrarClickCta(token)

  // --- Estados intermedios -------------------------------------------------

  if (fallo) {
    return (
      <Marco>
        <div className="tarjeta">
          <h1 className="text-2xl">{fallo}</h1>
          <p className="mt-4 text-[15px] leading-relaxed text-texto-suave">
            Escribinos y lo resolvemos a mano — tenemos tus respuestas guardadas.
          </p>
        </div>
      </Marco>
    )
  }

  if (!datos || datos.estado !== 'listo') {
    return (
      <Marco>
        <div className="tarjeta text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-borde border-t-marca-acento" />
          <h1 className="mt-7 text-xl">Estamos armando tu diagnóstico</h1>
          <p className="mx-auto mt-3 max-w-sm text-[15px] leading-relaxed text-texto-suave">
            Tarda un par de minutos. Podés dejar esta pestaña abierta: se
            actualiza sola.
          </p>
        </div>
      </Marco>
    )
  }

  // --- Diagnóstico listo ---------------------------------------------------

  const { contenido, nombre, whatsapp_url } = datos
  const primerNombre = (nombre || '').split(' ')[0]

  return (
    <Marco ancho>
      <article className="space-y-12">
        <header className="animate-aparecer">
          <p className="etiqueta mb-4">Diagnóstico operativo</p>
          <h1 className="text-[1.9rem] leading-[1.2] sm:text-[2.4rem]">
            {primerNombre && `${primerNombre}, `}
            <span className="texto-gradiente">
              {primerNombre ? enMinuscula(contenido.titular) : contenido.titular}
            </span>
          </h1>
          <p className="mt-6 text-[17px] leading-relaxed text-texto-suave">
            {contenido.resumen}
          </p>
        </header>

        <section className="animate-aparecer" style={{ animationDelay: '.08s' }}>
          <h2 className="mb-6 text-xl">Los tres cuellos de botella</h2>
          <div className="space-y-4">
            {contenido.cuellos.map((cuello, i) => (
              <div key={i} className="tarjeta">
                <div className="flex items-baseline gap-4">
                  <span className="texto-gradiente text-sm font-bold">0{i + 1}</span>
                  <div className="flex-1">
                    <h3 className="text-[17px] leading-snug">{cuello.titulo}</h3>
                    <p className="mt-2.5 text-[15px] leading-relaxed text-texto-suave">
                      {cuello.descripcion}
                    </p>
                    <p className="mt-4 inline-block rounded-lg bg-marca-acento/10 px-3 py-1.5 text-sm text-marca-acento">
                      {cuello.impacto}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="animate-aparecer" style={{ animationDelay: '.14s' }}>
          <h2 className="mb-6 text-xl">Por dónde empezaríamos</h2>
          <div className="tarjeta border-marca-acento/40">
            <h3 className="text-[17px] leading-snug">{contenido.recomendacion.titulo}</h3>
            <p className="mt-3 text-[15px] leading-relaxed text-texto-suave">
              {contenido.recomendacion.descripcion}
            </p>
            <p className="mt-5 text-sm text-texto-tenue">
              Tiempo estimado de implementación:{' '}
              <span className="text-texto-medio">{contenido.recomendacion.plazo}</span>
            </p>
          </div>
        </section>

        <section className="animate-aparecer" style={{ animationDelay: '.2s' }}>
          <h2 className="mb-2 text-xl">Algo que podés hacer solo esta semana</h2>
          <p className="mb-6 text-sm text-texto-tenue">
            Sin contratarnos y sin comprar nada.
          </p>
          <div className="tarjeta">
            <h3 className="text-[17px] leading-snug">{contenido.quick_win.titulo}</h3>
            <ol className="mt-5 space-y-3">
              {contenido.quick_win.pasos.map((paso, i) => (
                <li key={i} className="flex gap-3.5 text-[15px] leading-relaxed text-texto-suave">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-borde text-[11px] text-texto-tenue">
                    {i + 1}
                  </span>
                  {paso}
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section
          className="tarjeta animate-aparecer border-marca-acento/40 text-center"
          style={{ animationDelay: '.26s' }}
        >
          <p className="mx-auto max-w-md text-[15px] leading-relaxed text-texto-suave">
            {contenido.cierre}
          </p>
          <a
            href={whatsapp_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={abrirWhatsapp}
            className="boton mt-7 w-full sm:w-auto"
          >
            Hablar por WhatsApp
          </a>
          <p className="mt-4 text-xs text-texto-tenue">
            Te responde nuestro equipo. Si tiene sentido, coordinamos una llamada
            de 30 minutos.
          </p>
        </section>
      </article>
    </Marco>
  )
}

function Marco({ children, ancho = false }) {
  return (
    <main className={`mx-auto w-full px-5 py-16 ${ancho ? 'max-w-3xl' : 'max-w-2xl'}`}>
      <Logo className="mb-12" />
      {children}
      <footer className="mt-16 border-t border-borde pt-6 text-xs leading-relaxed text-texto-tenue">
        Este diagnóstico se generó con las respuestas que diste en el formulario.
        Las estimaciones salen de tus propios números, no de promedios de industria.
      </footer>
    </main>
  )
}
