# DOCUMENTACIÓN REALIZADA POR HERIBERTO PICENO ACOSTA TSU
# Versión 3.0 — Diseño Profesional de Gobierno Municipal

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
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Evaluación de Desempeño — Valle de Santiago",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# TOKENS DE DISEÑO
# ─────────────────────────────────────────────────────────────────────────────
GUINDA  = "#601a1e"
GUINDA2 = "#7a2226"
DORADO  = "#f1b80c"
VERDE   = "#117a4b"
GRIS_F  = "#f0f2f5"
GRIS_L  = "#e2e5ea"
GRIS_M  = "#9ca3af"
BLANCO  = "#ffffff"
TEXTO   = "#1c1f26"
TEXTO_S = "#6b7280"
PALETA  = ["#601a1e","#117a4b","#f1b80c","#2c3e50","#d35400","#7d3c98","#16a085","#2e4053"]

# ─────────────────────────────────────────────────────────────────────────────
# CSS PROFESIONAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp {{
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: {GRIS_F} !important;
    color: {TEXTO} !important;
}}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
#MainMenu, footer, header {{ visibility: hidden !important; display: none !important; }}

/* ── Sidebar completo ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {GUINDA} 0%, #3d1012 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.2) !important;
    min-width: 260px !important;
    max-width: 260px !important;
}}
[data-testid="stSidebar"] > div {{
    padding: 0 !important;
    background: transparent !important;
}}
/* Forzar fondo del sidebar en todos los niveles */
[data-testid="stSidebar"] * {{
    background-color: transparent !important;
}}
[data-testid="stSidebarContent"] {{
    background: transparent !important;
    padding: 0 !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    background: transparent !important;
}}

/* ── Logo area del sidebar ── */
.sidebar-logo-area {{
    padding: 24px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 8px;
    text-align: center;
}}
.sidebar-logo-area img {{
    max-width: 140px !important;
    margin-bottom: 10px !important;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
}}
.sidebar-org-name {{
    color: white;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
}}
.sidebar-admin {{
    color: {DORADO};
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}}

/* ── Menú de navegación sidebar ── */
.sidebar-section-label {{
    color: rgba(255,255,255,0.4);
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 16px 20px 6px;
}}
.nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 20px;
    margin: 2px 10px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    border: none;
    background: transparent;
    width: calc(100% - 20px);
    text-align: left;
    color: rgba(255,255,255,0.75);
    font-size: 0.87rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}}
.nav-item:hover {{ background: rgba(255,255,255,0.1) !important; color: white; }}
.nav-item.active {{
    background: rgba(255,255,255,0.15) !important;
    color: white !important;
    font-weight: 600;
    box-shadow: inset 3px 0 0 {DORADO};
}}
.nav-icon {{ font-size: 1.05rem; width: 20px; text-align: center; }}

/* ── Filtros en sidebar ── */
.sidebar-filter-area {{
    padding: 0 10px;
    margin-top: 4px;
}}
.sidebar-filter-label {{
    color: rgba(255,255,255,0.4);
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 16px 10px 6px;
    display: block;
}}
/* Inputs en sidebar oscuro */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {{
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: white !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: rgba(255,255,255,0.5) !important;
    font-size: 0.62rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-weight: 700 !important;
}}
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] input {{
    color: white !important;
    background: transparent !important;
}}
/* Botones sidebar */
[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.12) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 8px 14px !important;
    transition: all 0.2s !important;
    font-weight: 500 !important;
    margin: 0 10px !important;
    width: calc(100% - 20px) !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255,255,255,0.22) !important;
    border-color: {DORADO} !important;
}}
.sidebar-version {{
    position: absolute;
    bottom: 16px;
    left: 0; right: 0;
    text-align: center;
    color: rgba(255,255,255,0.25);
    font-size: 0.65rem;
}}

/* ── Contenido principal ── */
.main-content {{
    padding: 32px 36px 40px;
    background: {GRIS_F};
    min-height: 100vh;
}}

/* ── Header de página ── */
.page-header {{
    background: {BLANCO};
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid {GRIS_L};
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 20px;
}}
.page-header-icon {{
    width: 52px; height: 52px;
    background: linear-gradient(135deg, {GUINDA}, {GUINDA2});
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(96,26,30,0.3);
}}
.page-header-eyebrow {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {GUINDA};
    margin-bottom: 4px;
}}
.page-header-title {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {TEXTO};
    margin: 0;
    line-height: 1.2;
}}
.page-header-sub {{
    font-size: 0.82rem;
    color: {TEXTO_S};
    margin-top: 3px;
}}

/* ── KPI Cards ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}}
.kpi-card {{
    background: {BLANCO};
    border-radius: 12px;
    padding: 20px 22px;
    border: 1px solid {GRIS_L};
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: {GUINDA};
}}
.kpi-card.verde::before {{ background: {VERDE}; }}
.kpi-card.dorado::before {{ background: {DORADO}; }}
.kpi-label {{
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {TEXTO_S};
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 1.9rem;
    font-weight: 800;
    color: {TEXTO};
    line-height: 1;
    margin-bottom: 4px;
}}
.kpi-sub {{
    font-size: 0.75rem;
    color: {TEXTO_S};
    margin: 0;
}}

/* ── Métricas Streamlit ocultas (usamos HTML puro) ── */
div[data-testid="metric-container"] {{
    background: {BLANCO} !important;
    border: 1px solid {GRIS_L} !important;
    border-top: 3px solid {GUINDA} !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04) !important;
}}
[data-testid="stMetricLabel"] p {{
    color: {TEXTO_S} !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
[data-testid="stMetricValue"] div {{
    color: {TEXTO} !important;
    font-weight: 800 !important;
    font-size: 1.7rem !important;
}}

/* ── Contenedor de sección ── */
.section-card {{
    background: {BLANCO};
    border-radius: 12px;
    padding: 24px 26px;
    border: 1px solid {GRIS_L};
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}}
.section-title {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {TEXTO_S};
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid {GRIS_L};
    display: flex;
    align-items: center;
    gap: 8px;
}}
.section-title span {{ color: {GUINDA}; font-size: 1rem; }}

/* ── Directorio de colaboradores ── */
.dir-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
    margin-top: 4px;
}}
.dir-card {{
    background: {GRIS_F};
    border: 1px solid {GRIS_L};
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.15s;
}}
.dir-card:hover {{ border-color: {GUINDA}; box-shadow: 0 2px 10px rgba(96,26,30,0.12); }}
.dir-avatar {{
    width: 42px; height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, {GUINDA}, {GUINDA2});
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 800; color: white;
    flex-shrink: 0;
    border: 2px solid rgba(241,184,12,0.4);
}}
.dir-name {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {TEXTO};
    line-height: 1.3;
}}
.dir-status {{
    font-size: 0.68rem;
    color: {TEXTO_S};
    margin-top: 2px;
}}

/* ── Perfil card ── */
.profile-card {{
    background: {BLANCO};
    border-radius: 16px;
    padding: 30px 28px;
    border: 1px solid {GRIS_L};
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 20px;
}}
.profile-avatar-lg {{
    width: 100px; height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, {GUINDA}, {GUINDA2});
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 800; color: white;
    margin: 0 auto 16px;
    border: 4px solid {DORADO};
    box-shadow: 0 4px 20px rgba(96,26,30,0.3);
}}
.profile-name {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {TEXTO};
    margin-bottom: 4px;
}}
.profile-dept {{
    font-size: 0.8rem;
    color: {TEXTO_S};
    margin-bottom: 12px;
}}
.profile-no-photo {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {GRIS_F};
    border: 1px dashed {GRIS_M};
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 0.72rem;
    color: {TEXTO_S};
}}

/* ── Cap cards ── */
.cap-card {{
    background: {BLANCO};
    border-radius: 10px;
    padding: 16px 18px;
    border: 1px solid {GRIS_L};
    border-left: 4px solid {VERDE};
    margin-bottom: 12px;
}}
.cap-name {{
    font-size: 0.88rem;
    font-weight: 700;
    color: {GUINDA};
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.cap-badge {{
    background: {DORADO};
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
}}
.cap-item {{
    font-size: 0.82rem;
    color: {TEXTO};
    padding: 3px 0;
    border-bottom: 1px solid {GRIS_F};
}}
.cap-item:last-child {{ border-bottom: none; }}
.cap-item::before {{ content: "·  "; color: {GUINDA}; font-weight: 700; }}

/* ── Coming soon ── */
.coming-soon-card {{
    background: {BLANCO};
    border-radius: 14px;
    padding: 60px 40px;
    text-align: center;
    border: 1px solid {GRIS_L};
    border-top: 4px solid {GUINDA};
}}
.coming-soon-icon {{ font-size: 3rem; margin-bottom: 16px; }}
.coming-soon-title {{ font-size: 1.2rem; font-weight: 700; color: {TEXTO}; margin-bottom: 8px; }}
.coming-soon-desc {{ font-size: 0.87rem; color: {TEXTO_S}; max-width: 360px; margin: 0 auto 20px; line-height: 1.6; }}
.coming-badge {{
    display: inline-block;
    background: {GRIS_F};
    border: 1px solid {GRIS_L};
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.72rem;
    font-weight: 700;
    color: {TEXTO_S};
    letter-spacing: 0.5px;
}}

/* ── Botones ── */
.stButton > button, .stDownloadButton > button {{
    background: {GUINDA} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 2px 8px rgba(96,26,30,0.2) !important;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    background: {GUINDA2} !important;
    box-shadow: 0 4px 16px rgba(96,26,30,0.3) !important;
    transform: translateY(-1px) !important;
}}
/* Excepto sidebar */
[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.12) !important;
    box-shadow: none !important;
}}

/* ── Tablas ── */
.stDataFrame {{
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid {GRIS_L} !important;
}}
.stDataFrame th {{
    background: {GRIS_F} !important;
    color: {TEXTO_S} !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}}

/* ── Divisor ── */
hr {{ border: none; border-top: 1px solid {GRIS_L} !important; margin: 24px 0; }}

/* ── Expander ── */
.streamlit-expanderHeader {{
    background: {GRIS_F} !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: {TEXTO_S} !important;
}}
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
    "Comude": { "Rebeca Martínez García": "1gJVYV6S0UEIHBCKXHVJhp3qv9g3jwGC_" },
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
        "Diego Vilchis":          "1GwVCiHahHMryaY3iqgq5BfpQ3m6DPUGf",
        "Guillermo Medel Cardenas":"1Af6rjrKgqC7EMpqSXw7uW6JVjcuoCSE5",
    },
    "Imjuv": {
        "Brandon Alexis Núñez Lorenzo": "10WfZdp0o4h3Ho7JIhD_gda_-3wyATzHP",
        "Johana González González":     "1rIKeMoM8DopIxXhqLtCTmN5U2DtSAS6q",
        "Josue Adan Hernández Tavera":  "1kgVt19Sz9yTRDAB1Q89mlbz0x0eitYxa",
    },
    "Implan": {
        "Citlaly Arredondo García":        "1j-RhSieVJDz1OcDj6u9Bo_Fgo2B8Olrj",
        "Erendira Virginia Morales Pérez": "1tRIWGzEUHOMs1zX91tm-F-13Vh174H-z",
    },
    "Informática": {
        "Genesis Aurora Mercado Rodriguez": "1XqEk9AnSV9yseS9KMy9qMzMZBA9x--W7",
        "Julio Prieto Sanchez":             "1HZu9R94LkcXk4mjOGkxQ5_ph4lCZ8q6e",
        "Pablo Vazquez Barroso":            "1pDF0KYgpBdVPIy8VQDtc6e0ia49cebqP",
    },
    "Jurídico": {
        "Batriz Adriana Ramirez Garcia":  "1WPzGkbog8VNmUCI6K5SuL5orQUU5XWsl",
        "Berenice Butanda Granados":      "PENDIENTE",
        "Hector Israel Bautista Alegria": "PENDIENTE",
        "Liliana Armenta Rico":           "PENDIENTE",
        "Luis Angel Negrete Chavez":      "PENDIENTE",
        "Nancy Estefania Gamez Garcia":   "PENDIENTE",
        "Rodrigo Ortega Gomez":           "PENDIENTE",
    },
    "Limpia":             { "Manuel Alejandro Arroyo Garcia": "17eT4dCA8-tfW2zEzHq_OlVD_9vUeFQl_" },
    "Mercado Municipal":  { "Marco Antonio Mosqueda Murillo": "1tHvM80h5Ow4qayzsfneLzpuy8FMUQ6TI" },
    "Panteon Campo Florido": { "Letycia Ayala Carranza": "1utBDxOmZkoIDhbn-QIusJYaITA9YlWrT" },
    "Parques Y Jardines": { "Marcos García Franco": "1R4QDQm0ugjl_4q94hFqeuW_tjYt3dXtV" },
    "Procurador Auxiliar": {
        "Alondra Baeza Olivares":      "1WzeLJqrLG0OrlZYYPee_WCnYap-ZkYC4",
        "Dulce Paola Nieto Pallares":  "1VNsnLp8B4Jza8P1vNjkR-F-pQjnHTo52",
        "Maria Graciela Ramirez Alvarez": "1sXrk8XFzRLWaiX8D1o-5LDext4PC8qs4",
    },
    "Recursos Humanos": {
        "Ana Paulina Morales Manriquez":  "1xbx7As9G5d_aBvWKfxaZ71h5sAgvFTxC",
        "Diana Laura Albarran Ahumada":   "143bhUXq3llg_g72_55qyk49Iuulv5nho",
        "Fernanda Abigail Flores Lara":   "1P2pHHFYisvTxsAxvlAmWZMXzO6Jcsx8J",
        "Karla Marina Curtidor Aguilar":  "1A-X1y2yTfd_Crfm3ASUEe0c_1JZppm6K",
    },
    "Salud": {
        "Estefani Baltazar Chiquito":    "1exbbmUI1bGi51-07MhzLhKL3RPK2LIgy",
        "Martha Lidia Aguayo Melchor":   "1DR1UVnHwmkjL9K0zkxlj5NeUkIhh0Sy7",
        "Melani Taisha Yañez Gutierrez": "1MLTHcZDrT2V9nezUhsG3jw7DuQQkH2zt",
        "Susana Manrique León":          "1kaHFxz44_MHLEsGT_PTWbPs1MDzEG1xf",
        "Victor Manuel Santana Ayala":   "15vDT3OVb1hNo8KH1_DNK01mdijZdt97J",
    },
    "Servicios Municipales": {
        "Andrea Quiroz Paredes":          "10E_et9E8yEY884lTewKi8BFDAdN2yXAB",
        "Joanna Sánchez Noriega":         "1Nl10A1cNindQsK-dp4VF233wNoEVs68C",
        "Jose Luis Vazquez Morales":      "1wSk4intcsVxhnrsnc67v2Vhh_8etjUx5",
        "Liliana Deyanira Flores González":"1-QbLy5RBJ_IQmNPcvJGuO13RKjYF0EIH",
        "Ma. Guadalupe Nuñez Acuña":      "1olPLw-rViNRME_6YHhWSHvNtmHHjaB37",
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
    "Transparencia": { "Karla Adriana Alonso Moreno": "1VwsyFghn9owJZCud7oeCsQi9d009zj-W" },
    "Turismo": {
        "Cristian Ramon Gonzalez Gomez":  "17Vq-Fz2LyVzbxcOG-1oiWBlhZAYhilhS",
        "Diana Paola Flores Negrete":     "1lOEVbR7QsxBVqmZbL9GjUsyxAn2ACz_L",
        "Jose Juan Garcia Dominguez":     "1Zqi2jKj0XahjhVnOq2z45Nf0h-dJuWId",
        "Juan Carlos Hernández Quiroz":   "1n6crUbtdr2BQ_WME49yyLBmY-VJVx_C5",
    },
    "Unidad Deportiva": { "Nayeli Guadalupe Ramírez Medina": "1YkJxL_PfX3O46gjaAsvQUxs0GfImFntZ" },
}

ORDEN_MESES_BASE = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
                    "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
ORDEN_MESES = [f"{m} {y}" for y in ["2024","2025","2026","2027"] for m in ORDEN_MESES_BASE]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_initials(name):
    p = name.strip().split()
    return (p[0][0]+p[1][0]).upper() if len(p)>=2 else name[:2].upper()

def get_color_map(colaboradores):
    return {c: PALETA[i % len(PALETA)] for i, c in enumerate(sorted(colaboradores))}

def normalizar(t):
    return str(t).translate(str.maketrans("áéíóúüñÁÉÍÓÚÜÑ","aeiouunAEIOUUN")).lower().strip()

_MESES_DICT = {
    "ENERO":["ENERO","ENE","ENR"],"FEBRERO":["FEBRERO","FEB","FEBR"],
    "MARZO":["MARZO","MAR","MRZ"],"ABRIL":["ABRIL","ABR"],
    "MAYO":["MAYO","MAY"],"JUNIO":["JUNIO","JUN","JNO"],
    "JULIO":["JULIO","JUL","JLO"],"AGOSTO":["AGOSTO","AGO","AGS"],
    "SEPTIEMBRE":["SEPTIEMBRE","SEP","SEPT","SETIEMBRE","SEPTIEMRE"],
    "OCTUBRE":["OCTUBRE","OCT","OCUBRE"],"NOVIEMBRE":["NOVIEMBRE","NOV"],
    "DICIEMBRE":["DICIEMBRE","DIC","DIZ"],
}
_PAT_ANIO  = re.compile(r'\b(202[4-7]|[2][4-7])\b')
_TRANS_ACC = str.maketrans("ÁÉÍÓÚÜÑ","AEIOUUN")

def formatear_mes_anio(texto):
    if not texto or (isinstance(texto, float) and pd.isna(texto)): return None
    limpio = str(texto).upper().translate(_TRANS_ACC)
    limpio = re.sub(r'[\-/_]',' ',limpio); limpio = re.sub(r'\s+',' ',limpio).strip()
    anio = "2026"
    m = _PAT_ANIO.search(limpio)
    if m:
        anio = m.group(1); anio = "20"+anio if len(anio)==2 else anio
        limpio = limpio.replace(m.group(0),'').strip()
    for mes_std, variaciones in _MESES_DICT.items():
        if any(v in limpio for v in variaciones): return f"{mes_std} {anio}"
    return None

def es_tab_mes(nombre):
    return formatear_mes_anio(nombre) is not None

def limpiar_pct(valor):
    if pd.isna(valor): return None
    s = str(valor).strip()
    if s.startswith("#") or s in ("","-","N/A","NA"): return None
    try:
        n = float(s.replace("%","").strip())
        if "%" not in s and 0 <= n <= 1.5: n *= 100
        return round(min(n,119.0),1)
    except: return None

PAT_CAP = re.compile(r'capacitaci[oó]n(es)?(\s*(tomadas?|recibidas?|acreditadas?|formales?|cursadas?))?',re.IGNORECASE)
PALABRAS_NEG = {"ninguna","ninguno","-","n/a","na","observaciones","actividades","periodo",
    "evaluacion","rendimiento","promedio","total","semana","fecha","calificacion",
    "porcentaje","si","no","nombre","dependencia","area","firma",
    "total de actividades","#div/0!","#div/0","#ref!","#value!","#n/a","#null!","#num!","error","div/0"}

def _es_texto_valido_cap(txt):
    if not txt or len(txt)<5: return False
    if txt.upper().startswith("#"): return False
    if re.match(r'^[\d\.\%\,\-\#\s]+$',txt): return False
    tn = normalizar(txt)
    if tn in PALABRAS_NEG: return False
    for p in ["total de actividades","periodo de evaluacion","rendimiento","promedio general","calificacion"]:
        if p in tn: return False
    return True

def descargar_excel(file_id, reintentos=3, timeout=25):
    if not file_id or file_id.upper() in ("PENDIENTE",""): raise ValueError("ID pendiente")
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    ue = None
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r: return io.BytesIO(r.read())
        except Exception as e:
            ue = e
            if i < reintentos-1: time.sleep(1.5*(i+1))
    raise ue

@st.cache_data(ttl=3600, show_spinner=False)
def obtener_datos(alias, file_id, area):
    alias = alias.strip(); debug=[]
    try:
        raw = descargar_excel(file_id)
        excel_data = pd.read_excel(raw, sheet_name=None, header=None, engine="openpyxl")
    except Exception as e: return [],[],[],[f"Error: {e}"]
    resumenes,semanas,caps=[],[],[]
    for tab_name,df in excel_data.items():
        if not es_tab_mes(tab_name): continue
        mes = formatear_mes_anio(tab_name) or str(tab_name).upper()
        debug.append(f"'{tab_name}' → {mes}")
        nr,nc=df.shape; periodos,totales={},{}
        for i in range(nr):
            for j in range(nc):
                val=df.iat[i,j]
                if pd.isna(val): continue
                s=str(val).strip()
                if re.search(r'PERIODO\s*DE\s*EVALUACI',s,re.IGNORECASE):
                    for k in range(j+1,min(j+20,nc)):
                        v2=df.iat[i,k]
                        if pd.notna(v2) and str(v2).strip(): periodos[i]=str(v2).strip(); break
                if re.search(r'TOTAL\s*DE\s*ACTIVIDADES',s,re.IGNORECASE):
                    for k in range(nc-1,-1,-1):
                        p=limpiar_pct(df.iat[i,k])
                        if p is not None and p>0: totales[i]=p; break
                    if i not in totales:
                        nums=[]
                        for k in range(nc):
                            v=df.iat[i,k]
                            if pd.notna(v):
                                try:
                                    n=float(str(v).replace("%","").strip())
                                    if 1<=n<=500: nums.append(n)
                                except: pass
                        if len(nums)>=2:
                            proy,real=nums[-2],nums[-1]
                            if proy>0: totales[i]=round(min((real/proy)*100,119.0),1)
                if PAT_CAP.fullmatch(s.strip()):
                    for k in range(j+1,nc):
                        v=df.iat[i,k]
                        if pd.isna(v): continue
                        txt=str(v).strip()
                        if _es_texto_valido_cap(txt): caps.append({"Área":area,"Colaborador":alias,"Mes":mes,"Capacitación":txt})
                    for di in range(1,10):
                        ni=i+di
                        if ni>=nr: break
                        v=df.iat[ni,j]
                        if pd.isna(v) or not str(v).strip(): v=df.iat[ni,j+1] if j+1<nc else None
                        if v is None or pd.isna(v) or not str(v).strip(): break
                        txt=str(v).strip()
                        if PAT_CAP.fullmatch(txt) or re.match(r'^[\d\.\%\,\-\#]+$',txt) or normalizar(txt) in PALABRAS_NEG: break
                        if _es_texto_valido_cap(txt): caps.append({"Área":area,"Colaborador":alias,"Mes":mes,"Capacitación":txt})
        sem_tab,usados=[],set()
        for fp in sorted(periodos):
            for ft in sorted(totales):
                if ft>fp and ft not in usados:
                    p=periodos[fp]; mr=re.match(r'(\d+)',p)
                    sem_tab.append({"Área":area,"Colaborador":alias,"Mes":formatear_mes_anio(p) or mes,
                                    "Periodo":p,"Rendimiento":totales[ft],"_orden":int(mr.group(1)) if mr else 99})
                    usados.add(ft); break
        semanas.extend(sem_tab)
        if sem_tab:
            prom=sum(x["Rendimiento"] for x in sem_tab)/len(sem_tab)
            resumenes.append({"Área":area,"Colaborador":alias,"Mes":mes,"Promedio Mes":round(prom,1)})
    if not debug:
        tabs=", ".join(f"'{t}'" for t in excel_data.keys())
        debug=[f"Sin pestaña de mes. Pestañas: {tabs}"]
    return resumenes,semanas,caps,debug

# ─────────────────────────────────────────────────────────────────────────────
# ESTADO — página activa en menú
# ─────────────────────────────────────────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state.pagina = "equipo"
if "foto_colab" not in st.session_state:
    st.session_state.foto_colab = None

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Logo + menú + filtros
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Logo institucional ───────────────────────────────────────────────────
    try:
        st.image("Valle2027.png", use_container_width=True)
    except:
        st.markdown(f"""
        <div style='padding:20px 16px 16px;text-align:center;'>
          <div style='font-size:2rem;'>🏛️</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;padding:0 16px 18px;border-bottom:1px solid rgba(255,255,255,0.1);'>
      <div class='sidebar-org-name'>Valle de Santiago</div>
      <div class='sidebar-admin'>Administración 2024 – 2027</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Menú de navegación ───────────────────────────────────────────────────
    st.markdown("<div class='sidebar-section-label'>Menú principal</div>", unsafe_allow_html=True)

    MENU = [
        ("equipo",     "🏆", "Equipo de Alto Desempeño"),
        ("ranking",    "📊", "Ranking Trimestral"),
        ("resultados", "📋", "Resultados del Programa"),
    ]
    for key, icon, label in MENU:
        active = "active" if st.session_state.pagina == key else ""
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     help=label):
            st.session_state.pagina = key
            st.session_state.foto_colab = None
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Sincronizar ──────────────────────────────────────────────────────────
    st.markdown("<div class='sidebar-section-label'>Sistema</div>", unsafe_allow_html=True)
    if st.button("🔄  Sincronizar con Drive", key="sync", use_container_width=True):
        st.cache_data.clear()
        for k in ["global_df"]: st.session_state.pop(k, None)
        st.rerun()

    # ── Filtros ──────────────────────────────────────────────────────────────
    st.markdown("<div class='sidebar-section-label'>Filtros</div>", unsafe_allow_html=True)
    area_sel    = st.selectbox("Dependencia", list(AREAS.keys()))
    colabs_area = AREAS[area_sel]
    nombres_a   = [n.strip() for n in colabs_area]
    colab_sel   = st.multiselect("Personal", nombres_a, default=nombres_a)

    st.markdown(f"""
    <div class='sidebar-version'>v3.0 · Sistema de Evaluación de Desempeño</div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CARGA GLOBAL PARALELA
# ─────────────────────────────────────────────────────────────────────────────
if "global_df" not in st.session_state:
    tareas = [(n.strip(),fid,area)
              for area,cols in AREAS.items()
              for n,fid in cols.items()
              if fid.upper() not in ("PENDIENTE","")]
    ph = st.empty()
    with ph.container():
        prog = st.progress(0, text="Sincronizando evaluaciones…")
        all_res = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
            futuros = {ex.submit(obtener_datos,t[0],t[1],t[2]):t for t in tareas}
            for i,fut in enumerate(concurrent.futures.as_completed(futuros),1):
                try:
                    r,_,_,_ = fut.result(); all_res.extend(r)
                except: pass
                prog.progress(i/len(tareas), text=f"Cargando… {i}/{len(tareas)} servidores públicos")
    ph.empty()
    st.session_state["global_df"] = (
        pd.DataFrame(all_res, columns=["Área","Colaborador","Mes","Promedio Mes"])
        if all_res else pd.DataFrame(columns=["Área","Colaborador","Mes","Promedio Mes"])
    )

df_global = st.session_state["global_df"]
mejor_area_n, mejor_area_v = "N/A", 0.0
if not df_global.empty:
    rk = df_global.groupby("Área")["Promedio Mes"].mean().reset_index()
    f  = rk.loc[rk["Promedio Mes"].idxmax()]
    mejor_area_n, mejor_area_v = f["Área"], f["Promedio Mes"]

# ─────────────────────────────────────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

pagina = st.session_state.pagina

# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA: EQUIPO DE ALTO DESEMPEÑO
# ═══════════════════════════════════════════════════════════════════════════════
if pagina == "equipo":

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class='page-header'>
      <div class='page-header-icon'>🏆</div>
      <div>
        <div class='page-header-eyebrow'>Evaluación de Desempeño</div>
        <div class='page-header-title'>{area_sel}</div>
        <div class='page-header-sub'>H. Ayuntamiento de Valle de Santiago &nbsp;·&nbsp; Administración 2024–2027</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs globales rápidos
    k1, k2, k3 = st.columns(3)
    k1.metric("Área Líder Institucional", mejor_area_n)
    k2.metric("Eficiencia Área Líder",    f"{mejor_area_v:.1f}%")
    k3.metric("Dependencias Registradas", len(AREAS))
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Validar área con personal ────────────────────────────────────────────
    if not colabs_area:
        st.info(f"El área de **{area_sel}** aún no tiene personal asignado.")
        st.stop()

    # ── Carga de datos del área ──────────────────────────────────────────────
    colabs_validos = {n:fid for n,fid in colabs_area.items() if fid.upper() not in ("PENDIENTE","")}
    resumenes_a,semanas_a,caps_a,debug_info=[],[],[],{}
    if colabs_validos:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            futuros={ex.submit(obtener_datos,n.strip(),fid,area_sel):n.strip()
                     for n,fid in colabs_validos.items()}
            for fut in concurrent.futures.as_completed(futuros):
                nom=futuros[fut]
                try:
                    r,s,c,d=fut.result()
                    resumenes_a.extend(r); semanas_a.extend(s)
                    caps_a.extend(c);      debug_info[nom]=d
                except Exception as e: debug_info[nom]=[f"Error: {e}"]
    for n,fid in colabs_area.items():
        if fid.upper() in ("PENDIENTE",""): debug_info[n]=["⏳ Archivo pendiente"]

    C_RES=["Área","Colaborador","Mes","Promedio Mes"]
    C_SEM=["Área","Colaborador","Mes","Periodo","Rendimiento","_orden"]
    C_CAP=["Área","Colaborador","Mes","Capacitación"]
    df_res=(pd.DataFrame(resumenes_a,columns=C_RES).drop_duplicates(subset=["Colaborador","Mes"]))
    df_sem=(pd.DataFrame(semanas_a,columns=C_SEM).drop_duplicates(subset=["Colaborador","Periodo"]))
    df_cap=pd.DataFrame(caps_a,columns=C_CAP).drop_duplicates()

    _MES_HOY=f"{ORDEN_MESES_BASE[_dt.datetime.now().month-1]} {_dt.datetime.now().year}"
    _meses_ref=list(df_res["Mes"].unique()) if not df_res.empty else [_MES_HOY]
    _colabs_con_datos=set(df_res["Colaborador"].unique())
    _filas_cero=[]
    for _n in [n.strip() for n in colabs_area]:
        if _n not in _colabs_con_datos:
            for _m in _meses_ref:
                _filas_cero.append({"Área":area_sel,"Colaborador":_n,"Mes":_m,"Promedio Mes":0.0})
    if _filas_cero:
        df_res=pd.concat([df_res,pd.DataFrame(_filas_cero,columns=C_RES)],ignore_index=True)

    meses_d=[]
    if not df_res.empty:
        mp=list(df_res["Mes"].unique())
        meses_d=[m for m in ORDEN_MESES if m in mp]
        meses_d.extend([m for m in mp if m not in meses_d])

    with st.sidebar:
        st.markdown("<div class='sidebar-section-label'>Periodo</div>", unsafe_allow_html=True)
        mes_sel=st.selectbox("Mes", ["Todos"]+meses_d, label_visibility="collapsed")

    df_rf=df_res[df_res["Colaborador"].isin(colab_sel)].copy()
    df_sf=df_sem[df_sem["Colaborador"].isin(colab_sel)].copy()
    df_cf=df_cap[df_cap["Colaborador"].isin(colab_sel)].copy()
    if mes_sel!="Todos":
        df_rf=df_rf[df_rf["Mes"]==mes_sel]
        df_sf=df_sf[df_sf["Mes"]==mes_sel]
        df_cf=df_cf[df_cf["Mes"]==mes_sel]

    if not df_rf.empty:
        orden_final=[m for m in ORDEN_MESES if m in df_rf["Mes"].unique()]
        orden_final.extend([m for m in df_rf["Mes"].unique() if m not in orden_final])
        df_rf["Mes"]=pd.Categorical(df_rf["Mes"],categories=orden_final,ordered=True)
        colaboradores=df_rf["Colaborador"].unique()
        full_idx=pd.MultiIndex.from_product([colaboradores,orden_final],names=["Colaborador","Mes"])
        df_rf=(df_rf.set_index(["Colaborador","Mes"]).reindex(full_idx).reset_index())
        df_rf["Promedio Mes"]=df_rf["Promedio Mes"].fillna(0.0)
        df_rf["Área"]=df_rf["Área"].fillna(area_sel)
        df_rf["Mes"]=pd.Categorical(df_rf["Mes"],categories=orden_final,ordered=True)

        todos_colabs=sorted(df_rf["Colaborador"].unique())
        color_map={c:PALETA[i%len(PALETA)] for i,c in enumerate(todos_colabs)}
        prom_dep=df_rf["Promedio Mes"].mean()
        idx_max=df_rf["Promedio Mes"].idxmax()

        # ── KPIs del área ────────────────────────────────────────────────────
        a1,a2,a3=st.columns(3)
        a1.metric("Promedio General",       f"{prom_dep:.1f}%")
        a2.metric("Servidor Destacado",      df_rf.loc[idx_max,"Colaborador"],
                                             f"{df_rf.loc[idx_max,'Promedio Mes']}%")
        a3.metric("Evaluaciones Semanales", len(df_sf))
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Gráfica + botón PDF ──────────────────────────────────────────────
        fig=px.bar(df_rf.sort_values("Mes"),
                   x="Mes" if mes_sel=="Todos" else "Colaborador",
                   y="Promedio Mes", color="Colaborador",
                   barmode="group", text="Promedio Mes",
                   color_discrete_map=color_map)
        fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside",
                          cliponaxis=False, marker_line_width=1,
                          marker_line_color="rgba(0,0,0,0.08)")
        fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)", font_color=TEXTO,
                          font_family="Inter, Segoe UI, sans-serif",
                          legend=dict(orientation="h",yanchor="bottom",y=-0.28,
                                      xanchor="center",x=0.5,font_size=11),
                          margin=dict(t=20,b=10,l=10,r=10),
                          yaxis=dict(range=[0,115],gridcolor=GRIS_L,title=""),
                          xaxis=dict(title=""))

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'><span>📈</span> Rendimiento Mensual por Servidor Público</div>",
                    unsafe_allow_html=True)

        _, cbtn = st.columns([5,1])
        with cbtn:
            filas_html="".join(
                f"<tr><td>{r['Colaborador']}</td><td>{r['Mes']}</td>"
                f"<td style='font-weight:700;color:{GUINDA};'>{r['Promedio Mes']}%</td></tr>"
                for _,r in df_rf.iterrows())
            html_rep=f"""<html><head><meta charset='utf-8'>
            <style>body{{font-family:Arial;color:#212529;margin:30px;background:white}}
            .hdr{{text-align:center;border-bottom:3px solid {GUINDA};padding-bottom:15px;margin-bottom:20px}}
            .hdr h1{{color:{GUINDA};margin:0;font-size:24px}}.hdr p{{color:{DORADO};margin:5px 0 0;font-weight:bold;letter-spacing:2px;font-size:11px}}
            .mb{{background:#f8f9fa;padding:15px;border-left:5px solid {GUINDA};border-radius:4px;margin-bottom:20px}}
            table.dt{{width:100%;border-collapse:collapse;margin-top:15px}}
            table.dt th{{background:{GUINDA};color:white;padding:10px;text-align:left;font-size:13px}}
            table.dt td{{padding:9px;border-bottom:1px solid #e9ecef;font-size:12px}}
            table.dt tr:nth-child(even){{background:#f8f9fa}}
            @media print{{*{{-webkit-print-color-adjust:exact!important}}}}</style></head><body>
            <div class='hdr'><h1>VALLE DE SANTIAGO</h1>
            <p>PRESIDENCIA MUNICIPAL • ADMINISTRACIÓN 2024-2027</p></div>
            <h2>Reporte de Evaluación de Desempeño</h2>
            <div class='mb'><table>
            <tr><td width='35%'><b>Dependencia:</b></td><td>{area_sel}</td></tr>
            <tr><td><b>Periodo:</b></td><td>{mes_sel}</td></tr>
            <tr><td><b>Promedio General:</b></td><td style='color:{GUINDA};font-weight:bold;'>{prom_dep:.1f}%</td></tr>
            </table></div>
            <div>{fig.to_html(full_html=False,include_plotlyjs='cdn')}</div>
            <br><table class='dt'><thead><tr><th>Servidor Público</th><th>Mes</th><th>Rendimiento</th>
            </tr></thead><tbody>{filas_html}</tbody></table>
            <div style='margin-top:40px;text-align:center;font-size:11px;color:#6c757d;border-top:1px solid #e9ecef;padding-top:15px;'>
            H. Ayuntamiento de Valle de Santiago • Ctrl+P → Guardar como PDF</div>
            <script>window.onload=function(){{setTimeout(()=>window.print(),1000);}}</script>
            </body></html>"""
            st.download_button("📄 Exportar PDF", data=html_rep,
                               file_name=f"Reporte_{area_sel}.html",
                               mime="text/html", use_container_width=True)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Tabla + Semanales ────────────────────────────────────────────────
        tc1,tc2=st.columns([1,2])
        with tc1:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='section-title'><span>📅</span> Promedios por Mes</div>",unsafe_allow_html=True)
            st.dataframe(df_rf[["Colaborador","Mes","Promedio Mes"]], hide_index=True, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with tc2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='section-title'><span>📋</span> Evaluaciones Semanales</div>",unsafe_allow_html=True)
            if not df_sf.empty:
                st.dataframe(df_sf.sort_values(["Colaborador","_orden"])
                             [["Colaborador","Periodo","Rendimiento"]], hide_index=True, use_container_width=True)
            else:
                st.info("Sin evaluaciones semanales para este periodo.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── DIRECTORIO DEL EQUIPO ────────────────────────────────────────────
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'><span>👥</span> Directorio del Equipo — clic para ver perfil</div>",
                    unsafe_allow_html=True)

        grid_colabs=list(colabs_area.items())
        cols_per_row=3
        for row_s in range(0,len(grid_colabs),cols_per_row):
            gcols=st.columns(cols_per_row)
            for ci,(nombre,fid) in enumerate(grid_colabs[row_s:row_s+cols_per_row]):
                n_limpio=nombre.strip()
                tiene_dato=fid.upper() not in ("PENDIENTE","")
                ini=get_initials(n_limpio)
                with gcols[ci]:
                    st.markdown(f"""
                    <div class='dir-card'>
                      <div class='dir-avatar'>{ini}</div>
                      <div>
                        <div class='dir-name'>{n_limpio}</div>
                        <div class='dir-status'>{"✅ Con reporte" if tiene_dato else "⏳ Pendiente"}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                    if st.button("Ver perfil", key=f"prf_{n_limpio}", use_container_width=True):
                        st.session_state.foto_colab = n_limpio
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Modal de perfil ──────────────────────────────────────────────────
        if st.session_state.foto_colab:
            nom_m=st.session_state.foto_colab
            ini_m=get_initials(nom_m)
            p_col,_=st.columns([1,2])
            with p_col:
                st.markdown(f"""
                <div class='profile-card'>
                  <div class='profile-avatar-lg'>{ini_m}</div>
                  <div class='profile-name'>{nom_m}</div>
                  <div class='profile-dept'>{area_sel}</div>
                  <div class='profile-no-photo'>📷 Sin fotografía registrada</div>
                </div>""", unsafe_allow_html=True)
                if st.button("✕  Cerrar perfil", key="cerrar_perf"):
                    st.session_state.foto_colab = None
                    st.rerun()

        # ── CAPACITACIONES ───────────────────────────────────────────────────
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'><span>🎓</span> Capacitaciones y Desarrollo Profesional</div>",
                    unsafe_allow_html=True)
        if not df_cf.empty:
            cm1,cm2,cm3=st.columns(3)
            cm1.metric("Total de Capacitaciones",    df_cf.shape[0])
            cm2.metric("Servidores capacitados",     df_cf["Colaborador"].nunique())
            cm3.metric("Meses con registro",         df_cf["Mes"].nunique())
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            df_cnt=(df_cf.groupby("Colaborador").size().reset_index(name="Total")
                    .sort_values("Total",ascending=False))
            fig_c=px.bar(df_cnt,x="Colaborador",y="Total",text_auto=True,
                         color="Colaborador",
                         color_discrete_map=get_color_map(df_cnt["Colaborador"].unique()),
                         title="Cursos por Servidor Público")
            fig_c.update_layout(template="plotly_white",plot_bgcolor="rgba(0,0,0,0)",
                                 paper_bgcolor="rgba(0,0,0,0)",font_color=TEXTO,
                                 title_font_color=GUINDA,showlegend=False,
                                 xaxis_title="",yaxis_title="N° cursos",
                                 margin=dict(t=40,b=10),font_family="Inter,sans-serif")
            st.plotly_chart(fig_c, use_container_width=True)
            df_grp=(df_cf.groupby("Colaborador")
                    .agg(Total=("Capacitación","count"),Lista=("Capacitación",list))
                    .reset_index().sort_values("Total",ascending=False))
            cap_cols=st.columns(2)
            for idx,row in df_grp.iterrows():
                cursos_items="".join(f"<div class='cap-item'>{c}</div>" for c in row["Lista"])
                with cap_cols[idx%2]:
                    st.markdown(f"""
                    <div class='cap-card'>
                      <div class='cap-name'>{row['Colaborador']}
                        <span class='cap-badge'>{row['Total']} curso(s)</span>
                      </div>
                      {cursos_items}
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Sin capacitaciones registradas para el periodo seleccionado.")
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 Diagnóstico de hojas detectadas"):
            for colab,pests in debug_info.items():
                st.markdown(f"**{colab}**")
                for p in pests: st.markdown(f"&nbsp;&nbsp;&nbsp;{p}")
    else:
        st.info("No hay datos numéricos para mostrar con los filtros actuales.")

# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA: RANKING TRIMESTRAL
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "ranking":
    st.markdown(f"""
    <div class='page-header'>
      <div class='page-header-icon'>📊</div>
      <div>
        <div class='page-header-eyebrow'>Análisis de Rendimiento</div>
        <div class='page-header-title'>Ranking Trimestral</div>
        <div class='page-header-sub'>Comparativo de desempeño por periodo entre dependencias</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='coming-soon-card'>
      <div class='coming-soon-icon'>📊</div>
      <div class='coming-soon-title'>Ranking Trimestral en Construcción</div>
      <div class='coming-soon-desc'>
        Esta sección mostrará el comparativo de desempeño por trimestre entre todas
        las dependencias del H. Ayuntamiento. Próximamente disponible.
      </div>
      <div class='coming-badge'>🔒 &nbsp; Módulo en desarrollo</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA: RESULTADOS DEL PROGRAMA
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "resultados":
    st.markdown(f"""
    <div class='page-header'>
      <div class='page-header-icon'>📋</div>
      <div>
        <div class='page-header-eyebrow'>Evaluación Institucional</div>
        <div class='page-header-title'>Resultados del Programa de Evaluación</div>
        <div class='page-header-sub'>Desempeño general · {area_sel} · Administración 2024–2027</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    df_area_global=df_global[df_global["Área"]==area_sel] if not df_global.empty else pd.DataFrame()

    if not df_area_global.empty:
        prom_area=df_area_global["Promedio Mes"].mean()
        n_colabs =df_area_global["Colaborador"].nunique()
        n_meses  =df_area_global["Mes"].nunique()
        ranking=(df_global.groupby("Área")["Promedio Mes"].mean()
                 .sort_values(ascending=False).reset_index())
        ranking["Posición"]=range(1,len(ranking)+1)
        pos_area=ranking[ranking["Área"]==area_sel]["Posición"].values

        r1,r2,r3,r4=st.columns(4)
        r1.metric("Eficiencia del Área",    f"{prom_area:.1f}%")
        r2.metric("Servidores Evaluados",   n_colabs)
        r3.metric("Meses con Evaluación",   n_meses)
        r4.metric("Posición Global",
                  f"#{pos_area[0]} de {len(ranking)}" if len(pos_area) else "N/A")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Tendencia mensual
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'><span>📈</span> Tendencia de Desempeño — {area_sel}</div>",
                    unsafe_allow_html=True)
        df_tend=(df_area_global.groupby("Mes")["Promedio Mes"].mean().reset_index())
        df_tend["Mes_cat"]=pd.Categorical(
            df_tend["Mes"],
            categories=[m for m in ORDEN_MESES if m in df_tend["Mes"].values],ordered=True)
        df_tend=df_tend.sort_values("Mes_cat")
        if len(df_tend)>1:
            fig_t=px.line(df_tend,x="Mes",y="Promedio Mes",markers=True,
                          color_discrete_sequence=[GUINDA])
            fig_t.add_hline(y=df_global["Promedio Mes"].mean(),line_dash="dot",
                            line_color=VERDE,
                            annotation_text="Promedio institucional",
                            annotation_position="bottom right")
            fig_t.update_traces(line_width=3,marker_size=9,
                                marker_color=GUINDA,marker_line_color=DORADO,
                                marker_line_width=2)
            fig_t.update_layout(template="plotly_white",plot_bgcolor="rgba(0,0,0,0)",
                                 paper_bgcolor="rgba(0,0,0,0)",font_color=TEXTO,
                                 font_family="Inter,sans-serif",
                                 xaxis_title="",yaxis_title="% Promedio",
                                 yaxis=dict(range=[0,110],gridcolor=GRIS_L),
                                 margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_t, use_container_width=True)
        else:
            st.info("Se necesitan al menos 2 meses de datos para graficar la tendencia.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Comparativo institucional
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'><span>🏛️</span> Comparativo por Dependencia</div>",
                    unsafe_allow_html=True)
        df_comp=(df_global.groupby("Área")["Promedio Mes"].mean()
                 .sort_values(ascending=False).reset_index())
        df_comp["Color"]=df_comp["Área"].apply(lambda a: GUINDA if a==area_sel else "#d1d5db")
        fig_cmp=px.bar(df_comp,x="Área",y="Promedio Mes",text="Promedio Mes",
                       color="Área",
                       color_discrete_map={row["Área"]:row["Color"] for _,row in df_comp.iterrows()})
        fig_cmp.update_traces(texttemplate="%{text:.0f}%",textposition="outside",
                               cliponaxis=False,marker_line_width=0)
        fig_cmp.update_layout(template="plotly_white",plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",font_color=TEXTO,
                               font_family="Inter,sans-serif",showlegend=False,
                               xaxis_title="",yaxis_title="% Promedio",
                               xaxis=dict(tickangle=-35),
                               yaxis=dict(range=[0,115],gridcolor=GRIS_L),
                               margin=dict(t=20,b=80,l=10,r=10))
        st.plotly_chart(fig_cmp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Ver tabla de ranking completo"):
            df_rk2=df_comp.copy()
            df_rk2.insert(0,"Posición",range(1,len(df_rk2)+1))
            df_rk2["Promedio Mes"]=df_rk2["Promedio Mes"].map(lambda x:f"{x:.1f}%")
            st.dataframe(df_rk2[["Posición","Área","Promedio Mes"]], hide_index=True, use_container_width=True)
    else:
        st.markdown(f"""
        <div class='coming-soon-card'>
          <div class='coming-soon-icon'>📋</div>
          <div class='coming-soon-title'>Sin datos disponibles</div>
          <div class='coming-soon-desc'>
            Aún no hay datos para <strong>{area_sel}</strong>.
            Usa el botón <em>Sincronizar con Drive</em> o espera a que se carguen los reportes.
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
