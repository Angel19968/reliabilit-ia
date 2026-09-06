# Laboratorio interactivo de `reliability`

Recurso educativo en español para técnicos de mantenimiento, ingenieros de confiabilidad y responsables de mantenimiento.

- `index.html`: aplicación autocontenida que funciona en línea o sin conexión.
- `ejemplos-reliabilit-ia.py`: colección de los ejemplos utilizados para generar los escenarios del atlas.

Los datos y parámetros son sintéticos. Las recomendaciones explican supuestos y límites; no sustituyen la validación con datos, condiciones operativas y criterios de seguridad de cada planta.

Para ejecutar los ejemplos:

```bash
pip install reliability==0.9.0 pandas==2.2.3 sympy
python ejemplos-reliabilit-ia.py --list
python ejemplos-reliabilit-ia.py dist-Weibull_Distribution --scenario 0
```

Documentación de referencia: <https://reliability.readthedocs.io/en/latest/>
