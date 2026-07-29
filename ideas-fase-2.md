# Ideas para la Fase 2 — RELIABILIT-IA

Con los 15 módulos actuales ya cubrimos aprendizaje supervisado (regresión y clasificación), no supervisado (clustering, detección de anomalías, reducción de dimensionalidad) y un módulo de visión por reglas. Quedan tres paradigmas que mencionaste y que hoy no están representados: semi-supervisado, por refuerzo, y series de tiempo con memoria real (tipo LSTM). Van tres propuestas concretas, una por paradigma, más la incorporación de un dataset público real.

## 1. Módulo semi-supervisado — "Etiquetas Escasas"

El problema real: en la mayoría de plantas, solo una fracción pequeña de las lecturas históricas tiene una etiqueta confiable (alguien inspeccionó el equipo y confirmó si había falla o no). El resto son lecturas sin revisar. Un modelo puramente supervisado ignora todo ese historial no etiquetado; uno semi-supervisado lo aprovecha.

Propuesta técnica: self-training (pseudo-etiquetado) sobre un clasificador simple (por ejemplo, el mismo softmax de Semáforo de Bombas). Se entrena primero solo con el 10-15% de datos etiquetados, se predicen etiquetas para el resto con un umbral de confianza, se agregan al set de entrenamiento las predicciones más confiables, y se reentrena iterativamente. El demo mostraría, en vivo, cómo la frontera de decisión mejora a medida que se incorporan pseudo-etiquetas, y —siendo honestos— también el riesgo real de esta técnica: si el modelo inicial se equivoca con confianza, esos errores se refuerzan en las siguientes iteraciones. Esa es precisamente la lección que vale la pena mostrar.

## 2. Módulo por refuerzo — "Agenda de Mantenimiento"

El problema real: decidir CUÁNDO intervenir un equipo no es una clasificación de un solo punto en el tiempo, es una secuencia de decisiones (inspeccionar ahora vs. esperar) donde cada decisión tiene un costo y afecta el estado futuro del equipo.

Propuesta técnica: Q-learning tabular sobre un MDP simple: estado = nivel de desgaste discretizado (por ejemplo 5-10 buckets), acciones = {esperar, inspeccionar, reparar}, recompensa = -costo de la acción tomada, menos una penalización grande si el equipo falla por no haber actuado a tiempo. El demo dejaría ver la tabla Q entrenándose en vivo (miles de episodios simulados con el desgaste avanzando estocásticamente), y compararía la política aprendida contra una política ingenua de mantenimiento por calendario fijo, mostrando el ahorro esperado. Es el paradigma más distinto a lo que ya existe en el sitio, así que conviene dedicarle tiempo extra a explicar bien el MDP antes de mostrar código.

## 3. Módulo secuencial con memoria — "Memoria del Motor" (RNN/LSTM simplificada)

Esto responde directamente a tu comentario de que las líneas de tiempo actuales no se comportan "como si fueran LSTM": ahora mismo ningún módulo tiene memoria temporal real — cada predicción depende solo de la lectura actual (o de un promedio simple, como en Pulso Energético), no de la secuencia completa de lecturas pasadas.

Propuesta técnica: una RNN pequeña (o una LSTM simplificada de una sola capa) implementada desde cero en JS, entrenada con backpropagation through time sobre secuencias sintéticas de degradación (por ejemplo, la misma familia de curvas de vida útil que ya usamos en Radar de Rodamientos, pero como secuencia completa en vez de un solo punto). El valor de mostrar esto explícitamente: comparar la predicción de la RNN contra un modelo sin memoria (como el ya existente) sobre la misma secuencia, para que se vea con claridad qué gana un modelo con memoria temporal cuando el patrón de falla depende de la trayectoria y no solo del valor actual (por ejemplo, una subida rápida reciente es más preocupante que la misma vibración alcanzada gradualmente).

## 4. Dataset público real (ya conversado, incluido aquí para que quede junto al resto del plan)

Una vez cerrada la ronda de fechas sintéticas actual, el candidato más natural sigue siendo NASA C-MAPSS (motores turbofan, run-to-failure, ampliamente usado en benchmarks de mantenimiento predictivo) para un módulo de regresión de vida útil remanente (RUL), o AI4I 2020 (Kaggle/UCI) para un módulo de clasificación de fallas con variables tabulares reales. Cualquiera de los dos encajaría bien como "módulo bonus" que muestre el mismo algoritmo ya construido en algún módulo existente, pero corriendo sobre datos reales en vez de sintéticos — es una forma barata de ganar credibilidad sin construir un módulo nuevo desde cero.

## Orden sugerido

Si tuviera que priorizar, empezaría por el módulo secuencial (RNN/LSTM) porque responde directo a tu observación y es el que más se nota que falta; seguiría con semi-supervisado porque reutiliza mucho del código de clasificación ya existente; dejaría refuerzo al final porque es conceptualmente el más distinto y el que más tiempo de explicación necesita para que no quede como una caja negra.

Ninguno de estos módulos está implementado todavía — es una propuesta para decidir juntos qué construir primero.
