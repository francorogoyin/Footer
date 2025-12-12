# FOOTER - Motor de Búsqueda de Estadísticas de Fútbol

## Descripción del Proyecto

Footer es una plataforma web por suscripción que ofrece un motor de
búsqueda avanzado para estadísticas de fútbol. Su diferenciador es la
profundidad y flexibilidad de los filtros, permitiendo consultas muy
específicas que no existen en ninguna otra plataforma.

**Usuario objetivo:** Periodistas deportivos, analistas, administradores
de cuentas de estadísticas en redes sociales y YouTube, y fanáticos de
los datos.

---

## Reglas de interacción con Claude.

### Actitud general.

Claude debe ser **proactivo** en todo momento:
- **Cuestionador:** Cuestionar decisiones de diseño si ve problemas.
- **Crítico:** Señalar inconsistencias, redundancias o malas prácticas.
- **Sugeridor:** Proponer alternativas y mejoras.
- **Preguntón:** Hacer muchas preguntas de clarificación y disparadores.
- **Consejero:** Advertir sobre consecuencias de decisiones técnicas.

### Principios de desarrollo.

1. **Escalabilidad primero:** El modelo de datos debe soportar nuevos
   tipos de torneos, ligas, y atributos sin modificar el esquema base.

2. **Datos fácticos únicamente:** Solo se almacenan datos objetivos y
   verificables. Nada subjetivo como "mejor jugador del partido".

3. **NULL es válido:** Los datos históricos incompletos se almacenan
   con campos NULL. El sistema debe funcionar con datos parciales.

4. **Cálculo sobre almacenamiento:** Las posiciones de tabla,
   estadísticas agregadas y rankings se calculan en tiempo de
   consulta, no se almacenan.

---

## Alcance del proyecto.

### Competiciones incluidas.

**Clubes:**
- 9 ligas sudamericanas (primeras divisiones).
- Argentina: hasta tercera o cuarta división.
- 3 ligas norteamericanas (México, USA, Canadá).
- ~15 ligas europeas principales.
- 5-6 ligas principales de África y Asia.
- Liga australiana.
- Segundas divisiones solo de países principales.
- Copas nacionales de todos los países incluidos.
- Competiciones continentales (Libertadores, Champions, etc.).
- Competiciones mundiales (Mundial de Clubes, Intercontinental, etc.).

**Selecciones:**
- Todas las competiciones oficiales (Mundiales, Copas continentales).
- Eliminatorias.
- Amistosos internacionales.

### Profundidad histórica.

Desde el comienzo de cada liga/competición, según disponibilidad de
datos. Los datos incompletos se almacenan igualmente.

### Estadísticas incluidas (MVP).

- Resultados de partidos.
- Goles (con tipo, parte del cuerpo, minuto, zona).
- Asistencias.
- Tarjetas (amarillas, rojas).
- Cambios.
- Penales (en partido y en tanda).
- Alineaciones (titulares y suplentes).
- Árbitros.
- Técnicos.
- Capitanes.
- Público asistente.
- Revisiones VAR.

### Estadísticas NO Incluidas (por ahora).

- Pases.
- Posesión.
- Tiros.
- Formaciones tácticas.
- Posición del jugador por partido.
- Datos de tracking (distancia, sprints).

---

## Tipos de consulta soportados.

### Por resultado.

1. **Lista:** "Todos los partidos/jugadores/goles que cumplan X".
2. **Ranking:** "Top N de algo ordenado por métrica".
3. **Cantidad:** "Cuántos X cumplen Y".
4. **Promedio:** "Promedio de X en contexto Y".
5. **Comparación:** "X vs Y en tal métrica".
6. **Racha:** "Partidos/goles consecutivos de X".
7. **Primero/Último:** "Primer/último X en contexto Y".
8. **Récords:** "Máximo/mínimo de X en contexto Y".

### Filtros innegociables.

- Jugador/es.
- Equipo/s (incluyendo ambos equipos del partido)
- Selección/es.
- Estadio/s.
- Técnico/s.
- Árbitro/s (principal, líneas, cuarto).
- Titulares y/o suplentes.
- Fecha (día, mes, año, década, día de la semana).
- Hora del partido.
- Torneo/s.
- Edición del torneo.
- Tipo de torneo (liga, copa, etc.).
- Fase/instancia (final, semifinal, fecha 1, grupos, etc.).
- Ida/vuelta.
- Tipo de gol (cabeza, pie, penal, tiro libre, olímpico, etc.).
- Zona del gol (dentro/fuera del área).
- Minuto del evento.
- Resultado del partido (victoria, empate, derrota).
- Condición (local, visitante, neutral).
- Penales (convertido, atajado, desviado).
- Público asistente.
- Atributos de jugador (país, pie hábil, edad al momento, etc.).
- Atributos de equipo (país, confederación).
- Dorsal/número de camiseta.

---

## Stack tecnológico.

- **Backend:** Python
- **Frontend:** Preferentemente Python (Reflex, NiceGUI, o similar).
  Alternativamente React.
- **Base de datos:** A definir (PostgreSQL recomendado por queries
  complejas).
- **Arquitectura:** Web responsive, con soporte futuro para móvil
  (tipo Todoist: sincronización multiplataforma).

---

## Estructura de documentos del proyecto.

```
Footer/
├── CLAUDE.md                    # Este archivo.
├── Documentos/
│   ├── Base_De_Datos.md         # Diseño completo de la BD.
│   ├── Experiencia_Usuario.md   # Diseño de UX y filtros.
│   └── Casos_De_Uso.md          # Consultas ejemplo que debe resolver.
└── (código fuente - a desarrollar)
```

---

## Reglas de código.

- Pascal_Snake_Case en todo.
- Nombres descriptivos en español.
- Líneas máximo 70 caracteres.
- Docstrings exhaustivos.
- Comentarios descriptivos con punto final.

---

## Notas de diseño importantes.

### Partidos entre equipos y selecciones.

Históricamente han existido partidos entre clubes y selecciones. El
modelo debe soportar esto aunque sean entidades separadas.

### Cambios históricos.

El sistema debe trackear:
- Cambios de nombre de equipos.
- Cambios de nombre de estadios.
- Cambios de estadio de equipos.
- Cambios de formato de torneos.

### Sistema de puntos.

Varía históricamente (2-1-0 vs 3-1-0) y por torneo. Se guarda en la
edición del torneo y se usa para calcular posiciones.

---

## Preguntas abiertas (A Resolver).

- [ ] ¿Qué otros sistemas de puntos existen además de 2-1-0 y 3-1-0?
- [ ] ¿Cómo manejar desempates por sorteo o tercer partido?
- [ ] ¿Incluir convocatorias de selecciones como entidad separada?
- [ ] Fuente de datos (se deja para el final).
