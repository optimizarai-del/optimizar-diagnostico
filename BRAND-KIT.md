# Kit de marca Optimizar — versión ejecutable

> Consolidado de `brand.md` (junio 2026) + los activos gráficos de Drive +
> el doc "Sitio web | Optimizar". Es el manual de marca traducido a decisiones
> concretas de interfaz. Los tokens ya están implementados en
> `frontend/tailwind.config.js` e `index.css`.

## 1. Dónde vive cada cosa

| Pieza | Ubicación | Estado |
|---|---|---|
| `brand.md` (fuente) | `Bureau\OPTMIZAR\vibe marketing\files\optimizar_md_base\optimizar_md\` | ✅ |
| Isologotipo color con borde degradé | Drive — `Isologotipo color optimizar_con borde degrade.png` | ⚠️ solo PNG |
| Isologo con fondo degradé | Drive — `Isologo-optimizar-con-fondo-degrade-02.png` | ⚠️ solo PNG |
| Portada 1128×382 | Drive — `Portada-optimizar-1128-x-382-ppp_version-02.png` | ⚠️ solo PNG |
| Presentación de marca | Drive — `Presentación Optimizar.pdf` (10 MB, oct-2025) | referencia visual |
| Estructura y copy de sitio | Drive — doc `Sitio web \| Optimizar` (sep-2025) | ⚠️ usa "usted" |

**Deuda abierta:** no hay SVG del isologo. `frontend/src/components/Logo.jsx`
es un logotipo provisional construido en SVG. Cuando exista el archivo real, se
reemplaza ese componente y nada más.

## 2. Paleta

| Token | Hex | Uso |
|---|---|---|
| `marca.azul` | `#3B82F6` | Inicio del gradiente |
| `marca.violeta` | `#6B5CE7` | Medio del gradiente · botones sólidos |
| `marca.magenta` | `#DB2777` | Fin del gradiente · errores |
| `marca.acento` | `#8B5CF6` | Acento eléctrico: etiquetas, focus, íconos |
| `fondo` | `#0D0F1A` | Fondo principal oscuro |
| `superficie` | `#141726` | Tarjetas y campos (derivado) |
| `borde` | `#232741` | Bordes y separadores (derivado) |
| `texto.fuerte` | `#FFFFFF` | Títulos |
| `texto.medio` | `#C9CCD8` | Cuerpo |
| `texto.suave` | `#9AA0B4` | Cuerpo secundario |
| `texto.tenue` | `#6B7089` | Notas al pie, ayudas |

El gradiente de marca siempre corre en el mismo orden y ángulo:

```css
linear-gradient(110deg, #3B82F6 0%, #6B5CE7 50%, #DB2777 100%)
```

Se usa en: botón primario, barra de progreso, texto destacado del titular y las
líneas de la red de nodos. **No** se usa como fondo de pantallas completas ni
detrás de texto largo.

`superficie`, `borde` y los cuatro niveles de texto no están en `brand.md`: los
derivé del fondo `#0D0F1A` para tener una escala usable. Si el equipo define
otros valores en el manual nuevo, se cambian en `tailwind.config.js` y se
propagan solos.

## 3. Tipografía

**Poppins** (fallback Montserrat), cargada desde Google Fonts en `index.html`.
Pesos 300/400/500/600/700.

| Rol | Tamaño | Peso | Notas |
|---|---|---|---|
| Titular de landing | 2.1rem → 3rem | 600 | `tracking-tight`, interlineado 1.15 |
| Titular de pregunta | 1.5rem → 1.75rem | 600 | |
| Subtítulo de sección | 1.25rem | 600 | |
| Cuerpo | 15–17 px | 400 | interlineado 1.6–1.7 |
| Etiqueta | 11 px | 600 | mayúsculas, `tracking .18em`, color acento |

Nada de serif ni fuentes decorativas — `brand.md` las descarta explícitamente.

## 4. Elementos visuales

**Red de nodos** (`components/RedNodos.jsx`) — 18 nodos y 25 enlaces en SVG
inline, con halos de gradiente desenfocados. Representa el flujo de datos y la
automatización, que es lo que pide el manual. Va en SVG y no en imagen: pesa
unos pocos KB, escala a cualquier pantalla y no depende de un export.

**Formas geométricas con gradiente**, nunca fotos de personas.

Prohibido por `brand.md` y respetado en todo el build:
- Ilustraciones de IA de baja calidad (robots, cerebros con chips)
- Stock photos de gente en oficinas con laptops
- Diseños saturados
- Fuentes decorativas o serif

## 5. Voz — la decisión que tomé

`brand.md` dice **"Tuteamos"**. El doc del sitio web usa usted en todo
("Optimizamos sus procesos", "su empresa"). Son incompatibles.

**Va voseo**, por dos razones: `brand.md` es de junio 2026 y el doc del sitio de
septiembre 2025, y el voseo es coherente con el ICP (dueño de PyME, no gerente
corporativo). Todo el copy del proyecto está escrito así.

Si el equipo prefiere usted, hay que reescribir: `Landing.jsx`,
`Formulario.jsx`, `Diagnostico.jsx`, `services/email.py` y el bloque de tono en
`backend/app/vibe/contexto.md`.

## 6. Los cuatro filtros aplicados al producto

`brand.md` define cuatro guardarraíles. Así se implementaron:

1. **¿Suena a humano de Optimizar?** El prompt del generador prohíbe la jerga
   de agencia y lista las frases vetadas una por una.
2. **¿Tiene sustancia o es puro tono?** El diagnóstico incluye un *quick win*
   que la persona puede ejecutar sola, sin contratarnos.
3. **¿Promete algo que no podemos respaldar?** El prompt prohíbe estimar con
   benchmarks: toda cifra tiene que derivarse de lo que respondió el prospecto.
4. **¿Es consistente con el posicionamiento de socio operativo?** La
   recomendación sale del catálogo real de `oferta.md`, no de una idea genérica
   de automatización.
