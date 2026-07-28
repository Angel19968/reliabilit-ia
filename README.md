# RELIABILIT-IA — Demos Públicas

Hub de modelos interactivos de mantenimiento predictivo (Nivel 1 — Público). Cada carpeta bajo `modelos/` es una página HTML/JS independiente y autocontenida, pensada para GitHub Pages.

**Importante:** este repo solo contiene demos educativas con coeficientes de ejemplo y datos sintéticos. El código de entrenamiento real (`.py`) y los modelos calibrados con datos de cliente **nunca se suben aquí** — viven en el entorno privado, ver Suite Predictiva PRO.

## Estructura

```
reliabilit-ia/
├── index.html                          ← Hub: catálogo de modelos + CTA
├── modelos/
│   ├── radar-de-rodamientos/index.html ← Demo 1 (Reg. Polinomial, rodamientos)
│   └── pulso-energetico/index.html     ← Demo 2 (Serie de tiempo, energía)
├── assets/
│   ├── logo.svg
│   └── og-image.png                    ← (pendiente) imagen para previews al compartir
└── README.md
```

## Cómo publicar en GitHub Pages

1. Crear repo `tu-usuario.github.io` (o uno normal + activar Pages en Settings → Pages → branch `main` / carpeta `/`).
2. Subir el contenido de esta carpeta a la raíz del repo.
3. Activar GitHub Pages apuntando a `main` / `/root`.
4. Verificar que `index.html` cargue en `https://tu-usuario.github.io/`.

## Contacto y redes (ya cargados en el hub y en cada demo)

- WhatsApp comunidad: https://chat.whatsapp.com/GvBz1tuUeNZ0xwTkjsuE3z
- WhatsApp directo (Miguel): https://wa.me/51997610310
- YouTube: https://www.youtube.com/@miguelangelcayllahuaquispe998
- LinkedIn empresa: https://www.linkedin.com/company/reliabilit-ia/
- LinkedIn personal: https://www.linkedin.com/in/miguelcayllahua/
- Correo: miguelcquispe@gmail.com

Al agregar una demo nueva, copiar el mismo bloque de CTA + tarjeta de contacto (`.contact-card`) del archivo `modelos/radar-de-rodamientos/index.html`, solo cambiando el texto prellenado del WhatsApp directo para que mencione el modelo específico.

## Siguiente demo a construir

Según el roadmap: **Diagnóstico del Motor** (Clf_RandomForest) → carpeta `modelos/diagnostico-del-motor/index.html`, misma plantilla de 6 secciones y misma paleta.

## Checklist antes de publicar cada demo nueva

- [ ] Nombre comercial en título, carpeta y CTA (nunca el nombre interno del script `.py`)
- [ ] Máximo 2-4 sliders en Modo Básico
- [ ] Output traducido a lenguaje de negocio (nunca "predicción: 0.73")
- [ ] Modo Analista detrás de un toggle, no en pestaña separada
- [ ] Meta tags Open Graph (título, descripción, imagen)
- [ ] Probado en mobile (sliders usables con el dedo)
- [ ] Disclaimer de datos ilustrativos en el footer
- [ ] Datos 100% sintéticos, sin coincidencias con casos reales de clientes
