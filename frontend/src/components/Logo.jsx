/**
 * Logotipo provisional.
 *
 * PENDIENTE: el isologo oficial está en Drive solo como PNG
 * ("Isologotipo color optimizar_con borde degrade.png"). Cuando exista el SVG,
 * reemplazar este componente por el archivo real — el PNG pesa 60 KB y se
 * pixela en pantallas retina.
 */
export default function Logo({ className = '' }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden="true">
        <defs>
          <linearGradient id="logoMarca" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="50%" stopColor="#6B5CE7" />
            <stop offset="100%" stopColor="#DB2777" />
          </linearGradient>
        </defs>
        <circle cx="13" cy="13" r="11.5" stroke="url(#logoMarca)" strokeWidth="2" />
        <circle cx="13" cy="13" r="4" fill="url(#logoMarca)" />
      </svg>
      <span className="text-[15px] font-semibold tracking-tight text-texto-fuerte">
        Optimizar
      </span>
    </div>
  )
}
