
# -*- coding: utf-8 -*-
import re as Re
import unicodedata as Unicodedata
from pathlib import Path

import pandas as Pandas
from pypdf import PdfReader


def Normalizar_Espacios(Texto):
    """
    Normalizar espacios y eliminar saltos de linea.

    Parametros:
    - Texto: Texto original con espacios variados.

    Retorna:
    - Texto con espacios simples y sin saltos de linea.

    Ejemplos:
    - Normalizar_Espacios("A\n B")
    """

    if Texto is None:
        return None
    Texto = Re.sub(r"\s+", " ", Texto)
    return Texto.strip()


def Remover_Acentos(Texto):
    """
    Remover acentos y diacriticos de un texto.

    Parametros:
    - Texto: Texto original con acentos.

    Retorna:
    - Texto sin acentos.

    Ejemplos:
    - Remover_Acentos("Futbol")
    """

    if Texto is None:
        return None
    Texto_Normalizado = Unicodedata.normalize("NFD", Texto)
    Texto_Sin_Acentos = "".join(
        Caracter
        for Caracter in Texto_Normalizado
        if Unicodedata.category(Caracter) != "Mn"
    )
    return Texto_Sin_Acentos


def Normalizar_Clave(Texto):
    """
    Normalizar texto para usarlo en IDs.

    Parametros:
    - Texto: Texto original.

    Retorna:
    - Texto en mayusculas y con guiones bajos.

    Ejemplos:
    - Normalizar_Clave("River Plate")
    """

    Texto = Remover_Acentos(Texto or "")
    Texto = Texto.upper()
    Texto = Re.sub(r"[^A-Z0-9]+", "_", Texto)
    Texto = Texto.strip("_")
    Texto = Re.sub(r"_+", "_", Texto)
    return Texto


def Convertir_Fecha(Texto, Anio_Defecto):
    """
    Convertir fecha en texto a formato ISO.

    Parametros:
    - Texto: Texto de fecha.
    - Anio_Defecto: Anio para fechas sin anio.

    Retorna:
    - Fecha en formato AAAA-MM-DD o None.

    Ejemplos:
    - Convertir_Fecha("31 de mayo de 1931", 1931)
    """

    if not Texto:
        return None
    Texto_Limpio = Texto.strip()
    Texto_Limpio = Texto_Limpio.replace("(", "")
    Texto_Limpio = Texto_Limpio.replace(")", "")
    Texto_Limpio = Texto_Limpio.strip()
    Texto_Bajo = Texto_Limpio.lower()
    Patron_Corto = Re.search(
        r"(\d{1,2})\s*/\s*(\d{1,2})(?:\s*/\s*(\d{2,4}))?",
        Texto_Bajo,
    )
    if Patron_Corto:
        Dia = int(Patron_Corto.group(1))
        Mes = int(Patron_Corto.group(2))
        Anio_Grupo = Patron_Corto.group(3)
        if Anio_Grupo:
            Anio = int(Anio_Grupo)
            if Anio < 100:
                Anio = 1900 + Anio
        else:
            Anio = int(Anio_Defecto)
        return f"{Anio:04d}-{Mes:02d}-{Dia:02d}"
    Patron = (
        r"(\d{1,2})\s+de\s+"
        r"([a-z]+)\s+de\s+(\d{4})"
    )
    Resultado = Re.search(Patron, Texto_Bajo)
    if Resultado:
        Dia = int(Resultado.group(1))
        Mes_Texto = Resultado.group(2)
        Anio = int(Resultado.group(3))
        Meses = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "setiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12,
        }
        Mes = Meses.get(Mes_Texto)
        if Mes:
            return f"{Anio:04d}-{Mes:02d}-{Dia:02d}"
    return None

def Es_Linea_Equipo(Texto):
    """
    Determinar si una linea parece un equipo con goles.

    Parametros:
    - Texto: Linea a evaluar.

    Retorna:
    - True si parece linea de equipo.

    Ejemplos:
    - Es_Linea_Equipo("ATLANTA 0")
    """

    if not Texto:
        return False
    if ":" in Texto:
        return False
    Texto_Mayus = Texto.upper()
    if "FECHA" in Texto_Mayus:
        return False
    if "ARBITRO" in Texto_Mayus:
        return False
    if "CANCHA" in Texto_Mayus:
        return False
    if "RECAUDACION" in Texto_Mayus:
        return False
    if "M." in Texto_Mayus:
        return False
    if Texto.strip().startswith("("):
        return False
    return Re.search(r"\d+\s*$", Texto) is not None


def Extraer_Equipo_Y_Goles(Texto):
    """
    Extraer nombre de equipo y goles desde una linea.

    Parametros:
    - Texto: Linea con equipo y goles.

    Retorna:
    - Tupla (Equipo, Goles) o (None, None).

    Ejemplos:
    - Extraer_Equipo_Y_Goles("ATLANTA 0")
    """

    Resultado = Re.search(r"^(.*?)(\d+)\s*$", Texto)
    if not Resultado:
        return None, None
    Equipo = Resultado.group(1).strip()
    Goles = int(Resultado.group(2))
    return Equipo, Goles


def Extraer_Jugadores_De_Alineacion(Texto):
    """
    Extraer lista de jugadores desde una alineacion.

    Parametros:
    - Texto: Texto de alineacion.

    Retorna:
    - Lista de jugadores.

    Ejemplos:
    - Extraer_Jugadores_De_Alineacion("A; B y C")
    """

    Texto_Limpio = Normalizar_Espacios(Texto)
    Texto_Limpio = Texto_Limpio.replace(".", "")
    Grupos = [
        Grupo.strip()
        for Grupo in Texto_Limpio.split(";")
        if Grupo.strip()
    ]
    Jugadores = []
    for Grupo in Grupos:
        Grupo = Grupo.replace(" y ", ", ")
        Partes = [
            Parte.strip()
            for Parte in Grupo.split(",")
            if Parte.strip()
        ]
        Jugadores.extend(Partes)
    return Jugadores


def Crear_Alias_Jugadores(Lista_Jugadores):
    """
    Crear mapa de alias para buscar jugadores en eventos.

    Parametros:
    - Lista_Jugadores: Lista de nombres completos.

    Retorna:
    - Diccionario alias -> conjunto de nombres.

    Ejemplos:
    - Crear_Alias_Jugadores(["Juan Perez"])
    """

    Mapa_Alias = {}
    for Nombre in Lista_Jugadores:
        Texto = Remover_Acentos(Nombre).upper()
        Texto = Normalizar_Espacios(Texto)
        Partes = Texto.split(" ")
        Alias_Lista = []
        if Partes:
            Apellido = Partes[-1]
            if len(Partes) >= 2:
                Anterior = Partes[-2]
                if Anterior in ["DE", "DEL", "DA", "D"]:
                    Apellido = f"{Anterior} {Apellido}"
            Alias_Lista.append(Apellido)
            Iniciales = "".join(Parte[0] for Parte in Partes[:-1])
            if Iniciales:
                Alias_Lista.append(
                    f"{Iniciales[0]}. {Apellido}"
                )
            if len(Iniciales) > 1:
                Alias_Lista.append(
                    f"{'.'.join(Iniciales)}. {Apellido}"
                )
        Alias_Lista.append(Texto)
        for Alias in Alias_Lista:
            Alias_Limpio = Normalizar_Espacios(Alias)
            if Alias_Limpio not in Mapa_Alias:
                Mapa_Alias[Alias_Limpio] = set()
            Mapa_Alias[Alias_Limpio].add(Nombre)
    return Mapa_Alias


def Buscar_Jugador_Por_Alias(Nombre_Evento, Mapa_Alias):
    """
    Buscar jugador por alias dentro de un texto de evento.

    Parametros:
    - Nombre_Evento: Texto a evaluar.
    - Mapa_Alias: Alias posibles por jugador.

    Retorna:
    - Nombre del jugador si es unico, o None.

    Ejemplos:
    - Buscar_Jugador_Por_Alias("GOMEZ", Mapa)
    """

    Texto = Remover_Acentos(Nombre_Evento or "")
    Texto = Texto.upper()
    Texto = Re.sub(r"[^A-Z0-9. ]+", " ", Texto)
    Texto = Normalizar_Espacios(Texto)
    Coincidencias = set()
    for Alias, Nombres in Mapa_Alias.items():
        if Alias and Alias in Texto:
            Coincidencias.update(Nombres)
    if len(Coincidencias) == 1:
        return list(Coincidencias)[0]
    return None


def Extraer_Asistencia(Texto_Evento, Mapa_Alias):
    """
    Extraer asistencia desde un texto de gol.

    Parametros:
    - Texto_Evento: Texto del evento.
    - Mapa_Alias: Alias posibles por jugador.

    Retorna:
    - Tupla (Jugador, Es_Inferido) o (None, False).

    Ejemplos:
    - Extraer_Asistencia("tras pase de Perez", Mapa)
    """

    Patrones = [
        r"tras(?: un)? pase de ([A-Za-z .']+)",
        r"por (?:pase|centro) de ([A-Za-z .']+)",
        r"habilitado por ([A-Za-z .']+)",
        r"asistido(?: tambien)?(?: de cabeza)? por ([A-Za-z .']+)",
        r"luego de (?:una )?cesion de ([A-Za-z .']+)",
        r"tras centro de ([A-Za-z .']+)",
        r"corner ejecutado por ([A-Za-z .']+)",
    ]
    Texto_Bajo = Texto_Evento.lower()
    for Patron in Patrones:
        Resultado = Re.search(Patron, Texto_Bajo)
        if Resultado:
            Nombre = Resultado.group(1).strip()
            Nombre_Mapa = Buscar_Jugador_Por_Alias(
                Nombre,
                Mapa_Alias,
            )
            return Nombre_Mapa or Nombre.strip(), False
    return None, False


def Determinar_Parte_Cuerpo(Texto_Evento):
    """
    Determinar parte del cuerpo usada en un gol.

    Parametros:
    - Texto_Evento: Texto del evento.

    Retorna:
    - Tupla (Parte_Cuerpo, Es_Inferido, Detalle).

    Ejemplos:
    - Determinar_Parte_Cuerpo("cabeceo un centro")
    """

    Texto_Bajo = Texto_Evento.lower()
    if "cabece" in Texto_Bajo or "cabeza" in Texto_Bajo:
        return "Cabeza", False, None
    if "tiro" in Texto_Bajo or "remate" in Texto_Bajo:
        return "Pie", True, "Parte_Cuerpo por tiro o remate."
    if "pate" in Texto_Bajo or "disparo" in Texto_Bajo:
        return "Pie", True, "Parte_Cuerpo por pateo o disparo."
    return None, False, None


def Determinar_Tipo_Gol(Texto_Evento):
    """
    Determinar tipo de gol desde el texto del evento.

    Parametros:
    - Texto_Evento: Texto del evento.

    Retorna:
    - Tipo de gol o None.

    Ejemplos:
    - Determinar_Tipo_Gol("de penal")
    """

    Texto_Bajo = Texto_Evento.lower()
    if "penal" in Texto_Bajo:
        return "Penal"
    if "tiro libre" in Texto_Bajo:
        return "Tiro Libre"
    return None


Patron_Fecha_Pagina = Re.compile(
    "(\\d+)(?:a|\\u00aa)\\s*FECHA"
)

Ruta_Pdf = Path("Archivo/Primera/1931.pdf")
Lector = PdfReader(str(Ruta_Pdf))

Paginas_Validas = set()
Texto_Paginas = {}
for Indice_Pagina, Pagina in enumerate(Lector.pages, start = 1):
    Texto_Pagina = Pagina.extract_text() or ""
    Texto_Paginas[Indice_Pagina] = Texto_Pagina
    if Patron_Fecha_Pagina.search(Texto_Pagina):
        Paginas_Validas.add(Indice_Pagina)

Lineas = []
for Indice_Pagina, Texto in Texto_Paginas.items():
    if Indice_Pagina not in Paginas_Validas:
        continue
    for Linea in Texto.split("\n"):
        Linea_Limpia = Linea.strip()
        if not Linea_Limpia:
            continue
        Linea_Normal = Remover_Acentos(Linea_Limpia).lower()
        if "futbol argentino" in Linea_Normal:
            continue
        if Linea_Limpia.isdigit():
            continue
        Lineas.append(
            {
                "Texto": Linea_Limpia,
                "Pagina": Indice_Pagina,
            }
        )

Torneo = None
Numero_Fecha = None
Fecha_Programada = None
Fecha_Jugada_Pendiente = None

Ids_Usados = set()
Ids_Por_Tipo = {
    "EQP": {},
    "JUG": {},
    "ARB": {},
    "EST": {},
    "TEC": {},
}

Catalogos = []
Catalogos_Existentes = set()


def Registrar_Catalogo(Tipo, Id, Nombre, Pagina):
    """
    Registrar un elemento en la hoja de catalogos.

    Parametros:
    - Tipo: Tipo de entidad.
    - Id: Identificador unico.
    - Nombre: Nombre original.
    - Pagina: Pagina de origen.

    Retorna:
    - None.

    Ejemplos:
    - Registrar_Catalogo("Equipo", "EQP_ARG_RIV", "River", 3)
    """

    Clave = (Tipo, Id)
    if Clave in Catalogos_Existentes:
        return
    Catalogos_Existentes.add(Clave)
    Catalogos.append(
        {
            "Tipo": Tipo,
            "Id": Id,
            "Nombre": Nombre,
            "Observaciones": None,
            "Fuente_Pagina": Pagina,
            "Texto_Original": None,
        }
    )


def Obtener_Id(Tipo, Nombre, Prefijo_Pais = None, Pagina = None):
    """
    Obtener o crear un ID con patron por tipo.

    Parametros:
    - Tipo: Prefijo de tipo, ej: EQP.
    - Nombre: Nombre original.
    - Prefijo_Pais: Prefijo opcional.
    - Pagina: Pagina de origen.

    Retorna:
    - ID generado.

    Ejemplos:
    - Obtener_Id("EQP", "River Plate", "ARG")
    """

    if Nombre in Ids_Por_Tipo[Tipo]:
        return Ids_Por_Tipo[Tipo][Nombre]
    Clave = Normalizar_Clave(Nombre)
    if Prefijo_Pais:
        Base = f"{Tipo}_{Prefijo_Pais}_{Clave}"
    else:
        Base = f"{Tipo}_{Clave}"
    Id_Final = Base
    Contador = 2
    while Id_Final in Ids_Usados:
        Id_Final = f"{Base}_{Contador}"
        Contador += 1
    Ids_Usados.add(Id_Final)
    Ids_Por_Tipo[Tipo][Nombre] = Id_Final
    Tipo_Largo = {
        "EQP": "Equipo",
        "JUG": "Jugador",
        "ARB": "Arbitro",
        "EST": "Estadio",
        "TEC": "Tecnico",
    }.get(Tipo, Tipo)
    Registrar_Catalogo(Tipo_Largo, Id_Final, Nombre, Pagina)
    return Id_Final


Partidos = []
Jugadores_Partido = []
Goles_Partido = []
Penales_Partido = []
Tarjetas_Partido = []
Lesiones_Partido = []
Cambios_Partido = []

Id_Contadores = {
    "PAR": 1,
    "JPR": 1,
    "GOL": 1,
    "PEN": 1,
    "TAR": 1,
    "LES": 1,
    "CAM": 1,
}


def Generar_Id_Secuencial(Prefijo):
    """
    Generar un ID secuencial con prefijo.

    Parametros:
    - Prefijo: Prefijo del ID.

    Retorna:
    - ID secuencial.

    Ejemplos:
    - Generar_Id_Secuencial("PAR")
    """

    Valor = Id_Contadores[Prefijo]
    Id_Contadores[Prefijo] = Valor + 1
    return f"{Prefijo}_{Valor:04d}"


Partido_Actual = None
Etapa_Partido = None
Lineas_Alineacion_Local = []
Lineas_Alineacion_Visitante = []
Alineaciones_Registradas = False
Mapa_Alias_Partido = {}
Mapa_Jugador_Equipo = {}
Observaciones_Partido = []
Suspensiones_Partido = []

Patron_Fecha = Re.compile(
    "(\\d+)(?:a|\\u00aa)\\s*FECHA\\s*\\(([^)]+)\\)"
)
Patron_Minuto = Re.compile(r"^(\d+)\s*m\s*\.?\s*(.*)$")
Patron_Marcador = Re.compile(r"\b(\d+)\s*-\s*(\d+)\b")


def Registrar_Alineaciones(Pagina):
    """
    Registrar alineaciones del partido actual si faltan.

    Parametros:
    - Pagina: Pagina de origen.

    Retorna:
    - None.

    Ejemplos:
    - Registrar_Alineaciones(3)
    """

    global Alineaciones_Registradas
    global Mapa_Alias_Partido
    global Mapa_Jugador_Equipo
    if not Partido_Actual or Alineaciones_Registradas:
        return
    Texto_Local = Normalizar_Espacios(
        " ".join(Lineas_Alineacion_Local)
    )
    Texto_Visitante = Normalizar_Espacios(
        " ".join(Lineas_Alineacion_Visitante)
    )
    Jugadores_Local = Extraer_Jugadores_De_Alineacion(Texto_Local)
    Jugadores_Visitante = Extraer_Jugadores_De_Alineacion(
        Texto_Visitante
    )
    for Jugador in Jugadores_Local:
        Id_Jugador = Obtener_Id("JUG", Jugador, None, Pagina)
        Jugadores_Partido.append(
            {
                "Id_Registro": Generar_Id_Secuencial("JPR"),
                "Id_Partido_Extraido": Partido_Actual[
                    "Id_Partido_Extraido"
                ],
                "Equipo": Partido_Actual["Equipo_Local"],
                "Id_Equipo": Partido_Actual["Id_Equipo_Local"],
                "Jugador": Jugador,
                "Id_Jugador": Id_Jugador,
                "Es_Titular": True,
                "Dorsal": None,
                "Posicion": None,
                "Capitan": None,
                "Inferido": None,
                "Detalle_Inferencias": None,
                "Observaciones": None,
                "Fuente_Pagina": Pagina,
                "Texto_Original": Texto_Local,
            }
        )
        Mapa_Jugador_Equipo[Jugador] = Partido_Actual[
            "Equipo_Local"
        ]
    for Jugador in Jugadores_Visitante:
        Id_Jugador = Obtener_Id("JUG", Jugador, None, Pagina)
        Jugadores_Partido.append(
            {
                "Id_Registro": Generar_Id_Secuencial("JPR"),
                "Id_Partido_Extraido": Partido_Actual[
                    "Id_Partido_Extraido"
                ],
                "Equipo": Partido_Actual["Equipo_Visitante"],
                "Id_Equipo": Partido_Actual["Id_Equipo_Visitante"],
                "Jugador": Jugador,
                "Id_Jugador": Id_Jugador,
                "Es_Titular": True,
                "Dorsal": None,
                "Posicion": None,
                "Capitan": None,
                "Inferido": None,
                "Detalle_Inferencias": None,
                "Observaciones": None,
                "Fuente_Pagina": Pagina,
                "Texto_Original": Texto_Visitante,
            }
        )
        Mapa_Jugador_Equipo[Jugador] = Partido_Actual[
            "Equipo_Visitante"
        ]
    Lista_Jugadores = Jugadores_Local + Jugadores_Visitante
    Mapa_Alias_Partido = Crear_Alias_Jugadores(Lista_Jugadores)
    Alineaciones_Registradas = True


def Finalizar_Partido():
    """
    Finalizar el partido actual y guardar sus datos.

    Parametros:
    - None.

    Retorna:
    - None.

    Ejemplos:
    - Finalizar_Partido()
    """

    global Partido_Actual
    global Observaciones_Partido
    global Suspensiones_Partido
    global Lineas_Alineacion_Local
    global Lineas_Alineacion_Visitante
    global Alineaciones_Registradas
    global Mapa_Alias_Partido
    global Mapa_Jugador_Equipo
    if Partido_Actual is None:
        return
    Registrar_Alineaciones(Partido_Actual["Fuente_Pagina"])
    Partido_Actual["Observaciones"] = (
        Normalizar_Espacios(" | ".join(Observaciones_Partido))
        if Observaciones_Partido
        else None
    )
    Partido_Actual["Suspensiones"] = (
        Normalizar_Espacios(" | ".join(Suspensiones_Partido))
        if Suspensiones_Partido
        else None
    )
    Partido_Actual["Texto_Original"] = Normalizar_Espacios(
        " ".join(Partido_Actual["Lineas_Originales"])
    )
    Partidos.append(Partido_Actual)
    Partido_Actual = None
    Observaciones_Partido = []
    Suspensiones_Partido = []
    Lineas_Alineacion_Local = []
    Lineas_Alineacion_Visitante = []
    Alineaciones_Registradas = False
    Mapa_Alias_Partido = {}
    Mapa_Jugador_Equipo = {}

Indice = 0
while Indice < len(Lineas):
    Linea = Lineas[Indice]["Texto"]
    Pagina = Lineas[Indice]["Pagina"]
    Linea_Normal = Remover_Acentos(Linea).upper()

    if "CAMPEONATO" in Linea_Normal and "DIVISION" in Linea_Normal:
        Torneo = Normalizar_Espacios(Linea.title())
        Indice += 1
        continue

    Resultado_Fecha = Patron_Fecha.search(Linea)
    if Resultado_Fecha:
        Finalizar_Partido()
        Numero_Fecha = int(Resultado_Fecha.group(1))
        Fecha_Programada = Convertir_Fecha(
            Resultado_Fecha.group(2),
            1931,
        )
        Indice += 1
        continue

    if "SE JUG" in Linea_Normal:
        Fecha_Jugada_Pendiente = Convertir_Fecha(Linea, 1931)
        Indice += 1
        continue

    if Re.search(r"\s+vs\.?\s+", Linea, flags = Re.IGNORECASE):
        Partes_Vs = Re.split(
            r"\s+vs\.?\s+",
            Linea,
            flags = Re.IGNORECASE,
        )
        if len(Partes_Vs) == 2:
            Equipo_Local = Partes_Vs[0].strip()
            Equipo_Visitante = Partes_Vs[1].strip()
            if Partido_Actual is not None:
                Finalizar_Partido()
            Partido_Actual = {
                "Id_Partido_Extraido": Generar_Id_Secuencial("PAR"),
                "Torneo": Torneo,
                "Fecha": Fecha_Programada,
                "Fecha_Programada": Fecha_Programada,
                "Fecha_Jugada": None,
                "Numero_Fecha": Numero_Fecha,
                "Equipo_Local": Equipo_Local,
                "Equipo_Visitante": Equipo_Visitante,
                "Id_Equipo_Local": Obtener_Id(
                    "EQP",
                    Equipo_Local,
                    "ARG",
                    Pagina,
                ),
                "Id_Equipo_Visitante": Obtener_Id(
                    "EQP",
                    Equipo_Visitante,
                    "ARG",
                    Pagina,
                ),
                "Goles_Local": None,
                "Goles_Visitante": None,
                "Resultado_Walkover": None,
                "Arbitro_Principal": None,
                "Id_Arbitro_Principal": None,
                "Recaudacion": None,
                "Estadio": None,
                "Id_Estadio": None,
                "Publico": None,
                "Hora_Local": None,
                "Es_Neutral": None,
                "Tecnico_Local": None,
                "Tecnico_Visitante": None,
                "Id_Tecnico_Local": None,
                "Id_Tecnico_Visitante": None,
                "Suspensiones": None,
                "Observaciones": None,
                "Fuente_Pagina": Pagina,
                "Texto_Original": None,
                "Lineas_Originales": [],
            }
            if Fecha_Jugada_Pendiente:
                Partido_Actual["Fecha_Jugada"] = Fecha_Jugada_Pendiente
                Partido_Actual["Fecha"] = Fecha_Jugada_Pendiente
                Fecha_Jugada_Pendiente = None
            Etapa_Partido = "EVENTOS"
            Partido_Actual["Lineas_Originales"].append(Linea)
            Indice += 1
            continue

    if Es_Linea_Equipo(Linea):
        Equipo, Goles = Extraer_Equipo_Y_Goles(Linea)
        if Partido_Actual is None:
            Partido_Actual = {
                "Id_Partido_Extraido": Generar_Id_Secuencial("PAR"),
                "Torneo": Torneo,
                "Fecha": Fecha_Programada,
                "Fecha_Programada": Fecha_Programada,
                "Fecha_Jugada": None,
                "Numero_Fecha": Numero_Fecha,
                "Equipo_Local": Equipo,
                "Equipo_Visitante": None,
                "Id_Equipo_Local": Obtener_Id(
                    "EQP",
                    Equipo,
                    "ARG",
                    Pagina,
                ),
                "Id_Equipo_Visitante": None,
                "Goles_Local": Goles,
                "Goles_Visitante": None,
                "Resultado_Walkover": None,
                "Arbitro_Principal": None,
                "Id_Arbitro_Principal": None,
                "Recaudacion": None,
                "Estadio": None,
                "Id_Estadio": None,
                "Publico": None,
                "Hora_Local": None,
                "Es_Neutral": None,
                "Tecnico_Local": None,
                "Tecnico_Visitante": None,
                "Id_Tecnico_Local": None,
                "Id_Tecnico_Visitante": None,
                "Suspensiones": None,
                "Observaciones": None,
                "Fuente_Pagina": Pagina,
                "Texto_Original": None,
                "Lineas_Originales": [],
            }
            if Fecha_Jugada_Pendiente:
                Partido_Actual["Fecha_Jugada"] = Fecha_Jugada_Pendiente
                Partido_Actual["Fecha"] = Fecha_Jugada_Pendiente
                Fecha_Jugada_Pendiente = None
            Etapa_Partido = "LOCAL"
        else:
            if Partido_Actual["Equipo_Visitante"] is None:
                Partido_Actual["Equipo_Visitante"] = Equipo
                Partido_Actual["Id_Equipo_Visitante"] = Obtener_Id(
                    "EQP",
                    Equipo,
                    "ARG",
                    Pagina,
                )
                Partido_Actual["Goles_Visitante"] = Goles
                Etapa_Partido = "VISITANTE"
            else:
                Finalizar_Partido()
                continue
        Partido_Actual["Lineas_Originales"].append(Linea)
        Indice += 1
        continue

    if Partido_Actual is not None:
        Partido_Actual["Lineas_Originales"].append(Linea)
        Linea_Sin_Acentos = Remover_Acentos(Linea).lower()
        if "adjudico los puntos" in Linea_Sin_Acentos:
            Partido_Actual["Resultado_Walkover"] = Partido_Actual[
                "Equipo_Local"
            ]
            Observaciones_Partido.append(Linea)

    if "ARBITRO" in Linea_Normal:
        if Partido_Actual:
            Registrar_Alineaciones(Pagina)
            Segmento = Linea
            if "RECAUDACION" in Linea_Normal:
                Partes = Linea.split("RECAUDACION", 1)
                Segmento = Partes[0]
                Recaud = Partes[1]
                Numero = Re.search(r"(\d[\d\.]+)", Recaud)
                if Numero:
                    Partido_Actual["Recaudacion"] = int(
                        Numero.group(1).replace(".", "")
                    )
            Arbitro = Segmento.split(":", 1)[-1].strip()
            Arbitro = Arbitro.strip(" .")
            if Arbitro:
                Partido_Actual["Arbitro_Principal"] = Arbitro
                Partido_Actual["Id_Arbitro_Principal"] = Obtener_Id(
                    "ARB",
                    Arbitro,
                    None,
                    Pagina,
                )
        Etapa_Partido = "EVENTOS"
        Indice += 1
        continue

    if Linea_Normal.startswith("CANCHA"):
        if Partido_Actual:
            Estadio = Linea.split(":", 1)[-1].strip()
            Partido_Actual["Estadio"] = Estadio
            Partido_Actual["Id_Estadio"] = Obtener_Id(
                "EST",
                Estadio,
                None,
                Pagina,
            )
        Indice += 1
        continue

    Resultado_Minuto = Patron_Minuto.search(Linea)
    if Resultado_Minuto and Partido_Actual:
        Minuto_Base = int(Resultado_Minuto.group(1))
        Texto_Evento_Completo = Linea
        Indice_Temp = Indice + 1
        while Indice_Temp < len(Lineas):
            Linea_Siguiente = Lineas[Indice_Temp]["Texto"]
            Linea_Sig_Normal = Remover_Acentos(Linea_Siguiente).upper()
            if Patron_Minuto.search(Linea_Siguiente):
                break
            if Es_Linea_Equipo(Linea_Siguiente):
                break
            if "ARBITRO" in Linea_Sig_Normal:
                break
            if "CANCHA" in Linea_Sig_Normal:
                break
            if "SE JUG" in Linea_Sig_Normal:
                break
            if "FECHA" in Linea_Sig_Normal:
                break
            if Re.search(r"\s+vs\.?\s+", Linea_Siguiente, flags = Re.IGNORECASE):
                break
            Texto_Evento_Completo = (
                f"{Texto_Evento_Completo} {Linea_Siguiente}"
            )
            Indice_Temp += 1
        Texto_Evento = Normalizar_Espacios(Texto_Evento_Completo)
        Texto_Sin_Acentos = Remover_Acentos(Texto_Evento).lower()
        Minuto = Minuto_Base * 100
        Minuto_Adicional = None

        Marcador = Patron_Marcador.search(Texto_Evento)
        if Marcador:
            Texto_Despues = Texto_Evento[Marcador.end():].strip()
            Texto_Busqueda = Texto_Despues
            Texto_Lower = Texto_Busqueda.lower()
            Delimitadores = [
                ",",
                ".",
                " con ",
                " de ",
                " tras ",
                " luego ",
                " despues ",
                " habilitado ",
                " pateo ",
                " cabeceo ",
            ]
            Corte = len(Texto_Busqueda)
            for Delimitador in Delimitadores:
                Posicion = Texto_Lower.find(Delimitador)
                if Posicion != -1:
                    Corte = min(Corte, Posicion)
            Nombre_Gol = Texto_Busqueda[:Corte].strip()
            Detalle = Texto_Busqueda[Corte:].strip()
            Goleador = Buscar_Jugador_Por_Alias(
                Nombre_Gol,
                Mapa_Alias_Partido,
            )
            if not Goleador:
                Goleador = Nombre_Gol
            Id_Goleador = None
            if Goleador in Ids_Por_Tipo["JUG"]:
                Id_Goleador = Ids_Por_Tipo["JUG"][Goleador]
            Tipo_Gol = Determinar_Tipo_Gol(Texto_Evento)
            Parte_Cuerpo, Es_Inferido, Detalle_Inf = (
                Determinar_Parte_Cuerpo(Texto_Evento)
            )
            Asistente, Inferido_Asis = Extraer_Asistencia(
                Texto_Evento,
                Mapa_Alias_Partido,
            )
            Id_Asistente = None
            if Asistente in Ids_Por_Tipo["JUG"]:
                Id_Asistente = Ids_Por_Tipo["JUG"][Asistente]
            Es_En_Contra = "en contra" in Texto_Sin_Acentos
            Inferido = Es_Inferido or Inferido_Asis
            Detalles_Inf = []
            if Detalle_Inf:
                Detalles_Inf.append(Detalle_Inf)
            if Inferido_Asis:
                Detalles_Inf.append("Asistencia inferida.")
            Equipo_Gol = Mapa_Jugador_Equipo.get(Goleador)
            Id_Equipo_Gol = None
            if Equipo_Gol == Partido_Actual["Equipo_Local"]:
                Id_Equipo_Gol = Partido_Actual["Id_Equipo_Local"]
            elif Equipo_Gol == Partido_Actual["Equipo_Visitante"]:
                Id_Equipo_Gol = Partido_Actual["Id_Equipo_Visitante"]
            Goles_Partido.append(
                {
                    "Id_Gol_Extraido": Generar_Id_Secuencial("GOL"),
                    "Id_Partido_Extraido": Partido_Actual[
                        "Id_Partido_Extraido"
                    ],
                    "Equipo": Equipo_Gol,
                    "Id_Equipo": Id_Equipo_Gol,
                    "Jugador": Goleador,
                    "Id_Jugador": Id_Goleador,
                    "Minuto": Minuto,
                    "Minuto_Adicional": Minuto_Adicional,
                    "Es_Tiempo_Extra": None,
                    "Tipo_Gol": Tipo_Gol,
                    "Parte_Cuerpo": Parte_Cuerpo,
                    "Zona_Gol": None,
                    "Asistencia": Asistente,
                    "Jugador_Asiste": Asistente,
                    "Id_Jugador_Asiste": Id_Asistente,
                    "Es_En_Contra": Es_En_Contra,
                    "Inferido": Inferido or None,
                    "Detalle_Inferencias": (
                        " | ".join(Detalles_Inf)
                        if Detalles_Inf
                        else None
                    ),
                    "Detalle_Descripcion": Detalle or None,
                    "Texto_Original": Texto_Evento,
                    "Fuente_Pagina": Pagina,
                }
            )

            if "penal" in Texto_Sin_Acentos:
                Equipo_Penal = Equipo_Gol
                Id_Equipo_Penal = Id_Equipo_Gol
                Equipo_Penal = Mapa_Jugador_Equipo.get(Jugador_Patea)
                Id_Equipo_Penal = None
                if Equipo_Penal == Partido_Actual["Equipo_Local"]:
                    Id_Equipo_Penal = Partido_Actual["Id_Equipo_Local"]
                elif Equipo_Penal == Partido_Actual["Equipo_Visitante"]:
                    Id_Equipo_Penal = Partido_Actual["Id_Equipo_Visitante"]
                Equipo_Penal = Mapa_Jugador_Equipo.get(Jugador_Patea)
                Id_Equipo_Penal = None
                if Equipo_Penal == Partido_Actual["Equipo_Local"]:
                    Id_Equipo_Penal = Partido_Actual[
                        "Id_Equipo_Local"
                    ]
                elif Equipo_Penal == Partido_Actual[
                    "Equipo_Visitante"
                ]:
                    Id_Equipo_Penal = Partido_Actual[
                        "Id_Equipo_Visitante"
                    ]
                Penales_Partido.append(
                    {
                        "Id_Penal_Extraido": Generar_Id_Secuencial("PEN"),
                        "Id_Partido_Extraido": Partido_Actual[
                            "Id_Partido_Extraido"
                        ],
                        "Equipo": Equipo_Penal,
                        "Id_Equipo": Id_Equipo_Penal,
                        "Jugador_Patea": Goleador,
                        "Id_Jugador_Patea": Id_Goleador,
                        "Jugador_Ataja": None,
                        "Id_Jugador_Ataja": None,
                        "Minuto": Minuto,
                        "Orden_Tanda": None,
                        "Resultado": "Convertido",
                        "Tipo_Penal": "En Partido",
                        "Es_Tiempo_Extra": None,
                        "Inferido": True,
                        "Detalle_Inferencias": "Penal convertido.",
                        "Observaciones": None,
                        "Texto_Original": Texto_Evento,
                        "Fuente_Pagina": Pagina,
                    }
                )

        else:
            if "penal" in Texto_Sin_Acentos:
                Jugador_Patea = None
                Jugador_Ataja = None
                Resultado = None
                Resultado_Ataja = Re.search(
                    r"([A-Za-z .']+) le ataj",
                    Texto_Sin_Acentos,
                )
                if Resultado_Ataja:
                    Jugador_Ataja = Resultado_Ataja.group(1).strip()
                Resultado_A = Re.search(
                    r"penal a ([A-Za-z .']+)",
                    Texto_Sin_Acentos,
                )
                if Resultado_A:
                    Jugador_Patea = Resultado_A.group(1).strip()
                Resultado_R = Re.search(
                    r"remate de ([A-Za-z .']+)",
                    Texto_Sin_Acentos,
                )
                if Resultado_R and not Jugador_Patea:
                    Jugador_Patea = Resultado_R.group(1).strip()
                if "ataj" in Texto_Sin_Acentos:
                    Resultado = "Atajado"
                elif "salio" in Texto_Sin_Acentos:
                    Resultado = "Desviado"
                elif "palo" in Texto_Sin_Acentos:
                    Resultado = "Desviado"
                Jugador_Patea = Buscar_Jugador_Por_Alias(
                    Jugador_Patea,
                    Mapa_Alias_Partido,
                )
                Jugador_Ataja = Buscar_Jugador_Por_Alias(
                    Jugador_Ataja,
                    Mapa_Alias_Partido,
                )
                Id_Patea = None
                Id_Ataja = None
                if Jugador_Patea in Ids_Por_Tipo["JUG"]:
                    Id_Patea = Ids_Por_Tipo["JUG"][Jugador_Patea]
                if Jugador_Ataja in Ids_Por_Tipo["JUG"]:
                    Id_Ataja = Ids_Por_Tipo["JUG"][Jugador_Ataja]
                Equipo_Penal = Mapa_Jugador_Equipo.get(Jugador_Patea)
                Id_Equipo_Penal = None
                if Equipo_Penal == Partido_Actual["Equipo_Local"]:
                    Id_Equipo_Penal = Partido_Actual[
                        "Id_Equipo_Local"
                    ]
                elif Equipo_Penal == Partido_Actual[
                    "Equipo_Visitante"
                ]:
                    Id_Equipo_Penal = Partido_Actual[
                        "Id_Equipo_Visitante"
                    ]
                Penales_Partido.append(
                    {
                        "Id_Penal_Extraido": Generar_Id_Secuencial("PEN"),
                        "Id_Partido_Extraido": Partido_Actual[
                            "Id_Partido_Extraido"
                        ],
                        "Equipo": Equipo_Penal,
                        "Id_Equipo": Id_Equipo_Penal,
                        "Jugador_Patea": Jugador_Patea,
                        "Id_Jugador_Patea": Id_Patea,
                        "Jugador_Ataja": Jugador_Ataja,
                        "Id_Jugador_Ataja": Id_Ataja,
                        "Minuto": Minuto,
                        "Orden_Tanda": None,
                        "Resultado": Resultado,
                        "Tipo_Penal": "En Partido",
                        "Es_Tiempo_Extra": None,
                        "Inferido": None,
                        "Detalle_Inferencias": None,
                        "Observaciones": Texto_Evento,
                        "Texto_Original": Texto_Evento,
                        "Fuente_Pagina": Pagina,
                    }
                )
            elif "expuls" in Texto_Sin_Acentos:
                Motivo = None
                if " por " in Texto_Sin_Acentos:
                    Motivo = Texto_Evento.split("por", 1)[-1].strip()
                Nombres = []
                if "expulsados" in Texto_Sin_Acentos:
                    Segmento = Texto_Sin_Acentos.split(
                        "expulsados",
                        1,
                    )[-1]
                    Segmento = Segmento.split("por", 1)[0]
                    Segmento = Segmento.replace(" y ", ",")
                    Nombres = [
                        Parte.strip()
                        for Parte in Segmento.split(",")
                        if Parte.strip()
                    ]
                elif "expulso" in Texto_Sin_Acentos:
                    Segmento = Texto_Sin_Acentos.split("a", 1)[-1]
                    Nombres = [Segmento.strip()]
                else:
                    Segmento = Texto_Sin_Acentos.split(
                        "expulsado",
                        1,
                    )[-1]
                    Segmento = Segmento.split("por", 1)[0]
                    Nombres = [Segmento.strip()]
                for Nombre in Nombres:
                    Nombre_Mapa = Buscar_Jugador_Por_Alias(
                        Nombre,
                        Mapa_Alias_Partido,
                    )
                    Jugador = Nombre_Mapa or Nombre
                    Id_Jugador = None
                    if Jugador in Ids_Por_Tipo["JUG"]:
                        Id_Jugador = Ids_Por_Tipo["JUG"][Jugador]
                    Equipo_Tarjeta = Mapa_Jugador_Equipo.get(Jugador)
                    Id_Equipo_Tarjeta = None
                    if Equipo_Tarjeta == Partido_Actual["Equipo_Local"]:
                        Id_Equipo_Tarjeta = Partido_Actual[
                            "Id_Equipo_Local"
                        ]
                    elif Equipo_Tarjeta == Partido_Actual[
                        "Equipo_Visitante"
                    ]:
                        Id_Equipo_Tarjeta = Partido_Actual[
                            "Id_Equipo_Visitante"
                        ]
                    Tarjetas_Partido.append(
                        {
                            "Id_Tarjeta_Extraida": Generar_Id_Secuencial(
                                "TAR"
                            ),
                            "Id_Partido_Extraido": Partido_Actual[
                                "Id_Partido_Extraido"
                            ],
                            "Equipo": Equipo_Tarjeta,
                            "Id_Equipo": Id_Equipo_Tarjeta,
                            "Jugador": Jugador,
                            "Id_Jugador": Id_Jugador,
                            "Tipo_Tarjeta": "Roja",
                            "Minuto": Minuto,
                            "Es_Tiempo_Extra": None,
                            "Motivo": Motivo,
                            "Inferido": None,
                            "Detalle_Inferencias": None,
                            "Observaciones": Texto_Evento,
                            "Texto_Original": Texto_Evento,
                            "Fuente_Pagina": Pagina,
                        }
                    )
            elif "lesion" in Texto_Sin_Acentos:
                Jugador = None
                Segmento = Texto_Sin_Acentos.split("lesionado", 1)
                if len(Segmento) > 1:
                    Jugador = Segmento[1].strip().split(" ")[0]
                Jugador = Buscar_Jugador_Por_Alias(
                    Jugador,
                    Mapa_Alias_Partido,
                )
                Id_Jugador = None
                if Jugador in Ids_Por_Tipo["JUG"]:
                    Id_Jugador = Ids_Por_Tipo["JUG"][Jugador]
                Equipo_Lesion = Mapa_Jugador_Equipo.get(Jugador)
                Id_Equipo_Lesion = None
                if Equipo_Lesion == Partido_Actual["Equipo_Local"]:
                    Id_Equipo_Lesion = Partido_Actual[
                        "Id_Equipo_Local"
                    ]
                elif Equipo_Lesion == Partido_Actual[
                    "Equipo_Visitante"
                ]:
                    Id_Equipo_Lesion = Partido_Actual[
                        "Id_Equipo_Visitante"
                    ]
                Lesiones_Partido.append(
                    {
                        "Id_Lesion_Extraida": Generar_Id_Secuencial("LES"),
                        "Id_Partido_Extraido": Partido_Actual[
                            "Id_Partido_Extraido"
                        ],
                        "Equipo": Equipo_Lesion,
                        "Id_Equipo": Id_Equipo_Lesion,
                        "Jugador": Jugador,
                        "Id_Jugador": Id_Jugador,
                        "Minuto": Minuto,
                        "Parte_Cuerpo": None,
                        "Lateralidad": None,
                        "Gravedad": None,
                        "Inferido": None,
                        "Detalle_Inferencias": None,
                        "Observaciones": Texto_Evento,
                        "Texto_Original": Texto_Evento,
                        "Fuente_Pagina": Pagina,
                    }
                )
            else:
                if "terminar el encuentro" in Texto_Sin_Acentos:
                    Suspensiones_Partido.append(Texto_Evento)
                else:
                    Observaciones_Partido.append(Texto_Evento)

        Indice = Indice_Temp
        continue

    if Partido_Actual and Etapa_Partido in ["LOCAL", "VISITANTE"]:
        if Etapa_Partido == "LOCAL":
            Lineas_Alineacion_Local.append(Linea)
        else:
            Lineas_Alineacion_Visitante.append(Linea)
        Indice += 1
        continue

    Indice += 1

Finalizar_Partido()

Columnas_Partido = [
    "Id_Partido_Extraido",
    "Torneo",
    "Fecha",
    "Fecha_Programada",
    "Fecha_Jugada",
    "Numero_Fecha",
    "Equipo_Local",
    "Equipo_Visitante",
    "Id_Equipo_Local",
    "Id_Equipo_Visitante",
    "Goles_Local",
    "Goles_Visitante",
    "Resultado_Walkover",
    "Arbitro_Principal",
    "Id_Arbitro_Principal",
    "Recaudacion",
    "Estadio",
    "Id_Estadio",
    "Publico",
    "Hora_Local",
    "Es_Neutral",
    "Tecnico_Local",
    "Tecnico_Visitante",
    "Id_Tecnico_Local",
    "Id_Tecnico_Visitante",
    "Suspensiones",
    "Observaciones",
    "Fuente_Pagina",
    "Texto_Original",
]

Columnas_Jugadores_Partido = [
    "Id_Registro",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador",
    "Id_Jugador",
    "Es_Titular",
    "Dorsal",
    "Posicion",
    "Capitan",
    "Inferido",
    "Detalle_Inferencias",
    "Observaciones",
    "Fuente_Pagina",
    "Texto_Original",
]

Columnas_Goles_Partido = [
    "Id_Gol_Extraido",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador",
    "Id_Jugador",
    "Minuto",
    "Minuto_Adicional",
    "Es_Tiempo_Extra",
    "Tipo_Gol",
    "Parte_Cuerpo",
    "Zona_Gol",
    "Asistencia",
    "Jugador_Asiste",
    "Id_Jugador_Asiste",
    "Es_En_Contra",
    "Inferido",
    "Detalle_Inferencias",
    "Detalle_Descripcion",
    "Texto_Original",
    "Fuente_Pagina",
]

Columnas_Penales_Partido = [
    "Id_Penal_Extraido",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador_Patea",
    "Id_Jugador_Patea",
    "Jugador_Ataja",
    "Id_Jugador_Ataja",
    "Minuto",
    "Orden_Tanda",
    "Resultado",
    "Tipo_Penal",
    "Es_Tiempo_Extra",
    "Inferido",
    "Detalle_Inferencias",
    "Observaciones",
    "Texto_Original",
    "Fuente_Pagina",
]

Columnas_Tarjetas_Partido = [
    "Id_Tarjeta_Extraida",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador",
    "Id_Jugador",
    "Tipo_Tarjeta",
    "Minuto",
    "Es_Tiempo_Extra",
    "Motivo",
    "Inferido",
    "Detalle_Inferencias",
    "Observaciones",
    "Texto_Original",
    "Fuente_Pagina",
]

Columnas_Lesiones_Partido = [
    "Id_Lesion_Extraida",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador",
    "Id_Jugador",
    "Minuto",
    "Parte_Cuerpo",
    "Lateralidad",
    "Gravedad",
    "Inferido",
    "Detalle_Inferencias",
    "Observaciones",
    "Texto_Original",
    "Fuente_Pagina",
]

Columnas_Cambios_Partido = [
    "Id_Cambio_Extraido",
    "Id_Partido_Extraido",
    "Equipo",
    "Id_Equipo",
    "Jugador_Sale",
    "Id_Jugador_Sale",
    "Jugador_Entra",
    "Id_Jugador_Entra",
    "Minuto",
    "Es_Tiempo_Extra",
    "Motivo",
    "Inferido",
    "Detalle_Inferencias",
    "Observaciones",
    "Texto_Original",
    "Fuente_Pagina",
]

Columnas_Catalogos = [
    "Tipo",
    "Id",
    "Nombre",
    "Observaciones",
    "Fuente_Pagina",
    "Texto_Original",
]

Hoja_Partido = Pandas.DataFrame(
    Partidos,
    columns = Columnas_Partido,
)

Hoja_Jugadores_Partido = Pandas.DataFrame(
    Jugadores_Partido,
    columns = Columnas_Jugadores_Partido,
)

Hoja_Goles_Partido = Pandas.DataFrame(
    Goles_Partido,
    columns = Columnas_Goles_Partido,
)

Hoja_Penales_Partido = Pandas.DataFrame(
    Penales_Partido,
    columns = Columnas_Penales_Partido,
)

Hoja_Tarjetas_Partido = Pandas.DataFrame(
    Tarjetas_Partido,
    columns = Columnas_Tarjetas_Partido,
)

Hoja_Lesiones_Partido = Pandas.DataFrame(
    Lesiones_Partido,
    columns = Columnas_Lesiones_Partido,
)

Hoja_Cambios_Partido = Pandas.DataFrame(
    Cambios_Partido,
    columns = Columnas_Cambios_Partido,
)

Hoja_Catalogos = Pandas.DataFrame(
    Catalogos,
    columns = Columnas_Catalogos,
)

with Pandas.ExcelWriter(
    "Prueba.xlsx",
    engine = "openpyxl",
) as Escritor:
    Hoja_Partido.to_excel(
        Escritor,
        sheet_name = "Partido",
        index = False,
    )
    Hoja_Jugadores_Partido.to_excel(
        Escritor,
        sheet_name = "Jugadores_Partido",
        index = False,
    )
    Hoja_Goles_Partido.to_excel(
        Escritor,
        sheet_name = "Goles_Partido",
        index = False,
    )
    Hoja_Penales_Partido.to_excel(
        Escritor,
        sheet_name = "Penales_Partido",
        index = False,
    )
    Hoja_Tarjetas_Partido.to_excel(
        Escritor,
        sheet_name = "Tarjetas_Partido",
        index = False,
    )
    Hoja_Lesiones_Partido.to_excel(
        Escritor,
        sheet_name = "Lesiones_Partido",
        index = False,
    )
    Hoja_Cambios_Partido.to_excel(
        Escritor,
        sheet_name = "Cambios_Partido",
        index = False,
    )
    Hoja_Catalogos.to_excel(
        Escritor,
        sheet_name = "Catalogos",
        index = False,
    )
