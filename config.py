# ==============================================================================
# CONFIGURACIÓN DEL SISTEMA Y METADATOS
# ==============================================================================
import os
import streamlit as st

DB_PATH = 'operacion_dragon.db'
CACHE_TRM = 'trm_cache.json'
ADMIN_USERS = ['1152437543', 'admin']
CARPETA_MATRICES = 'matrices'
CARPETA_RECLAMOS = 'reclamaciones_archivos'
CLAVE_SECRETA_HMAC = b"DRAGON_MASTER_CRYPTOGRAPHIC_KEY_2026_COLOMBIA"
HONEYTOKENS = ['0000000000', '9999999999', '1234567890']

def obtener_config(clave, valor_defecto):
    val = os.environ.get(clave)
    if val: return val
    try:
        if clave in st.secrets: return st.secrets[clave]
    except Exception: pass
    return valor_defecto

REMITENTE_EMAIL = obtener_config("SMTP_USER", "personaldramirez@gmail.com")
REMITENTE_PASSWORD = obtener_config("SMTP_PASS", "qism kdgy mbnv eyfh")

TEMA_COLOR = {
    'cyber_dragon': {
        'accent': '#ea580c', 'accent_glow': '#f97316', 'sub_accent': '#00d2ff',
        'bg': '#090b0e', 'card': 'rgba(18, 21, 27, 0.85)', 'border': '#272c35'
    },
    'imperial_gold': {
        'accent': '#eab308', 'accent_glow': '#facc15', 'sub_accent': '#38bdf8',
        'bg': '#0b0c10', 'card': 'rgba(23, 20, 15, 0.88)', 'border': '#3d3423'
    }
}
