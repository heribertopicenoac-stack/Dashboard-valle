# DOCUMENTACIÓN REALIZADA POR HERIBERTO PICENO ACOSTA TSU
import streamlit as st
import pandas as pd
import plotly.express as px
import re
import concurrent.futures
import time
import urllib.request
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

@st.cache_data(show_spinner=False)
def get_foto_b64(nombre: str) -> str:
    ruta = get_foto_path(nombre)
    if ruta:
        data = ruta.read_bytes()
        ext  = ruta.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return get_avatar_svg(nombre)

# ── ÁREAS ──────────────────────────────────────────────────────────────────────
AREAS = {
    "Adquisiciones": {
        "Adriana Paola Vargas Ramirez":      "1sk0zdcf2uqJUe9jQrWu-ps3iMff2GrhF",
        "Ana María Alvarado Hernandez":      "1AsrG811fEvkn5nnPNMqg9Wt06uMhm9-i",
        "Brenda Aida Alvarez Perez":         "1BlIGAEkLUSxYKw55FBLelvbzFKEFMLl2",
        "Dulce Nayeli Hernandez Gonzalez":   "1Ee2tGNLy5JCeAlf5AnM0TMx0p9m6TrvC",
        "Itzel Moreno Hernandez":            "1fRTe8ZYLuX8M20V_6zWrLEeAPH2iaGQP",
        "Maricarmen Mosqueda Leon":          "1ism3nnwuwHzLclufiChZZZUlQf0O05ZN",
        "Monserrat Crespo Crespo":           "1UkgHnpqVBDBtRvCiAlwouhNbV2uArdK1",
    },
    "Archivo Histórico": {
        "Roquelia Martinez Arredondo":       "1HgGfIC9UFbU1se-WCkkTkJ_45-oKmn4N",
        "Yocelyn Esther Vazquez Granados":   "1JnHQm_MBiR1WVuOHQhIwOpb5jNFpmqOL",
    },
    "Casa de la Mujer": {
        "Alfredo Stefano Castro Enríquez":   "1dp8YTfe9wLxjYAnOmRXvsab0_-FaovBx",
        "Ana Lilia Tovar Roa":               "1yC-tPSreSdBeBPQT0IK0vjr43sORWfG2",
        "Ingrid Miroslava Juárez Lesso":     "1t1nrYFe55vbwgz69RkLDxJXiJqceuksm",
        "Juana Lucia González Beltrán":      "1XZkQ0Lnhin-3AZEJ792KTfnOreJh5w1k",
        "Karla Isabel Uribe Ortega":         "1vTq4NOoN1z5pNrFl8fT0HfSGoWaiJSUq",
        "Laura Adriana Andrade Cuevas":      "1Ip7AHzb1Iras3f0shdtgpalN9c6Svaox",
        "María del Pilar Vázquez Castro":    "1u71_gXDhqOPmcrKAsZH1Z_fsTkc755Sb",
    },
    "Catastro y Predial": {
        "Ana Lilia Curtidor Aguilar":        "10u5YPsZot0wIn4MMqTrLyxrgq6-GAh32",
        "Blanca Miriam Acosta Martinez":     "1ChXB--xAUrqBwCv2pyAa3k-K4fPDDS4L",
        "Eralio Morales Silva":              "1xJedBwmY1BoPBQeeyMg8-T-RO2uGnTjP",
        "Juan Carlos Ledesma Cano":          "1op2Uf1tj7SwA06IrPbJ7JWQR4a0DgYMS",
        "Rocio Joycelline Galvan Flores":    "1PnKD6a47rDgdoR6JiETY32TyTKFY1vht",
    },
    "Comude": {
        "Rebeca Martínez García":            "1gJVYV6S0UEIHBCKXHVJhp3qv9g3jwGC_",
    },
    "Comunicación Social": {
        "Eduardo Gonzalez Salazar":          "1BXKU-MDXV8Wenc_j7uLBK_zOPq0P1ccw",
        "Francisco Ivan González Salazar":   "1gvhWj-hfNGqpsCqGcDcea9Y4EkMZjZta",
        "Francisco Javier Vázquez Sardina":  "1mOB1VHs2eyeh1aYYC9OC-2k92j134ZEF",
        "Luis Felipe Gómez Ávila":           "1eyOTbcSsJkO9cUYrwJtO_8-e0_f9x77c",
        "Wendy Sharay Rivas Frias":          "1IiHyYCSK0_BhkolGfdJMYinsHCRUxqbb",
    },
    "Contraloria": {
        "Adriana Raquel Campos Guzmán":      "1DVg-WZVwYRNrpNeToYAEjaVsVn5wM9qr",
        "Ana María Cabrera Vázquez":         "1ktyah2NV8qei0cFRPda98DYxwJ4YpMKV",
        "Andros Arion García Ramírez":       "1ByQG8fLskd5vs1HN2MF-ID28-18aYx-p",
        "Carolina Arredondo Molina":         "1L3XJq3BnPTQxHsLLTSVTOO_SFMCciwiv",
        "Jessica Esthefanía Sixtos Núñez":   "1spNOa8B5PfpTIdRX54PSeUb_2ahiDqxQ",
        "José Jesús Ojeda García":           "1hJ6MPyt_dgJYwMvgazuIpCiniyAhSakR",
        "Juan Manuel Ríos Marceleño":        "11cqOcjAuylDlpPiGG-dAVR9Mu0uCIJt1",
        "Karla Marcela González Andrade":    "1xGPSVEoKtE_usAviUU4U2HSBljfY2DcV",
        "María del Carmen Moncada Rojas":    "1LWP_wi9wiBQnUTyCjssH0Q9xOuOKIwAw",
    },
    "Desarrollo Institucional": {
        "Dayra Monica Gómez Hueramo":        "1X1qCwXVq6Zbwq4bjM0k2APqgZI5eVJ_U",
        "Jorge Arath Ramirez Mayorquin":     "12NQb0jEF_eOFernGy2cg2hOScUFr_z8j",
        "Jorge Luis Garcia Cardenas":        "1Iqa8eQDqNGulD9CuJWfC2Sn0EzU7OBcM",
        "Pamela Sierra Gonzalez":            "1ge3cnPdBtO4ayyRw-vDRvQy4biS-OusK",
    },
    "Economía": {
        "Annel Cristina Rico Arroyo":        "1NaLqH5WoI2gS2ku_CQzbpvtqBikamNMF",
        "Esthefania Rico Gonzalez":          "1bmqnKzLpH26OGcdKrRIFi7BpF14b5zVm",
        "Sandra Monserrat Mosqueda Cano":    "1_km_l5X7QVThvT7v-BsxKzZi4HiF27lc",
        "Sanjuanita Zuñiga Tamayo":          "1bQndiDBheyWzLsdf5oK17fFxHCIOr253",
        "Steefany Garcia Gonzalez":          "1ZsUKnjyyZ99t4r1_V0L9XwPPKD00yd4K",
        "Ximena Guadalupe Andrade Rangel":   "1THFY4zm8CAs4Wiga12G7xaV4nhFZQtbf",
    },
    "Educación": {},
    "Gimnasio": {
        "Diego Vilchis":                     "1GwVCiHahHMryaY3iqgq5BfpQ3m6DPUGf",
        "Guillermo Medel Cardenas":          "1Af6rjrKgqC7EMpqSXw7uW6JVjcuoCSE5",
    },
    "Imjuv": {
        "Brandon Alexis Núñez Lorenzo":      "10WfZdp0o4h3Ho7JIhD_gda_-3wyATzHP",
        "Johana González González":          "1rIKeMoM8DopIxXhqLtCTmN5U2DtSAS6q",
        "Josue Adan Hernández Tavera":       "1kgVt19Sz9yTRDAB1Q89mlbz0x0eitYxa",
    },
    "Implan": {
        "Citlaly Arredondo García":          "1j-RhSieVJDz1OcDj6u9Bo_Fgo2B8Olrj",
        "Erendira Virginia Morales Pérez":   "1tRIWGzEUHOMs1zX91tm-F-13Vh174H-z",
    },
    "Informática": {
        "Genesis Aurora Mercado Rodriguez":  "1XqEk9AnSV9yseS9KMy9qMzMZBA9x--W7",
        "Julio Prieto Sanchez":              "1HZu9R94LkcXk4mjOGkxQ5_ph4lCZ8q6e",
        "Pablo Vazquez Barroso":             "1pDF0KYgpBdVPIy8VQDtc6e0ia49cebqP",
    },
    "Jurídico": {
        "Batriz Adriana Ramirez Garcia":     "1WPzGkbog8VNmUCI6K5SuL5orQUU5XWsl",
        "Berenice Butanda Granados":         "PENDIENTE",
        "Hector Israel Bautista Alegria":    "PENDIENTE",
        "Liliana Armenta Rico":              "PENDIENTE",
        "Luis Angel Negrete Chavez":         "PENDIENTE",
        "Nancy Estefania Gamez Garcia":      "PENDIENTE",
        "Rodrigo Ortega Gomez":              "PENDIENTE",
    },
    "Limpia": {
        "Manuel Alejandro Arroyo Garcia":    "17eT4dCA8-tfW2zEzHq_OlVD_9vUeFQl_",
    },
    "Mercado Municipal": {
        "Marco Antonio Mosqueda Murillo":    "1tHvM80h5Ow4qayzsfneLzpuy8FMUQ6TI",
    },
    "Panteon Campo Florido": {
        "Letycia Ayala Carranza":            "1utBDxOmZkoIDhbn-QIusJYaITA9YlWrT",
    },
    "Parques Y Jardines": {
        "Marcos García Franco":              "1R4QDQm0ugjl_4q94hFqeuW_tjYt3dXtV",
    },
    "Procurador Auxiliar": {
        "Alondra Baeza Olivares":            "1WzeLJqrLG0OrlZYYPee_WCnYap-ZkYC4",
        "Dulce Paola Nieto Pallares":        "1VNsnLp8B4Jza8P1vNjkR-F-pQjnHTo52",
        "Maria Graciela Ramirez Alvarez":    "1sXrk8XFzRLWaiX8D1o-5LDext4PC8qs4",
    },
    "Recursos Humanos": {
        "Ana Paulina Morales Manriquez":     "1xbx7As9G5d_aBvWKfxaZ71h5sAgvFTxC",
        "Diana Laura Albarran Ahumada":      "143bhUXq3llg_g72_55qyk49Iuulv5nho",
        "Fernanda Abigail Flores Lara":      "1P2pHHFYisvTxsAxvlAmWZMXzO6Jcsx8J",
        "Karla Marina Curtidor Aguilar":     "1A-X1y2yTfd_Crfm3ASUEe0c_1JZppm6K",
    },
    "Salud": {
        "Estefani Baltazar Chiquito":        "1exbbmUI1bGi51-07MhzLhKL3RPK2LIgy",
        "Martha Lidia Aguayo Melchor":       "1DR1UVnHwmkjL9K0zkxlj5NeUkIhh0Sy7",
        "Melani Taisha Yañez Gutierrez":     "1MLTHcZDrT2V9nezUhsG3jw7DuQQkH2zt",
        "Susana Manrique León":             "1kaHFxz44_MHLEsGT_PTWbPs1MDzEG1xf",
        "Victor Manuel Santana Ayala":       "15vDT3OVb1hNo8KH1_DNK01mdijZdt97J",
    },
    "Servicios Municipales": {
        "Andrea Quiroz Paredes":             "10E_et9E8yEY884lTewKi8BFDAdN2yXAB",
        "Joanna Sánchez Noriega":            "1Nl10A1cNindQsK-dp4VF233wNoEVs68C",
        "Jose Luis Vazquez Morales":         "1wSk4intcsVxhnrsnc67v2Vhh_8etjUx5",
        "Liliana Deyanira Flores González":  "1-QbLy5RBJ_IQmNPcvJGuO13RKjYF0EIH",
        "Ma. Guadalupe Nuñez Acuña":         "1olPLw-rViNRME_6YHhWSHvNtmHHjaB37",
    },
    "Tesorería": {
        "Amelia Morales Avila":              "PENDIENTE",
        "Angie Ledesma Bravo":               "14sim6I3WBLBFjOy6V8DwL5A_swig7AP4",
        "Federico Aguilera Servin":          "PENDIENTE",
        "Graciela Arroyo Hernandez":         "1bS2nycovePoztACrtfHgKTUsIZ9h7jBY",
        "Isabel Ireta Ortega":               "1OvbM_pHhq3Jyj_wSq4gyLOM2SwTKEJuJ",
        "Itzel Margarita Martinez Quiroz":   "1vFT7ffXf6_VPhFMLJmnEuL9Zu5NdK4E8",
        "Jaqueline Karely Robles Vargas":    "12JcRcmBajJ0yQ339tBt1cI82kfEWx1hK",
        "Jenifer Guadalupe Almanza Zavala":  "1kP7AlohyZlJen_jIS97r1qeqyPpZ9_4b",
        "Jorge Gervasio":                    "1-CTFVPMdRPDINakOpxF8C6U8s7xdCyWL",
        "Jose Armando Morales Espinosa":     "1slTX0raUlxbPFEbCR8x9P-lGMtiDXNGG",
        "Juan Jose Manuel Sanchez Gonzalez": "1U9p8rw4Kvp8g4nHieloEIeoFd43L1E-i",
        "Julia Garcia Hernandez":            "1JXVe7UycdS1vcG4FI0DQ7h53TG_GPOSU",
        "Karla Beatriz Hernandez Sardina":   "1zD9dolsjPIJXydLH2Y6M2_TW8_aNLO9B",
        "Maria Magdalena Miranda Razo":      "1oqepI27l83hRJUmYugdCmwnL7RGTZwoO",
        "Maricela Hernandez Gallardo":       "1_-jmmN87h5qw1o__nn928q0IN-p9PfYH",
        "Melanie Belinda Garcia Gonzalez":   "1E-ujtu0FXuvIk7-_-u_cn50kMkWpTz9Y",
        "Miguel Ledesma Arredondo":          "PENDIENTE",
        "Patricia Sierra Ledesma":           "PENDIENTE",
        "Paulina Martinez Lara":             "1LXTVU_JL8e_T-ZaUmavTes4gKKkIvCZZ",
        "Tania Elizabeth Salazar Figueroa":  "1Cl4BeJehDIH4BQUhBQCsCLPRouzqG8Pl",
    },
    "Transparencia": {
        "Karla Adriana Alonso Moreno":       "1VwsyFghn9owJZCud7oeCsQi9d009zj-W",
    },
    "Turismo": {
        "Cristian Ramon Gonzalez Gomez":     "17Vq-Fz2LyVzbxcOG-1oiWBlhZAYhilhS",
        "Diana Paola Flores Negrete":        "1lOEVbR7QsxBVqmZbL9GjUsyxAn2ACz_L",
        "Jose Juan Garcia Dominguez":        "1Zqi2jKj0XahjhVnOq2z45Nf0h-dJuWId",
        "Juan Carlos Hernández Quiroz":      "1n6crUbtdr2BQ_WME49yyLBmY-VJVx_C5",
    },
    "Unidad Deportiva": {
        "Nayeli Guadalupe Ramírez Medina":   "1YkJxL_PfX3O46gjaAsvQUxs0GfImFntZ",
    },
}

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
    limpio = re.sub(r'\s+',' ',limpio).strip()
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

def descargar_excel(file_id: str, reintentos: int = 3, timeout: int = 25):
    if not file_id or file_id.upper() in ("PENDIENTE",""):
        raise ValueError("ID pendiente")
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    ultimo_error = None
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return io.BytesIO(resp.read())
        except Exception as e:
            ultimo_error = e
            if intento < reintentos - 1:
                time.sleep(1.5 * (intento + 1))
    raise ultimo_error

@st.cache_data(ttl=3600, show_spinner=False)
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

# Función exclusiva para extraer la data dinámica del Excel de Ranking Trimestral
@st.cache_data(ttl=3600, show_spinner=False)
def obtener_datos_ranking():
    file_id = "1Bqd1lxSQg0Q8AIw7UuNScshXbV7V74DY"
    try:
        raw = descargar_excel(file_id)
        excel_data = pd.read_excel(raw, sheet_name=None, engine="openpyxl")
    except Exception as e:
        return None, f"Error al descargar o leer el archivo de ranking: {e}"

    all_rankings = []
    
    # Procesar dinámicamente cada hoja que contenga el ranking sin importar si en el futuro añaden más
    for tab_name, df in excel_data.items():
        header_idx = -1
        # Búsqueda adaptativa de los encabezados reales (fila que contenga "DEPENDENCIA" y "TOTAL")
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

                # Limpieza de datos
                df_clean.dropna(subset=["Dependencia", "Total"], inplace=True)
                df_clean = df_clean[df_clean["Dependencia"].astype(str).str.strip() != ""]
                df_clean["Total"] = pd.to_numeric(df_clean["Total"], errors="coerce")
                df_clean.dropna(subset=["Total"], inplace=True)

                all_rankings.append(df_clean)

    if all_rankings:
        final_df = pd.concat(all_rankings, ignore_index=True)
        return final_df, None
    return None, "No se encontraron columnas válidas de 'Dependencia' y 'Total' en las hojas."


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
st.sidebar.header("Panel de Control")

if st.sidebar.button("🔄 Sincronizar Drive", use_container_width=True):
    st.cache_data.clear()
    for k in ["global_df","global_ok"]:
        st.session_state.pop(k, None)
    st.rerun()

st.sidebar.markdown("<br>", unsafe_allow_html=True)

dark_val = "1" if DARK else "0"

# Botón HTML 1: Funcionalidad de enlace integrada y CSS protegido
st.sidebar.markdown(f"""
<a href="?_dark={dark_val}&seccion=ranking" target="_self" style="text-decoration:none;">
<div class="btn-html-sidebar" style='background:linear-gradient(135deg,{GUINDA_OFICIAL},{GUINDA_OFICIAL}cc);
     border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;
     box-shadow:0 3px 10px rgba(96,26,30,0.2);'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.4rem;'>🏆</span>
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

# Botón HTML 2: Funcionalidad de enlace integrada y CSS protegido
st.sidebar.markdown(f"""
<a href="?_dark={dark_val}&seccion=resultados" target="_self" style="text-decoration:none;">
<div class="btn-html-sidebar" style='background:linear-gradient(135deg,{VERDE_OFICIAL},{VERDE_OFICIAL}cc);
     border-radius:10px;padding:14px 16px;margin-bottom:10px;cursor:pointer;
     box-shadow:0 3px 10px rgba(17,122,75,0.2);'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.4rem;'>📋</span>
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

# ── INTERCEPTOR DE APARTADOS GESTIÓN DE VISTAS ───────────────────────────────
if SECCION != "principal":
    titulo_vista = "Ranking de Reportes Trimestrales" if SECCION == "ranking" else "📋 Resultados del Programa de Evaluación"
    
    # Botón para volver posicionado estratégicamente antes del título
    html_volver = f"""
    <a href="?_dark={dark_val}&seccion=principal" target="_self" style="text-decoration:none; color:#ffffff !important;">
        <div style='background:{VERDE_OFICIAL}; color:#ffffff !important; padding:8px 16px; border-radius:6px; display:inline-block; font-weight:bold; box-shadow:0 2px 5px rgba(0,0,0,0.15); font-family:Arial,sans-serif; margin-bottom:15px; font-size:0.9rem;'>
            ⬅ Volver al Dashboard Principal
        </div>
    </a>
    """
    st.markdown(html_volver, unsafe_allow_html=True)

    st.markdown(f"<h1 style='color:{GUINDA_OFICIAL};margin-bottom:0;'> {titulo_vista}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6c757d;font-size:1.1rem;'>H. Ayuntamiento de Valle de Santiago</p>", unsafe_allow_html=True)
    st.divider()
    
    if SECCION == "ranking":
        with st.spinner("Descargando y sincronizando el ranking trimestral..."):
            df_rk, err_rk = obtener_datos_ranking()
        
        if err_rk:
            st.error(f"Hubo un problema al cargar los datos del ranking: {err_rk}")
        elif df_rk is not None and not df_rk.empty:
            
            # Recuperar y organizar trimestres leídos de las hojas
            trimestres = list(df_rk["Trimestre"].unique())
            col_sel, _ = st.columns([1, 2])
            with col_sel:
                trim_sel = st.selectbox(" Seleccionar Trimestre:", trimestres)

            df_mostrar = df_rk[df_rk["Trimestre"] == trim_sel].copy()
            df_mostrar = df_mostrar.sort_values(by="Total", ascending=False).reset_index(drop=True)
            df_mostrar.index = df_mostrar.index + 1  # Formato numérico para el ranking (1, 2, 3...)

            # Métricas
            c1, c2 = st.columns(2)
            c1.metric("Dependencias Evaluadas", len(df_mostrar))
            c2.metric("Promedio General del Trimestre", f"{df_mostrar['Total'].mean():.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)

            # Generar gráfico visual con plotly
            fig_rk = px.bar(
                df_mostrar,
                x="Dependencia",
                y="Total",
                text="Total",
                color="Total",
                color_continuous_scale=["#e74c3c", DORADO_OFICIAL, VERDE_OFICIAL], # Paleta semáforo invertida a puntaje
            )
            fig_rk.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
            fig_rk.update_layout(
                template="plotly_white", 
                xaxis_tickangle=-45, 
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="Puntuación Total",
                xaxis_title="",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_rk, use_container_width=True)

            # Tabla de detalles ordenada por el total
            st.markdown(f"### 📋 Tabla de Posiciones ({trim_sel})")
            st.dataframe(
                df_mostrar[["Dependencia", "Total"]].style.format({"Total": "{:.1f}%"}),
                use_container_width=True
            )
            
        else:
            st.warning("El archivo de Google Drive está vacío o no tiene la estructura de ranking configurada.")

    elif SECCION == "resultados":
        st.info("ℹ️ Este apartado se encuentra actualmente vacío. Próximamente se integrará la información correspondiente.")
    
    st.stop()


# ── CARGA GLOBAL ───────────────────────────────────────────────────────────────
if "global_df" not in st.session_state:
    tareas = [
        (n.strip(), fid, area)
        for area, cols in AREAS.items()
        for n, fid in cols.items()
        if fid.upper() not in ("PENDIENTE","")
    ]
    placeholder = st.empty()
    with placeholder.container():
        prog    = st.progress(0, text="Cargando datos de todas las áreas...")
        all_res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
            futuros = {ex.submit(obtener_datos, t[0], t[1], t[2]): t for t in tareas}
            for i, fut in enumerate(concurrent.futures.as_completed(futuros), 1):
                try:
                    res, _, _, _ = fut.result()
                    all_res.extend(res)
                except Exception:
                    pass
                prog.progress(i/len(tareas),
                              text=f"Cargando... {i}/{len(tareas)} colaboradores")
    placeholder.empty()
    st.session_state["global_df"] = (
        pd.DataFrame(all_res, columns=["Área","Colaborador","Mes","Promedio Mes"])
        if all_res else
        pd.DataFrame(columns=["Área","Colaborador","Mes","Promedio Mes"])
    )

df_global = st.session_state["global_df"]

mejor_area_n, mejor_area_v = "N/A", 0.0
if not df_global.empty:
    rk = df_global.groupby("Área")["Promedio Mes"].mean().reset_index()
    f  = rk.loc[rk["Promedio Mes"].idxmax()]
    mejor_area_n, mejor_area_v = f["Área"], f["Promedio Mes"]

# ── ENCABEZADO ─────────────────────────────────────────────────────────────────
st.markdown(f"<h1 style='color:{GUINDA_OFICIAL};margin-bottom:0;'>"
            " Sistema de Evaluación de Desempeño</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6c757d;font-size:1.1rem;'>"
            "H. Ayuntamiento de Valle de Santiago</p>", unsafe_allow_html=True)
k1, k2, k3 = st.columns(3)
k1.metric("Área Líder", mejor_area_n)
k2.metric("Eficiencia de Área Líder", f"{mejor_area_v:.1f}%")
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

resumenes_a, semanas_a, caps_a, debug_info = [], [], [], {}
if colabs_validos:
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
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
