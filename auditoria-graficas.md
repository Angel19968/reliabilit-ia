# Auditoría de gráficas — 15 módulos RELIABILIT-IA

Revisé el canvas y la función de dibujo de cada gráfica en los 15 módulos. Cada módulo sigue el mismo patrón de 3-4 gráficas: **instrumento** (simulación en vivo), **chart** (mapa de decisión / dispersión / dendrograma), **segunda gráfica de calidad del modelo** (residuos, exactitud por clase, matriz de confusión o estabilidad), y **projection** (costo estimado por nivel). Esto es lo que encontré, de más a menos importante.

## 1. La gráfica de "costo estimado" está en los 15 módulos y no aporta análisis

Todos los módulos tienen un `<canvas id="projection">` con un gráfico de barras de 3 valores ("costo de intervención por nivel") — números fijos, ilustrativos, no calculados a partir de nada del modelo. Es la misma gráfica repetida 15 veces con distintas cifras hardcodeadas. Es la que menos aporta de todo el sitio: no cambia con los datos, no depende del modelo entrenado, y no enseña nada sobre cómo funciona el algoritmo — es puramente decorativa/narrativa de negocio.

**Propuesta:** en vez de eliminarla (cumple un rol de "traducir a negocio"), la volvería dinámica y la ligaría al modelo real. Por ejemplo: que la altura de la barra o el costo mostrado dependa de la confianza/margen/distancia real que calculó el modelo para la lectura actual (ya tienen ese número calculado en cada módulo — score, margen, distancia de Mahalanobis, etc.), no solo de a qué nivel cayó. Así deja de ser una ilustración fija y pasa a reflejar el cálculo real cada vez que mueves los sliders.

## 2. Dos módulos no tienen segunda gráfica de calidad del modelo — inconsistente con el resto

Los otros 13 módulos tienen una gráfica adicional que muestra qué tan bien generaliza el modelo (residuos, exactitud por clase, matriz de confusión, estabilidad por bootstrap, pureza train/test). Dos no la tienen:

- **nubes-de-sensores** (DBSCAN): solo tiene el mapa de clusters. No hay gráfica de cómo cambian el número de clusters, el ruido detectado o la pureza según `eps`/`minPts`.
- **ojo-termico** (visión basada en reglas): solo tiene la imagen térmica. El umbral ΔT es ajustable y la tabla de 10 casos históricos se recalcula, pero no hay gráfica de cómo se mueven los falsos positivos vs. las detecciones perdidas según el umbral.

**Propuesta:**
- nubes-de-sensores: agregar una gráfica de barras/líneas de "clusters detectados" y "% ruido" en función de eps, para que se vea visualmente el trade-off al mover el slider (ahora mismo ese trade-off solo se explica en texto).
- ojo-termico: agregar una curva de "detecciones correctas vs. falsas alarmas" en función del umbral ΔT sobre los 10 casos históricos — es el gráfico ROC-simplificado que le falta al módulo y que ya tiene todos los datos para construir sin generar nada nuevo.

## 3. Tres módulos de clasificación usan barras de exactitud por clase — podrían ser matriz de confusión completa

**diagnostico-del-motor**, **pulso-del-motor** y **semaforo-de-bombas** muestran exactitud por clase como barras separadas (train vs. test). Es correcto pero limitado: no muestra *con qué clase se confunde* cada error. **frontera-de-vibracion** ya implementa una matriz de confusión completa para el mismo tipo de problema (3 clases) — sería fácil y consistente extender ese mismo componente a los otros tres, y es más informativo: en vez de solo "cuánto acierta la clase Alerta", muestra si sus errores caen hacia Estable o hacia Crítico, que es justamente la distinción que le importa a un analista de mantenimiento.

**Propuesta:** reemplazar las barras de exactitud por clase por la misma matriz de confusión N×N que ya funciona en frontera-de-vibracion, en los tres módulos mencionados.

## 4. Gráficas que ya están bien y no tocaría

- Los residuos de regresión (radar-de-rodamientos, oido-industrial, pulso-energetico, termometro-del-motor) son apropiados y ya cambian con el grado/hiperparámetro elegido.
- Las barras de estabilidad por bootstrap (guardian-de-la-bomba, mapa-de-anomalias) son un tipo de gráfica poco común en demos así — las dejaría igual, aportan bien la idea de "qué tan confiable es el resultado con pocos datos".
- El dendrograma (familias-de-turbinas) y el mapa de decisión con regiones coloreadas (varios módulos) cumplen su función.

## Resumen de lo propuesto (sin implementar aún)

1. Volver dinámica la gráfica de costo/projection en los 15 módulos, ligándola al score/margen real del modelo.
2. Agregar gráfica de calidad de modelo a nubes-de-sensores (clusters/ruido vs. eps) y a ojo-termico (detecciones vs. falsas alarmas según umbral).
3. Reemplazar barras de exactitud por clase por matriz de confusión en diagnostico-del-motor, pulso-del-motor y semaforo-de-bombas.

Quedo pendiente de tu visto bueno antes de tocar código — dime si avanzamos con las tres, con alguna en particular, o si prefieres otro orden de prioridad.
