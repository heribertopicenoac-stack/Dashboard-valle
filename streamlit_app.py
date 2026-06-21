# DOCUMENTACIÓN REALIZADA POR HERIBERTO PICENO ACOSTA TSU
# Refactorizado y ampliado — Junio 2026

import streamlit as st
import pandas as pd
import plotly.express as px
import re
import concurrent.futures
import time
import urllib.request
import io
import datetime as _dt

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard AD Desarrollo",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# PALETA INSTITUCIONAL
# ─────────────────────────────────────────────────────────────────────────────
GUINDA   = "#601a1e"
DORADO   = "#f1b80c"
VERDE    = "#117a4b"
GRIS_F   = "#f4f5f7"
GRIS_L   = "#e8eaed"
BLANCO   = "#ffffff"
TEXTO    = "#1a1a2e"
TEXTO_S  = "#6b7280"
PALETA   = ["#601a1e","#117a4b","#f1b80c","#2c3e50","#d35400","#7d3c98","#16a085","#2e4053"]

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL — limpio, sin contaminación visual
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* ── Reset base ── */
  .stApp {{ background-color:{GRIS_F}!important; color:{TEXTO}!important; }}
  [data-testid="stSidebar"] {{
    background-color:{BLANCO}!important;
    border-right:1px solid {GRIS_L};
    padding-top:0!important;
  }}

  /* ── Tipografía ── */
  h1,h2,h3,h4 {{ font-family:'Segoe UI',sans-serif; }}

  /* ── Métricas ── */
  div[data-testid="metric-container"] {{
    background:{BLANCO}!important;
    border:1px solid {GRIS_L}!important;
    border-top:3px solid {GUINDA}!important;
    border-radius:10px!important;
    padding:16px 20px!important;
    box-shadow:0 2px 8px rgba(0,0,0,0.05)!important;
  }}
  [data-testid="stMetricLabel"] p {{ color:{TEXTO_S}!important; font-size:0.8rem!important; font-weight:600!important; text-transform:uppercase; letter-spacing:.5px; }}
  [data-testid="stMetricValue"] div {{ color:{GUINDA}!important; font-weight:700!important; font-size:1.6rem!important; }}

  /* ── Botones ── */
  .stButton>button, .stDownloadButton>button {{
    background:{VERDE}!important; color:{BLANCO}!important;
    border:none!important; border-radius:8px!important;
    font-weight:600!important; transition:all .2s;
    padding:8px 18px!important;
  }}
  .stButton>button:hover, .stDownloadButton>button:hover {{
    background:{GUINDA}!important; box-shadow:0 4px 12px rgba(0,0,0,0.15);
  }}

  /* ── Nav tabs personalizados ── */
  .nav-container {{
    display:flex; gap:6px; margin-bottom:28px;
    background:{BLANCO}; padding:6px; border-radius:12px;
    border:1px solid {GRIS_L}; width:fit-content;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
  }}
  .nav-btn {{
    padding:9px 20px; border-radius:8px; font-size:0.88rem;
    font-weight:600; cursor:pointer; border:none; transition:all .2s;
    background:transparent; color:{TEXTO_S};
    font-family:'Segoe UI',sans-serif;
  }}
  .nav-btn.active {{
    background:{GUINDA}; color:{BLANCO};
    box-shadow:0 2px 8px rgba(96,26,30,0.3);
  }}
  .nav-btn:hover:not(.active) {{ background:{GRIS_F}; color:{TEXTO}; }}

  /* ── Cards genéricas ── */
  .card {{
    background:{BLANCO}; border-radius:12px; padding:20px 24px;
    border:1px solid {GRIS_L}; margin-bottom:16px;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
  }}
  .card-accent {{ border-top:3px solid {VERDE}; }}
  .card-gold   {{ border-top:3px solid {DORADO}; }}

  /* ── Chip/Badge ── */
  .badge {{
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:0.75rem; font-weight:700; letter-spacing:.3px;
  }}
  .badge-green {{ background:#d1fae5; color:#065f46; }}
  .badge-red   {{ background:#fee2e2; color:#991b1b; }}
  .badge-gold  {{ background:#fef3c7; color:#92400e; }}

  /* ── Modal de foto ── */
  .foto-modal {{
    position:fixed; top:0; left:0; width:100%; height:100%;
    background:rgba(0,0,0,0.6); z-index:9999; display:flex;
    align-items:center; justify-content:center;
  }}
  .foto-card {{
    background:{BLANCO}; border-radius:16px; padding:32px;
    max-width:320px; width:90%; text-align:center;
    box-shadow:0 20px 60px rgba(0,0,0,0.3);
  }}
  .foto-avatar {{
    width:120px; height:120px; border-radius:50%;
    border:4px solid {GUINDA}; object-fit:cover;
    margin:0 auto 16px;
  }}
  .foto-avatar-placeholder {{
    width:120px; height:120px; border-radius:50%;
    background:{GRIS_L}; display:flex; align-items:center;
    justify-content:center; margin:0 auto 16px;
    border:4px solid {GRIS_L};
  }}

  /* ── Tabla de colaboradores clicable ── */
  .colab-row {{
    display:flex; align-items:center; gap:10px;
    padding:8px 12px; border-radius:8px; cursor:pointer;
    transition:background .15s;
  }}
  .colab-row:hover {{ background:{GRIS_F}; }}
  .avatar-sm {{
    width:32px; height:32px; border-radius:50%;
    background:{GRIS_L}; flex-shrink:0; display:flex;
    align-items:center; justify-content:center;
    font-size:0.75rem; font-weight:700; color:{TEXTO_S};
    border:2px solid {GRIS_L};
  }}

  /* ── Coming soon / placeholder ── */
  .coming-soon {{
    text-align:center; padding:80px 20px; color:{TEXTO_S};
  }}
  .coming-soon .icon {{ font-size:3rem; margin-bottom:16px; }}
  .coming-soon h3 {{ color:{TEXTO}; font-size:1.3rem; margin-bottom:8px; }}
  .coming-soon p {{ font-size:0.9rem; max-width:380px; margin:0 auto; }}

  /* ── Divider ── */
  hr {{ border:none; border-top:1px solid {GRIS_L}!important; margin:24px 0; }}

  /* ── Sidebar section labels ── */
  .sidebar-label {{
    font-size:0.7rem; text-transform:uppercase; letter-spacing:1px;
    color:{TEXTO_S}; font-weight:700; margin:16px 0 8px;
    padding-left:4px;
  }}

  /* ── Ocultar header default de Streamlit ── */
  #MainMenu, footer, header {{ visibility:hidden; }}
  .block-container {{ padding-top:24px!important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ÁREAS CON IDs DE GOOGLE DRIVE
# ─────────────────────────────────────────────────────────────────────────────
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
        "Susana Manrique León":              "1kaHFxz44_MHLEsGT_PTWbPs1MDzEG1xf",
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

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE MESES
# ─────────────────────────────────────────────────────────────────────────────
ORDEN_MESES_BASE = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
                    "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
ORDEN_MESES = [f"{m} {y}" for y in ["2024","2025","2026","2027"] for m in ORDEN_MESES_BASE]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
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
_PAT_ANIO = re.compile(r'\b(202[4-7]|[2][4-7])\b')
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
    n = str(nombre).strip()
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
    if not txt or len(txt) < 5: return False
    if txt.upper().startswith("#"): return False
    if re.match(r'^[\d\.\%\,\-\#\s]+$', txt): return False
    txt_norm = normalizar(txt)
    if txt_norm in PALABRAS_NEG: return False
    for p in ["total de actividades","periodo de evaluacion","rendimiento","promedio general","calificacion"]:
        if p in txt_norm: return False
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
        raw = descargar_excel(file_id)
        excel_data = pd.read_excel(raw, sheet_name=None, header=None, engine="openpyxl")
    except Exception as e:
        return [], [], [], [f"Error: {e}"]

    resumenes, semanas, caps = [], [], []

    for tab_name, df in excel_data.items():
        if not es_tab_mes(tab_name): continue
        mes = formatear_mes_anio(tab_name) or str(tab_name).upper()
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
                            caps.append({"Área":area,"Colaborador":alias,"Mes":mes,"Capacitación":txt})
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
                            caps.append({"Área":area,"Colaborador":alias,"Mes":mes,"Capacitación":txt})

        sem_tab, usados = [], set()
        for fp in sorted(periodos):
            for ft in sorted(totales):
                if ft > fp and ft not in usados:
                    p = periodos[fp]
                    m_re = re.match(r'(\d+)', p)
                    sem_tab.append({
                        "Área":area,"Colaborador":alias,
                        "Mes":formatear_mes_anio(p) or mes,
                        "Periodo":p,"Rendimiento":totales[ft],
                        "_orden":int(m_re.group(1)) if m_re else 99,
                    })
                    usados.add(ft); break
        semanas.extend(sem_tab)
        if sem_tab:
            prom = sum(x["Rendimiento"] for x in sem_tab) / len(sem_tab)
            resumenes.append({"Área":area,"Colaborador":alias,"Mes":mes,"Promedio Mes":round(prom,1)})

    if not debug:
        tabs = ", ".join(f"'{t}'" for t in excel_data.keys())
        debug = [f"Sin pestaña de mes. Pestañas: {tabs}"]
    return resumenes, semanas, caps, debug

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / header institucional
    st.markdown(f"""
    <div style='background:{GUINDA};padding:20px 16px;margin:-20px -20px 0;text-align:center;'>
      <div style='font-size:2rem;margin-bottom:6px;'>🏛️</div>
      <div style='color:white;font-weight:700;font-size:1rem;letter-spacing:.5px;'>
        VALLE DE SANTIAGO
      </div>
      <div style='color:{DORADO};font-size:0.7rem;letter-spacing:2px;margin-top:4px;font-weight:600;'>
        PRESIDENCIA MUNICIPAL
      </div>
      <div style='color:rgba(255,255,255,0.6);font-size:0.72rem;margin-top:6px;'>
        Administración 2024 – 2027
      </div>
    </div>
    <div style='margin-bottom:20px;'></div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Sincronizar Drive", use_container_width=True):
        st.cache_data.clear()
        for k in ["global_df","global_ok"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown(f"<div class='sidebar-label'>Dependencia</div>", unsafe_allow_html=True)
    area_sel = st.selectbox("", list(AREAS.keys()), label_visibility="collapsed")
    colabs_area = AREAS[area_sel]

    nombres_a = [n.strip() for n in colabs_area]
    st.markdown(f"<div class='sidebar-label'>Personal</div>", unsafe_allow_html=True)
    colab_sel = st.multiselect("", nombres_a, default=nombres_a, label_visibility="collapsed")

# ─────────────────────────────────────────────────────────────────────────────
# CARGA GLOBAL PARALELA
# ─────────────────────────────────────────────────────────────────────────────
if "global_df" not in st.session_state:
    tareas = [
        (n.strip(), fid, area)
        for area, cols in AREAS.items()
        for n, fid in cols.items()
        if fid.upper() not in ("PENDIENTE","")
    ]
    placeholder = st.empty()
    with placeholder.container():
        prog = st.progress(0, text="Cargando evaluaciones de todas las dependencias…")
        all_res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
            futuros = {ex.submit(obtener_datos, t[0], t[1], t[2]): t for t in tareas}
            for i, fut in enumerate(concurrent.futures.as_completed(futuros), 1):
                try:
                    res, _, _, _ = fut.result()
                    all_res.extend(res)
                except Exception:
                    pass
                prog.progress(i/len(tareas), text=f"Cargando… {i}/{len(tareas)} servidores")
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

# ─────────────────────────────────────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:8px;'>
  <div style='font-size:0.78rem;color:{TEXTO_S};font-weight:600;
       text-transform:uppercase;letter-spacing:1px;'>
    Sistema de Evaluación de Desempeño
  </div>
  <h1 style='color:{GUINDA};font-size:1.8rem;margin:4px 0 2px;font-weight:700;'>
    {area_sel}
  </h1>
  <div style='color:{TEXTO_S};font-size:0.88rem;'>
    H. Ayuntamiento de Valle de Santiago &nbsp;·&nbsp; Administración 2024–2027
  </div>
</div>
""", unsafe_allow_html=True)

# Métricas globales
k1, k2, k3 = st.columns(3)
k1.metric("Área con Mejor Desempeño", mejor_area_n)
k2.metric("Eficiencia Área Líder", f"{mejor_area_v:.1f}%")
k3.metric("Dependencias Registradas", len(AREAS))

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAVEGACIÓN EN TABS (3 secciones)
# ─────────────────────────────────────────────────────────────────────────────
TAB_LABELS = [
    "📊  Ranking Trimestral",
    "🏆  Equipo de Alto Desempeño",
    "📋  Resultados del Programa",
]
tab1, tab2, tab3 = st.tabs(TAB_LABELS)

# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS POR ÁREA (para tabs 2 y 3)
# ─────────────────────────────────────────────────────────────────────────────
if not colabs_area:
    with tab2:
        st.info(f"El área de **{area_sel}** aún no tiene personal asignado.")
    with tab3:
        st.info(f"El área de **{area_sel}** aún no tiene personal asignado.")
else:
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

    # Relleno con 0% para colaboradores sin datos
    _MES_HOY = f"{ORDEN_MESES_BASE[_dt.datetime.now().month - 1]} {_dt.datetime.now().year}"
    _meses_ref = list(df_res["Mes"].unique()) if not df_res.empty else [_MES_HOY]
    _colabs_con_datos = set(df_res["Colaborador"].unique())
    _filas_cero = []
    for _nombre in [n.strip() for n in colabs_area.keys()]:
        if _nombre not in _colabs_con_datos:
            for _mes in _meses_ref:
                _filas_cero.append({"Área":area_sel,"Colaborador":_nombre,"Mes":_mes,"Promedio Mes":0.0})
    if _filas_cero:
        df_res = pd.concat([df_res, pd.DataFrame(_filas_cero, columns=C_RES)], ignore_index=True)

    meses_d = []
    if not df_res.empty:
        meses_presentes = list(df_res["Mes"].unique())
        meses_d = [m for m in ORDEN_MESES if m in meses_presentes]
        meses_d.extend([m for m in meses_presentes if m not in meses_d])

    # Filtro de mes en sidebar (solo relevante para tabs 2 y 3)
    with st.sidebar:
        st.markdown(f"<div class='sidebar-label'>Periodo</div>", unsafe_allow_html=True)
        mes_sel = st.selectbox("", ["Todos"] + meses_d, label_visibility="collapsed")

    df_rf = df_res[df_res["Colaborador"].isin(colab_sel)].copy()
    df_sf = df_sem[df_sem["Colaborador"].isin(colab_sel)].copy()
    df_cf = df_cap[df_cap["Colaborador"].isin(colab_sel)].copy()
    if mes_sel != "Todos":
        df_rf = df_rf[df_rf["Mes"]==mes_sel]
        df_sf = df_sf[df_sf["Mes"]==mes_sel]
        df_cf = df_cf[df_cf["Mes"]==mes_sel]

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 — RANKING TRIMESTRAL
    # ──────────────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown(f"""
        <div class='coming-soon'>
          <div class='icon'>📊</div>
          <h3>Ranking Trimestral</h3>
          <p>Esta sección mostrará el comparativo de desempeño por trimestre entre
          dependencias y servidores públicos. Próximamente disponible.</p>
          <div style='margin-top:24px;display:inline-block;
               background:{GRIS_L};border-radius:20px;padding:6px 16px;
               font-size:0.8rem;color:{TEXTO_S};font-weight:600;'>
            🔒 En desarrollo
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 — EQUIPO DE ALTO DESEMPEÑO
    # ──────────────────────────────────────────────────────────────────────────
    with tab2:
        if not df_rf.empty:
            # Ordenar meses
            orden_final = [m for m in ORDEN_MESES if m in df_rf["Mes"].unique()]
            orden_final.extend([m for m in df_rf["Mes"].unique() if m not in orden_final])
            df_rf["Mes"] = pd.Categorical(df_rf["Mes"], categories=orden_final, ordered=True)

            # Completar meses faltantes con 0%
            colaboradores = df_rf["Colaborador"].unique()
            full_index = pd.MultiIndex.from_product([colaboradores, orden_final], names=["Colaborador","Mes"])
            df_rf = (df_rf.set_index(["Colaborador","Mes"]).reindex(full_index)
                     .reset_index())
            df_rf["Promedio Mes"] = df_rf["Promedio Mes"].fillna(0.0)
            df_rf["Área"] = df_rf["Área"].fillna(area_sel)
            df_rf["Mes"] = pd.Categorical(df_rf["Mes"], categories=orden_final, ordered=True)

            todos_colabs = sorted(df_rf["Colaborador"].unique())
            color_map = {c: PALETA[i % len(PALETA)] for i, c in enumerate(todos_colabs)}

            # ── KPIs ──────────────────────────────────────────────────────────
            prom_dep = df_rf["Promedio Mes"].mean()
            idx_max  = df_rf["Promedio Mes"].idxmax()

            c1, c2, c3 = st.columns(3)
            c1.metric("Promedio General de la Dependencia", f"{prom_dep:.1f}%")
            c2.metric(
                "Servidor Destacado",
                df_rf.loc[idx_max, "Colaborador"],
                f"{df_rf.loc[idx_max,'Promedio Mes']}%",
            )
            c3.metric("Reportes Semanales Registrados", len(df_sf))

            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

            # ── Botón PDF ─────────────────────────────────────────────────────
            fig_tmp = px.bar(
                df_rf.sort_values("Mes"),
                x="Mes" if mes_sel=="Todos" else "Colaborador",
                y="Promedio Mes", color="Colaborador",
                barmode="group", text="Promedio Mes",
                color_discrete_map=color_map,
            )
            fig_tmp.update_traces(texttemplate="%{text:.0f}%", textposition="outside",
                                  cliponaxis=False, marker_line_width=1,
                                  marker_line_color="rgba(0,0,0,0.1)")
            fig_tmp.update_layout(
                template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)", font_color=TEXTO,
                legend=dict(orientation="h",yanchor="bottom",y=-0.3,xanchor="center",x=0.5),
                margin=dict(t=30,b=20),
            )

            filas_html = "".join(
                f"<tr><td>{r['Colaborador']}</td><td>{r['Mes']}</td>"
                f"<td style='font-weight:bold;color:{GUINDA};'>{r['Promedio Mes']}%</td></tr>"
                for _, r in df_rf.iterrows()
            )
            html_rep = f"""<html><head><meta charset='utf-8'>
            <style>
              body{{font-family:Arial;color:#212529;margin:30px;background:white}}
              .hdr{{text-align:center;border-bottom:3px solid {GUINDA};padding-bottom:15px;margin-bottom:20px}}
              .hdr h1{{color:{GUINDA};margin:0;font-size:24px}}
              .hdr p{{color:{DORADO};margin:5px 0 0;font-weight:bold;letter-spacing:2px;font-size:11px}}
              .mb{{background:#f8f9fa;padding:15px;border-left:5px solid {GUINDA};border-radius:4px;margin-bottom:20px}}
              table.dt{{width:100%;border-collapse:collapse;margin-top:15px}}
              table.dt th{{background:{GUINDA};color:white;padding:10px;text-align:left;font-size:13px}}
              table.dt td{{padding:9px;border-bottom:1px solid #e9ecef;font-size:12px}}
              table.dt tr:nth-child(even){{background:#f8f9fa}}
              @media print{{*{{-webkit-print-color-adjust:exact!important}}}}
            </style></head><body>
            <div class='hdr'><h1>VALLE DE SANTIAGO</h1>
              <p>PRESIDENCIA MUNICIPAL • ADMINISTRACIÓN 2024-2027</p></div>
            <h2>Reporte de Evaluación de Desempeño — {area_sel}</h2>
            <div class='mb'><table>
              <tr><td width='35%'><b>Dependencia:</b></td><td>{area_sel}</td></tr>
              <tr><td><b>Periodo:</b></td><td>{mes_sel}</td></tr>
              <tr><td><b>Promedio General:</b></td>
                  <td style='color:{GUINDA};font-weight:bold;'>{prom_dep:.1f}%</td></tr>
            </table></div>
            <div>{fig_tmp.to_html(full_html=False,include_plotlyjs='cdn')}</div>
            <br><table class='dt'><thead><tr>
              <th>Servidor Público</th><th>Mes</th><th>Rendimiento</th>
            </tr></thead><tbody>{filas_html}</tbody></table>
            <div style='margin-top:40px;text-align:center;font-size:11px;color:#6c757d;
                 border-top:1px solid #e9ecef;padding-top:15px;'>
              H. Ayuntamiento de Valle de Santiago • Ctrl+P → Guardar como PDF</div>
            <script>window.onload=function(){{setTimeout(()=>window.print(),1000);}}</script>
            </body></html>"""

            _, col_btn = st.columns([5, 1])
            with col_btn:
                st.download_button(
                    "📄 Exportar PDF",
                    data=html_rep,
                    file_name=f"Reporte_{area_sel}.html",
                    mime="text/html",
                    use_container_width=True,
                )

            # ── Gráfica de barras ─────────────────────────────────────────────
            st.plotly_chart(fig_tmp, use_container_width=True)

            # ── Tabla + Evaluaciones semanales ────────────────────────────────
            t1_col, t2_col = st.columns([1, 2])
            with t1_col:
                st.markdown(f"""
                <div style='font-size:0.78rem;text-transform:uppercase;
                     letter-spacing:.8px;color:{TEXTO_S};font-weight:600;
                     margin-bottom:10px;'>
                  Promedios por Mes
                </div>""", unsafe_allow_html=True)
                st.dataframe(
                    df_rf[["Colaborador","Mes","Promedio Mes"]],
                    hide_index=True, use_container_width=True,
                )
            with t2_col:
                st.markdown(f"""
                <div style='font-size:0.78rem;text-transform:uppercase;
                     letter-spacing:.8px;color:{TEXTO_S};font-weight:600;
                     margin-bottom:10px;'>
                  Evaluaciones Semanales
                </div>""", unsafe_allow_html=True)
                if not df_sf.empty:
                    st.dataframe(
                        df_sf.sort_values(["Colaborador","_orden"])
                             [["Colaborador","Periodo","Rendimiento"]],
                        hide_index=True, use_container_width=True,
                    )
                else:
                    st.info("Sin evaluaciones semanales para el periodo seleccionado.")

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── DIRECTORIO CON FOTOS ───────────────────────────────────────────
            st.markdown(f"""
            <div style='font-size:0.78rem;text-transform:uppercase;
                 letter-spacing:.8px;color:{TEXTO_S};font-weight:600;
                 margin-bottom:14px;'>
              Directorio del Equipo
            </div>""", unsafe_allow_html=True)
            st.caption("Toca el nombre de un servidor público para ver su perfil.")

            # Inicializar estado de foto
            if "foto_colab" not in st.session_state:
                st.session_state.foto_colab = None

            # Generar iniciales para avatar
            def get_initials(name):
                parts = name.split()
                if len(parts) >= 2:
                    return (parts[0][0] + parts[1][0]).upper()
                return name[:2].upper()

            # Grid de colaboradores (3 por fila)
            grid_colabs = list(colabs_area.items())
            for row_start in range(0, len(grid_colabs), 3):
                cols = st.columns(3)
                for ci, (nombre, fid) in enumerate(grid_colabs[row_start:row_start+3]):
                    nombre_limpio = nombre.strip()
                    tiene_dato = fid.upper() not in ("PENDIENTE","")
                    initials = get_initials(nombre_limpio)
                    with cols[ci]:
                        # Mini card de colaborador
                        col_a, col_b = st.columns([1, 3])
                        with col_a:
                            st.markdown(f"""
                            <div class='avatar-sm'
                                 style='width:40px;height:40px;border-radius:50%;
                                        background:{GUINDA};color:white;
                                        display:flex;align-items:center;
                                        justify-content:center;font-size:0.8rem;
                                        font-weight:700;border:2px solid {DORADO};'>
                              {initials}
                            </div>""", unsafe_allow_html=True)
                        with col_b:
                            # Botón que abre perfil
                            if st.button(
                                nombre_limpio,
                                key=f"btn_{nombre_limpio}",
                                use_container_width=True,
                                help="Ver perfil"
                            ):
                                st.session_state.foto_colab = nombre_limpio

                        # Badge de estado
                        estado = "✅ Con reporte" if tiene_dato else "⏳ Pendiente"
                        color_badge = VERDE if tiene_dato else "#9ca3af"
                        st.markdown(f"""
                        <div style='font-size:0.7rem;color:{color_badge};
                             padding:0 4px 12px;font-weight:600;'>
                          {estado}
                        </div>""", unsafe_allow_html=True)

            # ── Modal de foto ─────────────────────────────────────────────────
            if st.session_state.foto_colab:
                nombre_m = st.session_state.foto_colab
                initials_m = get_initials(nombre_m)
                # Buscar área del colaborador
                area_m = area_sel

                with st.container():
                    st.markdown(f"""
                    <div style='background:{BLANCO};border:1px solid {GRIS_L};
                         border-radius:16px;padding:28px;margin-top:12px;
                         max-width:380px;box-shadow:0 8px 32px rgba(0,0,0,0.1);'>
                      <div style='text-align:center;'>
                        <div style='width:96px;height:96px;border-radius:50%;
                             background:{GUINDA};color:white;
                             display:flex;align-items:center;justify-content:center;
                             font-size:2rem;font-weight:700;margin:0 auto 16px;
                             border:4px solid {DORADO};'>
                          {initials_m}
                        </div>
                        <h3 style='color:{GUINDA};margin:0 0 4px;font-size:1.05rem;'>
                          {nombre_m}
                        </h3>
                        <div style='color:{TEXTO_S};font-size:0.82rem;margin-bottom:6px;'>
                          {area_m}
                        </div>
                        <div style='color:{TEXTO_S};font-size:0.75rem;
                             background:{GRIS_F};border-radius:6px;padding:4px 10px;
                             display:inline-block;margin-bottom:4px;'>
                          📷 Sin fotografía registrada
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("✕  Cerrar perfil", key="cerrar_foto"):
                        st.session_state.foto_colab = None
                        st.rerun()

            # ── Capacitaciones ─────────────────────────────────────────────────
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='font-size:0.78rem;text-transform:uppercase;
                 letter-spacing:.8px;color:{TEXTO_S};font-weight:600;
                 margin-bottom:14px;'>
              🎓 Capacitaciones y Desarrollo Profesional
            </div>""", unsafe_allow_html=True)

            if not df_cf.empty:
                m1, m2, m3 = st.columns(3)
                m1.metric("Total de Capacitaciones", df_cf.shape[0])
                m2.metric("Servidores capacitados", df_cf["Colaborador"].nunique())
                m3.metric("Meses con registro", df_cf["Mes"].nunique())

                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

                df_cnt = (df_cf.groupby("Colaborador").size()
                          .reset_index(name="Total")
                          .sort_values("Total", ascending=False))
                color_map_cap = get_color_map(df_cnt["Colaborador"].unique())
                fig_c = px.bar(df_cnt, x="Colaborador", y="Total", text_auto=True,
                               color="Colaborador", color_discrete_map=color_map_cap,
                               title="Cursos por Servidor Público")
                fig_c.update_layout(
                    template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)", font_color=TEXTO,
                    title_font_color=GUINDA, showlegend=False,
                    xaxis_title="", yaxis_title="N° cursos", margin=dict(t=40,b=10),
                )
                st.plotly_chart(fig_c, use_container_width=True)

                df_grp = (df_cf.groupby("Colaborador")
                          .agg(Total=("Capacitación","count"), Lista=("Capacitación",list))
                          .reset_index().sort_values("Total", ascending=False))
                cols2 = st.columns(2)
                for idx, row in df_grp.iterrows():
                    with cols2[idx % 2]:
                        cursos_h = "".join(
                            f"<div style='margin:4px 0 4px 12px;color:{TEXTO};font-size:0.85rem;'>"
                            f"• {c}</div>" for c in row["Lista"]
                        )
                        st.markdown(f"""
                        <div style='background:{BLANCO};padding:16px 20px;border-radius:10px;
                             border:1px solid {GRIS_L};border-left:4px solid {VERDE};
                             margin-bottom:14px;'>
                          <div style='display:flex;justify-content:space-between;
                               align-items:center;margin-bottom:10px;'>
                            <div style='color:{GUINDA};font-weight:700;font-size:0.92rem;'>
                              {row['Colaborador']}
                            </div>
                            <span style='background:{DORADO};color:white;padding:2px 10px;
                                  border-radius:12px;font-size:0.75rem;font-weight:700;'>
                              {row['Total']} curso(s)
                            </span>
                          </div>
                          {cursos_h}
                        </div>""", unsafe_allow_html=True)
            else:
                st.info("Sin capacitaciones registradas para el periodo seleccionado.")

            # ── Diagnóstico ────────────────────────────────────────────────────
            with st.expander("🔍 Diagnóstico de hojas detectadas"):
                for colab, pests in debug_info.items():
                    st.markdown(f"**{colab}**")
                    for p in pests:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;{p}")

        else:
            st.info("No hay datos numéricos para mostrar con los filtros actuales.")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 — RESULTADOS DEL PROGRAMA DE EVALUACIÓN
    # ──────────────────────────────────────────────────────────────────────────
    with tab3:
        # Resumen general del área con datos globales
        df_area_global = df_global[df_global["Área"] == area_sel] if not df_global.empty else pd.DataFrame()

        if not df_area_global.empty:
            prom_area = df_area_global["Promedio Mes"].mean()
            n_colabs  = df_area_global["Colaborador"].nunique()
            n_meses   = df_area_global["Mes"].nunique()

            # ── KPIs del programa ───────────────────────────────────────────
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Eficiencia del Área", f"{prom_area:.1f}%")
            p2.metric("Servidores Evaluados", n_colabs)
            p3.metric("Meses con Evaluación", n_meses)

            # Posición del área en el ranking global
            if not df_global.empty:
                ranking = (df_global.groupby("Área")["Promedio Mes"].mean()
                           .sort_values(ascending=False).reset_index())
                ranking["Posición"] = range(1, len(ranking)+1)
                pos_area = ranking[ranking["Área"]==area_sel]["Posición"].values
                p4.metric("Posición Global", f"#{pos_area[0]} de {len(ranking)}" if len(pos_area) else "N/A")

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            # ── Tendencia mensual del área (línea) ─────────────────────────
            df_tend = (df_area_global.groupby("Mes")["Promedio Mes"].mean().reset_index())
            df_tend["Mes_cat"] = pd.Categorical(
                df_tend["Mes"],
                categories=[m for m in ORDEN_MESES if m in df_tend["Mes"].values],
                ordered=True,
            )
            df_tend = df_tend.sort_values("Mes_cat")

            if len(df_tend) > 1:
                fig_tend = px.line(
                    df_tend, x="Mes", y="Promedio Mes",
                    markers=True,
                    title=f"Tendencia de Desempeño — {area_sel}",
                    color_discrete_sequence=[GUINDA],
                )
                fig_tend.add_hline(
                    y=df_global["Promedio Mes"].mean(),
                    line_dash="dot", line_color=VERDE,
                    annotation_text="Promedio institucional",
                    annotation_position="bottom right",
                )
                fig_tend.update_traces(line_width=3, marker_size=8)
                fig_tend.update_layout(
                    template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)", font_color=TEXTO,
                    title_font_color=GUINDA, xaxis_title="", yaxis_title="% Promedio",
                    margin=dict(t=50, b=10),
                    yaxis=dict(range=[0, 110]),
                )
                st.plotly_chart(fig_tend, use_container_width=True)

            # ── Comparativo con otras áreas ─────────────────────────────────
            st.markdown(f"""
            <div style='font-size:0.78rem;text-transform:uppercase;
                 letter-spacing:.8px;color:{TEXTO_S};font-weight:600;
                 margin:20px 0 12px;'>
              Comparativo Institucional de Dependencias
            </div>""", unsafe_allow_html=True)

            df_comp = (df_global.groupby("Área")["Promedio Mes"].mean()
                       .sort_values(ascending=False).reset_index())
            df_comp["Color"] = df_comp["Área"].apply(
                lambda a: GUINDA if a == area_sel else "#d1d5db"
            )
            fig_comp = px.bar(
                df_comp, x="Área", y="Promedio Mes",
                text="Promedio Mes",
                color="Área",
                color_discrete_map={row["Área"]: row["Color"] for _, row in df_comp.iterrows()},
            )
            fig_comp.update_traces(
                texttemplate="%{text:.0f}%", textposition="outside",
                cliponaxis=False, marker_line_width=0,
            )
            fig_comp.update_layout(
                template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)", font_color=TEXTO,
                showlegend=False, xaxis_title="", yaxis_title="% Promedio",
                xaxis=dict(tickangle=-35),
                margin=dict(t=20, b=80),
                yaxis=dict(range=[0, 115]),
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            # ── Tabla de ranking completo ────────────────────────────────────
            with st.expander("Ver tabla de ranking completo"):
                df_rank_show = df_comp.copy()
                df_rank_show.insert(0, "Posición", range(1, len(df_rank_show)+1))
                df_rank_show["Promedio Mes"] = df_rank_show["Promedio Mes"].map(lambda x: f"{x:.1f}%")
                df_rank_show = df_rank_show[["Posición","Área","Promedio Mes"]]
                st.dataframe(df_rank_show, hide_index=True, use_container_width=True)

        else:
            st.markdown(f"""
            <div class='coming-soon'>
              <div class='icon'>📋</div>
              <h3>Resultados del Programa</h3>
              <p>Aún no hay datos disponibles para <strong>{area_sel}</strong>.
              Sincroniza con Drive o espera a que se carguen los reportes.</p>
            </div>
            """, unsafe_allow_html=True)
