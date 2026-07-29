# RELIABILIT-IA — Demos Públicas

**Modelos interactivos que anticipan fallas, no solo las registran.**

RELIABILIT-IA es un proyecto de mantenimiento predictivo aplicado. Este repositorio reúne 15 demos interactivas, cada una explicando —de forma visual y en el navegador, sin instalar nada— un algoritmo real de machine learning aplicado a un problema concreto de planta: vibración en rodamientos, temperatura de motores, fugas de aire comprimido, anomalías en compresores, agrupamiento de sensores, imágenes térmicas, y más.

Cada demo funciona en dos modos: un **Modo Básico**, pensado para cualquier persona (mueve un par de sliders y mira la predicción cambiar en vivo, traducida a decisiones de negocio, no a números sueltos), y un **Modo Analista**, pensado para quien quiera ver el modelo por dentro — el dataset, los hiperparámetros ajustables, y cómo cambian las métricas de ajuste (subajuste, sobreajuste, exactitud, matrices de confusión) según las decisiones que tomes.

## ¿Qué vas a encontrar en cada demo?

- Un problema de mantenimiento explicado en términos de planta, no de estadística.
- Un algoritmo real implementado desde cero (regresión, árboles de decisión, k-NN, SVM, PCA, k-means, clustering jerárquico, DBSCAN, redes neuronales, Isolation Forest, segmentación de imágenes, entre otros) — sin librerías de ML de por medio, para que el código sea legible de principio a fin.
- Un dataset sintético de ejemplo, generado con un generador de números aleatorios con semilla fija (reproducible), con fechas, hiperparámetros y umbrales validados externamente antes de mostrarse — no hay números inventados sobre la marcha.
- Una traducción de negocio: qué significa cada resultado para una planta real, y qué se pierde o gana al mover el umbral de decisión.

## Un aviso importante sobre los datos

**Todos los datos de este repositorio son sintéticos**, generados específicamente para poder compartir la metodología públicamente sin exponer información de ningún cliente. La metodología (los algoritmos, la forma de validar el ajuste, el enfoque de cada problema) es real y es la misma que usamos en proyectos reales — los números de cada dataset, no.

El modelo calibrado con datos reales de una planta —el que sí sirve para decidir cuándo intervenir un equipo real— vive en un entorno privado (Suite Predictiva PRO) y no se publica aquí. Si tienes datos de tus propios equipos y quieres explorar cómo se vería esto calibrado con tu información, hay contactos directos al final de este documento y en cada demo.

## Catálogo de las 15 demos

| Demo | Categoría | Qué resuelve |
|---|---|---|
| [Radar de Rodamientos](modelos/radar-de-rodamientos/) | Regresión | Estima días hasta falla según vibración RMS y temperatura |
| [Pulso Energético](modelos/pulso-energetico/) | Serie de tiempo | Proyecta consumo energético y detecta desvíos anómalos |
| [Diagnóstico del Motor](modelos/diagnostico-del-motor/) | Clasificación | Clasifica el estado de un motor en 5 niveles de severidad |
| [Pulso del Motor](modelos/pulso-del-motor/) | Clasificación | Diagnóstico por firma de corriente (MCSA) con pinza amperimétrica |
| [Oído Industrial](modelos/oido-industrial/) | Regresión | Traduce nivel ultrasónico en costo estimado de fuga de aire |
| [Detector de Anomalías del Compresor](modelos/detector-anomalias-compresor/) | No supervisado | Detecta lecturas fuera de patrón sin ejemplos previos de falla |
| [Radiografía de Planta](modelos/radiografia-de-planta/) | No supervisado | Reduce 10 sensores a un mapa visual de 2 ejes |
| [Semáforo de Bombas](modelos/semaforo-de-bombas/) | Clasificación | Clasifica una bomba centrífuga en verde, amarillo o rojo |
| [Guardián de la Bomba](modelos/guardian-de-la-bomba/) | No supervisado | Detecta comportamiento anómalo con muy pocos datos históricos |
| [Frontera de Vibración](modelos/frontera-de-vibracion/) | Clasificación | Separa 3 estados de vibración con un límite de decisión (SVM) |
| [Familias de Turbinas](modelos/familias-de-turbinas/) | No supervisado | Agrupa turbinas similares según su comportamiento operativo |
| [Nubes de Sensores](modelos/nubes-de-sensores/) | No supervisado | Descubre grupos naturales en una nube de datos de sensores (DBSCAN) |
| [Termómetro del Motor](modelos/termometro-del-motor/) | Regresión | Estima la temperatura de un motor eléctrico con una red neuronal |
| [Mapa de Anomalías](modelos/mapa-de-anomalias/) | No supervisado | Ubica lecturas fuera de patrón entre varios sensores (Isolation Forest) |
| [Ojo Térmico](modelos/ojo-termico/) | Visión por computadora | Detecta puntos calientes en imágenes térmicas por segmentación |

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
├── index.html                          ← Hub: catálogo de modelos + CTA
├── modelos/                            ← 15 carpetas, una por demo, cada una autocontenida (HTML/CSS/JS sin dependencias)
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

Las 15 demos del roadmap de Nivel 1 (público) están completas. Ver `ideas-fase-2.md` para propuestas de próximos módulos (semi-supervisado, por refuerzo, secuencial/LSTM) y `auditoria-graficas.md` para el estado de las visualizaciones de cada módulo.

</details>
