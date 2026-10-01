# ==============================================================================
# BASE DE DATOS SQLITE WAL CON AUTO-MIGRACIÓN RESILIENTE
# ==============================================================================
import sqlite3
import pandas as pd
import os
from datetime import datetime
from config import DB_PATH, CARPETA_MATRICES, CARPETA_RECLAMOS

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=25, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA busy_timeout=5000;')
    return conn

def init_db():
    if not os.path.exists(CARPETA_MATRICES):
        os.makedirs(CARPETA_MATRICES, exist_ok=True)
    if not os.path.exists(CARPETA_RECLAMOS):
        os.makedirs(CARPETA_RECLAMOS, exist_ok=True)
    with get_db_connection() as conn:
        # 1. Tabla Usuarios
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            dni TEXT PRIMARY KEY,
            hash TEXT NOT NULL,
            correo TEXT,
            fecha_registro TEXT,
            totp_secret TEXT
        )''')
        
        # MIGRACIÓN AUTOMÁTICA EN CALIENTE: Garantizar que columnas existan siempre
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(usuarios)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        if 'totp_secret' not in columnas_existentes:
            try: conn.execute("ALTER TABLE usuarios ADD COLUMN totp_secret TEXT")
            except Exception: pass
        if 'fecha_registro' not in columnas_existentes:
            try: conn.execute("ALTER TABLE usuarios ADD COLUMN fecha_registro TEXT")
            except Exception: pass
            
        # 2. Bitácora forense de auditoría
        conn.execute('''CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            dni TEXT,
            accion TEXT,
            detalle TEXT
        )''')
        # Migración: asegurar columna 'detalle' en auditoria
        cursor.execute("PRAGMA table_info(auditoria)")
        cols_auditoria = [col[1] for col in cursor.fetchall()]
        if 'detalle' not in cols_auditoria:
            try: conn.execute("ALTER TABLE auditoria ADD COLUMN detalle TEXT")
            except Exception: pass
            
        # Migración: asegurar columna 'es_admin' en usuarios
        cursor.execute("PRAGMA table_info(usuarios)")
        cols_us = [col[1] for col in cursor.fetchall()]
        if 'es_admin' not in cols_us:
            try: conn.execute("ALTER TABLE usuarios ADD COLUMN es_admin INTEGER DEFAULT 0")
            except Exception: pass
        # 3. Catálogo de activos dinámico
        conn.execute('''CREATE TABLE IF NOT EXISTS catalogo_activos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio_usd REAL NOT NULL,
            icono TEXT,
            activo INTEGER DEFAULT 1
        )''')
        # 4. Preferencias del usuario (Fiducia vs Nube)
        conn.execute('''CREATE TABLE IF NOT EXISTS preferencias_usuarios (
            dni TEXT PRIMARY KEY,
            pct_fiducia REAL DEFAULT 100.0,
            pct_nube REAL DEFAULT 0.0,
            fecha_modificacion TEXT
        )''')
        # 5. Modificaciones manuales del Admin por cédula
        conn.execute('''CREATE TABLE IF NOT EXISTS modificaciones_manuales (
            dni TEXT PRIMARY KEY,
            formula_modificada TEXT,
            nombre_modificado TEXT,
            fecha_modificacion TEXT
        )''')
        # 6. Parámetros globales editables
        conn.execute('''CREATE TABLE IF NOT EXISTS parametros_globales (
            clave TEXT PRIMARY KEY,
            valor REAL NOT NULL
        )''')
        # 7. Rate limiting y bloqueos anti-fuerza bruta
        conn.execute('''CREATE TABLE IF NOT EXISTS bloqueos_seguridad (
            dni TEXT PRIMARY KEY,
            intentos_fallidos INTEGER DEFAULT 0,
            bloqueado_hasta TEXT
        )''')
        # 8. Reclamaciones de Usuarios (Buzón)
        conn.execute('''CREATE TABLE IF NOT EXISTS reclamaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cedula TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            archivo_path TEXT,
            estado TEXT DEFAULT 'PENDIENTE'
        )''')
        # Migración automática en caliente para reclamaciones
        cursor.execute("PRAGMA table_info(reclamaciones)")
        cols_rec = [col[1] for col in cursor.fetchall()]
        if 'cedula' not in cols_rec:
            if 'dni' in cols_rec:
                try: conn.execute("ALTER TABLE reclamaciones RENAME COLUMN dni TO cedula")
                except Exception:
                    try: conn.execute("ALTER TABLE reclamaciones ADD COLUMN cedula TEXT")
                    except Exception: pass
            else:
                try: conn.execute("ALTER TABLE reclamaciones ADD COLUMN cedula TEXT")
                except Exception: pass
        if 'archivo_path' not in cols_rec:
            if 'ruta_archivo' in cols_rec:
                try: conn.execute("ALTER TABLE reclamaciones RENAME COLUMN ruta_archivo TO archivo_path")
                except Exception:
                    try: conn.execute("ALTER TABLE reclamaciones ADD COLUMN archivo_path TEXT")
                    except Exception: pass
            else:
                try: conn.execute("ALTER TABLE reclamaciones ADD COLUMN archivo_path TEXT")
                except Exception: pass
        if 'estado' not in cols_rec:
            try: conn.execute("ALTER TABLE reclamaciones ADD COLUMN estado TEXT DEFAULT 'PENDIENTE'")
            except Exception: pass

        # Insertar activos iniciales por defecto si no existen
        activos_default = [
            ('Q', 'QUINTILLION', 5000000, '💴', 1),
            ('N', 'NONGENTILLION', 10000000, '💵', 1),
            ('V', 'VIGINTILLION', 7500000, '💶', 1),
            ('ZIM', 'MONEDA DE ZIM', 500000, '🪙', 1),
            ('BZ', 'BILLETE ZIMBABWE', 12500000, '🧾', 1),
            ('AZ', 'AGROCHEQUE ZIM', 500000, '📜', 1),
            ('MHK', 'MHK', 15000000, '🎫', 1),
            ('G', 'GOOGOPLEX', 500000000, '🐲', 1),
        ]
        for cod, nom, pre, ico, act in activos_default:
            conn.execute('INSERT OR IGNORE INTO catalogo_activos (codigo, nombre, precio_usd, icono, activo) VALUES (?, ?, ?, ?, ?)', (cod, nom, pre, ico, act))

        # 9. Configuraciones del Sistema (Correos, Notificaciones, etc.)
        conn.execute('''CREATE TABLE IF NOT EXISTS configuraciones_sistema (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        )''')
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('correo_remitente_otp', 'personaldramirez@gmail.com'))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('password_remitente_otp', 'qism kdgy mbnv eyfh'))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('servidor_smtp', 'smtp.gmail.com'))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('puerto_smtp', '587'))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('correo_destino_reclamos', 'personaldramirez@gmail.com'))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('otros_correos_reclamos', ''))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('otros_correos_otp_copia', ''))
        conn.execute('INSERT OR IGNORE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)', ('notificar_por_correo', '1'))

        # Insertar parámetros iniciales por defecto
        conn.execute('INSERT OR IGNORE INTO parametros_globales (clave, valor) VALUES (?, ?)', ('descuento_general', 10.0))
        conn.execute('INSERT OR IGNORE INTO parametros_globales (clave, valor) VALUES (?, ?)', ('comision_banco', 1.0))

init_db()

# --- Funciones de Configuración del Sistema (Correos, Canales, etc.) ---
def obtener_config_sistema(clave, default=""):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT valor FROM configuraciones_sistema WHERE clave=?", (clave,))
        row = c.fetchone()
        return row[0] if row else default

def guardar_config_sistema(clave, valor):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO configuraciones_sistema (clave, valor) VALUES (?, ?)",
            (clave, str(valor).strip())
        )

# --- Funciones de Catálogo Dinámico ---
def obtener_catalogo_activos():
    with get_db_connection() as conn:
        df = pd.read_sql_query("SELECT codigo, nombre, precio_usd, icono, activo FROM catalogo_activos WHERE activo=1", conn)
        cat = {}
        for _, r in df.iterrows():
            cat[r['codigo']] = {
                'nombre': r['nombre'],
                'precio': float(r['precio_usd']),
                'icono': r['icono']
            }
        return cat

def guardar_activo(codigo, nombre, precio, icono):
    with get_db_connection() as conn:
        conn.execute(
            'INSERT OR REPLACE INTO catalogo_activos (codigo, nombre, precio_usd, icono, activo) VALUES (?, ?, ?, ?, 1)',
            (codigo.strip().upper(), nombre.strip().upper(), float(precio), icono.strip())
        )

# --- Funciones de Parámetros Globales ---
def obtener_parametros_globales():
    with get_db_connection() as conn:
        df = pd.read_sql_query("SELECT clave, valor FROM parametros_globales", conn)
        params = {'descuento_general': 10.0, 'comision_banco': 1.0}
        for _, r in df.iterrows():
            params[r['clave']] = float(r['valor'])
        return params

def guardar_parametro_global(clave, valor):
    with get_db_connection() as conn:
        conn.execute('INSERT OR REPLACE INTO parametros_globales (clave, valor) VALUES (?, ?)', (clave, float(valor)))

# --- Funciones de Preferencias de Usuario (Fiducia vs Nube) ---
def obtener_preferencia_usuario(dni):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT pct_fiducia, pct_nube FROM preferencias_usuarios WHERE dni=?', (str(dni),))
        row = c.fetchone()
        if row: return float(row[0]), float(row[1])
        return 100.0, 0.0

def guardar_preferencia_usuario(dni, pct_fiducia, pct_nube):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        conn.execute(
            'INSERT OR REPLACE INTO preferencias_usuarios (dni, pct_fiducia, pct_nube, fecha_modificacion) VALUES (?, ?, ?, ?)',
            (str(dni), float(pct_fiducia), float(pct_nube), fecha)
        )

# --- Modificaciones Manuales por Cédula (Override) ---
def obtener_modificacion_manual(dni):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT formula_modificada, nombre_modificado FROM modificaciones_manuales WHERE dni=?', (str(dni),))
        row = c.fetchone()
        if row: return {'formula': row[0], 'nombre': row[1]}
        return None

def guardar_modificacion_manual(dni, formula, nombre=""):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        conn.execute(
            'INSERT OR REPLACE INTO modificaciones_manuales (dni, formula_modificada, nombre_modificado, fecha_modificacion) VALUES (?, ?, ?, ?)',
            (str(dni), formula.strip(), nombre.strip(), fecha)
        )

# --- Verificación de Usuario Anti-Fallo de Esquema ---
def verificar_usuario(dni):
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute('SELECT hash, correo, totp_secret, es_admin FROM usuarios WHERE dni=?', (str(dni),))
            res = c.fetchone()
            return {"hash": res[0], "correo": res[1], "totp_secret": res[2] if len(res)>2 else None, "es_admin": bool(res[3])} if res else None
        except sqlite3.OperationalError:
            try:
                c.execute('SELECT hash, correo, totp_secret FROM usuarios WHERE dni=?', (str(dni),))
                res = c.fetchone()
                return {"hash": res[0], "correo": res[1], "totp_secret": res[2] if len(res)>2 else None, "es_admin": False} if res else None
            except sqlite3.OperationalError:
                c.execute('SELECT hash, correo FROM usuarios WHERE dni=?', (str(dni),))
                res = c.fetchone()
                return {"hash": res[0], "correo": res[1], "totp_secret": None, "es_admin": False} if res else None

def promover_admin(cedula):
    with get_db_connection() as conn:
        conn.execute('UPDATE usuarios SET es_admin = 1 WHERE dni=?', (str(cedula),))

def guardar_usuario(cedula, password_hash, correo="", totp_secret=""):
    fecha_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        conn.execute(
            'INSERT OR REPLACE INTO usuarios (dni, hash, correo, fecha_registro, totp_secret) VALUES (?, ?, ?, ?, ?)',
            (str(cedula), password_hash, correo, fecha_reg, totp_secret)
        )

def registrar_auditoria(dni, accion, detalle=""):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_db_connection() as conn:
            conn.execute('INSERT INTO auditoria (fecha, dni, accion, detalle) VALUES (?, ?, ?, ?)', (fecha_actual, str(dni), accion, detalle))
    except Exception: pass

def obtener_logs():
    with get_db_connection() as conn:
        return pd.read_sql_query('SELECT fecha, dni, accion, detalle FROM auditoria ORDER BY id DESC LIMIT 200', conn)

