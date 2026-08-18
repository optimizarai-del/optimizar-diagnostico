/**
 * Las 13 preguntas del diagnóstico.
 *
 * IMPORTANTE: los `id` de pregunta y los `valor` de cada opción tienen que
 * coincidir exactamente con `backend/app/form_spec.py`. El backend puntúa y
 * arma el prompt de la IA a partir de esos valores.
 */

export const PREGUNTAS = [
  // --- Bloque 1: contexto (califica el ICP) ------------------------------
  {
    id: 'rubro',
    bloque: 'Tu empresa',
    texto: '¿A qué se dedica tu empresa?',
    opciones: [
      { valor: 'contable', texto: 'Estudio contable o impositivo' },
      { valor: 'inmobiliaria', texto: 'Inmobiliaria' },
      { valor: 'construccion', texto: 'Constructora o desarrollador' },
      { valor: 'eventos', texto: 'Producción de eventos' },
      { valor: 'agro', texto: 'Agro' },
      { valor: 'comercio', texto: 'Comercio o distribuidora' },
      { valor: 'servicios', texto: 'Servicios profesionales' },
      { valor: 'salud', texto: 'Salud' },
      { valor: 'otro', texto: 'Otro' },
    ],
  },
  {
    id: 'provincia',
    bloque: 'Tu empresa',
    texto: '¿En qué provincia operan?',
    // Solo para contables: hay una exclusividad territorial que respetar.
    condicion: (r) => r.rubro === 'contable',
    opciones: [
      { valor: 'buenos-aires', texto: 'Buenos Aires o CABA' },
      { valor: 'cordoba', texto: 'Córdoba' },
      { valor: 'santa-fe', texto: 'Santa Fe' },
      { valor: 'la-pampa', texto: 'La Pampa' },
      { valor: 'otra', texto: 'Otra provincia' },
    ],
  },
  {
    id: 'tamano',
    bloque: 'Tu empresa',
    texto: '¿Cuántas personas trabajan con vos?',
    opciones: [
      { valor: 'solo', texto: 'Solo yo' },
      { valor: '2-4', texto: '2 a 4' },
      { valor: '5-15', texto: '5 a 15' },
      { valor: '16-50', texto: '16 a 50' },
      { valor: '50+', texto: 'Más de 50' },
    ],
  },
  {
    id: 'rol',
    bloque: 'Tu empresa',
    texto: '¿Cuál es tu rol?',
    opciones: [
      { valor: 'dueno', texto: 'Dueño o socio' },
      { valor: 'director', texto: 'Director o gerente general' },
      { valor: 'area', texto: 'Responsable de un área' },
      { valor: 'empleado', texto: 'Trabajo en la empresa' },
    ],
  },

  // --- Bloque 2: dónde se va el tiempo ----------------------------------
  {
    id: 'tareas',
    bloque: 'Tu día a día',
    texto: '¿Cuál de estas te come más tiempo?',
    ayuda: 'Elegí hasta 3',
    multiple: true,
    maximo: 3,
    opciones: [
      { valor: 'consultas', texto: 'Responder consultas de clientes' },
      { valor: 'carga-datos', texto: 'Cargar datos a mano' },
      { valor: 'presupuestos', texto: 'Armar presupuestos o contratos' },
      { valor: 'cobranzas', texto: 'Perseguir cobranzas' },
      { valor: 'reportes', texto: 'Armar reportes' },
      { valor: 'coordinar', texto: 'Coordinar al equipo' },
      { valor: 'buscar-info', texto: 'Buscar información desparramada' },
      { valor: 'turnos', texto: 'Turnos y agenda' },
    ],
  },
  {
    id: 'horas',
    bloque: 'Tu día a día',
    texto: 'Entre todo el equipo, ¿cuántas horas por semana se van en eso?',
    opciones: [
      { valor: 'menos-5', texto: 'Menos de 5 horas' },
      { valor: '5-10', texto: '5 a 10 horas' },
      { valor: '10-20', texto: '10 a 20 horas' },
      { valor: '20+', texto: 'Más de 20 horas' },
      { valor: 'no-se', texto: 'No tengo idea' },
    ],
  },
  {
    id: 'quien',
    bloque: 'Tu día a día',
    texto: '¿Quién lo hace hoy?',
    opciones: [
      { valor: 'yo-mismo', texto: 'Yo mismo' },
      { valor: 'una-persona', texto: 'Una persona del equipo' },
      { valor: 'varias', texto: 'Varias personas' },
      { valor: 'a-medias', texto: 'Se hace a medias, cuando se puede' },
    ],
  },

  // --- Bloque 3: cómo entra y se atiende la demanda ----------------------
  {
    id: 'canales',
    bloque: 'Tus clientes',
    texto: '¿Por dónde te llegan los clientes nuevos?',
    ayuda: 'Podés elegir varios',
    multiple: true,
    opciones: [
      { valor: 'whatsapp', texto: 'WhatsApp' },
      { valor: 'redes', texto: 'Instagram o Facebook' },
      { valor: 'web', texto: 'La web' },
      { valor: 'telefono', texto: 'Teléfono' },
      { valor: 'referidos', texto: 'Referidos' },
      { valor: 'presencial', texto: 'Presencial' },
      { valor: 'salgo-a-buscar', texto: 'No me llegan solos, salgo a buscarlos' },
    ],
  },
  {
    id: 'respuesta',
    bloque: 'Tus clientes',
    texto: 'Cuando entra una consulta, ¿en cuánto responden?',
    opciones: [
      { valor: 'minutos', texto: 'En minutos' },
      { valor: 'horas', texto: 'En horas' },
      { valor: 'dia-siguiente', texto: 'Al día siguiente' },
      { valor: 'depende', texto: 'Depende del día' },
      { valor: 'se-pierden', texto: 'A veces se nos pierden' },
    ],
  },
  {
    id: 'seguimiento',
    bloque: 'Tus clientes',
    texto: '¿Le hacés seguimiento al que consultó y no compró?',
    opciones: [
      { valor: 'sistematico', texto: 'Sí, sistemático' },
      { valor: 'a-veces', texto: 'A veces, cuando me acuerdo' },
      { valor: 'no', texto: 'No' },
    ],
  },

  // --- Bloque 4: sistemas y datos ---------------------------------------
  {
    id: 'sistemas',
    bloque: 'Tus sistemas',
    texto: '¿Con qué trabajan hoy?',
    ayuda: 'Podés elegir varios',
    multiple: true,
    opciones: [
      { valor: 'excel', texto: 'Excel o Google Sheets' },
      { valor: 'whatsapp', texto: 'WhatsApp' },
      { valor: 'papel', texto: 'Papel o cuaderno' },
      { valor: 'erp', texto: 'Un sistema de gestión o ERP' },
      { valor: 'crm', texto: 'Un CRM' },
      { valor: 'cada-uno', texto: 'Cada uno con lo suyo' },
    ],
  },
  {
    id: 'trazabilidad',
    bloque: 'Tus sistemas',
    texto:
      'Si ahora necesitás saber cuánto facturaste este mes o qué te debe un cliente, ¿cuánto tardás?',
    opciones: [
      { valor: 'al-toque', texto: 'Lo veo al toque' },
      { valor: 'minutos', texto: 'Unos minutos' },
      { valor: 'pedirlo', texto: 'Se lo tengo que pedir a alguien' },
      { valor: 'no-puedo', texto: 'No lo puedo saber con certeza' },
    ],
  },

  // --- Bloque 5: intención ----------------------------------------------
  {
    id: 'prioridad',
    bloque: 'Lo que viene',
    texto: 'Si pudieras resolver una sola cosa en los próximos 3 meses, ¿cuál sería?',
    ayuda: 'Escribilo con tus palabras. Es lo que más nos sirve.',
    abierta: true,
    placeholder: 'Ej: dejar de perder consultas de WhatsApp los fines de semana',
  },
  {
    id: 'timing',
    bloque: 'Lo que viene',
    texto: '¿Para cuándo?',
    opciones: [
      { valor: 'ya', texto: 'Ya, es urgente' },
      { valor: '1-3-meses', texto: 'En 1 a 3 meses' },
      { valor: 'este-ano', texto: 'Este año' },
      { valor: 'mirando', texto: 'Estoy mirando nomás' },
    ],
  },
]

/** Preguntas visibles según lo que ya respondió (resuelve las condicionales). */
export function preguntasVisibles(respuestas) {
  return PREGUNTAS.filter((p) => !p.condicion || p.condicion(respuestas))
}
