# Google Business Profile — 3 fichas + sistema de reseñas

Una ficha **por sede donde atendés con horario fijo**. NAP idéntico a `site/config.json` (mismo formato de teléfono, misma escritura de calle).

## Configuración común
- **Nombre:** `Dr. Federico Corujo - Oftalmólogo` (Google permite nombre del profesional + especialidad; no agregar palabras clave extra: causa suspensión).
- **Categoría principal:** Oftalmólogo. **Secundarias:** Cirujano oftalmológico, Clínica oftalmológica (solo si aplica a esa sede).
- **Web:** `https://drcorujo.uy/?utm_source=google&utm_medium=organic&utm_campaign=gbp-<sede>` (para medir en GA4 qué ficha trae tráfico).
- **Botón de reserva / WhatsApp:** enlace `https://wa.me/59898656789?text=Hola,%20quiero%20una%20consulta%20en%20<sede>`.
- **Fotos (10 mínimo):** fachada, sala de espera, consultorio, equipo, el doctor (retrato + en consulta), logo. Nada de pacientes identificables.
- **Servicios:** Cirugía de cataratas · Lentes intraoculares multifocales/EDOF/tóricos · Cirugía facorrefractiva · Control de catarata · Consulta oftalmológica · Segunda opinión quirúrgica.

## Descripción (750 caracteres; adaptar ciudad)
> El Dr. Federico Corujo es cirujano oftalmólogo especializado en cirugía de cataratas y cirugía facorrefractiva con lentes intraoculares monofocales, tóricos y multifocales. Egresado de la Universidad de la República, con formación en cirugía de segmento anterior en Argentina y docente de oftalmología en la Universidad CLAEH. Atiende consultas en [San José de Mayo / Libertad / Montevideo]: evaluación de catarata, estudios prequirúrgicos, planificación del lente intraocular y controles posoperatorios. El mismo cirujano acompaña al paciente desde la primera consulta hasta el alta. Consultas y turnos por WhatsApp.

## Preguntas y respuestas (cargar desde la cuenta propia)
1. ¿Atienden en San José de Mayo? → Sí, consultas [días]. Las cirugías se realizan en [institución].
2. ¿Trabajan con mutualistas? → [completar].
3. ¿Cuánto cuesta la cirugía de cataratas? → Depende del lente intraocular y de los estudios; se informa un presupuesto cerrado tras la consulta. [Si se aprueba: rango orientativo.]
4. ¿Cuánto demora el turno? → Habitualmente menos de 7 días.
5. ¿Necesito acompañante? → Para la cirugía sí; para la consulta se recomienda si se dilatan pupilas.

## Publicaciones (1 por semana, se reutiliza el contenido de redes)
Usar el calendario de Notion; mismo texto corto + imagen + botón "Más información".

## Sistema de reseñas (meta: 20 por sede en 90 días)
**Cuándo:** control posoperatorio de 1 semana (paciente ya ve mejor). **Nunca** el día de la cirugía.
**Cómo:**
1. Tarjeta con QR al enlace de reseña (GBP → "Pedir reseñas") en el escritorio de cada sede.
2. Mismo día, WhatsApp desde la secretaría:
> Hola [nombre], gracias por confiar en el Dr. Corujo. Si tiene un minuto, su opinión en Google ayuda a otras personas a informarse: [enlace]. Si algo no estuvo bien, respóndanos por acá y lo vemos personalmente.
3. Recordatorio único a los 7 días si no dejó. No más.
4. Etiqueta en WhatsApp Business: `reseña pedida` / `reseña dejada`. Campo en Notion.

**Reglas:** pedir a **todos** (Google prohíbe la selección), sin incentivos, no redactar la reseña por el paciente, no pedir desde el wifi del consultorio en bloque (filtro antispam).

**Responder** todas en < 72 h con la skill `responder-resena` (sin confirmar que la persona es paciente ni datos clínicos).
