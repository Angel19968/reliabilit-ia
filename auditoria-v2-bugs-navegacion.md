# Auditoría v2 — bugs, espacios en blanco y navegación

Revisé el sitio en vivo (https://angel19968.github.io/reliabilit-ia/) con el navegador, más el código fuente local, poniéndome en el lugar de front-end/back-end dev, AI engineer, ingeniero de datos, científico de datos e ingeniero de confiabilidad. Esto es lo que encontré, separado en bugs concretos (para corregir ya, bajo riesgo) y propuesta de v2 (para decidir juntos antes de construir).

## Respuesta directa a tu pregunta: los espacios en blanco

Ninguna de las dos — no es minimalismo intencional ni "nada pensado ahí". Es un efecto secundario de CSS: el catálogo usa un grid donde todas las tarjetas de una misma fila se estiran a la misma altura (comportamiento por defecto de CSS Grid), pero la descripción de cada demo tiene distinto largo (una o tres líneas). Entonces la tarjeta con texto corto (por ejemplo "Radar de Rodamientos") queda con un hueco vacío entre el texto y el borde inferior, mientras la tarjeta vecina con texto largo lo llena. Lo confirmé visualmente: es un hueco real, no un placeholder para contenido futuro.

**Corrección de bajo riesgo:** convertir el contenido de cada tarjeta en un contenedor flex-columna y anclar el badge "● Disponible" al fondo con `margin-top:auto`, para que quede alineado parejo en toda la fila sin importar el largo del texto. Es un cambio de CSS de unas pocas líneas, sin tocar la lógica de ninguna demo.

## Bugs confirmados (para corregir localmente ya)

1. **`assets/og-image.png` no existe — 404 confirmado en las 16 páginas.** Lo verifiqué haciendo fetch directo al archivo en el sitio en vivo: responde 404. Todas las páginas (hub + 15 demos) referencian esta imagen en sus meta tags Open Graph — significa que cualquier link compartido en WhatsApp, LinkedIn o Slack se ve sin imagen de previsualización. Es rápido de resolver: genero una imagen 1200×630 con el logo/paleta del sitio y la subimos a `assets/`.

2. **CSS muerto:** las clases `.card.disabled` y `.status.soon` siguen en el CSS del hub pero ningún HTML las usa (las 15 tarjetas están "Disponible"). No rompen nada, pero es código sin uso que puede confundir a futuro — limpieza menor, cero riesgo.

3. **Sin navegación entre demos.** Confirmé en el sitio en vivo: la única forma de moverte de una demo a otra es el link "← Volver al catálogo" en la esquina superior — no hay atajo para saltar directo de "Mapa de Anomalías" a, por ejemplo, "Guardián de la Bomba" sin pasar por el hub. Esto es justo lo que mencionas en tu pregunta ("cómo me dirijo a otra ventana rápidamente") — no es un bug de código, es una limitación de navegación real que vale la pena resolver en v2 (ver abajo).

4. **Posible confusión de escala en algunos gauges.** En Mapa de Anomalías, por ejemplo, una lectura clasificada como "Normal" con confianza alta muestra un gauge de "66/100". No es un error de cálculo (66 = qué tan cerca está del umbral de "Anómalo", no "qué tan anómalo es en términos absolutos" — y el texto de ayuda debajo sí lo explica), pero a primera vista puede leerse como contradictorio. Vale la pena agregar una marca visual en la barra del gauge mostrando dónde caen los umbrales de "Atención" y "Anómalo", para que el número se entienda sin tener que leer la nota.

Ninguno de estos bugs es grave ni bloqueante — el sitio funciona correctamente — pero los cuatro son baratos de corregir y no dependen de decisiones de diseño más grandes.

## Propuesta de navegación v2 (para decidir el alcance)

Sobre tus ideas de agrupar por modelo, sector, base de datos, precisión, y navegación rápida entre demos:

- **Agrupar por paradigma de aprendizaje** (supervisado / no supervisado / serie de tiempo / visión por reglas): ya tenemos el dato — es el badge que agregamos a cada demo. Agregar filtro por chips en el hub es directo.
- **Agrupar por tipo de equipo/sector** (bombas, motores, turbinas, compresores, sensores múltiples): también directo, ya está en el "tag" de cada tarjeta (ej. "Anomalías · Compresor").
- **Agrupar por técnica/algoritmo** (regresión, árbol, k-NN, SVM, clustering, red neuronal, etc.): posible, aunque son 15 demos con técnicas casi todas distintas — el valor de este filtro es menor que los dos anteriores, a menos que planees agregar más demos con la misma técnica.
- **"Agrupar por base de datos"**: si te refieres a agrupar por el tipo de dataset (sintético vs. el futuro dataset público real de la Fase 2), tiene sentido más adelante, cuando exista más de una fuente de datos — hoy todas son sintéticas, así que este filtro no aportaría nada todavía.
- **"Agrupar por precisión"**: esto es lo más delicado de los cinco. La "precisión" de cada modelo no es un número fijo — cambia según el hiperparámetro que el visitante elige en Modo Analista (profundidad del árbol, k, λ, etc.). No hay una sola cifra de precisión por demo para ordenar o filtrar; sería honesto mostrar un rango ("70-95% según ajuste") en vez de un número único, o directamente no ofrecer este filtro para no dar una falsa sensación de comparabilidad entre demos con problemas distintos.
- **Navegación rápida entre demos** (tu pregunta de "cómo me dirijo a otra ventana rápidamente"): propongo una barra de navegación fija (sticky) en la parte superior de cada demo, con: volver al catálogo, y un menú desplegable o carrusel de "otras demos" agrupadas por paradigma, para saltar directo sin recargar el hub completo.

## Sobre mobile

El sitio ya tiene breakpoints en 760px (grid de la demo pasa a una columna), 700px (tarjeta de contacto) y 520px (resultado en columna). Es una base razonable. Mi herramienta de navegador no logró forzar un viewport angosto en esta sesión para confirmarlo con capturas reales — te recomiendo revisarlo tú mismo en tu celular antes de decidir qué entra en v2 (sliders, botones de "Modo Analista" y las tablas de dataset son los tres puntos que más vale la pena probar con el dedo).

## Qué propongo hacer primero

Los 4 bugs de arriba los puedo corregir localmente ahora mismo (bajo riesgo, no tocan la lógica de ningún modelo) y dejarlos listos para tu revisión antes de subir a GitHub. La navegación v2 (filtros + salto rápido entre demos) es un cambio más grande de diseño e implica tocar las 16 páginas — prefiero que me confirmes qué combinación de filtros quieres (¿paradigma + sector? ¿los dos + navegación rápida?) antes de construirlo, para no rehacer trabajo.
