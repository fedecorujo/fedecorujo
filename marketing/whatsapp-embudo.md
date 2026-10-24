# WhatsApp como embudo

El 70-80 % de los contactos llega por WhatsApp. Ahí se gana o se pierde la cirugía. Regla: **primera respuesta < 15 min en horario hábil**, cada lead registrado en Notion → **Pipeline Cataratas**.

## Configuración WhatsApp Business (app gratuita, 30 min)
- **Perfil:** "Dr. Federico Corujo · Cirujano oftalmólogo". Descripción: "Cirugía de cataratas y facorrefractiva. Consultas en Montevideo, San José de Mayo y Libertad." Web + horario.
- **Catálogo:** 4 ítems sin precio (o con rango si se aprueba): Consulta oftalmológica · Evaluación de catarata · Cirugía de catarata · Cirugía facorrefractiva / LIO premium. Cada uno enlaza a su página.
- **Etiquetas:** `nuevo` · `consulta agendada` · `indicación quirúrgica` · `presupuesto enviado` · `cirugía agendada` · `operado` · `reseña pedida` · `perdido`.

## Mensaje de bienvenida
> Hola, gracias por escribir al consultorio del Dr. Federico Corujo, cirujano oftalmólogo. Para ayudarle más rápido, cuéntenos:
> 1️⃣ ¿La consulta es para usted o para un familiar?
> 2️⃣ ¿En qué ciudad prefiere atenderse? (Montevideo, San José de Mayo o Libertad)
> 3️⃣ ¿Ya le dijeron que tiene catarata o es una primera consulta?
> Le respondemos en minutos en horario de consultorio.
> _No envíe datos médicos sensibles por este medio._

## Mensaje de ausencia
> Gracias por escribir. Estamos fuera de horario; le respondemos mañana desde las [hora]. Mientras tanto puede leer cómo es la cirugía de cataratas: https://drcorujo.uy/cirugia-de-cataratas/

## Respuestas rápidas (`/atajo`)
- `/precio` → "El costo depende del tipo de lente intraocular y de los estudios necesarios. En la primera consulta el doctor evalúa su caso y le entregamos un presupuesto cerrado, sin compromiso. ¿Le reservo un turno?"
- `/mutualista` → "[Completar: con qué mutualistas/seguros se trabaja y cómo funciona el copago o la diferencia por lente premium]."
- `/turno` → "Tenemos disponibilidad en [sede] el [día] a las [hora] o el [día] a las [hora]. ¿Cuál le queda mejor?" (**siempre ofrecer 2 opciones concretas**, nunca "¿cuándo puede?").
- `/sanjose` `/libertad` `/montevideo` → dirección + mapa (enlace GBP) + cómo llegar.
- `/preparacion` → qué traer a la consulta (lentes actuales, estudios previos, lista de medicación, acompañante si se dilatan pupilas).
- `/miedo` → "Es muy común sentir nervios. La cirugía es ambulatoria, con anestesia local y dura entre 15 y 30 minutos. En la consulta el doctor le explica cada paso. Acá hay más información: https://drcorujo.uy/preguntas-frecuentes/"
- `/premium` → "Además del lente estándar existen lentes que corrigen astigmatismo o permiten ver de lejos y cerca. Cuál conviene depende de cada ojo; el doctor lo evalúa en consulta: https://drcorujo.uy/cirugia-facorrefractiva/"
- `/reseña` → texto del kit de GBP.

**Toda pregunta clínica** (síntomas, medicación, urgencias) → "Eso lo tiene que evaluar el doctor; le doy el primer turno disponible." Ojo rojo con dolor o pérdida brusca de visión → "Consulte en emergencia hoy mismo."

## Seguimiento (donde está la plata)
| Situación | Cuándo | Mensaje |
|---|---|---|
| Preguntó y no agendó | +24 h | "Hola [nombre], ¿pudo ver los horarios? Le guardo el turno del [día] hasta mañana." |
| Sigue sin agendar | +7 días | "Le escribo por última vez para no molestar: si más adelante quiere la consulta, este es el número. Que tenga buena semana." |
| Consulta hecha, con indicación, sin agendar cirugía | +3 días | "Hola [nombre], ¿le quedó alguna duda sobre la cirugía o el presupuesto? El doctor puede responderle en una llamada breve." |
| Ídem | +14 días | Llamada telefónica de la secretaria (no mensaje). |
| Operado | +7 días | Pedido de reseña. |
| Operado primer ojo | al alta del 1.º | Agendar segundo ojo antes de que se vaya. |

## Automatización
- **Hoy:** app + respuestas rápidas + etiquetas + Notion (la secretaria carga 1 línea por lead: 20 s).
- **Mes 3+ si > 100 leads/mes:** WhatsApp Cloud API + agente Claude que responde FAQ administrativas, ofrece turnos (Google Calendar) y deriva a humano todo lo clínico. Ver `docs/MARKETING-CATARATAS.md` §4.
