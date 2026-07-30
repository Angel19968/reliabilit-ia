# RELIABILIT-IA — Prompt Maestro y Roadmap de Continuidad

> **Cómo usar este documento:** pega este archivo completo como primer mensaje en una conversación nueva con Claude (Cowork) para retomar el proyecto exactamente donde quedó, sin perder nada del contexto acumulado. Está escrito para que un agente sin memoria previa entienda el proyecto, las reglas de trabajo y qué falta por hacer.

---

## 1. Qué es RELIABILIT-IA

RELIABILIT-IA es un repositorio público de GitHub (`angel19968/reliabilit-ia`, propietario Miguel Angel Cayllahua Quispe) con demos interactivas de mantenimiento predictivo, publicado vía GitHub Pages en:

**https://angel19968.github.io/reliabilit-ia/**

Es el "Nivel 1 público": 15 demos HTML/JS/CSS interactivas, cada una implementando un algoritmo de machine learning **desde cero en JavaScript vanilla** (sin librerías de ML) sobre **datos sintéticos** generados con un PRNG determinístico (seeded random + Box-Muller para gaussianas). El objetivo del sitio es educativo/comercial: mostrar la idea de cada modelo para que visitantes de distintas industrias pidan una asesoría real calibrada con sus propios datos.

Carpeta de trabajo local: `C:\Users\LENOVO\Claude\Projects\reliabilit-ia\`

---

## 2. Reglas del proyecto (no negociables — seguir siempre)

1. **Construir/editar siempre en local primero.** Todo cambio se hace en `C:\Users\LENOVO\Claude\Projects\reliabilit-ia\`. Nunca editar directo en GitHub.
2. **Nunca hacer push a GitHub de forma proactiva.** Solo subir cuando el usuario lo pida explícitamente, y hacerlo en un solo paso batcheado (clone → rsync → commit → push) al final.
3. **Todo algoritmo de ML implementado desde cero** en JavaScript vanilla — sin TensorFlow.js, sin librerías externas de ML.
4. **Datos sintéticos con RNG determinístico** (seeded random). Nunca datos reales de terceros sin autorización.
5. **Umbrales e hiperparámetros se validan externamente en Node.js antes de hardcodearlos** en el HTML/JS (no adivinar constantes "a ojo").
6. **Patrón de auditoría-antes-que-acción:** ante pedidos grandes o ambiguos (ej. "mejora la navegación", "qué le falta al sitio"), primero auditar/proponer por escrito y esperar confirmación del alcance antes de tocar código. Ya establecido y confirmado varias veces por el usuario.
7. **Push a GitHub — mecánica exacta:** no existe un tool MCP de GitHub con permiso de escritura disponible en este entorno (el conector "GitHub" que aparece conectado pertenece a la indexación de búsqueda de Notion, no da push). El flujo que sí funciona:
   - Pedir al usuario un Personal Access Token (PAT) fresco con scope `repo` (o `contents:write` si es fine-grained) para `angel19968/reliabilit-ia`.
   - `git clone https://github.com/angel19968/reliabilit-ia.git` a una carpeta temporal.
   - `rsync -a --exclude='.git' <local>/ <clone>/` para sincronizar todo el contenido local.
   - Cuidado con un falso-positivo de diff en `assets/logo.svg` por cambio de modo de archivo (100644↔100755) — corregir con `chmod 644` antes de commitear si aparece.
   - `git config user.email "miguelcquispe@gmail.com"` y `git config user.name "Miguel Angel Cayllahua Quispe"` si el commit falla por falta de identidad.
   - `git add -A && git commit -m "..."` y `git push https://angel19968:<TOKEN>@github.com/angel19968/reliabilit-ia.git main`.
   - **Redactar el token de cualquier output impreso** (usar `sed` para reemplazar el token por `[REDACTED]` en los logs mostrados).
   - **Después de cada push, recomendar al usuario revocar/rotar el token.** Nunca reutilizar un token de una sesión anterior — pedir uno nuevo cada vez.
   - Limpiar la carpeta temporal de clone al terminar.
8. **El repo puede aparecer con redirect a `Angel19968` (mayúscula)** — es solo un aviso de GitHub, no afecta el push.

---

## 3. Estructura del repo y las 15 demos

```
index.html                          ← hub/catálogo con filtros y grid de tarjetas
assets/
  logo.svg
  og-image.png                      ← imagen Open Graph 1200×630
README.md                           ← visitor-facing, tabla de las 15 demos, cómo verlo, contacto
ideas-fase-2.md                     ← propuestas de evolución algorítmica (ver sección 5.4)
auditoria-graficas.md               ← auditoría de gráficas (ya resuelta)
auditoria-v2-bugs-navegacion.md     ← auditoría de bugs + propuesta de navegación v2 (ya resuelta)
modelos/
  radar-de-rodamientos/index.html          Regresión · Rodamientos
  pulso-energetico/index.html              Series de tiempo · Energía
  diagnostico-del-motor/index.html         Clasificación · Motor
  pulso-del-motor/index.html               Nuevas tecnologías · Motor (MCSA)
  oido-industrial/index.html               Nuevas tecnologías · Aire comprimido
  detector-anomalias-compresor/index.html  Anomalías · Compresor
  radiografia-de-planta/index.html         Clustering · Planta
  semaforo-de-bombas/index.html            Clasificación · Bomba centrífuga
  guardian-de-la-bomba/index.html          Anomalías · Bomba
  frontera-de-vibracion/index.html         Clasificación · Vibración
  familias-de-turbinas/index.html          Clustering · Turbina
  nubes-de-sensores/index.html             Clustering · Sensores
  termometro-del-motor/index.html          Regresión · Motor eléctrico
  mapa-de-anomalias/index.html             Anomalías · Sensores múltiples
  ojo-termico/index.html                   Visión · Termografía
```

Cada página de módulo tiene: link "← Volver al catálogo RELIABILIT-IA", un `<select class="quick-nav">` para saltar directo a cualquiera de los otros 14 modelos, gauge(s) de resultado con marcas de umbral (`.gauge-tick`) donde el umbral es matemáticamente válido, y una sección final "De esta demo a tu planta" con CTA hacia la asesoría real.

El hub (`index.html`) tiene chips de filtro por **Paradigma** (regresión, series de tiempo, clasificación, anomalías, clustering, visión, nuevas tecnologías) y por **Sector** (rodamientos, motores, bombas, compresores, aire comprimido, turbinas, energía, planta, sensores, vibración, termografía), combinables con AND, con contador de resultados y estado vacío.

---

## 4. Historial de lo completado (orden cronológico)

1. **Auditoría de gráficas** (`auditoria-graficas.md`) resuelta: indicador de proyección continuo en 11 módulos, curvas de calidad nuevas en nubes-de-sensores y ojo-térmico, matrices de confusión reemplazando barras de precisión por clase en 3 módulos.
2. **`ideas-fase-2.md`** escrito con 4 propuestas de evolución algorítmica (ver sección 5.4).
3. **README.md reescrito** para visitantes (antes era casi idéntico al prompt interno de construcción).
4. **Primer push a GitHub** (commit `ee513a1`): completó las 15 demos en el repo remoto (antes solo tenía 2), agregó fechas/badges de paradigma, las mejoras de gráficas y el README nuevo.
5. **Auditoría v2 de bugs y navegación** (`auditoria-v2-bugs-navegacion.md`), hecha con inspección de código + inspección en vivo del sitio (Claude in Chrome). Encontró 4 bugs confirmados y propuso una v2 de navegación.
6. **4 bugs corregidos localmente:**
   - Espacio en blanco en tarjetas del hub → `display:flex; flex-direction:column` + `margin-top:auto` en el badge (mitigado, no 100% resuelto — ver 5.1).
   - `assets/og-image.png` faltante (404 en meta og:image) → generada y agregada (1200×630, on-brand).
   - CSS muerto (`.card.disabled`, `.status.soon`) → eliminado.
   - Marcas de umbral en gauges → agregadas en 8 módulos donde el umbral es un punto fijo 1D en la misma escala del gauge (semáforo-de-bombas, diagnóstico-del-motor, detector-anomalías-compresor, guardián-de-la-bomba, mapa-de-anomalías, ojo-térmico, pulso-del-motor, termómetro-del-motor). Excluidos con justificación matemática documentada: frontera-de-vibración (margen SVM), radiografía-de-planta (distancia a centroide), oído-industrial (función de 2 variables `estimateFlow(dB, presión)`).
   - Validado con `node --check` + arnés DOM-stub en los 9 archivos tocados.
7. **v2 de navegación implementada:** filtros de paradigma+sector en el hub (chips, JS de filtrado combinado, contador, estado vacío) y quick-nav (`<select>`) en las 15 páginas de módulo para saltar entre demos sin volver al hub. Validado con jsdom (casos: un filtro, dos filtros combinados, toggle, reset, caso sin resultados) y con `node --check` en los 16 archivos.
8. **Segundo push a GitHub** (commit `44a702c`): subió los 4 bugs corregidos + la v2 de navegación completa (18 archivos).
9. **Ronda de consultoría multidisciplinar** (la más reciente antes de este documento): revisión en vivo del sitio + propuesta de mejoras visuales adicionales y de nuevos modelos por industria (ver sección 5).

---

## 5. Pendiente / Roadmap (nada de esto se ha empezado a construir todavía)

### 5.1 Decisión pendiente: cierre real del espacio en blanco en tarjetas

El fix actual evita que el badge "Disponible" flote con un hueco gigante, pero **no elimina del todo el problema**: en filas donde una tarjeta tiene descripción corta y su vecina larga, el grid iguala la altura de la fila y la tarjeta de texto corto sigue mostrando un hueco entre el párrafo y el badge (visible en vivo entre "Pulso del Motor" / "Oído Industrial" y sus vecinas). Dos opciones para resolverlo de raíz, pendientes de que el usuario elija:
- **(a)** Normalizar todas las descripciones a la misma longitud aproximada (2 líneas fijas, con `line-clamp`).
- **(b) (recomendada)** Rellenar ese espacio con información útil en vez de dejarlo vacío — ej. un dato tipo "Datos sintéticos · actualizado jul 2026" o un ícono de sector.

### 5.2 Mejoras visuales propuestas (no implementadas aún)

- Tooltips/glosario para términos técnicos (MCSA, RMS, dB, ΔT, deslizamiento) — el público de asesoría no siempre es ingeniero de confiabilidad.
- Resumen "en palabras simples" junto al resultado técnico de cada gauge (ej. "Esto significa: revisa el motor en 2-4 semanas").
- Iconografía por sector en las tarjetas del hub, para escaneo visual más rápido junto con los filtros nuevos.
- Hacer sticky (fijo al hacer scroll) el link "volver" + el quick-nav en páginas de demo largas.
- Validación real de responsividad móvil en un dispositivo físico — los breakpoints existen en el CSS (760px/700px/520px) pero no se pudieron confirmar visualmente en este entorno (la herramienta de resize de navegador no cambia el viewport real aquí).

### 5.3 Nuevos modelos por industria — "Fase 3: ampliación del banco por sector" (propuesta, orden de prioridad sugerido)

El catálogo actual cubre bien motores, bombas, rodamientos, compresores/aire comprimido, turbinas, energía y sensores/planta en general, pero le faltan anclas reconocibles para varios sectores grandes:

1. **Transformadores eléctricos** (energía/utilities) — análisis de gases disueltos (DGA) simplificado — paradigma regresión o anomalías.
2. **Correas transportadoras** (minería, cemento, agroindustria) — clasificación de desalineación/desgaste — sector muy reconocible en Perú.
3. **Calderas / generación de vapor** (alimentos, papel, química, textil) — series de tiempo de eficiencia térmica declinante.
4. **Aerogeneradores** (energía renovable) o **flota de vehículos/motores diésel** (logística/transporte/construcción) — anomalías de vibración en caja de engranajes, o regresión de vida remanente — elegir según el sector que más interese captar.

Pendiente: que el usuario elija cuáles construir primero (no es necesario hacer los 4 de una vez).

### 5.4 Fase 2 — evolución algorítmica (`ideas-fase-2.md`, ya escrito, nada construido)

Documento ya entregado con 4 propuestas, priorizadas en este orden si se retoma:
1. **"Memoria del Motor"** — módulo secuencial RNN/LSTM implementado desde cero (prioridad más alta).
2. **"Etiquetas Escasas"** — semi-supervisado (self-training).
3. Dataset público real (NASA C-MAPSS o AI4I 2020) reemplazando o complementando los sintéticos.
4. **"Agenda de Mantenimiento"** — reinforcement learning (Q-learning MDP) (prioridad más baja).

---

## 6. Notas de seguridad

- El usuario ha compartido Personal Access Tokens de GitHub en texto plano en el chat en más de una ocasión para poder hacer push (no hay otra vía de escritura disponible en este entorno). Cada vez que esto ocurra: usar el token una sola vez para el push, redactarlo de cualquier log impreso, y recomendar explícitamente revocarlo/rotarlo después. Nunca asumir que un token de una conversación anterior sigue siendo válido — pedir uno nuevo.

---

## 7. Cómo retomar (primer paso sugerido en la próxima conversación)

Al recibir este documento, preguntar al usuario cuál de estos frentes quiere atacar primero (pueden ser varios en paralelo si el usuario lo pide):

- Cerrar el punto 5.1 (espacio en blanco) — elegir opción (a) o (b).
- Construir 1+ de los modelos nuevos de industria del punto 5.3 — confirmar cuáles.
- Implementar alguna(s) de las mejoras visuales del punto 5.2.
- Retomar Fase 2 (punto 5.4), empezando por el módulo secuencial LSTM si se decide avanzar ahí.

Como siempre: construir y validar todo en local primero (`C:\Users\LENOVO\Claude\Projects\reliabilit-ia\`), y solo hacer push a GitHub cuando el usuario lo pida explícitamente, en un solo paso batcheado, pidiendo un PAT nuevo en ese momento.
