/**
 * Fondo de red de nodos — el elemento visual distintivo que pide `brand.md`
 * ("red de nodos y líneas de conexión: flujo de datos y automatización").
 *
 * Va en SVG y no en imagen: pesa unos pocos KB, escala a cualquier pantalla y
 * no depende de que un diseñador exporte nada.
 */

// Coordenadas fijas (nada de random): así el render es idéntico siempre.
const NODOS = [
  { x: 8, y: 18, r: 2.5 }, { x: 22, y: 9, r: 1.8 }, { x: 34, y: 24, r: 3.2 },
  { x: 17, y: 38, r: 2.0 }, { x: 48, y: 14, r: 2.2 }, { x: 61, y: 30, r: 2.8 },
  { x: 76, y: 12, r: 1.9 }, { x: 89, y: 26, r: 2.6 }, { x: 70, y: 47, r: 2.1 },
  { x: 92, y: 55, r: 1.7 }, { x: 12, y: 62, r: 2.4 }, { x: 30, y: 72, r: 1.8 },
  { x: 45, y: 58, r: 3.0 }, { x: 57, y: 78, r: 2.2 }, { x: 80, y: 70, r: 2.5 },
  { x: 24, y: 90, r: 2.0 }, { x: 66, y: 93, r: 1.8 }, { x: 94, y: 86, r: 2.3 },
]

// Pares de índices que se conectan
const ENLACES = [
  [0, 1], [1, 2], [2, 3], [0, 3], [1, 4], [4, 5], [5, 6], [6, 7], [5, 8],
  [7, 9], [8, 9], [3, 10], [10, 11], [11, 12], [12, 8], [12, 13], [13, 14],
  [14, 9], [11, 15], [15, 13], [13, 16], [16, 17], [14, 17], [2, 12], [4, 6],
]

export default function RedNodos() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden="true">
      {/* Halos de gradiente: dan profundidad sin cargar imágenes */}
      <div className="absolute -left-40 -top-40 h-[36rem] w-[36rem] rounded-full bg-marca-azul/15 blur-[120px]" />
      <div className="absolute -right-40 top-1/4 h-[32rem] w-[32rem] rounded-full bg-marca-violeta/15 blur-[120px]" />
      <div className="absolute bottom-0 left-1/3 h-[28rem] w-[28rem] rounded-full bg-marca-magenta/10 blur-[130px]" />

      <svg
        className="absolute inset-0 h-full w-full opacity-[0.55]"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <linearGradient id="lineaMarca" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="50%" stopColor="#6B5CE7" />
            <stop offset="100%" stopColor="#DB2777" />
          </linearGradient>
          <radialGradient id="nodoMarca">
            <stop offset="0%" stopColor="#8B5CF6" />
            <stop offset="100%" stopColor="#3B82F6" />
          </radialGradient>
        </defs>

        <g stroke="url(#lineaMarca)" strokeWidth="0.12" opacity="0.5">
          {ENLACES.map(([a, b], i) => (
            <line
              key={i}
              x1={NODOS[a].x}
              y1={NODOS[a].y}
              x2={NODOS[b].x}
              y2={NODOS[b].y}
            />
          ))}
        </g>

        <g fill="url(#nodoMarca)">
          {NODOS.map((n, i) => (
            <circle
              key={i}
              cx={n.x}
              cy={n.y}
              r={n.r * 0.22}
              className="animate-latir"
              style={{ animationDelay: `${(i % 7) * 0.55}s` }}
            />
          ))}
        </g>
      </svg>
    </div>
  )
}
