# Publicidad paga (encender recién en semana 4)

Prerrequisitos: páginas locales y facorrefractiva publicadas (`reviewed: true`), GBP verificado, WhatsApp con respuestas rápidas, campo "¿Cómo nos conoció?" en Notion. Sin esto, se paga por leads que se pierden.

Presupuesto inicial sugerido: **USD 400/mes** (Google 250 · Meta 150). Revisar a los 60 días con costo por cirugía, no por clic.

## Políticas que aplican
- Google Ads: categoría "Atención médica" — permitido para servicios médicos; no usar términos de condición personal en el anuncio ("¿Tiene usted catarata?") en remarketing. Sin remarketing de visitantes de páginas médicas.
- Meta: sin segmentación por condición de salud; no afirmar ni insinuar atributos personales ("¿Ves borroso?" → mejor "Cuando la catarata limita el día a día…").
- Deontología: ver `docs/MARKETING-CATARATAS.md` §6.

## Google Ads — Búsqueda
**Campaña 1 — Catarata local** (USD 5/día). Ubicación: San José (departamento) + Canelones oeste (Libertad no es Canelones: es San José; incluir Ciudad del Plata, Rodríguez, Santa Lucía, Las Piedras opcional). Idioma español. Horario: lun-sáb 8-20.
- Concordancia de frase: "cirugía de cataratas", "operación de cataratas", "oftalmólogo san josé", "oftalmólogo libertad", "operarse de cataratas", "cirujano de cataratas".
- Destino: `/cataratas-san-jose/` o `/cataratas-libertad/` según grupo.

**Campaña 2 — LIO premium / facorrefractiva** (USD 3/día). Ubicación: Montevideo + Canelones costa + San José.
- "lente intraocular multifocal", "lente multifocal catarata", "cirugía para dejar los lentes", "presbicia cirugía", "lente edof", "operación de vista cansada".
- Destino: `/cirugia-facorrefractiva/`.

**Negativas (ambas):** gratis, hospital de ojos, josé martí, mutualista nombre si no se trabaja con ella, láser lasik barato, cataratas del iguazú, iguazú, perro, gato, veterinario, curso, residencia, trabajo, sueldo, pdf, tesis.

**Anuncios (RSA) — títulos (≤ 30 caracteres):**
Cirugía de cataratas · Oftalmólogo en San José · Consultas en Libertad · Turno en menos de 7 días · Mismo cirujano de inicio a fin · Docente universitario · +10 años operando cataratas · Lentes multifocales y tóricos · Escríbanos por WhatsApp · Dr. Federico Corujo
**Descripciones (≤ 90):**
- Evaluación de catarata y planificación del lente intraocular. Consultas en San José y Libertad.
- Cirugía ambulatoria con anestesia local. Presupuesto cerrado tras la consulta.
- Planificación visual personalizada para depender menos de los lentes. Agende por WhatsApp.

**Extensiones:** llamada, ubicación (GBP), enlaces: Cómo es la cirugía · Recuperación · Preguntas frecuentes · Contacto.
**Conversión:** clic en WhatsApp/teléfono (GA4 evento `contact_whatsapp`, `contact_phone`) importado a Google Ads.

## Meta Ads (Facebook + Instagram)
**Público A — hijos/as decisores:** 38-58 años, San José + Canelones oeste + Montevideo oeste. Sin intereses de salud. Placement: Facebook feed + Reels.
- Creativo: video de 45-60 s del doctor: "¿Cuándo conviene operar la catarata de un padre o una madre?" CTA: Enviar mensaje (WhatsApp).
**Público B — premium:** 45-65, Montevideo + Costa de Oro + Punta del Este (ojo: campaña aparte), intereses amplios (viajes, golf, náutica, pádel, remo).
- Creativo: "Remo, náutica, pádel: qué cambia con un lente intraocular" (tu diferencial auténtico).
**Público C — remarketing:** solo interacciones con videos de la página (no visitantes web de páginas médicas).

Rotar creativos cada 3-4 semanas. Objetivo de campaña: Mensajes (WhatsApp).

## Lectura mensual (skill `reporte-captacion`)
Costo por conversación · conversación → consulta · consulta → cirugía · **costo por cirugía por canal**. Cortar lo que supere USD 150/cirugía a 60 días.
