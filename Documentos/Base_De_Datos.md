# Footer - Diseño de Base de Datos

## Índice

1. [Filosofía de Diseño](#filosofía-de-diseño)
2. [Tablas de Referencia (Catálogos)](#tablas-de-referencia-catálogos)
3. [Tablas de Entidades Principales](#tablas-de-entidades-principales)
4. [Tablas de Configuración de Torneos](#tablas-de-configuración-de-torneos)
5. [Tablas de Partidos y Eventos](#tablas-de-partidos-y-eventos)
6. [Tablas de Relaciones Históricas](#tablas-de-relaciones-históricas)
7. [Consideraciones Técnicas](#consideraciones-técnicas)

---

## Filosofía de Diseño

### Principios

1. **Flexibilidad sobre rigidez:** Usar tablas de configuración en
   lugar de atributos fijos cuando el dominio puede cambiar.

2. **Normalización:** Evitar redundancia. Cada dato vive en un solo
   lugar.

3. **NULL es información:** Un campo NULL significa "dato no
   disponible", no "no aplica". Si no aplica, no debería existir la
   relación.

4. **IDs universales:** Todas las tablas tienen ID autoincremental
   como clave primaria.

5. **Soft deletes:** No se borra nada. Se marca como inactivo si es
   necesario.

6. **Auditoría:** Campos de fecha de creación y modificación en
   tablas principales.

### Nomenclatura

- Tablas: `Pascal_Snake_Case` en singular (`Jugador`, `Partido`).
- Campos: `Pascal_Snake_Case` (`Fecha_Nacimiento`, `Id_Equipo`).
- Foreign Keys: `Id_` + nombre de la tabla referenciada.
- Tablas de relación N:M: `Entidad1_Entidad2` (ej: `Equipo_Estadio`).

---

## Tablas de Referencia (Catálogos).

### Confederacion
- Id: Identificador único. PK.
- Nombre: Nombre completo. "CONMEBOL".
- Abreviatura: Código corto. "CSF".

Datos: CONMEBOL, UEFA, CONCACAF, CAF, AFC, OFC.

---

### Pais
- Id: Identificador único. PK.
- Nombre: Nombre del país. "Argentina".
- Codigo_ISO: Código ISO 3166-1 alfa-3. "ARG".
- Id_Confederacion: FK a Confederacion.

---

### Ciudad
- Id: Identificador único. PK.
- Nombre: Nombre de la ciudad. "Buenos Aires".
- Id_Pais: FK a Pais.

---

### Estadio
- Id: Identificador único. PK.
- Id_Ciudad: FK a Ciudad.
- Capacidad: Capacidad actual (puede cambiar). 70000.

Nota: El nombre va en Nombre_Estadio porque puede cambiar.

---
### Nombre_Estadio
- Id: Identificador único. PK.
- Id_Estadio: FK a Estadio.
- Nombre: Nombre en este período. "Estadio Monumental".
- Anio_Inicio: Año desde que tiene este nombre. 1938.
- Anio_Fin: Año hasta (NULL = actual). NULL.

---

### Parte_Cuerpo
- Id: Identificador único. PK.
- Nombre: Parte del cuerpo. "Cabeza".

Datos: Cabeza, Pie Derecho, Pie Izquierdo, Otro, Desconocido.

---

### Zona_Gol
- Id: Identificador único. PK.
- Nombre: Desde dónde se ejecutó. "Dentro del Área".

Datos: Dentro del Área, Fuera del Área.

---

### Tipo_Gol
- Id: Identificador único. PK.
- Nombre: Cómo se originó. "Penal".

Datos: Jugada, Penal, Tiro Libre Directo, Olímpico, En Contra.

---

### Tipo_Tarjeta
- Id: Identificador único. PK.
- Nombre: Tipo de tarjeta. "Amarilla".

Datos: Amarilla, Roja, Doble Amarilla.

---

### Tipo_Penal
- Id: Identificador único. PK.
- Nombre: Contexto del penal. "En Partido".

Datos: En Partido, En Tanda.

---

### Resultado_Penal
- Id: Identificador único. PK.
- Nombre: Resultado del penal. "Convertido".

Datos: Convertido, Atajado, Desviado, Poste.

---

### Tipo_Revision_VAR
- Id: Identificador único. PK.
- Nombre: Motivo de revisión. "Gol".

Datos: Gol, Penal, Tarjeta Roja, Identidad.

---

### Resultado_Revision_VAR
- Id: Identificador único. PK.
- Nombre: Resultado de la revisión. "Confirmado".

Datos: Confirmado, Revertido, Sin Decisión.

---

### Posicion_Jugador
- Id: Identificador único. PK.
- Nombre: Posición natural. "Arquero".
- Abreviatura: Código corto. "ARQ".

Datos: Arquero, Defensor, Mediocampista, Delantero.

---

### Pie_Habil
- Id: Identificador único. PK.
- Nombre: Pie hábil. "Derecho".

Datos: Derecho, Izquierdo, Ambidiestro.

---

### Tipo_Fase
- Id: Identificador único. PK.
- Nombre: Tipo de fase. "Semifinal".
- Orden: Para ordenar cronológicamente. 4.

Datos: Fase de Grupos, Octavos de Final, Cuartos de Final,
Semifinal, Tercer Puesto, Final, Fecha Regular, Repechaje,
Play-off, Zona, Cruce Interzonal, Liguilla.

---

### Tipo_Instancia
- Id: Identificador único. PK.
- Nombre: Tipo de instancia para eliminatorias. "Ida".

Datos: Ida, Vuelta, Desempate, Único.

Nota: Solo para eliminatorias. Las ligas usan Numero_Fecha en Partido.

---

### Estado_Partido
- Id: Identificador único. PK.
- Nombre: Estado del partido. "Finalizado".

Datos: Finalizado, Suspendido, Anulado, Walkover, Reprogramado.

Nota: Anulado = se jugó pero se anuló (River-Boca 2015).
Walkover = ganador por incomparecencia. Suspendido = no terminó.

---

## Tablas de Entidades principales.

### Equipo
- Id: Identificador único. PK.
- Id_Pais: FK a Pais.
- Id_Ciudad: FK a Ciudad. NULL si desconocido.
- Fecha_Fundacion: Fecha de fundación. 1905-04-01.
- Activo: Si el equipo sigue existiendo. true.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

---

### Nombre_Equipo
- Id: Identificador único. PK.
- Id_Equipo: FK a Equipo.
- Nombre: Nombre en este período. "River Plate".
- Anio_Inicio: Año desde que tiene este nombre. 1905.
- Anio_Fin: Año hasta (NULL = actual). NULL.

---

### Seleccion
- Id: Identificador único. PK.
- Id_Pais: FK a Pais. El país que representa.
- Id_Confederacion: FK a Confederacion. Redundante pero útil.
- Activo: Si sigue existiendo. true.

Nota: El nombre se toma del país. Casos especiales como
"Alemania Occidental" se manejan aparte.

---

### Equipo_Estadio
- Id: Identificador único. PK.
- Id_Equipo: FK a Equipo.
- Id_Estadio: FK a Estadio.
- Anio_Inicio: Desde cuándo juega ahí. 1938.
- Anio_Fin: Hasta cuándo (NULL = actual). NULL.
- Es_Principal: Si es el estadio principal. true.

---

### Jugador
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Lionel Andrés Messi Cuccittini".
- Nombre_Conocido: Nombre público. "Lionel Messi".
- Fecha_Nacimiento: Fecha de nacimiento. 1987-06-24.
- Id_Pais_Nacimiento: FK a Pais. Donde nació.
- Id_Posicion: FK a Posicion_Jugador. Posición natural.
- Id_Pie_Habil: FK a Pie_Habil.
- Altura_Cm: Altura en centímetros. 170.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

Nota: Nacionalidades múltiples en Jugador_Nacionalidad.

---

### Jugador_Nacionalidad
- Id: Identificador único. PK.
- Id_Jugador: FK a Jugador.
- Id_Pais: FK a Pais. País de la nacionalidad.
- Es_Principal: Si es la nacionalidad principal. true.

Nota: Di María puede tener argentina y española. La principal
es con la que jugó en selecciones.

---

### Contrato_Jugador
- Id: Identificador único. PK.
- Id_Jugador: FK a Jugador.
- Id_Equipo: FK a Equipo.
- Fecha_Inicio: Inicio del contrato. 2004-07-01.
- Fecha_Fin: Fin del contrato (NULL = actual). NULL.
- Monto_Fichaje: Monto de transferencia. 35000000.
- Moneda: Moneda del monto. "EUR".

---

### Tecnico
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Marcelo Alberto Bielsa Caldera".
- Nombre_Conocido: Nombre público. "Marcelo Bielsa".
- Fecha_Nacimiento: Fecha de nacimiento. 1955-07-21.
- Id_Pais_Nacimiento: FK a Pais.
- Id_Jugador: FK a Jugador. Si fue jugador, referencia.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

---

### Contrato_Tecnico
- Id: Identificador único. PK.
- Id_Tecnico: FK a Tecnico.
- Id_Equipo: FK a Equipo. NULL si es selección.
- Id_Seleccion: FK a Seleccion. NULL si es equipo.
- Fecha_Inicio: Inicio del contrato. 2018-08-01.
- Fecha_Fin: Fin del contrato (NULL = actual). NULL.

Restricción: Exactamente uno de Id_Equipo o Id_Seleccion NOT NULL.

---

### Arbitro
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Néstor Fabián Pitana".
- Fecha_Nacimiento: Fecha de nacimiento. 1975-06-17.
- Id_Pais: FK a Pais.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.

---

### Rol_Cuerpo_Tecnico
- Id: Identificador único. PK.
- Nombre: Nombre del rol. "Ayudante de Campo".

Datos: Ayudante de Campo, Preparador Físico, Entrenador de Arqueros,
Analista de Video, Médico, Kinesiólogo.

---

### Miembro_Cuerpo_Tecnico
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Pablo Aimar".
- Fecha_Nacimiento: Fecha de nacimiento.
- Id_Pais: FK a Pais.
- Id_Jugador: FK a Jugador. Si fue jugador, referencia.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.

---

### Contrato_Cuerpo_Tecnico
- Id: Identificador único. PK.
- Id_Miembro: FK a Miembro_Cuerpo_Tecnico.
- Id_Rol: FK a Rol_Cuerpo_Tecnico.
- Id_Equipo: FK a Equipo. NULL si es selección.
- Id_Seleccion: FK a Seleccion. NULL si es equipo.
- Fecha_Inicio: Inicio del contrato. 2018-08-01.
- Fecha_Fin: Fin del contrato (NULL = actual). NULL.

Restricción: Exactamente uno de Id_Equipo o Id_Seleccion NOT NULL.

---

## Tablas de Configuración de Torneos.

### Tipo_Torneo
- Id: Identificador único. PK.
- Nombre: Nombre del tipo. "Liga Ida y Vuelta".
- Descripcion: Descripción detallada del formato.

Datos: Liga Ida y Vuelta, Liga Solo Ida, Copa Eliminación Directa,
Copa con Grupos y Eliminación, Copa con Zonas, Liga con Liguilla,
Copa Estilo Nuevo Champions.

---

### Configuracion_Tipo_Torneo
- Id: Identificador único. PK.
- Id_Tipo_Torneo: FK a Tipo_Torneo.
- Clave: Nombre del parámetro. "tiene_fase_grupos".
- Valor_Default: Valor por defecto. "si".
- Descripcion: Qué significa este parámetro.

Claves: tiene_fase_grupos, cantidad_grupos, equipos_por_grupo,
partidos_grupo_ida_vuelta, clasifican_por_grupo, tiene_repechaje,
eliminacion_ida_vuelta, tiene_tercer_puesto, tiene_zonas,
cruce_interzonal, tiene_liguilla.

---

### Torneo
- Id: Identificador único. PK.
- Nombre: Nombre del torneo. "Copa Libertadores".
- Id_Tipo_Torneo: FK a Tipo_Torneo. Tipo base.
- Id_Pais: FK a Pais. NULL si internacional.
- Id_Confederacion: FK a Confederacion. Organizadora.
- Es_Selecciones: Si es torneo de selecciones. false.
- Nivel: División. 1 = primera, 2 = segunda.
- Fecha_Creacion: Auditoría.

---

### Sistema_Puntos
- Id: Identificador único. PK.
- Nombre: Nombre del sistema. "Moderno 3-1-0".
- Puntos_Victoria: Puntos por ganar. 3.
- Puntos_Empate: Puntos por empatar. 1.
- Puntos_Derrota: Puntos por perder. 0.

---

### Edicion_Torneo
- Id: Identificador único. PK.
- Id_Torneo: FK a Torneo.
- Temporada: Identificador de temporada. "2023-24".
- Fecha_Inicio: Fecha de inicio. 2023-08-01.
- Fecha_Fin: Fecha de fin. 2024-05-30.
- Id_Sistema_Puntos: FK a Sistema_Puntos. Si aplica.
- Cantidad_Equipos: Equipos participantes. 20.

---

### Configuracion_Edicion
- Id: Identificador único. PK.
- Id_Edicion_Torneo: FK a Edicion_Torneo.
- Clave: Nombre del parámetro. "cantidad_grupos".
- Valor: Valor para esta edición. "8".

Override de configuraciones del tipo de torneo.

---

### Criterio_Desempate
- Id: Identificador único. PK.
- Id_Edicion_Torneo: FK a Edicion_Torneo.
- Orden: Prioridad (1 = primero). 1.
- Tipo: Tipo de criterio. "diferencia_gol".

Tipos: diferencia_gol, goles_favor, enfrentamiento_directo,
goles_visitante, sorteo.

---

### Grupo_Edicion
- Id: Identificador único. PK.
- Id_Edicion_Torneo: FK a Edicion_Torneo.
- Nombre: Nombre del grupo. "A".

---

### Equipo_Grupo
- Id: Identificador único. PK.
- Id_Grupo_Edicion: FK a Grupo_Edicion.
- Id_Equipo: FK a Equipo. NULL si es de selecciones.
- Id_Seleccion: FK a Seleccion. NULL si es de clubes.

Restricción: Exactamente uno de Id_Equipo o Id_Seleccion NOT NULL.

---

## Tablas de Partidos y Eventos

### Partido
- Id: Identificador único. PK.
- Id_Edicion_Torneo: FK a Edicion_Torneo.
- Id_Fase: FK a Tipo_Fase.
- Id_Tipo_Instancia: FK a Tipo_Instancia. Ida/Vuelta/Único. NULL en ligas.
- Numero_Fecha: Número de fecha en ligas. 15. NULL en eliminatorias.
- Id_Grupo: FK a Grupo_Edicion. Si aplica.
- Fecha: Fecha del partido. 2024-03-15.
- Hora_Local: Hora local. 21:00.
- Id_Estadio: FK a Estadio.
- Id_Equipo_Local: FK a Equipo. NULL si selecciones.
- Id_Equipo_Visitante: FK a Equipo. NULL si selecciones.
- Id_Seleccion_Local: FK a Seleccion. NULL si clubes.
- Id_Seleccion_Visitante: FK a Seleccion. NULL si clubes.
- Goles_Local: Goles del local (90 min + extra). 2.
- Goles_Visitante: Goles del visitante. 1.
- Penales_Local: Goles en tanda de penales. 4.
- Penales_Visitante: Goles en tanda de penales. 3.
- Publico: Asistencia. 65000.
- Es_Cancha_Neutral: Si se jugó en cancha neutral. false.
- Id_Arbitro_Principal: FK a Arbitro.
- Id_Arbitro_Linea_1: FK a Arbitro. Primer asistente.
- Id_Arbitro_Linea_2: FK a Arbitro. Segundo asistente.
- Id_Arbitro_Cuarto: FK a Arbitro.
- Id_Arbitro_VAR: FK a Arbitro. Árbitro de video.
- Id_Arbitro_AVAR: FK a Arbitro. Asistente de VAR.
- Id_Tecnico_Local: FK a Tecnico.
- Id_Tecnico_Visitante: FK a Tecnico.
- Id_Estado: FK a Estado_Partido. Default: Finalizado.
- Motivo_Estado: Razón si no es Finalizado. "Gas pimienta".
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

Notas:
- Equipos vs Equipos: usar Id_Equipo_Local/Visitante.
- Selecciones vs Selecciones: usar Id_Seleccion_Local/Visitante.
- Partidos mixtos históricos: se pueden combinar.
- Es_Cancha_Neutral = true: ninguno es realmente "local".

---

### Alineacion
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador.
- Es_Local: Si jugó para el equipo local. true.
- Es_Titular: Si fue titular. true.
- Dorsal: Número de camiseta. 10.
- Es_Capitan: Si fue capitán. false.
- Minuto_Entrada: Minuto que entró (NULL si titular). NULL.
- Minuto_Salida: Minuto que salió (NULL si terminó). NULL.

---

### Gol
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador. Quien hizo el gol.
- Minuto: Minuto del gol (formato MMAA). 4502 = 45+2.
- Es_Tiempo_Extra: Si fue en tiempo extra. false.
- Id_Tipo_Gol: FK a Tipo_Gol. Jugada, penal, etc.
- Id_Parte_Cuerpo: FK a Parte_Cuerpo.
- Id_Zona_Gol: FK a Zona_Gol.
- Es_En_Contra: Si fue autogol. false.
- Es_Para_Local: Si el gol fue a favor del local. true.

---

### Asistencia
- Id: Identificador único. PK.
- Id_Gol: FK a Gol.
- Id_Jugador: FK a Jugador. Quien asistió.

Nota: Relación 1:1 con Gol (un gol tiene máximo una asistencia).

---

### Tarjeta
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador. Amonestado.
- Id_Tipo_Tarjeta: FK a Tipo_Tarjeta.
- Minuto: Minuto de la tarjeta (formato MMAA). 4500 = 45'.
- Es_Tiempo_Extra: Si fue en tiempo extra. false.

---

### Cambio
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Sale: FK a Jugador. Quien sale.
- Id_Entra: FK a Jugador. Quien entra.
- Minuto: Minuto del cambio (formato MMAA). 6000 = 60'.
- Es_Tiempo_Extra: Si fue en tiempo extra. false.

---

### Penal
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador_Patea: FK a Jugador.
- Id_Jugador_Ataja: FK a Jugador. Arquero, si se conoce.
- Id_Tipo_Penal: FK a Tipo_Penal. En partido o en tanda.
- Id_Resultado_Penal: FK a Resultado_Penal.
- Minuto: Minuto si es en partido (formato MMAA). 8500 = 85'.
- Orden_Tanda: Orden en la tanda. 3.
- Es_Para_Local: Si lo pateó el equipo local. true.

---

### Revision_VAR
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Minuto: Minuto de la revisión (formato MMAA). 6700 = 67'.
- Id_Tipo_Revision: FK a Tipo_Revision_VAR.
- Id_Resultado_Revision: FK a Resultado_Revision_VAR.
- Descripcion: Detalle de lo que pasó.

---

### Lesion
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador. Lesionado.
- Minuto: Minuto de la lesión (formato MMAA). 3200 = 32'.
- Descripcion: Descripción de la lesión.

---

## Tablas de Relaciones Históricas

### Fusion_Equipo
- Id: Identificador único. PK.
- Id_Equipo_Origen_1: FK a Equipo. Primer equipo fusionado.
- Id_Equipo_Origen_2: FK a Equipo. Segundo equipo, si aplica.
- Id_Equipo_Resultado: FK a Equipo. Equipo resultante.
- Fecha_Fusion: Fecha de la fusión.
- Descripcion: Contexto histórico.

Nota: Permite rastrear que equipo X es resultado de fusión de A y B.

---

### Sorteo_Desempate
- Id: Identificador único. PK.
- Id_Edicion_Torneo: FK a Edicion_Torneo.
- Id_Fase: FK a Tipo_Fase. En qué fase ocurrió.
- Id_Grupo: FK a Grupo_Edicion. Si fue en fase de grupos.
- Fecha: Fecha del sorteo.
- Posicion_Disputa: Qué posición se disputaba. 2.
- Descripcion: Contexto del sorteo.

Nota: Tabla peculiar para registrar sorteos históricos.
Equipos involucrados en Sorteo_Participante.

---

### Sorteo_Participante
- Id: Identificador único. PK.
- Id_Sorteo: FK a Sorteo_Desempate.
- Id_Equipo: FK a Equipo. NULL si selecciones.
- Id_Seleccion: FK a Seleccion. NULL si clubes.
- Gano: Si ganó el sorteo. true/false.

Restricción: Exactamente uno de Id_Equipo o Id_Seleccion NOT NULL.

---

## Consideraciones Técnicas

### Índices Recomendados

```sql
-- Búsquedas por jugador.
CREATE INDEX idx_alineacion_jugador ON Alineacion(Id_Jugador);
CREATE INDEX idx_gol_jugador ON Gol(Id_Jugador);
CREATE INDEX idx_contrato_jugador ON Contrato_Jugador(Id_Jugador);

-- Búsquedas por equipo.
CREATE INDEX idx_partido_equipo_local ON Partido(Id_Equipo_Local);
CREATE INDEX idx_partido_equipo_visitante
    ON Partido(Id_Equipo_Visitante);

-- Búsquedas por fecha.
CREATE INDEX idx_partido_fecha ON Partido(Fecha);

-- Búsquedas por torneo.
CREATE INDEX idx_partido_edicion ON Partido(Id_Edicion_Torneo);
CREATE INDEX idx_edicion_torneo ON Edicion_Torneo(Id_Torneo);

-- Búsquedas por estadio.
CREATE INDEX idx_partido_estadio ON Partido(Id_Estadio);
```

### Consultas Frecuentes a Optimizar

1. Partidos de un jugador en un rango de fechas.
2. Goles por tipo en un torneo.
3. Tabla de posiciones de una edición.
4. Historial de enfrentamientos entre dos equipos.
5. Estadísticas agregadas por jugador/equipo/técnico.

### Manejo de Datos Históricos

- Todos los campos que pueden no existir son NULL.
- Las consultas deben usar COALESCE o CASE para manejar NULLs.
- Nunca se borran datos, solo se marcan como inactivos.

### Integridad Referencial

- Todas las FK tienen ON DELETE RESTRICT.
- No se permite borrar entidades referenciadas.
- Para "borrar" se usa soft delete con campo Activo = false.

---

## Pendientes de Diseño

- [ ] Tabla para convocatorias de selecciones (futuro).
