import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import Logo from '../components/Logo'
import { leerUtm, registrarEvento, resolverVariante } from '../api'

const PASOS = [
  {
    // Sin número: los estudios contables suman una pregunta más (provincia).
    titulo: 'Respondés el formulario',
    detalle: 'Dos minutos. Casi todas de un toque.',
  },
  {
    titulo: 'Analizamos tu operación',
    detalle: 'Cruzamos tus respuestas con lo que ya construimos para empresas como la tuya.',
  },
  {
    titulo: 'Recibís el diagnóstico',
    detalle: 'Los tres cuellos de botella que detectamos y qué automatizaríamos primero.',
  },
]

export default function Landing() {
  const navigate = useNavigate()
  const variante = resolverVariante()

  useEffect(() => {
    registrarEvento('landing_view', variante, leerUtm())
  }, [variante])

  const empezar = () => {
    const params = new URLSearchParams(window.location.search)
    params.set('v', variante)
    navigate(`/diagnostico?${params.toString()}`)
  }

  return (
    <main className="contenedor flex min-h-screen flex-col justify-center py-16">
      <header className="mb-14 animate-aparecer">
        <Logo />
      </header>

      <div className="animate-aparecer" style={{ animationDelay: '.05s' }}>
        <p className="etiqueta mb-5">Diagnóstico sin costo</p>

        <h1 className="text-[2.1rem] leading-[1.15] sm:text-5xl sm:leading-[1.1]">
          ¿Dirigís tu negocio,
          <br />
          <span className="texto-gradiente">o sos rehén de él?</span>
        </h1>

        <p className="mt-7 max-w-xl text-[17px] leading-relaxed text-texto-suave">
          En dos minutos nos contás cómo trabaja tu empresa hoy y te decimos
          exactamente qué procesos se pueden automatizar, cuánto tiempo te están
          costando y por dónde empezaríamos nosotros.
        </p>

        <p className="mt-4 max-w-xl text-[15px] leading-relaxed text-texto-tenue">
          Sin costo, sin compromiso y sin que te llame nadie que no quieras que te llame.
        </p>

        <button onClick={empezar} className="boton mt-10 w-full sm:w-auto">
          Empezar el diagnóstico
          <span aria-hidden="true">→</span>
        </button>

        <p className="mt-3 text-sm text-texto-tenue">Toma 2 minutos.</p>
      </div>

      <ol className="mt-16 grid gap-6 sm:grid-cols-3">
        {PASOS.map((paso, i) => (
          <li
            key={paso.titulo}
            className="animate-aparecer border-t border-borde pt-5"
            style={{ animationDelay: `${0.15 + i * 0.07}s` }}
          >
            <span className="texto-gradiente text-sm font-bold">0{i + 1}</span>
            <h2 className="mt-2 text-[15px] font-medium text-texto-fuerte">{paso.titulo}</h2>
            <p className="mt-1.5 text-sm leading-relaxed text-texto-tenue">{paso.detalle}</p>
          </li>
        ))}
      </ol>

      <footer className="mt-16 border-t border-borde pt-6 text-sm leading-relaxed text-texto-tenue">
        Optimizar construye sistemas a medida y agentes de IA para PyMEs argentinas.
        Ya lo hicimos para estudios contables, inmobiliarias y productoras de eventos.
      </footer>
    </main>
  )
}
