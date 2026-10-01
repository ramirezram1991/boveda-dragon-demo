# ==============================================================================
# SEGURIDAD FORENSE (ANTI-FUERZA BRUTA, HMAC, HONEYTOKENS)
# ==============================================================================
import re
import hmac
import hashlib
from datetime import datetime, timedelta
from database import get_db_connection, registrar_auditoria
from config import CLAVE_SECRETA_HMAC, HONEYTOKENS

def sanitizar_texto(texto: str) -> str:
    if not isinstance(texto, str): return ""
    return re.sub(r'[<>{}\";]', '', texto).strip()

def verificar_bloqueo_seguridad(dni: str):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT intentos_fallidos, bloqueado_hasta FROM bloqueos_seguridad WHERE dni=?', (str(dni),))
        row = c.fetchone()
        if row and row[1]:
            try:
                bloqueado_hasta = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                if datetime.now() < bloqueado_hasta:
                    minutos_restantes = int((bloqueado_hasta - datetime.now()).total_seconds() // 60) + 1
                    return True, f"⛔ Bóveda bloqueada por {minutos_restantes} min debido a reiterados fallos de seguridad."
            except Exception: pass
        return False, ""

def registrar_intento_fallido(dni: str):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT intentos_fallidos FROM bloqueos_seguridad WHERE dni=?', (str(dni),))
        row = c.fetchone()
        intentos = (row[0] + 1) if row else 1
        bloqueado_hasta = None
        if intentos >= 5:
            bloqueado_hasta = (datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
            registrar_auditoria(dni, "BLOQUEO_SEGURIDAD_FUERZA_BRUTA", f"5 intentos fallidos acumulados")
        conn.execute('INSERT OR REPLACE INTO bloqueos_seguridad (dni, intentos_fallidos, bloqueado_hasta) VALUES (?, ?, ?)', (str(dni), intentos, bloqueado_hasta))
        return intentos

def limpiar_intentos_fallidos(dni: str):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM bloqueos_seguridad WHERE dni=?', (str(dni),))

def generar_firma_hmac(datos_clave: str) -> str:
    return hmac.new(CLAVE_SECRETA_HMAC, datos_clave.encode('utf-8'), hashlib.sha256).hexdigest()

