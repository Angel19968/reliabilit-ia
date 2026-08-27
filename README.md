# RELIABILIT-IA — Demos Públicas

**Modelos interactivos que anticipan fallas, no solo las registran.**

RELIABILIT-IA es un proyecto de mantenimiento predictivo e ingeniería de confiabilidad aplicada. Este repositorio reúne tres bloques de contenido, todos autocontenidos en HTML/CSS/JS (sin backend, sin build step, sin librerías de ML de por medio):

1. **24 demos interactivas de machine learning** (`modelos/`) — cada una explica, en el navegador, un algoritmo real aplicado a un problema concreto de planta: vibración en rodamientos, temperatura de motores, firma de corriente de motores (MCSA), fugas de aire comprimido, gemelos digitales físicos, redes neuronales recurrentes, imágenes térmicas, y más.
2. **16 análisis de ingeniería de confiabilidad estadística** (`confiabilidad-calculos/` y `confiabilidad-avanzada/`) — Weibull, Kaplan-Meier, Nelson-Aalen, MCF/ROCOF de sistemas reparables, curva de Duane, stress-strength interference, entre otros, cada uno **auditado numéricamente contra la librería Python `reliability`** (no solo implementado, sino verificado).
3. **Un panel de Business Intelligence** (`panel-analitico/`) con 15 tipos de gráfico construidos a mano en SVG, aplicados a datos de planta.

Cada demo de `modelos/` funciona en dos modos: un **Modo Básico**, pensado para cualquier persona (mueve un par de sliders y mira la predicción cambiar en vivo, traducida a decisiones de negocio, no a números sueltos), y un **Modo Analista**, pensado para quien quiera ver el modelo por dentro — el dataset, los hiperparámetros ajustables, y cómo cambian las métricas de ajuste (subajuste, sobreajuste, exactitud, matrices de confusión) según las decisiones que tomes.

## ¿Qué vas a encontrar en cada demo de `modelos/`?

- Un problema de mantenimiento explicado en términos de planta, no de estadística.
- Un algoritmo real implementado desde cero (regresión, árboles de decisión, k-NN, SVM, PCA, k-means, clustering jerárquico, DBSCAN, redes neuronales, LSTM entrenada con BPTT, modelos físicos de gemelo digital, Isolation Forest, segmentación de imágenes, entre otros) — sin librerías de ML de por medio, para que el código sea legible de principio a fin.
- Un dataset sintético de ejemplo, generado con un generador de números aleatorios con semilla fija (reproducible), con fechas, hiperparámetros y umbrales validados externamente antes de mostrarse — no hay números inventados sobre la marcha.
- Una traducción de negocio: qué significa cada resultado para una planta real, y qué se pierde o gana al mover el umbral de decisión.

## Rigor metodológico: `confiabilidad-calculos/` y `confiabilidad-avanzada/`

Estas dos páginas son el bloque de ingeniería de confiabilidad clásica, con un estándar de verificación distinto al de las demos de `modelos/`: cada gráfico se generó con un script de Python (`gen_*.py`, incluido en la misma carpeta) y luego **se auditó su salida contra una fuente de verdad externa** antes de publicarse — la librería `reliability`, `scipy.integrate.quad`, o la reproducción manual de la fórmula exacta leída con `inspect.getsource` cuando la librería tenía un bug de compatibilidad en este entorno. El resultado de cada auditoría queda registrado en `*_audit.json` en la misma carpeta.

**`confiabilidad-calculos/`** (8 análisis, dataset base: 40 unidades, 32 fallas + 8 censuras, β≈2.28, η≈9,348h):
Weibull (R/F/f) · Kaplan-Meier · Nelson-Aalen · Mixture model · Competing risks model · Optimal replacement time · QQ plot · PP plot semiparamétricos.

**`confiabilidad-avanzada/`** (8 análisis de complejidad media):
Histograma de fallas + PDF superpuesta · MCF de sistema reparable (NHPP Power Law simulado) · ROCOF (test de Laplace) · Gráfico de probabilidad de Weibull · Reliability growth / curva de Duane · Sequential sampling chart · Stress-Strength interference · DSZI model.

## Panel Analítico (`panel-analitico/`)

15 tipos de gráfico de Business Intelligence construidos a mano en SVG sobre datos de planta: comparaciones y tendencias (columnas/barras agrupadas, columnas apiladas, líneas, áreas apiladas), parte-a-todo (dona, treemap, embudo, cascada), relación (dispersión/burbujas), mapas, KPIs, tablas detalladas y visualizaciones de estructura de modelos de IA (árbol de descomposición, jerarquías).

## Un aviso importante sobre los datos

**Todos los datos de este repositorio son sintéticos**, generados específicamente para poder compartir la metodología públicamente sin exponer información de ningún cliente. La metodología (los algoritmos, la forma de validar el ajuste, el enfoque de cada problema) es real y es la misma que usamos en proyectos reales — los números de cada dataset, no.

El modelo calibrado con datos reales de una planta —el que sí sirve para decidir cuándo intervenir un equipo real— vive en un entorno privado (Suite Predictiva PRO) y no se publica aquí. Si tienes datos de tus propios equipos y quieres explorar cómo se vería esto calibrado con tu información, hay contactos directos al final de este documento y en cada demo.

## Catálogo de las 24 demos (`modelos/`)

### Rotativos (13)

| Demo | Categoría | Qué resuelve |
|---|---|---|
| [Radar de Rodamientos](modelos/radar-de-rodamientos/) | Regresión · Rodamientos | Estima días hasta falla según vibración RMS y temperatura |
| [Diagnóstico del Motor](modelos/diagnostico-del-motor/) | Clasificación · Motor | Clasifica el estado de un motor en 5 niveles de severidad |
| [Pulso del Motor](modelos/pulso-del-motor/) | Nuevas tecnologías · Motor | Diagnóstico por firma de corriente (MCSA) con pinza amperimétrica |
| [Detector de Anomalías del Compresor](modelos/detector-anomalias-compresor/) | Anomalías · Compresor | Detecta lecturas fuera de patrón sin ejemplos previos de falla |
| [Semáforo de Bombas](modelos/semaforo-de-bombas/) | Clasificación · Bomba centrífuga | Clasifica una bomba en verde, amarillo o rojo |
| [Guardián de la Bomba](modelos/guardian-de-la-bomba/) | Anomalías · Bomba | Detecta comportamiento anómalo con muy pocos datos históricos |
| [Frontera de Vibración](modelos/frontera-de-vibracion/) | Clasificación · Vibración | Separa 3 estados de vibración con un límite de decisión (SVM) |
| [Horizonte de Falla](modelos/horizonte-de-falla/) | Regresión · Vibración | Proyecta con 90% de confianza cuándo la vibración cruzará alerta y alarma |
| [Familias de Turbinas](modelos/familias-de-turbinas/) | Clustering · Turbina | Agrupa turbinas similares (clustering jerárquico) |
| [Centinela del Aerogenerador](modelos/centinela-del-aerogenerador/) | Anomalías · Aerogenerador | Detecta lecturas anómalas en la caja de engranajes |
| [Termómetro del Motor](modelos/termometro-del-motor/) | Regresión · Motor eléctrico | Estima la temperatura de un motor con una red neuronal |
| [Memoria del Motor](modelos/memoria-del-motor/) | Series de tiempo · Motor | LSTM entrenada desde cero (BPTT) vs. modelo sin memoria |
| [Gemelo Digital del Motor](modelos/gemelo-digital-del-motor/) | Gemelo digital · Motor eléctrico | Modelo físico en vivo vs. sensor real para detectar refrigeración/aislamiento degradados |

### Estáticos y energía (5)

| Demo | Categoría | Qué resuelve |
|---|---|---|
| [Pulso Energético](modelos/pulso-energetico/) | Series de tiempo · Energía | Proyecta consumo energético y detecta desvíos anómalos |
| [Rastreador de Correas](modelos/correas-transportadoras/) | Clasificación · Correas transportadoras | Clasifica el desvío lateral de una correa antes de que desgaste el borde |
| [Transformadores (DGA)](modelos/transformadores-dga/) | Clasificación · Transformadores | Clasifica el tipo de falla vía Triángulo de Duval (análisis de gases disueltos) |
| [Gemelo Térmico del Transformador](modelos/gemelo-termico-del-transformador/) | Gemelo digital · Transformadores | Modelo térmico IEEE C57.91 en vivo, estima envejecimiento del aislamiento |
| [Pulso de la Caldera](modelos/pulso-de-la-caldera/) | Series de tiempo · Calderas | Sigue la eficiencia térmica y detecta avance de incrustación |

### Planta y multi-sensor (3)

| Demo | Categoría | Qué resuelve |
|---|---|---|
| [Radiografía de Planta](modelos/radiografia-de-planta/) | Clustering · Planta | Reduce 10 sensores a un mapa visual de 2 ejes (PCA + k-means) |
| [Nubes de Sensores](modelos/nubes-de-sensores/) | Clustering · Sensores | Descubre grupos naturales en una nube de datos (DBSCAN) |
| [Mapa de Anomalías](modelos/mapa-de-anomalias/) | Anomalías · Sensores múltiples | Ubica lecturas anómalas entre varios sensores (Isolation Forest) |

### Termografía y nuevas técnicas (3)

| Demo | Categoría | Qué resuelve |
|---|---|---|
| [Oído Industrial](modelos/oido-industrial/) | Nuevas tecnologías · Aire comprimido | Traduce nivel ultrasónico en costo estimado de fuga |
| [Ojo Térmico](modelos/ojo-termico/) | Visión · Termografía | Clasifica imágenes térmicas por segmentación |
| [Huella del Aceite](modelos/huella-del-aceite/) | Nuevas tecnologías · Aceite | Clasifica el estado de un equipo según TAN y hierro disuelto |

Cada tarjeta del [hub principal](index.html) indica también su paradigma de aprendizaje (supervisado, no supervisado o basado en reglas) directamente en la página de la demo.

## Cómo verlo

**Sitio en vivo:** https://angel19968.github.io/reliabilit-ia/

Es un sitio estático, sin backend ni build step: también puedes clonar el repositorio y abrir `index.html` directamente en cualquier navegador.

## Contacto

¿Tienes datos de tus propios equipos y quieres ver cómo se vería esto calibrado con tu información?

- WhatsApp comunidad: https://chat.whatsapp.com/GvBz1tuUeNZ0xwTkjsuE3z
- WhatsApp directo (Miguel): https://wa.me/51997610310
- YouTube: https://www.youtube.com/@miguelangelcayllahuaquispe998
- LinkedIn empresa: https://www.linkedin.com/company/reliabilit-ia/
- LinkedIn personal: https://www.linkedin.com/in/miguelcayllahua/
- Correo: miguelcquispe@gmail.com

---

<details>
<summary><strong>Notas para quien mantiene este repositorio</strong> (estructura interna, checklist de publicación)</summary>

### Estructura

```
reliabilit-ia/
├── index.html                          ← Hub: catálogo de 24 modelos + CTA
├── modelos/                            ← 24 carpetas, una por demo, cada una autocontenida (HTML/CSS/JS sin dependencias)
├── confiabilidad-calculos/             ← 8 análisis de confiabilidad ("simples"), + gen_*.py y *_audit.json de reproducibilidad
├── confiabilidad-avanzada/             ← 8 análisis de confiabilidad (complejidad media), + gen_*.py y *_audit.json de reproducibilidad
├── panel-analitico/                    ← Panel BI, 15 tipos de gráfico SVG
├── assets/
│   ├── logo.svg
│   └── og-image.png
└── README.md
```

### Cómo publicar en GitHub Pages

1. Crear repo `tu-usuario.github.io` (o uno normal + activar Pages en Settings → Pages → branch `main` / carpeta `/`).
2. Subir el contenido de esta carpeta a la raíz del repo.
3. Activar GitHub Pages apuntando a `main` / `/root`.
4. Verificar que `index.html` cargue correctamente.

### Checklist antes de publicar una demo nueva

- [ ] Nombre comercial en título, carpeta y CTA (nunca el nombre interno del script `.py`)
- [ ] Máximo 2-4 sliders en Modo Básico
- [ ] Output traducido a lenguaje de negocio (nunca "predicción: 0.73")
- [ ] Modo Analista detrás de un toggle, no en pestaña separada
- [ ] Meta tags Open Graph (título, descripción, imagen)
- [ ] Probado en mobile (sliders usables con el dedo)
- [ ] Disclaimer de datos ilustrativos en el footer
- [ ] Datos 100% sintéticos, sin coincidencias con casos reales de clientes
- [ ] Badge de paradigma de aprendizaje agregado junto al badge de categoría
- [ ] Columna de fecha agregada a la tabla del dataset

Las 24 demos del roadmap de Nivel 1 (público) y los 16 análisis de confiabilidad de Nivel 2 están completos. El detalle de auditoría de cada análisis de confiabilidad vive en los `*_audit.json` de su propia carpeta (no hay un archivo de auditoría centralizado separado).

</details>
