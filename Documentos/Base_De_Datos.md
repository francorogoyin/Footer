# Footer - Diseño de Base de Datos

## Índice

1. [Filosofía de Diseño](#filosofía-de-diseño)
2. [Tablas de Geografía](#tablas-de-geografía)
3. [Tablas de Referencia (Catálogos)](#tablas-de-referencia-catálogos)
4. [Tablas de Entidades Principales](#tablas-de-entidades-principales)
5. [Tablas de Configuración de Torneos](#tablas-de-configuración-de-torneos)
6. [Tablas de Partidos y Eventos](#tablas-de-partidos-y-eventos)
7. [Tablas de Relaciones Históricas](#tablas-de-relaciones-históricas)
8. [Consideraciones Técnicas](#consideraciones-técnicas)

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

## Tablas de Geografía

### Continente
- Id: Identificador único. PK.
- Nombre: Nombre del continente. "América del Sur".

Datos: América del Sur, Europa, Asia, África, Oceanía,
América del Norte y Central.

---

### Region
- Id: Identificador único. PK.
- Nombre: Nombre de la región. "Argentina".
- Id_Continente: FK a Continente.
- Tipo: Tipo de región. "Pais".

Tipos: Pais, Confederacion, Continente, Estado, Mundial.

Nota: Unifica todas las regiones posibles para torneos. El Paulistao
tendría una Region tipo "Estado" para São Paulo.

---

### Confederacion
- Id: Identificador único. PK.
- Nombre: Nombre completo. "CONMEBOL".
- Abreviatura: Código corto. "CSF".
- Id_Continente: FK a Continente.

Datos: CONMEBOL, UEFA, CONCACAF, CAF, AFC, OFC.

---

### Pais
- Id: Identificador único. PK.
- Nombre: Nombre del país. "Argentina".
- Codigo_ISO: Código ISO 3166-1 alfa-3. "ARG".
- Id_Confederacion: FK a Confederacion.
- Id_Region: FK a Region. Para linkear con torneos.

---

### Provincia_Estado
- Id: Identificador único. PK.
- Nombre: Nombre de la provincia/estado. "Buenos Aires".
- Id_Pais: FK a Pais.

Nota: Permite torneos como Paulistao (São Paulo) o Carioca (Río).
Para torneos estaduales, la provincia tiene su propia Region en
la tabla Region con Tipo = "Estado".

---

### Ciudad
- Id: Identificador único. PK.
- Nombre: Nombre de la ciudad. "Buenos Aires".
- Id_Provincia_Estado: FK a Provincia_Estado.

---

### Barrio
- Id: Identificador único. PK.
- Nombre: Nombre del barrio. "Núñez".
- Id_Ciudad: FK a Ciudad.

Nota: Útil para filtrar equipos de Buenos Aires por barrio
(Boedo, Núñez, La Boca, Parque Patricios, etc.).

---

### Estadio
- Id: Identificador único. PK.
- Id_Ciudad: FK a Ciudad.
- Id_Barrio: FK a Barrio. NULL si no se conoce.
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

## Tablas de Referencia (Catálogos)

### Lateralidad
- Id: Identificador único. PK.
- Nombre: Lateralidad. "Izquierda".

Datos: Izquierda, Derecha, No Aplica.

---

### Parte_Cuerpo
- Id: Identificador único. PK.
- Nombre: Parte del cuerpo. "Pie".
- Tiene_Lateralidad: Si aplica izquierda/derecha. true.

Datos (con lateralidad): Pie, Rodilla, Muslo, Brazo, Hombro,
Mano, Codo.

Datos (sin lateralidad): Cabeza, Cadera, Pecho, Abdomen,
Genitales, Espalda, Desconocido.

Nota: Cuando se usa en Gol o Lesion, si Tiene_Lateralidad = true,
se debe especificar Id_Lateralidad en la tabla que referencia.

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

Datos: Amarilla, Roja.

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
- Motivo: Qué se revisa. "Gol".
- Es_Revision: Si es revisión de algo cobrado (true) o posible
  no cobrado (false). true.

Datos:
- Gol + Es_Revision=true: Revisión de gol ya cobrado.
- Gol + Es_Revision=false: Posible gol no cobrado.
- Penal + Es_Revision=true: Revisión de penal ya cobrado.
- Penal + Es_Revision=false: Posible penal no cobrado.
- Tarjeta Roja + Es_Revision=true: Revisión de roja ya mostrada.
- Tarjeta Roja + Es_Revision=false: Posible roja no mostrada.

---

### Causa_Revision_VAR
- Id: Identificador único. PK.
- Nombre: Causa de la revisión. "Offside Previo".

Datos: Mano Previa, Falta Previa, Offside Previo, Falta en el Área,
Agresión.

Nota: Se usa en Revision_VAR para especificar qué se revisaba.

---

### Resultado_Revision_VAR
- Id: Identificador único. PK.
- Nombre: Resultado de la revisión. "Confirmado".

Datos: Confirmado, Revertido, Sin Decisión.

---

### Zona_Campo
- Id: Identificador único. PK.
- Nombre: Zona del campo. "Defensa".

Datos: Arco, Defensa, Mediocampo, Ataque.

---

### Posicion_Jugador
- Id: Identificador único. PK.
- Nombre: Posición natural. "Arquero".
- Abreviatura: Código corto. "ARQ".
- Id_Zona_Campo: FK a Zona_Campo.

Datos:
- Arco: Arquero (ARQ).
- Defensa: Defensor Central (DFC), Lateral Derecho (LTD),
  Lateral Izquierdo (LTI), Carrilero Derecho (CAD),
  Carrilero Izquierdo (CAI).
- Mediocampo: Mediocampista Central (MC), Mediocampista
  Defensivo (MCD), Mediocampista Ofensivo (MCO),
  Volante Derecho (VOD), Volante Izquierdo (VOI), Enganche (ENG).
- Ataque: Extremo Derecho (EXD), Extremo Izquierdo (EXI),
  Mediapunta (MP), Delantero Centro (DC), Segunda Punta (SP).

---

### Pie_Habil
- Id: Identificador único. PK.
- Nombre: Pie hábil. "Derecho".

Datos: Derecho, Izquierdo, Ambidiestro.

---

### Tipo_Fase
- Id: Identificador único. PK.
- Nombre: Tipo de fase. "Semifinal".
- Orden: Para ordenar cronológicamente. 7.

Datos (en orden):
1. Fecha Regular
2. Fase de Grupos
3. Treintaidosavos de Final
4. Dieciseisavos de Final
5. Octavos de Final
6. Cuartos de Final
7. Semifinal
8. Tercer Puesto
9. Final
10. Repechaje

Nota: Eliminatorias mundialistas usan Fecha Regular con Numero_Fecha
en Partido.

---

### Tipo_Instancia
- Id: Identificador único. PK.
- Nombre: Tipo de instancia para eliminatorias. "Ida".

Datos: Ida, Vuelta, Desempate, Único.

Nota: Solo para eliminatorias. Las ligas usan Numero_Fecha en Partido.

---

### Ambito_Torneo
- Id: Identificador único. PK.
- Nombre: Ámbito del torneo. "Nacional".

Datos: Nacional, Internacional, Selecciones.

---

## Tablas de Entidades Principales

### Equipo
- Id: Identificador único. PK.
- Id_Ciudad: FK a Ciudad. Ciudad de fundación/origen.
- Fecha_Fundacion: Fecha de fundación. 1905-04-01.
- Activo: Si el equipo sigue existiendo. true.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

Nota: Id_Ciudad es la ciudad de origen/fundación del equipo.
El estadio actual puede estar en otra ciudad (ej: equipos que
se mudaron), pero esto registra de dónde es históricamente.

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

Nota: De aquí se deduce la ubicación histórica del equipo.

---

### Jugador
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Lionel Andrés Messi Cuccittini".
- Nombre_Conocido: Nombre público. "Lionel Messi".
- Fecha_Nacimiento: Fecha de nacimiento. 1987-06-24.
- Id_Pais_Nacimiento: FK a Pais. Donde nació.
- Id_Provincia_Nacimiento: FK a Provincia_Estado. NULL si desconocido.
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

### Dorsal_Temporada
- Id: Identificador único. PK.
- Id_Jugador: FK a Jugador.
- Id_Equipo: FK a Equipo.
- Dorsal: Número de camiseta. 10.
- Temporada: Identificador de temporada. "2023-24".

Nota: Un jugador puede tener distintos dorsales en distintas
temporadas en el mismo equipo. Para consultas por partido, usar
el dorsal en Alineacion (que puede diferir del oficial de temporada).

---

### Tecnico
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Marcelo Alberto Bielsa Caldera".
- Nombre_Conocido: Nombre público. "Marcelo Bielsa".
- Fecha_Nacimiento: Fecha de nacimiento. 1955-07-21.
- Id_Ciudad_Nacimiento: FK a Ciudad.
- Id_Jugador: FK a Jugador. Si fue jugador, referencia.
- Altura_Cm: Altura en centímetros. NULL si desconocido.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

---

### Contrato_Tecnico
- Id: Identificador único. PK.
- Id_Tecnico: FK a Tecnico.
- Id_Participante: ID del equipo o selección.
- Tipo_Participante: "Equipo" o "Seleccion".
- Fecha_Inicio: Inicio del contrato. 2018-08-01.
- Fecha_Fin: Fin del contrato (NULL = actual). NULL.

Nota: Id_Participante referencia a Equipo o Seleccion según
Tipo_Participante.

---

### Arbitro
- Id: Identificador único. PK.
- Nombre_Completo: Nombre legal. "Néstor Fabián Pitana".
- Fecha_Nacimiento: Fecha de nacimiento. 1975-06-17.
- Id_Ciudad_Nacimiento: FK a Ciudad.
- Altura_Cm: Altura en centímetros. NULL si desconocido.
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
- Id_Ciudad_Nacimiento: FK a Ciudad.
- Id_Jugador: FK a Jugador. Si fue jugador, referencia.
- Fecha_Fallecimiento: Fecha de fallecimiento. NULL si vive.

---

### Contrato_Cuerpo_Tecnico
- Id: Identificador único. PK.
- Id_Miembro: FK a Miembro_Cuerpo_Tecnico.
- Id_Rol: FK a Rol_Cuerpo_Tecnico.
- Id_Participante: ID del equipo o selección.
- Tipo_Participante: "Equipo" o "Seleccion".
- Fecha_Inicio: Inicio del contrato. 2018-08-01.
- Fecha_Fin: Fin del contrato (NULL = actual). NULL.

Nota: Id_Participante referencia a Equipo o Seleccion según
Tipo_Participante.

---

## Tablas de Configuración de Torneos

### Tipo_Torneo
- Id: Identificador único. PK.
- Nombre: Nombre del tipo. "Liga Ida y Vuelta".
- Descripcion: Descripción detallada del formato.
- Es_Oficial: Si es torneo oficial o amistoso. true.
- Id_Ambito: FK a Ambito_Torneo.

Datos: Liga Ida y Vuelta, Liga Solo Ida, Copa Eliminación Directa,
Copa con Grupos y Eliminación, Copa con Zonas, Liga con Liguilla,
Copa Estilo Nuevo Champions, Amistoso.

Nota: Para partidos amistosos sueltos, usar torneo "Amistosos
Internacionales" con edición por año.

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
- Id_Region: FK a Region. Organizadora del torneo.
- Nivel: División. 1 = primera, 2 = segunda.
- Fecha_Creacion: Auditoría.

Nota: Id_Region puede ser un país (Liga Argentina), confederación
(Copa Libertadores), estado (Paulistao), o mundial (FIFA).

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
- Id_Participante: ID del equipo o selección.
- Tipo_Participante: "Equipo" o "Seleccion".

Nota: Id_Participante referencia a Equipo o Seleccion según
Tipo_Participante.

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
- Id_Local: ID del equipo o selección local.
- Id_Visitante: ID del equipo o selección visitante.
- Tipo_Participante: "Equipo" o "Seleccion".
- Goles_Local: Goles del local (90 min + extra). 2.
- Goles_Visitante: Goles del visitante. 1.
- Penales_Local: Goles en tanda de penales. 4.
- Penales_Visitante: Goles en tanda de penales. 3.
- Resultado_Walkover: Resultado por walkover. "3-0". NULL si no aplica.
- Publico: Asistencia. 65000.
- Es_Neutral: Si se jugó en cancha neutral. false.
- Id_Arbitro_Principal: FK a Arbitro.
- Id_Arbitro_Linea_1: FK a Arbitro. Primer asistente.
- Id_Arbitro_Linea_2: FK a Arbitro. Segundo asistente.
- Id_Arbitro_Cuarto: FK a Arbitro.
- Id_Arbitro_VAR: FK a Arbitro. Árbitro de video.
- Id_Arbitro_AVAR: FK a Arbitro. Asistente de VAR.
- Id_Tecnico_Local: FK a Tecnico.
- Id_Tecnico_Visitante: FK a Tecnico.
- Id_Tecnico_Interino_Local: FK a Tecnico. Reemplazante en ese partido.
- Id_Tecnico_Interino_Visitante: FK a Tecnico. Reemplazante en ese partido.
- Fecha_Creacion: Auditoría.
- Fecha_Modificacion: Auditoría.

Notas:
- Id_Local/Id_Visitante referencian a Equipo o Seleccion según Tipo_Participante.
- Es_Neutral = true: ninguno es realmente "local".
- Resultado_Walkover: si no es NULL, el partido fue definido por mesa.
  Los goles del walkover se computan al capitán del equipo beneficiado.
- Tecnico_Interino: cuando el DT oficial no puede dirigir ese partido
  específico (ej: Gallardo suspendido en final Libertadores 2018).

---

### Alineacion
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador.
- Es_Local: Si jugó para el equipo local. true.
- Es_Titular: Si fue titular. true.
- Dorsal: Número de camiseta. 10.

Nota: Minutos de entrada/salida se deducen de la tabla Cambio.
Capitán se registra en tabla Capitania.

---

### Capitania
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador.
- Es_Local: Si es capitán del equipo local. true.
- Orden: Orden de capitanía. 1.

Nota: Orden = 1 es el capitán titular. Si sale o es expulsado y
otro toma la cinta, ese tiene Orden = 2, etc. Permite registrar
todos los capitanes de un partido si hubo cambios.

---

### Gol
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador. Quien hizo el gol.
- Minuto: Minuto del gol (formato MMAA). 4502 = 45+2.
- Es_Tiempo_Extra: Si fue en tiempo extra. false.
- Id_Tipo_Gol: FK a Tipo_Gol. Jugada, penal, etc.
- Id_Parte_Cuerpo: FK a Parte_Cuerpo.
- Id_Lateralidad: FK a Lateralidad. Si Parte_Cuerpo tiene lateralidad.
- Id_Zona_Gol: FK a Zona_Gol.
- Es_En_Contra: Si fue autogol. false.

Nota: Si fue para local o visitante se deduce de Alineacion.
Id_Lateralidad es NULL si la parte del cuerpo no tiene lateralidad
(ej: Cabeza) o si no se conoce.

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
- Id_Sancionado: ID del sancionado (jugador, técnico o cuerpo técnico).
- Tipo_Sancionado: Tipo de persona sancionada. "Jugador".
- Id_Tipo_Tarjeta: FK a Tipo_Tarjeta.
- Minuto: Minuto de la tarjeta (formato MMAA). 4500 = 45'.
- Es_Tiempo_Extra: Si fue en tiempo extra. false.

Tipos_Sancionado: Jugador, Tecnico, Miembro_Cuerpo_Tecnico.

Nota: Id_Sancionado referencia a la tabla según Tipo_Sancionado.
Jugador → Jugador.Id, Tecnico → Tecnico.Id, etc.

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
- Es_Tiempo_Extra: Si fue en tiempo extra. false.
- Repeticiones: Cantidad de veces que se repitió. 0.

Nota: Repeticiones = 0 significa que se pateó una sola vez.
Si hubo VAR y se repitió, Repeticiones = 1, etc.
Si fue para local o visitante se deduce de Alineacion.

---

### Revision_VAR
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Minuto: Minuto de la revisión (formato MMAA). 6700 = 67'.
- Id_Tipo_Revision: FK a Tipo_Revision_VAR.
- Id_Causa_Revision: FK a Causa_Revision_VAR. NULL si no aplica.
- Id_Resultado_Revision: FK a Resultado_Revision_VAR.
- Descripcion: Detalle de lo que pasó.

---

### Lesion
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Id_Jugador: FK a Jugador. Lesionado.
- Minuto: Minuto de la lesión (formato MMAA). 3200 = 32'.
- Id_Parte_Cuerpo: FK a Parte_Cuerpo. Parte lesionada.
- Id_Lateralidad: FK a Lateralidad. Si Parte_Cuerpo tiene lateralidad.
- Descripcion: Descripción de la lesión.

Nota: Id_Lateralidad es NULL si la parte del cuerpo no tiene
lateralidad (ej: Cabeza) o si no se conoce.

---

### Suspension_Partido
- Id: Identificador único. PK.
- Id_Partido: FK a Partido.
- Minuto: Minuto de la suspensión (formato MMAA). 500 = 5'.
- Causa: Razón de la suspensión. "Invasión de Anvisa".

Nota: El resultado al momento de suspensión se calcula con los
goles registrados hasta ese minuto.

---

### Reanudacion
- Id: Identificador único. PK.
- Id_Partido: FK a Partido. El partido original suspendido.
- Fecha: Fecha de reanudación.
- Id_Estadio: FK a Estadio. Puede ser distinto al original.
- Formato: Descripción del formato. "Dos tiempos de 14 minutos".
- Minuto_Inicio: Desde qué minuto se reanuda. 500 = 5'.

Nota: Linkea el partido original con su continuación. Los eventos
de la reanudación se registran en el mismo Id_Partido original.

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
- Id_Participante: ID del equipo o selección.
- Tipo_Participante: "Equipo" o "Seleccion".
- Gano: Si ganó el sorteo. true/false.

Nota: Id_Participante referencia a Equipo o Seleccion según
Tipo_Participante.

---

## Consideraciones Técnicas

### Formato de Minutos (MMAA)

Los minutos de eventos se almacenan como INT con formato MMAA:
- MM = minuto base (01-90, o más en tiempo extra).
- AA = minutos de adición (00-99).

Ejemplos:
- 4500 = minuto 45 exacto.
- 4502 = minuto 45+2 (segundo minuto de adición del primer tiempo).
- 9000 = minuto 90 exacto.
- 9005 = minuto 90+5.

Valor especial:
- 4599 = entretiempo (para cambios realizados en el descanso).

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

-- Búsquedas por región.
CREATE INDEX idx_torneo_region ON Torneo(Id_Region);
```

### Consultas Frecuentes a Optimizar

1. Partidos de un jugador en un rango de fechas.
2. Goles por tipo en un torneo.
3. Tabla de posiciones de una edición.
4. Historial de enfrentamientos entre dos equipos.
5. Estadísticas agregadas por jugador/equipo/técnico.
6. Equipos de un barrio específico.
7. Torneos de una región específica.

### Manejo de Datos Históricos

- Todos los campos que pueden no existir son NULL.
- Las consultas deben usar COALESCE o CASE para manejar NULLs.
- Nunca se borran datos, solo se marcan como inactivos.

### Integridad Referencial

- Todas las FK tienen ON DELETE RESTRICT.
- No se permite borrar entidades referenciadas.
- Para "borrar" se usa soft delete con campo Activo = false.

### FKs Polimórficas

Las siguientes tablas usan FKs polimórficas (Id + Tipo):
- Partido (Id_Local/Id_Visitante + Tipo_Participante)
- Contrato_Tecnico (Id_Participante + Tipo_Participante)
- Contrato_Cuerpo_Tecnico (Id_Participante + Tipo_Participante)
- Equipo_Grupo (Id_Participante + Tipo_Participante)
- Sorteo_Participante (Id_Participante + Tipo_Participante)
- Tarjeta (Id_Sancionado + Tipo_Sancionado)

Estas no tienen FK real en la BD; la integridad se valida en la
aplicación.

---

## Pendientes de Diseño

- [ ] Tabla para convocatorias de selecciones (futuro).
