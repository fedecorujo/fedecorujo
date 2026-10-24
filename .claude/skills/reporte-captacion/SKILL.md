---
name: reporte-captacion
description: Reporte mensual de captación de cirugías del Dr. Corujo. Lee el pipeline y derivadores en Notion, el último CSV de geo-monitor y exports de Search Console/Ads si se adjuntan, y devuelve una página con decisiones. Usar cuando pidan "reporte", "cómo venimos", "métricas del mes".
---

# Reporte de captación (1 página)

1. Fuente del pipeline: si existe `privado/pacientes/` y `privado/derivadores/` (vault de Obsidian, solo en la máquina local), leer el front matter de esas notas; si no, Notion → "Pipeline Cataratas" y "Red de derivadores". Nunca copiar datos de pacientes a archivos versionados.
2. Calcular para el mes y vs. mes anterior: leads, tasa lead→consulta, consulta→cirugía, cirugías por fuente ("¿Cómo nos conoció?"), % LIO premium, tiempo de primera respuesta si está cargado, leads perdidos y motivo, reseñas pedidas/dejadas, derivadores activos.
3. `geo-monitor/results/` último CSV: menciones de marca y preguntas genéricas citadas.
4. Si hay export de Ads: costo por conversación y **costo por cirugía por canal**.
5. Salida: tabla de KPIs vs. metas de `docs/MARKETING-CATARATAS.md` §7, 3 hallazgos, **máximo 3 decisiones** (escalar / cortar / corregir), y 1 tarea para el doctor (≤ 30 min). Sin relleno.
