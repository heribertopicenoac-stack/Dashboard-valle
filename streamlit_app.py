# DOCUMENTACIÓN REALIZADA POR HERIBERTO PICENO ACOSTA TSU
import streamlit as st
import pandas as pd
import plotly.express as px
import re
import concurrent.futures
import time
import urllib.request
import urllib.error
import requests
import io
import base64
import os
from pathlib import Path

st.set_page_config(
    page_title="Dashboard AD Desarrollo",
    page_icon="Valle2027.png",
    layout="wide"
)

FONDO_PAGINA   = "#f8f9fa"
FONDO_SIDEBAR  = "#ffffff"
GUINDA_OFICIAL = "#601a1e"
DORADO_OFICIAL = "#f1b80c"
VERDE_OFICIAL  = "#117a4b"
TEXTO_DARK     = "#212529"
BORDE_SUAVE    = "#e9ecef"


# ── MODO OSCURO AUTO (detecta el sistema operativo del usuario) ────────────────
import streamlit.components.v1 as _components

_components.html("""
<script>
(function() {
    const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const msg  = { type: 'streamlit:setComponentValue', value: dark };
    // Enviar al session_state via query param hack
    if (dark) {
        const url = new URL(window.parent.location.href);
        if (!url.searchParams.get('_dark')) {
            url.searchParams.set('_dark', '1');
            window.parent.history.replaceState({}, '', url);
            window.parent.location.reload();
        }
    } else {
        const url = new URL(window.parent.location.href);
        if (url.searchParams.get('_dark')) {
            url.searchParams.delete('_dark');
            window.parent.history.replaceState({}, '', url);
            window.parent.location.reload();
        }
    }
    // Escuchar cambios en tiempo real
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const url = new URL(window.parent.location.href);
        if (e.matches) {
            url.searchParams.set('_dark', '1');
        } else {
            url.searchParams.delete('_dark');
        }
        window.parent.history.replaceState({}, '', url);
        window.parent.location.reload();
    });
})();
</script>
""", height=0)

import urllib.parse as _up
_qp     = st.query_params
DARK    = _qp.get("_dark", "0") == "1"
SECCION = _qp.get("seccion", "principal")

if DARK:
    BG_PAGE    = "#0e1117"
    BG_SIDEBAR = "#1a1d24"
    BG_CARD    = "#1e2130"
    TXT_MAIN   = "#e8eaf0"
    TXT_MUTED  = "#8b8fa8"
    BORDER_C   = "#2d3147"
else:
    BG_PAGE    = FONDO_PAGINA
    BG_SIDEBAR = FONDO_SIDEBAR
    BG_CARD    = "#ffffff"
    TXT_MAIN   = TEXTO_DARK
    TXT_MUTED  = "#6c757d"
    BORDER_C   = BORDE_SUAVE

# Estilos optimizados para evitar conflictos de especificidad CSS
st.markdown(f"""
<style>
.stApp {{ background-color:{BG_PAGE}!important; color:{TXT_MAIN}!important; }}

/* Configuración de la barra lateral sin selectores universales agresivos */
[data-testid="stSidebar"] {{
    background-color:{BG_SIDEBAR}!important;
    border-right:1px solid {BORDER_C};
    color:{TXT_MAIN};
}}
[data-testid="stSidebar"] .stMarkdown p {{ color:{TXT_MAIN}; }}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ color:{TXT_MAIN}!important; }}

/* Contenedores de métricas estándar */
[data-testid="stMetricSimpleValue"],[data-testid="stMetric"],
div[data-testid="metric-container"],.stMetric {{
    background-color:{BG_CARD}!important;
    border-left:5px solid {GUINDA_OFICIAL}!important;
    border-top:1px solid {BORDER_C}!important;
    border-right:1px solid {BORDER_C}!important;
    border-bottom:1px solid {BORDER_C}!important;
    border-radius:8px!important; padding:15px!important;
    box-shadow:0 4px 6px rgba(0,0,0,0.1)!important;
}}
[data-testid="stMetricLabel"] p {{ color:{TXT_MUTED}!important; font-weight:500!important; }}
[data-testid="stMetricValue"] div {{ color:{GUINDA_OFICIAL}!important; font-weight:bold!important; }}

/* Botones nativos y de descarga */
.stButton>button, .stDownloadButton>button {{
    background-color:{VERDE_OFICIAL}!important; color:white!important;
    border-radius:6px!important; border:none!important;
    transition:all 0.3s ease; font-weight:bold!important;
}}

/* Forzar que el texto y los iconos internos de los botones permanezcan blancos */
.stButton>button *, .stDownloadButton>button * {{
    color: white !important;
    text-decoration: none !important;
}}

.stButton>button:hover, .stDownloadButton>button:hover {{
    background-color:{GUINDA_OFICIAL}!important; color:white!important;
    box-shadow:0 4px 8px rgba(0,0,0,0.2);
}}

hr {{ border-top:1px solid {GUINDA_OFICIAL}!important; opacity:0.2; }}
img {{ max-width:100%; }}
p, h1, h2, h3, h4 {{ color:{TXT_MAIN}!important; }}

[data-testid="stExpander"] {{
    background-color:{BG_CARD}!important;
    border:1px solid {BORDER_C}!important;
}}
.stSelectbox > div > div, .stMultiSelect > div > div {{
    background-color:{BG_CARD}!important;
    color:{TXT_MAIN}!important;
    border-color:{BORDER_C}!important;
}}
[data-testid="stDataFrame"] {{ background-color:{BG_CARD}!important; }}

/* Clase para forzar texto blanco e inmunidad en botones HTML del menú */
.btn-html-sidebar, .btn-html-sidebar * {{
    color: #ffffff !important;
}}
.btn-html-sidebar .subtexto-btn {{
    color: rgba(255,255,255,0.75) !important;
}}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    try:
        st.image("Valle2027.png", use_container_width=True)
    except:
        st.markdown(f"""<div style='background-color:{GUINDA_OFICIAL};padding:20px;
            border-radius:8px;text-align:center;margin-bottom:10px;'>
            <h3 style='color:white;margin:0;font-size:1.2rem;'>VALLE DE SANTIAGO</h3>
            <p style='color:{DORADO_OFICIAL};margin:5px 0 0;font-size:0.8rem;
            letter-spacing:2px;'>PRESIDENCIA MUNICIPAL</p></div>""", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;color:{GUINDA_OFICIAL};font-weight:bold;"
                f"margin-top:10px;margin-bottom:20px;'>Administración 2024 - 2027</div>",
                unsafe_allow_html=True)
    st.divider()

# ── FOTOS DE PERFIL ────────────────────────────────────────────────────────────
FOTOS_DIR = Path("fotos")

def get_foto_path(nombre: str):
    """Devuelve Path si existe foto real, o None si hay que usar avatar SVG."""
    for ext in ("png", "jpg", "jpeg", "webp", "avif" ):
        ruta = FOTOS_DIR / f"{nombre}.{ext}"
        if ruta.exists():
            return ruta
    fallback = Path("ValleFoto.webp")
    if fallback.exists():
        return fallback
    return None

def get_avatar_svg(nombre: str) -> str:
    """Genera avatar SVG con iniciales como data URI."""
    iniciales = "".join(p[0].upper() for p in nombre.split()[:2] if p)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
        f'<circle cx="50" cy="50" r="50" fill="{GUINDA_OFICIAL}"/>'
        f'<text x="50" y="58" font-family="Arial" font-size="32" '
        f'fill="white" text-anchor="middle" font-weight="bold">{iniciales}</text>'
        f'</svg>'
    )
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

# Mantener compatibilidad con código de capacitaciones que usa get_foto_b64
@st.cache_data(show_spinner=False)
def get_foto_b64(nombre: str) -> str:
    ruta = get_foto_path(nombre)
    if ruta:
        data = ruta.read_bytes()
        ext  = ruta.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return get_avatar_svg(nombre)

# ══════════════════════════════════════════════════════════════════════════
# ── ÁREAS Y COLABORADORES: DESCUBRIMIENTO AUTOMÁTICO DESDE GOOGLE DRIVE ─────
# ══════════════════════════════════════════════════════════════════════════
#
# Estructura que debes crear UNA sola vez en Drive (ya no se toca el código
# nunca más, solo se mueven/crean carpetas y archivos):
#
#   📁 Carpeta raíz  (su ID va en secrets["root_folder_id"])
#      📁 Adquisiciones                 <- el nombre de la carpeta = nombre del área
#         📄 Adriana Paola Vargas Ramirez   <- Google Sheet, nombre = nombre del colaborador
#         📄 Ana María Alvarado Hernandez
#      📁 Jurídico
#         📄 Batriz Adriana Ramirez Garcia
#         📁 Berenice Butanda Granados      <- si aún NO tiene Excel, crea una
#                                              carpeta vacía con su nombre: el
#                                              dashboard la marcará "PENDIENTE"
#                                              automáticamente, igual que antes.
#
# Requisitos (una sola vez):
#   1) En Google Cloud Console habilita la "Google Drive API" y crea una
#      API key (restríngela a esa API).
#   2) Comparte la carpeta raíz como "Cualquiera con el enlace - Lector"
#      (el mismo nivel de acceso que ya usas para exportar los Excel).
#   3) Guarda esto en .streamlit/secrets.toml:
#         drive_api_key   = "TU_API_KEY"
#         root_folder_id  = "ID_DE_LA_CARPETA_RAIZ"
#
# A partir de ahí: agregar un área = crear una carpeta. Agregar una persona
# = subir su Google Sheet dentro de la carpeta del área. Un clic en
# "🔄 Sincronizar Drive" (o esperar el TTL de la caché) y aparece solo.

# ⚠️ CORRECCIÓN DE SEGURIDAD: ya NO se deja la API key ni el folder id como
# valor por defecto (fallback) dentro del código. Si el repositorio es
# público en GitHub, Google detecta la key expuesta y la deshabilita
# automáticamente, lo cual provocaba los errores 403 intermitentes.
# Configura estos valores únicamente en `.streamlit/secrets.toml` (local) o
# en "Secrets" del panel de Streamlit Cloud (producción).
DRIVE_API_KEY  = st.secrets.get("drive_api_key", "")
ROOT_FOLDER_ID = st.secrets.get("root_folder_id", "")

_MIME_SHEET     = "application/vnd.google-apps.spreadsheet"
_MIME_XLSX      = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
_MIME_XLS       = "application/vnd.ms-excel"
_MIME_FOLDER    = "application/vnd.google-apps.folder"
_MIME_SHORTCUT  = "application/vnd.google-apps.shortcut"
_MIMES_HOJA     = {_MIME_SHEET, _MIME_XLSX, _MIME_XLS}

# Mapa file_id -> mimeType, se llena al descubrir las áreas y lo usa
# descargar_excel() para saber si debe "exportar" (Google Sheet nativo)
# o "descargar tal cual" (.xlsx/.xls subido directamente a Drive).
_MIME_POR_ID = {}


def _listar_hijos_drive(folder_id: str, api_key: str, mime: str = None):
    """Lista los archivos/carpetas hijos directos de folder_id vía Drive API v3."""
    base = "https://www.googleapis.com/drive/v3/files"
    q = f"'{folder_id}' in parents and trashed = false"
    if mime:
        q += f" and mimeType = '{mime}'"
    params = {"q": q, "key": api_key,
               "fields": "nextPageToken, files(id,name,mimeType,shortcutDetails)",
               "pageSize": 1000}
    items, token = [], None
    while True:
        if token:
            params["pageToken"] = token
        r = requests.get(base, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("files", []))
        token = data.get("nextPageToken")
        if not token:
            break
    return items


@st.cache_data(ttl=1800, show_spinner=False)
def descubrir_areas_desde_drive(root_id: str, api_key: str):
    """
    Recorre la carpeta raíz en Drive y construye el mismo diccionario
    AREAS = {"Área": {"Colaborador": file_id_o_'PENDIENTE'}} que antes
    se escribía a mano, pero leído en vivo desde Drive. También regresa
    un mapa file_id -> mimeType para saber cómo descargar cada archivo
    (Google Sheet nativo vs .xlsx/.xls subido directo).
    """
    areas, mimes = {}, {}
    carpetas_area = _listar_hijos_drive(root_id, api_key, mime=_MIME_FOLDER)

    for carpeta in sorted(carpetas_area, key=lambda x: x["name"].strip().lower()):
        area_nombre = carpeta["name"].strip()
        hijos = _listar_hijos_drive(carpeta["id"], api_key)

        colaboradores = {}
        for h in hijos:
            nombre    = h["name"].strip()
            mime_real = h["mimeType"]
            id_real   = h["id"]

            # Si es un "acceso directo" de Drive, se resuelve al archivo real
            # que apunta (mismo nombre visible, pero id y mimeType distintos).
            if mime_real == _MIME_SHORTCUT:
                sd = h.get("shortcutDetails", {}) or {}
                id_real   = sd.get("targetId", id_real)
                mime_real = sd.get("targetMimeType", mime_real)

            # quita la extensión visible si subieron "Nombre.xlsx"
            nombre = re.sub(r'\.(xlsx|xls)$', '', nombre, flags=re.IGNORECASE).strip()
            if mime_real in _MIMES_HOJA:
                colaboradores[nombre] = id_real
                mimes[id_real] = mime_real
            elif mime_real == _MIME_FOLDER:
                # carpeta con el nombre de la persona pero sin Excel aún
                colaboradores.setdefault(nombre, "PENDIENTE")

        areas[area_nombre] = dict(sorted(colaboradores.items(),
                                          key=lambda kv: kv[0].lower()))
    return areas, mimes


if not DRIVE_API_KEY or not ROOT_FOLDER_ID:
    st.error(
        "⚠️ Falta configurar `drive_api_key` y `root_folder_id` en "
        "`.streamlit/secrets.toml` para poder leer las áreas y colaboradores "
        "automáticamente desde Google Drive."
    )
    st.stop()

try:
    AREAS, _mimes_encontrados = descubrir_areas_desde_drive(ROOT_FOLDER_ID, DRIVE_API_KEY)
    _MIME_POR_ID.update(_mimes_encontrados)
except Exception as e:
    st.error(f"⚠️ No se pudo leer la estructura de áreas desde Drive: {e}")
    AREAS = st.session_state.get("_ultimo_areas_ok", {})
    _MIME_POR_ID.update(st.session_state.get("_ultimo_mimes_ok", {}))

if AREAS:
    st.session_state["_ultimo_areas_ok"]  = AREAS
    st.session_state["_ultimo_mimes_ok"]  = dict(_MIME_POR_ID)
else:
    st.warning("No se encontraron áreas en la carpeta raíz de Drive. "
               "Verifica que la carpeta tenga subcarpetas y que esté "
               "compartida como 'Cualquiera con el enlace'.")

ORDEN_MESES_BASE = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
                    "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
ORDEN_MESES = [f"{m} {y}" for y in ["2024","2025","2026","2027"] for m in ORDEN_MESES_BASE]

PALETA = ["#601a1e","#117a4b","#f1b80c","#2c3e50","#d35400","#7d3c98","#16a085","#2e4053"]

def get_color_map(colaboradores):
    return {c: PALETA[i % len(PALETA)] for i, c in enumerate(sorted(colaboradores))}

def normalizar(t):
    return str(t).translate(str.maketrans(
        "áéíóúüñÁÉÍÓÚÜÑ","aeiouunAEIOUUN")).lower().strip()

_MESES_DICT = {
    "ENERO":      ["ENERO","ENE","ENR","ENREO"],
    "FEBRERO":    ["FEBRERO","FEB","FEBR","FEBERERO"],
    "MARZO":      ["MARZO","MAR","MRZ","MARSO"],
    "ABRIL":      ["ABRIL","ABR","ABRL"],
    "MAYO":       ["MAYO","MAY","MAI"],
    "JUNIO":      ["JUNIO","JUN","JNO","JUNOI"],
    "JULIO":      ["JULIO","JUL","JLO","JULLIO"],
    "AGOSTO":     ["AGOSTO","AGO","AGS","AGOS"],
    "SEPTIEMBRE": ["SEPTIEMBRE","SEP","SEPT","SETIEMBRE","SEPTIEMRE","SEPTBRE"],
    "OCTUBRE":    ["OCTUBRE","OCT","OCUBRE","OCTBRE"],
    "NOVIEMBRE":  ["NOVIEMBRE","NOV","NVIEMBRE","NOVBRE"],
    "DICIEMBRE":  ["DICIEMBRE","DIC","DICIEMRE","DIZ","DICBRE"],
}
_PAT_ANIO  = re.compile(r'\b(202[4-7]|[2][4-7])\b')
_TRANS_ACC = str.maketrans("ÁÉÍÓÚÜÑ","AEIOUUN")

def formatear_mes_anio(texto):
    if not texto or (isinstance(texto, float) and pd.isna(texto)):
        return None
    limpio = str(texto).upper().translate(_TRANS_ACC)
    limpio = limpio.replace('-',' ').replace('/',' ').replace('_',' ')
    limpio = limpio.replace(r'\s+',' ').strip()
    anio = "2026"
    m = _PAT_ANIO.search(limpio)
    if m:
        anio = m.group(1)
        if len(anio) == 2: anio = "20" + anio
        limpio = limpio.replace(m.group(0),'').strip()
    for mes_std, variaciones in _MESES_DICT.items():
        if any(v in limpio for v in variaciones):
            return f"{mes_std} {anio}"
    return None

def es_tab_mes(nombre):
    n      = str(nombre).strip()
    n_norm = n.lower().replace(" ","").replace("_","").replace("-","")
    if n_norm.startswith("resumen"):
        return formatear_mes_anio(n) is not None
    return formatear_mes_anio(n) is not None

def limpiar_pct(valor):
    if pd.isna(valor): return None
    s = str(valor).strip()
    if s.startswith("#") or s in ("","-","N/A","NA"): return None
    try:
        s_clean = s.replace("%","").strip()
        n = float(s_clean)
        if "%" not in s and 0 <= n <= 1.5:
            n = n * 100
        return round(min(n, 119.0), 1)
    except:
        return None

PAT_CAP = re.compile(
    r'capacitaci[oó]n(es)?(\s*(tomadas?|recibidas?|acreditadas?|formales?|cursadas?))?',
    re.IGNORECASE)

PALABRAS_NEG = {
    "ninguna","ninguno","-","n/a","na","observaciones","actividades",
    "periodo","evaluacion","rendimiento","promedio","total","semana",
    "fecha","calificacion","porcentaje","si","no","nombre",
    "dependencia","area","firma","na",
    "total de actividades","#div/0!","#div/0","#ref!","#value!",
    "#n/a","#null!","#num!","error","div/0",
}

def _es_texto_valido_cap(txt: str) -> bool:
    if not txt or len(txt) < 5:
        return False
    if txt.upper().startswith("#"):
        return False
    if re.match(r'^[\d\.\%\,\-\#\s]+$', txt):
        return False
    txt_norm = normalizar(txt)
    if txt_norm in PALABRAS_NEG:
        return False
    for palabra in ["total de actividades","periodo de evaluacion",
                    "rendimiento","promedio general","calificacion"]:
        if palabra in txt_norm:
            return False
    return True

def _resolver_mime(file_id: str) -> str:
    """Si no conocemos el mimeType de un file_id (p.ej. el del Ranking, que
    no pasa por el descubrimiento de áreas), se le pregunta a Drive."""
    mime = _MIME_POR_ID.get(file_id)
    if mime:
        return mime
    if not DRIVE_API_KEY:
        return ""
    try:
        r = requests.get(
            f"https://www.googleapis.com/drive/v3/files/{file_id}",
            params={"key": DRIVE_API_KEY, "fields": "mimeType"},
            timeout=15,
        )
        r.raise_for_status()
        mime = r.json().get("mimeType", "")
        _MIME_POR_ID[file_id] = mime
        return mime
    except Exception:
        return ""


def descargar_excel(file_id: str, reintentos: int = 5, timeout: int = 15):
    """
    Descarga el Excel/Google Sheet indicado por file_id.

    ⚠️ CORRECCIÓN: se subió `reintentos` de 3 a 5 y el backoff pasó de
    lineal (1.5s, 3s, 4.5s) a exponencial (2s, 4s, 8s, 16s). Los 403 con
    la página HTML genérica "Sorry... Google" suelen ser bloqueos
    TEMPORALES por rate-limiting a nivel de proyecto; con más intentos y
    más tiempo de espera entre ellos, la app se recupera sola sin que el
    usuario tenga que dar clic en "Sincronizar Drive" manualmente.

    Si Google responde con un error HTTP (403, 404, etc.), se captura
    el cuerpo de la respuesta (donde Google explica la causa real: archivo
    no compartido, API key con restricciones de referrer, API deshabilitada,
    etc.) y se incluye en el mensaje de la excepción, en vez de mostrar
    solo "HTTP Error 403: Forbidden". Además, si el cuerpo es HTML (la
    página "Sorry..." de Google) en vez de JSON, se traduce a un mensaje
    más claro para el usuario final.
    """
    if not file_id or file_id.upper() in ("PENDIENTE", ""):
        raise ValueError("ID pendiente")

    mime = _resolver_mime(file_id)
    if mime == _MIME_SHEET:
        # Google Sheet nativo -> se exporta a xlsx
        url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    else:
        # .xlsx/.xls subido directo a Drive (o mimeType desconocido) -> se
        # descarga el binario tal cual vía la Drive API.
        if DRIVE_API_KEY:
            url = (f"https://www.googleapis.com/drive/v3/files/{file_id}"
                   f"?alt=media&key={DRIVE_API_KEY}")
        else:
            url = f"https://drive.google.com/uc?export=download&id={file_id}"

    ultimo_error = None
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/124.0 Safari/537.36")
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return io.BytesIO(resp.read())
        except urllib.error.HTTPError as e:
            # Capturamos el cuerpo del error: Google normalmente devuelve un
            # JSON o HTML explicando la causa exacta del 403/404/etc.
            try:
                cuerpo = e.read().decode("utf-8", errors="ignore")[:500]
            except Exception:
                cuerpo = "(no se pudo leer el cuerpo de la respuesta)"

            if "<html" in cuerpo.lower():
                cuerpo = ("Google bloqueó temporalmente la solicitud (rate "
                          "limiting, API key inválida/restringida, o error "
                          "transitorio de Google). Reintentando...")

            ultimo_error = Exception(f"HTTP {e.code} en {url}\nRespuesta de Google: {cuerpo}")
            if intento < reintentos - 1:
                time.sleep(2 * (2 ** intento))  # 2s, 4s, 8s, 16s
        except Exception as e:
            ultimo_error = e
            if intento < reintentos - 1:
                time.sleep(2 * (2 ** intento))
    raise ultimo_error

@st.cache_data(ttl=21600, show_spinner=False)
def obtener_datos(alias: str, file_id: str, area: str):
    alias = alias.strip()
    debug = []
    try:
        raw        = descargar_excel(file_id)
        excel_data = pd.read_excel(raw, sheet_name=None, header=None, engine="openpyxl")
    except Exception as e:
        return [], [], [], [f"Error: {e}"]

    resumenes, semanas, caps = [], [], []

    for tab_name, df in excel_data.items():
        if not es_tab_mes(tab_name):
            continue
        mes    = formatear_mes_anio(tab_name) or str(tab_name).upper()
        debug.append(f"'{tab_name}' → {mes}")
        n_rows, n_cols = df.shape
        periodos, totales = {}, {}

        for i in range(n_rows):
            for j in range(n_cols):
                val = df.iat[i, j]
                if pd.isna(val): continue
                s = str(val).strip()

                if re.search(r'PERIODO\s*DE\s*EVALUACI', s, re.IGNORECASE):
                    for k in range(j+1, min(j+20, n_cols)):
                        v2 = df.iat[i, k]
                        if pd.notna(v2) and str(v2).strip():
                            periodos[i] = str(v2).strip(); break

                if re.search(r'TOTAL\s*DE\s*ACTIVIDADES', s, re.IGNORECASE):
                    for k in range(n_cols-1, -1, -1):
                        pct = limpiar_pct(df.iat[i, k])
                        if pct is not None and pct > 0:
                            totales[i] = pct; break
                    if i not in totales:
                        nums = []
                        for k in range(n_cols):
                            v = df.iat[i, k]
                            if pd.notna(v):
                                try:
                                    n = float(str(v).replace("%","").strip())
                                    if 1 <= n <= 500: nums.append(n)
                                except: pass
                        if len(nums) >= 2:
                            proy, real = nums[-2], nums[-1]
                            if proy > 0:
                                totales[i] = round(min((real/proy)*100, 119.0), 1)

                if PAT_CAP.fullmatch(s.strip()):
                    for k in range(j+1, n_cols):
                        v = df.iat[i, k]
                        if pd.isna(v): continue
                        txt = str(v).strip()
                        if _es_texto_valido_cap(txt):
                            caps.append({"Área":area,"Colaborador":alias,
                                         "Mes":mes,"Capacitación":txt})
                    for di in range(1, 10):
                        ni = i + di
                        if ni >= n_rows: break
                        v = df.iat[ni, j]
                        if pd.isna(v) or not str(v).strip():
                            v = df.iat[ni, j+1] if j+1 < n_cols else None
                        if v is None or pd.isna(v) or not str(v).strip(): break
                        txt = str(v).strip()
                        if PAT_CAP.fullmatch(txt): break
                        if re.match(r'^[\d\.\%\,\-\#]+$', txt): break
                        if normalizar(txt) in PALABRAS_NEG: break
                        if _es_texto_valido_cap(txt):
                            caps.append({"Área":area,"Colaborador":alias,
                                         "Mes":mes,"Capacitación":txt})

        sem_tab, usados = [], set()
        for fp in sorted(periodos):
            for ft in sorted(totales):
                if ft > fp and ft not in usados:
                    p   = periodos[fp]
                    m_re = re.match(r'(\d+)', p)
                    sem_tab.append({
                        "Área": area, "Colaborador": alias,
                        "Mes": formatear_mes_anio(p) or mes,
                        "Periodo": p, "Rendimiento": totales[ft],
                        "_orden": int(m_re.group(1)) if m_re else 99,
                    })
                    usados.add(ft); break

        semanas.extend(sem_tab)
        if sem_tab:
            prom = sum(x["Rendimiento"] for x in sem_tab) / len(sem_tab)
            resumenes.append({"Área":area,"Colaborador":alias,
                               "Mes":mes,"Promedio Mes":round(prom,1)})

    if not debug:
        tabs  = ", ".join(f"'{t}'" for t in excel_data.keys())
        debug = [f"Ninguna pestaña de mes encontrada. Pestañas: {tabs}"]

    return resumenes, semanas, caps, debug

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
st.sidebar.header("Panel de Control")

if st.sidebar.button("🔄 Sincronizar Drive", use_container_width=True):
    st.cache_data.clear()
    for k in ["global_df","global_ok"]:
        st.session_state.pop(k, None)
    st.rerun()

st.sidebar.markdown("<br>", unsafe_allow_html=True)

dark_val = "1" if DARK else "0"

# Botón HTML 1: Ranking
st.sidebar.markdown(f"""
<a href="?_dark={dark_val}&seccion=ranking" target="_self" style="text-decoration:none;">
<div class="btn-html-sidebar" style='background:linear-gradient(135deg,{GUINDA_OFICIAL},{GUINDA_OFICIAL}cc);
     border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;
     box-shadow:0 3px 10px rgba(96,26,30,0.2);'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.4rem;'></span>
    <div>
      <div style='font-weight:700;font-size:0.88rem;line-height:1.3;'>
        Ranking de Reportes Trimestrales</div>
      <div class="subtexto-btn" style='font-size:0.72rem;margin-top:2px;'>
        Ingresar al apartado</div>
    </div>
  </div>
</div>
</a>
""", unsafe_allow_html=True)

# Botón HTML 2 (NUEVO): Sistema de Evaluación de Desempeño
st.sidebar.markdown(f"""
<a href="?_dark={dark_val}&seccion=desempeno" target="_self" style="text-decoration:none;">
<div class="btn-html-sidebar" style='background:linear-gradient(135deg,{DORADO_OFICIAL},{DORADO_OFICIAL}cc);
     border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;
     box-shadow:0 3px 10px rgba(241,184,12,0.2);'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.4rem;'></span>
    <div>
      <div style='font-weight:700;font-size:0.88rem;line-height:1.3;'>
        Sistema de Evaluación de Desempeño</div>
      <div class="subtexto-btn" style='font-size:0.72rem;margin-top:2px;'>
        Ingresar al dashboard principal</div>
    </div>
  </div>
</div>
</a>
""", unsafe_allow_html=True)

# Botón HTML 3: Resultados
st.sidebar.markdown(f"""
<a href="?_dark={dark_val}&seccion=resultados" target="_self" style="text-decoration:none;">
<div class="btn-html-sidebar" style='background:linear-gradient(135deg,{VERDE_OFICIAL},{VERDE_OFICIAL}cc);
     border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;
     box-shadow:0 3px 10px rgba(17,122,75,0.2);'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.4rem;'></span>
    <div>
      <div style='font-weight:700;font-size:0.88rem;line-height:1.3;'>
        Resultados del Programa de Evaluación</div>
      <div class="subtexto-btn" style='font-size:0.72rem;margin-top:2px;'>
        Ingresar al apartado</div>
    </div>
  </div>
</div>
</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ── RUTEO DE PÁGINAS ────────────────────────────────────────────────────────
# 1. Página Principal (Solo muestra la imagen responsiva)
if SECCION == "principal":
    try:
        st.image("fondo.png", use_container_width=True)
    except Exception:
        st.warning("⚠️ No se encontró la imagen 'fondo.png'. Asegúrate de que esté en la misma carpeta que este script.")
    st.stop()

# 2. Apartados en construcción (Resultados)
elif SECCION == "resultados":
    st.markdown(f"<h1 style='color:{GUINDA_OFICIAL};margin-bottom:0;'> 📋 Resultados del Programa de Evaluación</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6c757d;font-size:1.1rem;'>H. Ayuntamiento de Valle de Santiago</p>", unsafe_allow_html=True)
    st.divider()
    
    st.info("ℹ️ Este apartado se encuentra actualmente vacío. Próximamente se integrará la información correspondiente.")
    
    html_volver = f"""
    <a href="?_dark={dark_val}&seccion=principal" target="_self" style="text-decoration:none; color:#ffffff !important;">
        <div style='background:{VERDE_OFICIAL}; color:#ffffff !important; padding:10px 20px; border-radius:6px; display:inline-block; font-weight:bold; box-shadow:0 2px 5px rgba(0,0,0,0.15); font-family:Arial,sans-serif;'>
            Volver a la Página Principal
        </div>
    </a>
    """
    st.markdown(html_volver, unsafe_allow_html=True)
    st.stop()


# 3. Lógica de extracción de datos desde Google Sheets (Dinámica para hojas trimestrales)
@st.cache_data(ttl=3600, show_spinner=False)
def obtener_datos_ranking():
    file_id = "1Bqd1lxSQg0Q8AIw7UuNScshXbV7V74DY"
    try:
        raw = descargar_excel(file_id)
        excel_data = pd.read_excel(raw, sheet_name=None, engine="openpyxl")
    except Exception as e:
        return None, f"Error al descargar o leer el archivo de ranking: {e}"

    all_rankings = []
    pestañas_procesadas = set() # Control para evitar duplicados
    
    for tab_name, df in excel_data.items():
        # FILTRO: Solo procesar si el nombre de la pestaña contiene "RANKING"
        # y si no la hemos procesado ya anteriormente.
        if "RANKING" not in str(tab_name).upper() or tab_name in pestañas_procesadas:
            continue
            
        header_idx = -1
        # Búsqueda adaptativa de los encabezados reales
        for i in range(min(15, len(df))):
            row_vals = [str(x).upper() for x in df.iloc[i].values]
            if any("DEPENDENCIA" in str(v) for v in row_vals) and any("TOTAL" in str(v) for v in row_vals):
                header_idx = i
                break

        if header_idx != -1:
            df.columns = df.iloc[header_idx]
            df = df.iloc[header_idx+1:].copy()
            df.columns = [str(c).upper().strip() for c in df.columns]

            col_dep = next((c for c in df.columns if "DEPENDENCIA" in c), None)
            col_tot = next((c for c in df.columns if "TOTAL" in c), None)

            if col_dep and col_tot:
                df_clean = df[[col_dep, col_tot]].copy()
                df_clean.rename(columns={col_dep: "Dependencia", col_tot: "Total"}, inplace=True)
                df_clean["Trimestre"] = str(tab_name).strip()

                df_clean.dropna(subset=["Dependencia", "Total"], inplace=True)
                df_clean = df_clean[df_clean["Dependencia"].astype(str).str.strip() != ""]
                df_clean["Total"] = pd.to_numeric(df_clean["Total"], errors="coerce")
                df_clean.dropna(subset=["Total"], inplace=True)

                all_rankings.append(df_clean)
                pestañas_procesadas.add(tab_name) # Marcamos la pestaña como procesada

    if all_rankings:
        final_df = pd.concat(all_rankings, ignore_index=True)
        return final_df, None
    return None, "No se encontraron pestañas válidas que contengan 'RANKING'."


# 4. Interceptor de vista para visualizar el Ranking
if SECCION == "ranking":
    st.markdown(f"<h1 style='color:{GUINDA_OFICIAL};margin-bottom:0;'>Ranking de Reportes Trimestrales</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6c757d;font-size:1.1rem;'>H. Ayuntamiento de Valle de Santiago</p>", unsafe_allow_html=True)
    st.divider()

    with st.spinner("Descargando y sincronizando el ranking trimestral..."):
        df_rk, err_rk = obtener_datos_ranking()
    
    if err_rk:
        st.error(f"Hubo un problema al cargar los datos del ranking: {err_rk}")
    elif df_rk is not None and not df_rk.empty:
        
        # Selector de trimestre
        trimestres = list(df_rk["Trimestre"].unique())
        col_sel, _ = st.columns([1, 2])
        with col_sel:
            trim_sel = st.selectbox("Seleccionar Trimestre:", trimestres)

        df_mostrar = df_rk[df_rk["Trimestre"] == trim_sel].copy()
        df_mostrar = df_mostrar.sort_values(by="Total", ascending=False).reset_index(drop=True)
        df_mostrar.index = df_mostrar.index + 1  # Formato de posición

        # --- LÓGICA DE COLORES ---
        def obtener_color_categoria(valor):
            if valor >= 71: return 'Verde'
            elif valor >= 41: return 'Amarillo'
            else: return 'Rojo'

        df_mostrar['CategoriaColor'] = df_mostrar['Total'].apply(obtener_color_categoria)
        
        mapa_colores = {
            'Verde': VERDE_OFICIAL,
            'Amarillo': DORADO_OFICIAL,
            'Rojo': '#e74c3c'
        }
        # -------------------------

        # Métricas
        c1, c2 = st.columns(2)
        c1.metric("Dependencias Evaluadas", len(df_mostrar))
        c2.metric("Promedio General del Trimestre", f"{df_mostrar['Total'].mean():.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico de barras actualizado
        fig_rk = px.bar(
            df_mostrar,
            x="Dependencia",
            y="Total",
            text="Total",
            color="CategoriaColor",          # Usamos la columna de categoría
            color_discrete_map=mapa_colores  # Mapeamos los colores definidos
        )
        
        fig_rk.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
        fig_rk.update_layout(
            template="plotly_white", 
            xaxis_tickangle=-45, 
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Puntuación Total",
            xaxis_title="",
            showlegend=False # Ocultamos la leyenda
        )
        st.plotly_chart(fig_rk, use_container_width=True)

        # Tabla de posiciones
        st.markdown(f"### 📋 Tabla de Posiciones ({trim_sel})")
        st.dataframe(
            df_mostrar[["Dependencia", "Total"]].style.format({"Total": "{:.1f}%"}),
            use_container_width=True
        )
    else:
        st.warning("El archivo de Google Drive está vacío o no tiene la estructura de ranking configurada.")

    # 🛑 Esto detiene la ejecución
    st.stop()

# ==============================================================================
# 5. TODO LO QUE ESTÁ ABAJO SOLO SE EJECUTARÁ SI SECCION == "desempeno"
# ==============================================================================

# ── ENCABEZADO (DESEMPEÑO) ─────────────────────────────────────────────────────
# ⚠️ CORRECCIÓN DE VELOCIDAD: antes, la app descargaba los 111 colaboradores
# de TODAS las áreas antes de mostrar nada (la barra "Cargando... 7/111").
# Ahora el encabezado se pinta de inmediato con un placeholder, el usuario
# puede elegir su área y ver sus datos sin esperar, y el cálculo de "Área
# Líder" (que sí necesita los 111 colaboradores) se hace en segundo plano,
# al final del script, actualizando este mismo espacio cuando termine.
st.markdown(f"<h1 style='color:{GUINDA_OFICIAL};margin-bottom:0;'>"
            " Sistema de Evaluación de Desempeño</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6c757d;font-size:1.1rem;'>"
            "H. Ayuntamiento de Valle de Santiago</p>", unsafe_allow_html=True)

header_metrics_placeholder = st.empty()
with header_metrics_placeholder.container():
    k1, k2, k3 = st.columns(3)
    if "global_df" in st.session_state:
        _df_global_prev = st.session_state["global_df"]
        if not _df_global_prev.empty:
            _rk_prev = _df_global_prev.groupby("Área")["Promedio Mes"].mean().reset_index()
            _f_prev  = _rk_prev.loc[_rk_prev["Promedio Mes"].idxmax()]
            k1.metric("Área Líder", _f_prev["Área"])
            k2.metric("Eficiencia de Área Líder", f"{_f_prev['Promedio Mes']:.1f}%")
        else:
            k1.metric("Área Líder", "N/A")
            k2.metric("Eficiencia de Área Líder", "0.0%")
    else:
        k1.metric("Área Líder", "Calculando…")
        k2.metric("Eficiencia de Área Líder", "…")
    k3.metric("Dependencias Evaluadas", len(AREAS))
st.divider()

# ── FILTROS ────────────────────────────────────────────────────────────────────
st.sidebar.subheader("Filtrar Información")
area_sel    = st.sidebar.selectbox("Seleccionar Dependencia:", list(AREAS.keys()))
colabs_area = AREAS[area_sel]

if not colabs_area:
    st.markdown(f"<h3 style='color:{GUINDA_OFICIAL};'> Análisis Específico: {area_sel}</h3>",
                unsafe_allow_html=True)
    st.info(f"ℹ️ El área de **{area_sel}** aún no tiene personal asignado.")
    st.stop()

colabs_validos = {n: fid for n, fid in colabs_area.items()
                  if fid.upper() not in ("PENDIENTE","")}

# ── DESCARGA DE COLABORADORES DEL ÁREA SELECCIONADA (CON BARRA DE PROGRESO) ──
# ⚠️ NUEVO: se agrega una barra de progreso visible mientras se descargan
# los colaboradores del área elegida, y se sube max_workers de 16 a 32
# (es trabajo de red/I-O, se puede paralelizar más sin problema, igual
# que ya se hacía en la carga global de "Área Líder").
resumenes_a, semanas_a, caps_a, debug_info = [], [], [], {}
if colabs_validos:
    total_colabs_area = len(colabs_validos)
    progreso_area_placeholder = st.empty()
    with progreso_area_placeholder.container():
        barra_area = st.progress(
            0, text=f"Descargando 0/{total_colabs_area} colaboradores de {area_sel}...")
        completados_area = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
            futuros = {ex.submit(obtener_datos, n.strip(), fid, area_sel): n.strip()
                       for n, fid in colabs_validos.items()}
            for fut in concurrent.futures.as_completed(futuros):
                nom = futuros[fut]
                try:
                    r, s, c, d = fut.result()
                    resumenes_a.extend(r); semanas_a.extend(s)
                    caps_a.extend(c);      debug_info[nom] = d
                except Exception as e:
                    debug_info[nom] = [f"Error: {e}"]
                completados_area += 1
                barra_area.progress(
                    completados_area / total_colabs_area,
                    text=f"Descargando {completados_area}/{total_colabs_area} "
                         f"colaboradores de {area_sel}...")
    progreso_area_placeholder.empty()

for n, fid in colabs_area.items():
    if fid.upper() in ("PENDIENTE",""):
        debug_info[n] = ["⏳ Archivo pendiente de agregar"]

C_RES = ["Área","Colaborador","Mes","Promedio Mes"]
C_SEM = ["Área","Colaborador","Mes","Periodo","Rendimiento","_orden"]
C_CAP = ["Área","Colaborador","Mes","Capacitación"]

df_res = (pd.DataFrame(resumenes_a, columns=C_RES)
          .drop_duplicates(subset=["Colaborador","Mes"]))
df_sem = (pd.DataFrame(semanas_a, columns=C_SEM)
          .drop_duplicates(subset=["Colaborador","Periodo"]))
df_cap = pd.DataFrame(caps_a, columns=C_CAP).drop_duplicates()

import datetime as _dt
_MES_HOY       = f"{ORDEN_MESES_BASE[_dt.datetime.now().month-1]} {_dt.datetime.now().year}"
_meses_ref     = list(df_res["Mes"].unique()) if not df_res.empty else [_MES_HOY]
_colabs_datos  = set(df_res["Colaborador"].unique())
_filas_cero    = []
for _n in [n.strip() for n in colabs_area.keys()]:
    if _n not in _colabs_datos:
        for _m in _meses_ref:
            _filas_cero.append({"Área":area_sel,"Colaborador":_n,
                                 "Mes":_m,"Promedio Mes":0.0})
if _filas_cero:
    df_res = pd.concat([df_res, pd.DataFrame(_filas_cero, columns=C_RES)],
                       ignore_index=True)

meses_d = []
if not df_res.empty:
    mp     = list(df_res["Mes"].unique())
    meses_d = [m for m in ORDEN_MESES if m in mp]
    meses_d.extend([m for m in mp if m not in meses_d])

mes_sel    = st.sidebar.selectbox("Periodo Mensual:", ["Todos"] + meses_d)
nombres_a  = [n.strip() for n in colabs_area]
colab_sel  = st.sidebar.multiselect("Personal de la Dependencia:",
                                    nombres_a, default=nombres_a)

df_rf = df_res[df_res["Colaborador"].isin(colab_sel)].copy()
df_sf = df_sem[df_sem["Colaborador"].isin(colab_sel)].copy()
df_cf = df_cap[df_cap["Colaborador"].isin(colab_sel)].copy()
if mes_sel != "Todos":
    df_rf = df_rf[df_rf["Mes"]==mes_sel]
    df_sf = df_sf[df_sf["Mes"]==mes_sel]
    df_cf = df_cf[df_cf["Mes"]==mes_sel]

# ── ANÁLISIS ───────────────────────────────────────────────────────────────────
st.markdown(f"<h3 style='color:{GUINDA_OFICIAL};'> Análisis Específico: {area_sel}</h3>",
            unsafe_allow_html=True)

if not df_rf.empty:
    orden_final = [m for m in ORDEN_MESES if m in df_rf["Mes"].unique()]
    orden_final.extend([m for m in df_rf["Mes"].unique() if m not in orden_final])
    df_rf["Mes"] = pd.Categorical(df_rf["Mes"], categories=orden_final, ordered=True)

    colaboradores = df_rf["Colaborador"].unique()
    full_index    = pd.MultiIndex.from_product(
        [colaboradores, orden_final], names=["Colaborador","Mes"])
    df_rf = (df_rf.set_index(["Colaborador","Mes"])
                  .reindex(full_index).reset_index())
    df_rf["Promedio Mes"] = df_rf["Promedio Mes"].fillna(0.0)
    df_rf["Área"]         = df_rf["Área"].fillna(area_sel)
    df_rf["Mes"]          = pd.Categorical(df_rf["Mes"],
                                           categories=orden_final, ordered=True)

    todos_colabs = sorted(df_rf["Colaborador"].unique())
    color_map    = {c: PALETA[i % len(PALETA)] for i, c in enumerate(todos_colabs)}

    fig = px.bar(df_rf.sort_values("Mes"),
                 x="Mes" if mes_sel=="Todos" else "Colaborador",
                 y="Promedio Mes", color="Colaborador",
                 barmode="group", text="Promedio Mes",
                 color_discrete_map=color_map)
    fig.update_traces(
        texttemplate="%{text:.0f}%", textposition="outside",
        cliponaxis=False, marker_line_width=1,
        marker_line_color="rgba(0,0,0,0.15)"
    )
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=TEXTO_DARK,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3,
                    xanchor="center", x=0.5)
    )

    prom_dep   = df_rf["Promedio Mes"].mean()
    filas_html = "".join(
        f"<tr><td>{r['Colaborador']}</td><td>{r['Mes']}</td>"
        f"<td style='font-weight:bold;color:#601a1e;'>{r['Promedio Mes']}%</td></tr>"
        for _, r in df_rf.iterrows())
    html_rep = f"""<html><head><meta charset='utf-8'>
    <style>
      body{{font-family:Arial;color:#212529;margin:30px;background:white}}
      .hdr{{text-align:center;border-bottom:3px solid #601a1e;padding-bottom:15px;margin-bottom:20px}}
      .hdr h1{{color:#601a1e;margin:0;font-size:24px}}
      .hdr p{{color:#f1b80c;margin:5px 0 0;font-weight:bold;letter-spacing:2px;font-size:11px}}
      .mb{{background:#f8f9fa;padding:15px;border-left:5px solid #601a1e;border-radius:4px;margin-bottom:20px}}
      .pb{{page-break-before:always;margin-top:40px}}
      table.dt{{width:100%;border-collapse:collapse;margin-top:15px}}
      table.dt th{{background:#601a1e;color:white;padding:10px;text-align:left;font-size:13px}}
      table.dt td{{padding:9px;border-bottom:1px solid #e9ecef;font-size:12px}}
      table.dt tr:nth-child(even){{background:#f8f9fa}}
      @media print{{*{{-webkit-print-color-adjust:exact!important}}}}
    </style></head><body>
    <div class='hdr'><h1>VALLE DE SANTIAGO</h1>
      <p>PRESIDENCIA MUNICIPAL • ADMINISTRACIÓN 2024-2027</p></div>
    <h2>Reporte de Evaluación de Desempeño</h2>
    <div class='mb'><table>
      <tr><td width='35%'><b>Dependencia:</b></td><td>{area_sel}</td></tr>
      <tr><td><b>Periodo:</b></td><td>{mes_sel}</td></tr>
      <tr><td><b>Promedio General:</b></td>
          <td style='color:#601a1e;font-weight:bold;'>{prom_dep:.1f}%</td></tr>
    </table></div>
    <div>{fig.to_html(full_html=False,include_plotlyjs='cdn')}</div>
    <div class='pb'></div>
    <table class='dt'><thead><tr>
      <th>Servidor Público</th><th>Mes</th><th>Rendimiento</th>
    </tr></thead><tbody>{filas_html}</tbody></table>
    <div style='margin-top:40px;text-align:center;font-size:11px;color:#6c757d;
         border-top:1px solid #e9ecef;padding-top:15px;'>
      H. Ayuntamiento de Valle de Santiago • Ctrl+P → Guardar como PDF</div>
    <script>window.onload=function(){{setTimeout(()=>window.print(),1000);}}</script>
    </body></html>"""

    _, col_btn = st.columns([5,1])
    with col_btn:
        st.download_button("📄 Generar PDF", data=html_rep,
                           file_name=f"Reporte_{area_sel}.html",
                           mime="text/html", use_container_width=True)

    c1, c2, c3 = st.columns(3)
    idx_max = df_rf["Promedio Mes"].idxmax()
    c1.metric("Promedio General",   f"{df_rf['Promedio Mes'].mean():.1f}%")
    c2.metric("Servidor Destacado",
              f"{df_rf.loc[idx_max,'Promedio Mes']}%",
              df_rf.loc[idx_max,'Colaborador'])
    c3.metric("Reportes Semanales", len(df_sf))

    st.plotly_chart(fig, use_container_width=True)

    # ── SELECTOR DE COLABORADOR CON TARJETA DE PERFIL ─────────────────────────
    st.markdown(
        f"<p style='color:#6c757d;font-size:0.9rem;margin-bottom:4px;'>"
        f"👤 Selecciona un colaborador para ver su perfil:</p>",
        unsafe_allow_html=True)

    prom_colab = (df_rf.groupby("Colaborador")["Promedio Mes"]
                       .mean().round(1).to_dict())

    colab_vista = st.selectbox(
        "Colaborador", options=["— Elige uno —"] + sorted(colab_sel),
        label_visibility="collapsed")

    if colab_vista != "— Elige uno —":
        _b64   = get_foto_b64(colab_vista)
        _prom  = prom_colab.get(colab_vista, 0.0)
        _color = VERDE_OFICIAL if _prom >= 80 else (DORADO_OFICIAL if _prom >= 50 else "#e74c3c")

        _meses_colab = (df_rf[df_rf["Colaborador"]==colab_vista]
                        .sort_values("Mes")[["Mes","Promedio Mes"]]
                        .drop_duplicates())
        _filas_meses = "".join(
            f"<div style='display:flex;justify-content:space-between;"
            f"padding:5px 0;border-bottom:1px solid {BORDE_SUAVE};'>"
            f"<span style='color:#6c757d;font-size:0.85rem;'>{r['Mes']}</span>"
            f"<span style='font-weight:bold;color:{GUINDA_OFICIAL};font-size:0.85rem;'>"
            f"{r['Promedio Mes']}%</span></div>"
            for _, r in _meses_colab.iterrows()
        )

        col_foto, col_hist = st.columns([1, 2])
        with col_foto:
            _ruta_foto = get_foto_path(colab_vista)
            if _ruta_foto:
                _img_data  = Path(_ruta_foto).read_bytes()
                _ext       = Path(_ruta_foto).suffix.lower()
                _mime      = "image/png" if _ext == ".png" else "image/jpeg"
                _img_src   = f"data:{_mime};base64,{base64.b64encode(_img_data).decode()}"
            else:
                _img_src   = get_avatar_svg(colab_vista)

            st.markdown(f"""
            <div style='background:#fff;border-radius:14px;padding:24px 20px;
                 border:1px solid {BORDE_SUAVE};text-align:center;
                 box-shadow:0 4px 16px rgba(0,0,0,0.07);'>
              <div style='display:flex;justify-content:center;margin-bottom:14px;'>
                <img src='{_img_src}'
                     style='width:110px;height:110px;border-radius:50%;
                            object-fit:cover;border:4px solid {GUINDA_OFICIAL};
                            box-shadow:0 4px 12px rgba(96,26,30,0.25);'/>
              </div>
              <div style='font-size:1rem;font-weight:700;color:{TEXTO_DARK};
                   line-height:1.4;margin-bottom:6px;'>{colab_vista}</div>
              <div style='font-size:0.78rem;color:#6c757d;margin-bottom:14px;'>
                {area_sel}</div>
              <div style='font-size:2rem;font-weight:800;color:{_color};
                   line-height:1;'>{_prom}%</div>
              <div style='font-size:0.72rem;color:#6c757d;margin-top:4px;'>
                promedio general</div>
            </div>""", unsafe_allow_html=True)

        with col_hist:
            st.markdown(f"""
            <div style='background:#fff;border-radius:14px;padding:20px 24px;
                 border:1px solid {BORDE_SUAVE};
                 box-shadow:0 4px 16px rgba(0,0,0,0.07);'>
              <div style='font-weight:700;color:{GUINDA_OFICIAL};
                   margin-bottom:14px;font-size:0.95rem;'>
                📅 Rendimiento por mes
              </div>
              {_filas_meses if _filas_meses else
               "<span style='color:#adb5bd;font-size:0.85rem;'>Sin registros</span>"}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2 = st.columns([1,2])
    with t1:
        st.markdown("**Calificaciones Promedio**")
        st.dataframe(df_rf[["Colaborador","Mes","Promedio Mes"]],
                     hide_index=True, use_container_width=True)
    with t2:
        st.markdown("**Evaluaciones Semanales**")
        if not df_sf.empty:
            st.dataframe(df_sf.sort_values(["Colaborador","_orden"])
                         [["Colaborador","Periodo","Rendimiento"]],
                         hide_index=True, use_container_width=True)
else:
    st.info("No hay datos numéricos para mostrar con los filtros actuales.")

with st.expander("🔍 Diagnóstico de hojas detectadas"):
    for colab, pests in debug_info.items():
        st.markdown(f"**{colab}**")
        for p in pests:
            st.markdown(f"&nbsp;&nbsp;&nbsp;{p}")

st.divider()

# ── CAPACITACIONES ─────────────────────────────────────────────────────────────
st.markdown(f"<h3 style='color:{GUINDA_OFICIAL};margin-top:20px;'>"
            "🎓 Capacitaciones y Desarrollo Profesional</h3>", unsafe_allow_html=True)

if not df_cf.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Capacitaciones",   df_cf.shape[0])
    m2.metric("Colaboradores capacitados", df_cf["Colaborador"].nunique())
    m3.metric("Meses con registro",        df_cf["Mes"].nunique())
    st.markdown("<br>", unsafe_allow_html=True)

    df_cnt = (df_cf.groupby("Colaborador").size()
              .reset_index(name="Total").sort_values("Total", ascending=False))
    color_map_cap = get_color_map(df_cnt["Colaborador"].unique())
    fig_c = px.bar(df_cnt, x="Colaborador", y="Total", text_auto=True,
                   color="Colaborador", color_discrete_map=color_map_cap,
                   title="Cursos por Colaborador")
    fig_c.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                        font_color=TEXTO_DARK, title_font_color=GUINDA_OFICIAL,
                        showlegend=False, xaxis_title="", yaxis_title="N° cursos")
    st.plotly_chart(fig_c, use_container_width=True)

    df_grp = (df_cf.groupby("Colaborador")
              .agg(Total=("Capacitación","count"), Lista=("Capacitación",list))
              .reset_index().sort_values("Total", ascending=False))

    cols2 = st.columns(2)
    for idx, row in df_grp.iterrows():
        _b64     = get_foto_b64(row["Colaborador"])
        cursos_h = "".join(
            f"<div style='margin-bottom:6px;color:{TEXTO_DARK};'>"
            f"• <i>{c}</i></div>" for c in row["Lista"])
        with cols2[idx % 2]:
            st.markdown(f"""
            <div style='background:#fff;padding:16px;border-radius:12px;
                 border-left:5px solid {VERDE_OFICIAL};border-top:1px solid {BORDE_SUAVE};
                 border-right:1px solid {BORDE_SUAVE};border-bottom:1px solid {BORDE_SUAVE};
                 margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.04);'>
              <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px;'>
                <img src='{_b64}'
                     style='width:52px;height:52px;border-radius:50%;object-fit:cover;
                            border:3px solid {GUINDA_OFICIAL};flex-shrink:0;'/>
                <div style='flex:1;min-width:0;'>
                  <div style='font-weight:700;color:{GUINDA_OFICIAL};font-size:0.95rem;
                       white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>
                    {row["Colaborador"]}
                  </div>
                  <span style='background:{DORADO_OFICIAL};color:white;padding:2px 10px;
                        border-radius:10px;font-size:0.8rem;font-weight:bold;
                        display:inline-block;margin-top:4px;'>
                    {row["Total"]} Curso(s)
                  </span>
                </div>
              </div>
              <div style='padding-left:4px;border-top:1px solid {BORDE_SUAVE};
                   padding-top:10px;'>
                {cursos_h}
              </div>
            </div>""", unsafe_allow_html=True)
else:
    st.info("No se registraron capacitaciones para el personal seleccionado.")

# ══════════════════════════════════════════════════════════════════════════
# ── CARGA GLOBAL (EN SEGUNDO PLANO) — solo para calcular "Área Líder" ──────
# ══════════════════════════════════════════════════════════════════════════
# Se ejecuta AL FINAL del script, después de que el usuario ya vio el
# análisis completo de su área seleccionada. Así la app se siente rápida:
# lo que el usuario pidió aparece de inmediato, y el dato global (que
# requiere descargar los 111 colaboradores de todas las áreas) llega un
# poco después, actualizando el encabezado sin haber bloqueado nada.
#
# max_workers subido de 16 a 32 (es trabajo de red/I-O, no de CPU, así que
# se puede paralelizar mucho más sin problema).
if "global_df" not in st.session_state:
    tareas = [
        (n.strip(), fid, area)
        for area, cols in AREAS.items()
        for n, fid in cols.items()
        if fid.upper() not in ("PENDIENTE","")
    ]
    prog_placeholder = st.sidebar.empty()
    with prog_placeholder.container():
        prog    = st.progress(0, text="Calculando área líder...")
        all_res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
            futuros = {ex.submit(obtener_datos, t[0], t[1], t[2]): t for t in tareas}
            for i, fut in enumerate(concurrent.futures.as_completed(futuros), 1):
                try:
                    res, _, _, _ = fut.result()
                    all_res.extend(res)
                except Exception:
                    pass
                prog.progress(i/len(tareas),
                              text=f"Calculando área líder... {i}/{len(tareas)}")
    prog_placeholder.empty()

    st.session_state["global_df"] = (
        pd.DataFrame(all_res, columns=["Área","Colaborador","Mes","Promedio Mes"])
        if all_res else
        pd.DataFrame(columns=["Área","Colaborador","Mes","Promedio Mes"])
    )

    df_global = st.session_state["global_df"]
    with header_metrics_placeholder.container():
        k1, k2, k3 = st.columns(3)
        mejor_area_n, mejor_area_v = "N/A", 0.0
        if not df_global.empty:
            rk = df_global.groupby("Área")["Promedio Mes"].mean().reset_index()
            f  = rk.loc[rk["Promedio Mes"].idxmax()]
            mejor_area_n, mejor_area_v = f["Área"], f["Promedio Mes"]
        k1.metric("Área Líder", mejor_area_n)
        k2.metric("Eficiencia de Área Líder", f"{mejor_area_v:.1f}%")
        k3.metric("Dependencias Evaluadas", len(AREAS))
