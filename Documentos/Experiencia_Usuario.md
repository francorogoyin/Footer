# Footer - Diseño de Experiencia de Usuario

## Índice

1. [Flujo General](#flujo-general)
2. [Constructor de Búsqueda](#constructor-de-búsqueda)
3. [Sistema de Filtros](#sistema-de-filtros)
4. [Tipos de Resultado](#tipos-de-resultado)
5. [Visualización de Resultados](#visualización-de-resultados)
6. [Wireframes Conceptuales](#wireframes-conceptuales)

---

## Flujo General

### Arquitectura de la Búsqueda

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSTRUCTOR DE BÚSQUEDA                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ¿QUÉ BUSCO?          2. ¿CÓMO LO QUIERO?                   │
│  ┌─────────────────┐     ┌─────────────────┐                    │
│  │ ○ Partidos      │     │ ○ Lista         │                    │
│  │ ○ Goles         │     │ ○ Ranking       │                    │
│  │ ○ Jugadores     │     │ ○ Cantidad      │                    │
│  │ ○ Equipos       │     │ ○ Promedio      │                    │
│  │ ○ Técnicos      │     │ ○ Comparación   │                    │
│  │ ○ Árbitros      │     │ ○ Racha         │                    │
│  │ ...             │     │ ○ Primero/Último│                    │
│  └─────────────────┘     │ ○ Récord        │                    │
│                          └─────────────────┘                    │
│                                                                  │
│  3. FILTROS (dinámicos según selección)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  [+ Agregar filtro]                                      │   │
│  │                                                          │   │
│  │  Jugador: [Messi        ] [+] [NO ▼]                [x]  │   │
│  │  Jugador: [Di María     ] [+] [SÍ ▼]                [x]  │   │
│  │  Torneo:  [Copa Libertadores    ] [SÍ ▼]            [x]  │   │
│  │  Fecha:   [1990] - [2020]                           [x]  │   │
│  │  Tipo:    [✓] Gol de cabeza      [SÍ ▼]             [x]  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [BUSCAR]                                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Principios de UX

1. **Progresivo:** Primero qué busco, luego cómo lo quiero, luego
   filtros. No abrumar con todo de entrada.

2. **Filtros dinámicos:** Los filtros disponibles cambian según la
   entidad seleccionada. Si busco "Goles", aparecen filtros de tipo
   de gol. Si busco "Partidos", no.

3. **Feedback inmediato:** Mostrar contador estimado de resultados
   mientras se agregan filtros.

4. **Guardar búsquedas:** Permitir guardar búsquedas frecuentes.

5. **Compartir búsquedas:** URL única por búsqueda para compartir.

---

## Constructor de Búsqueda

### Paso 1: ¿Qué Busco? (Entidad Principal)

| Entidad    | Descripción                                  |
|------------|----------------------------------------------|
| Partidos   | Lista de partidos que cumplen criterios      |
| Goles      | Lista de goles individuales                  |
| Asistencias| Lista de asistencias                         |
| Jugadores  | Lista de jugadores                           |
| Equipos    | Lista de equipos                             |
| Selecciones| Lista de selecciones                         |
| Técnicos   | Lista de técnicos                            |
| Árbitros   | Lista de árbitros                            |
| Tarjetas   | Lista de tarjetas                            |
| Penales    | Lista de penales                             |

### Paso 2: ¿Cómo lo Quiero? (Tipo de Resultado)

| Tipo        | Descripción                               | Ejemplo                                |
|-------------|-------------------------------------------|----------------------------------------|
| Lista       | Todos los elementos que cumplen           | "Todos los goles de Messi en Champions"|
| Ranking     | Top N ordenado por métrica                | "Top 10 goleadores de Libertadores"    |
| Cantidad    | Conteo total                              | "Cuántos goles hizo Ronaldo de cabeza" |
| Promedio    | Media aritmética                          | "Promedio de goles por partido de X"   |
| Comparación | Dos entidades lado a lado                 | "Messi vs Ronaldo en goles de tiro libre"|
| Racha       | Secuencias consecutivas                   | "Mayor racha goleadora de Higuaín"     |
| Primero     | Primera ocurrencia                        | "Primer gol de Maradona"               |
| Último      | Última ocurrencia                         | "Último partido de Riquelme"           |
| Récord      | Máximo o mínimo histórico                 | "Partido con más goles en la historia" |

### Paso 3: Filtros

Ver sección [Sistema de Filtros](#sistema-de-filtros).

---

## Sistema de Filtros

### Filtros Universales (Aplican a Todas las Entidades)

| Filtro          | Tipo de Input      | Descripción                      |
|-----------------|--------------------|----------------------------------|
| Fecha           | Rango de fechas    | Desde - Hasta                    |
| Año             | Rango numérico     | Año inicio - Año fin             |
| Década          | Selección múltiple | 1980s, 1990s, 2000s...           |
| Mes             | Selección múltiple | Enero, Febrero...                |
| Día de semana   | Selección múltiple | Lunes, Martes...                 |
| Torneo          | Autocompletado     | Buscar y seleccionar             |
| Edición torneo  | Autocompletado     | Depende del torneo seleccionado  |
| Tipo torneo     | Selección múltiple | Liga, Copa, etc.                 |
| Nivel torneo    | Selección múltiple | Primera, Segunda división...     |
| Confederación   | Selección múltiple | CONMEBOL, UEFA...                |
| País            | Autocompletado     | Buscar y seleccionar             |

### Filtros de Partido

| Filtro              | Tipo de Input      | Descripción                    |
|---------------------|--------------------|--------------------------------|
| Equipo              | Autocompletado     | Cualquiera de los dos equipos  |
| Equipo local        | Autocompletado     | Solo el equipo local           |
| Equipo visitante    | Autocompletado     | Solo el equipo visitante       |
| Selección           | Autocompletado     | Para partidos de selecciones   |
| Estadio             | Autocompletado     | Estadio donde se jugó          |
| Árbitro             | Autocompletado     | Árbitro principal              |
| Técnico             | Autocompletado     | Técnico de cualquier equipo    |
| Fase                | Selección múltiple | Final, Semifinal, Grupos...    |
| Instancia           | Selección múltiple | Ida, Vuelta, Único             |
| Resultado           | Selección múltiple | Victoria local, Empate, etc.   |
| Cancha neutral      | Checkbox           | Sí / No                        |
| Con penales         | Checkbox           | Partidos que fueron a penales  |
| Con tiempo extra    | Checkbox           | Partidos con tiempo extra      |
| Rango de goles      | Rango numérico     | Total de goles en el partido   |
| Rango de público    | Rango numérico     | Asistencia de público          |

### Filtros de Jugador

| Filtro             | Tipo de Input      | Descripción                     |
|--------------------|--------------------|---------------------------------|
| Jugador            | Autocompletado     | Buscar jugador                  |
| País nacimiento    | Autocompletado     | Nacionalidad del jugador        |
| Posición           | Selección múltiple | Arquero, Defensor, etc.         |
| Pie hábil          | Selección múltiple | Derecho, Izquierdo, Ambidiestro |
| Edad               | Rango numérico     | Edad al momento del evento      |
| Altura             | Rango numérico     | En centímetros                  |
| Equipo del jugador | Autocompletado     | En qué equipo jugaba            |
| Titular/Suplente   | Selección          | Cómo inició el partido          |
| Es capitán         | Checkbox           | Si era capitán                  |
| Dorsal             | Rango numérico     | Número de camiseta              |

### Filtros de Gol

| Filtro          | Tipo de Input      | Descripción                     |
|-----------------|--------------------|---------------------------------|
| Jugador         | Autocompletado     | Quién hizo el gol               |
| Tipo de gol     | Selección múltiple | Jugada, Penal, Tiro libre...    |
| Parte del cuerpo| Selección múltiple | Cabeza, Pie derecho, etc.       |
| Zona            | Selección múltiple | Dentro del área, Fuera          |
| Es autogol      | Checkbox           | Goles en contra                 |
| Minuto          | Rango numérico     | Minuto del gol                  |
| En tiempo extra | Checkbox           | Si fue en tiempo extra          |
| Con asistencia  | Checkbox           | Si tuvo asistencia registrada   |
| Asistidor       | Autocompletado     | Quién dio la asistencia         |

### Filtros de Técnico

| Filtro           | Tipo de Input   | Descripción                      |
|------------------|-----------------|----------------------------------|
| Técnico          | Autocompletado  | Buscar técnico                   |
| País nacimiento  | Autocompletado  | Nacionalidad                     |
| Fue jugador      | Checkbox        | Si tiene carrera como jugador    |
| Equipo dirigido  | Autocompletado  | En qué equipo dirigía            |

### Filtros de Árbitro

| Filtro           | Tipo de Input   | Descripción                      |
|------------------|-----------------|----------------------------------|
| Árbitro          | Autocompletado  | Buscar árbitro                   |
| País             | Autocompletado  | Nacionalidad                     |
| Rol              | Selección       | Principal, Línea, Cuarto         |

### Filtros de Penal

| Filtro           | Tipo de Input      | Descripción                   |
|------------------|--------------------|-------------------------------|
| Jugador patea    | Autocompletado     | Quién lo pateó                |
| Arquero          | Autocompletado     | Quién lo atajó/recibió        |
| Tipo             | Selección          | En partido / En tanda         |
| Resultado        | Selección múltiple | Convertido, Atajado, etc.     |
| Minuto           | Rango numérico     | Si fue en partido             |

### Filtros de Tarjeta

| Filtro           | Tipo de Input      | Descripción                   |
|------------------|--------------------|-------------------------------|
| Jugador          | Autocompletado     | Quién la recibió              |
| Tipo             | Selección múltiple | Amarilla, Roja, Doble amarilla|
| Minuto           | Rango numérico     | Minuto de la tarjeta          |

---

## Tipos de Resultado

### Lista

**Muestra:** Tabla paginada con todas las coincidencias.

**Columnas dinámicas:** Según la entidad buscada.

**Ordenamiento:** Por fecha (default), por cualquier columna.

**Ejemplo de resultado - Lista de Goles:**

| Fecha       | Jugador     | Equipo | vs      | Torneo          | Min | Tipo    |
|-------------|-------------|--------|---------|-----------------|-----|---------|
| 15/06/2014  | Messi       | ARG    | BIH     | Mundial 2014    | 65' | Jugada  |
| 21/06/2014  | Messi       | ARG    | IRN     | Mundial 2014    | 91' | Jugada  |
| ...         | ...         | ...    | ...     | ...             | ... | ...     |

---

### Ranking

**Muestra:** Top N ordenado por métrica específica.

**Requiere:** Seleccionar métrica de ordenamiento (goles, partidos,
asistencias, etc.).

**Ejemplo - Top 5 Goleadores de Libertadores:**

| #  | Jugador        | Goles | Partidos | Promedio |
|----|----------------|-------|----------|----------|
| 1  | Alberto Spencer| 54    | 87       | 0.62     |
| 2  | Fernando Morena| 37    | 65       | 0.57     |
| 3  | Pedro Rocha    | 36    | 80       | 0.45     |
| 4  | Daniel Onega   | 31    | 53       | 0.58     |
| 5  | Luizão         | 29    | 48       | 0.60     |

---

### Cantidad

**Muestra:** Un número con contexto.

**Ejemplo:**

```
Goles de cabeza de Cristiano Ronaldo en Champions League

           ┌─────────┐
           │   23    │
           └─────────┘

   De un total de 140 goles (16.4%)
```

---

### Promedio

**Muestra:** Número con contexto y comparación.

**Ejemplo:**

```
Promedio de goles por partido de Lewandowski en Bundesliga

           ┌─────────┐
           │  0.89   │
           └─────────┘

   253 goles en 284 partidos

   Comparación con promedio de la liga: 0.31
```

---

### Comparación

**Muestra:** Dos entidades lado a lado.

**Ejemplo - Messi vs Ronaldo en goles de tiro libre:**

```
         MESSI                    RONALDO

          62         Tiros libres        61
          48         En liga             43
          14         En Champions         9
         0.08        Por partido       0.06
```

---

### Racha

**Muestra:** Secuencia consecutiva con detalles.

**Ejemplo - Mayor racha goleadora de Higuaín:**

```
Partidos consecutivos marcando gol: 11

┌────────────┬──────────────────┬────────┬───────┐
│ Fecha      │ Partido          │ Goles  │ Total │
├────────────┼──────────────────┼────────┼───────┤
│ 01/09/2013 │ Napoli vs X      │ 2      │ 2     │
│ 08/09/2013 │ Napoli vs Y      │ 1      │ 3     │
│ ...        │ ...              │ ...    │ ...   │
│ 15/12/2013 │ Napoli vs Z      │ 1      │ 15    │
└────────────┴──────────────────┴────────┴───────┘
```

---

### Primero / Último

**Muestra:** El evento específico con todo su contexto.

**Ejemplo - Primer gol de Maradona:**

```
PRIMER GOL DE DIEGO MARADONA

Fecha:    20 de octubre de 1976
Partido:  Argentinos Juniors 2 - 1 San Lorenzo
Torneo:   Metropolitano 1976
Estadio:  La Paternal
Minuto:   78'
Tipo:     Jugada
Edad:     15 años, 341 días

[Ver partido completo]
```

---

### Récord

**Muestra:** El máximo/mínimo con contexto histórico.

**Ejemplo - Partido con más goles en Copa Libertadores:**

```
RÉCORD: PARTIDO CON MÁS GOLES EN COPA LIBERTADORES

Peñarol 11 - 2 Valencia (VEN)
Fecha: 24 de marzo de 1970
Fase: Primera Ronda
Estadio: Centenario

Total de goles: 13

Goleadores:
- Fernando Morena (4)
- Pedro Rocha (3)
- ...
```

---

## Visualización de Resultados

### Advertencias de Datos

Cuando los datos están incompletos, mostrar advertencia:

```
⚠️ Advertencia: Los datos anteriores a 1960 pueden estar incompletos.
   Esta búsqueda incluye 23 partidos sin información de minutos.
```

### Exportación (Futuro)

- [ ] Exportar a CSV
- [ ] Exportar a PDF
- [ ] Compartir por URL

### Detalle de Elemento

Al hacer clic en cualquier elemento de la lista, expandir con más
información:

- **Partido:** Alineaciones, todos los eventos, árbitros, etc.
- **Jugador:** Carrera completa, estadísticas agregadas
- **Gol:** Contexto del partido, video si existe (futuro)

---

## Wireframes Conceptuales

### Pantalla Principal

```
┌─────────────────────────────────────────────────────────────────┐
│  FOOTER                                    [Usuario] [Salir]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ¿Qué querés buscar?                          │
│                                                                  │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐             │
│    │Partidos │ │  Goles  │ │Jugadores│ │ Equipos │  ...        │
│    └─────────┘ └─────────┘ └─────────┘ └─────────┘             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│                    Búsquedas recientes                          │
│                                                                  │
│    • Goles de Messi en Champions League                         │
│    • Top 10 goleadores de Libertadores                          │
│    • Partidos de River vs Boca en Monumental                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│                    Búsquedas guardadas                          │
│                                                                  │
│    ★ Mis estadísticas de Argentina                              │
│    ★ Goleadores históricos                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Constructor de Búsqueda

```
┌─────────────────────────────────────────────────────────────────┐
│  FOOTER                                    [Usuario] [Salir]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Buscar: [GOLES]                    Tipo: [RANKING     ▼]       │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ FILTROS ACTIVOS                                           │  │
│  │                                                           │  │
│  │ Torneo: Copa Libertadores                            [x]  │  │
│  │ Tipo de gol: Cabeza                                  [x]  │  │
│  │ Años: 2000 - 2023                                    [x]  │  │
│  │                                                           │  │
│  │ [+ Agregar filtro]                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Ordenar ranking por: [Cantidad de goles ▼]  Top: [10 ▼]        │
│                                                                  │
│  Resultados estimados: ~847 goles de 156 jugadores              │
│                                                                  │
│              [BUSCAR]        [Guardar búsqueda]                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Resultados

```
┌─────────────────────────────────────────────────────────────────┐
│  FOOTER                                    [Usuario] [Salir]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Top 10 goleadores de cabeza en Copa Libertadores (2000-2023)   │
│  [Modificar búsqueda]                        [Compartir] [★]    │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ #  │ Jugador          │ Goles │ Partidos │ % del total   │  │
│  ├────┼──────────────────┼───────┼──────────┼───────────────┤  │
│  │ 1  │ Luis Fabiano     │ 12    │ 45       │ 26.7%         │  │
│  │ 2  │ Gabigol          │ 10    │ 52       │ 19.2%         │  │
│  │ 3  │ Lucas Pratto     │ 9     │ 38       │ 23.7%         │  │
│  │ ...│ ...              │ ...   │ ...      │ ...           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ⚠️ Nota: 23 goles no tienen registrado el tipo. No se          │
│     incluyeron en esta búsqueda.                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mecánicas de Filtros Avanzados

### Filtros Múltiples del Mismo Tipo

Cada filtro tiene un botón **[+]** que permite agregar otro campo del
mismo tipo. Esto permite búsquedas como:

- "Partidos donde jugaron Messi Y Di María" (dos filtros Jugador)
- "Goles en Libertadores O Champions" (dos filtros Torneo)

```
┌──────────────────────────────────────────────────────────────┐
│  Jugador: [Messi        ] [+] [SÍ ▼]                    [x]  │
│  Jugador: [Di María     ] [+] [SÍ ▼]                    [x]  │
│  Jugador: [            ] [+]                            [x]  │
└──────────────────────────────────────────────────────────────┘
```

El **[+]** agrega un nuevo campo vacío debajo.

### Filtros Excluyentes (Negación)

Cada filtro tiene un selector **[SÍ/NO]** que permite negar la
condición:

- **SÍ:** Incluir elementos que cumplen el filtro
- **NO:** Excluir elementos que cumplen el filtro

Ejemplos:
- "Partidos donde jugó Messi pero NO Di María"
- "Goles que NO fueron de penal"
- "Partidos en estadios que NO sean el Monumental"

```
┌──────────────────────────────────────────────────────────────┐
│  Jugador: [Messi        ] [+] [SÍ ▼]                    [x]  │
│  Jugador: [Di María     ] [+] [NO ▼]                    [x]  │
└──────────────────────────────────────────────────────────────┘
```

Esta búsqueda devuelve: "Partidos donde jugó Messi pero no Di María".

### Tablas de Posiciones

Las tablas de posiciones se agregan como tipo de resultado adicional
en búsquedas de **Equipos** o **Selecciones**:

| Tipo             | Descripción                                |
|------------------|--------------------------------------------|
| Tabla Posiciones | Posiciones en una edición de torneo        |

**Requiere:** Seleccionar una edición de torneo específica.

**Muestra:** Tabla calculada con puntos, PJ, PG, PE, PP, GF, GC, DG.

```
TABLA DE POSICIONES - Apertura 2023

| Pos | Equipo        | PJ | PG | PE | PP | GF | GC | DG | Pts |
|-----|---------------|----|----|----|----|----|----|-----|-----|
| 1   | River Plate   | 14 | 10 | 3  | 1  | 28 | 10 | +18 | 33  |
| 2   | Boca Juniors  | 14 | 9  | 3  | 2  | 22 | 12 | +10 | 30  |
| ... | ...           | ...| ...| ...| ...| ...| ...| ... | ... |
```

---

## Interacciones Pendientes de Definir

- [ ] ¿Cómo funciona el autocompletado de jugadores con nombres
      similares?
- [ ] ¿Hay búsqueda por texto libre además de los filtros?
- [ ] ¿Operador AND/OR entre filtros del mismo tipo?
