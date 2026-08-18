/** Tokens de `brand.md`. Si cambia el manual de marca, se cambia acá. */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        fondo: '#0D0F1A',
        superficie: '#141726',
        borde: '#232741',
        marca: {
          azul: '#3B82F6',
          violeta: '#6B5CE7',
          magenta: '#DB2777',
          acento: '#8B5CF6',
        },
        texto: {
          fuerte: '#FFFFFF',
          medio: '#C9CCD8',
          suave: '#9AA0B4',
          tenue: '#6B7089',
        },
      },
      fontFamily: {
        sans: ['Poppins', 'Montserrat', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'marca-gradiente':
          'linear-gradient(110deg, #3B82F6 0%, #6B5CE7 50%, #DB2777 100%)',
      },
      keyframes: {
        aparecer: {
          '0%': { opacity: 0, transform: 'translateY(12px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        latir: {
          '0%, 100%': { opacity: 0.35 },
          '50%': { opacity: 1 },
        },
      },
      animation: {
        aparecer: 'aparecer .45s cubic-bezier(.16,1,.3,1) both',
        latir: 'latir 4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
