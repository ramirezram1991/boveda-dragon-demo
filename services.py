# ==============================================================================
# SERVICIOS DE MATRICES, CÁLCULOS FINANCIEROS Y TRM
# ==============================================================================
import os
import glob
import re
import json
import requests
import pandas as pd
import streamlit as st
from database import get_db_connection
from config import CACHE_TRM, CARPETA_MATRICES

def cargar_super_matriz():
    if os.path.exists('super_matriz_cache.pkl'):
        try:
            df_cached = pd.read_pickle('super_matriz_cache.pkl')
            with get_db_connection() as conn:
                mods = pd.read_sql_query("SELECT dni, formula_modificada, nombre_modificado FROM modificaciones_manuales", conn)
                if not mods.empty:
                    for _, m in mods.iterrows():
                        mask = df_cached['ID/CC/DNI'] == str(m['dni'])
                        if mask.any():
                            if m['formula_modificada']: df_cached.loc[mask, 'PRODUCTO / MATERIAL'] = m['formula_modificada']
                            if m['nombre_modificado']: df_cached.loc[mask, 'NOMBRE COMPLETO'] = m['nombre_modificado']
            return df_cached
        except Exception:
            pass
    rutas = glob.glob("*.xls*") + glob.glob(f"{CARPETA_MATRICES}/*.xls*")
    archivos_excel = [f for f in set(rutas) if not os.path.basename(f).startswith("~$")]
    lista_dfs = []
    
    for archivo in archivos_excel:
        try:
            m_lider = re.search(r'LIDER\s+([^.]+)', os.path.basename(archivo), re.IGNORECASE)
            lider_archivo = m_lider.group(1).strip() if m_lider else "LÍDER GENERAL"

            excel_obj = pd.ExcelFile(archivo)
            hoja_objetivo = next((h for h in ['DATOS GENERALES', 'DATA COMPRAS', 'DATA GENERAL', 'MATRIZ LISTADO'] if h in excel_obj.sheet_names), excel_obj.sheet_names[0])
            df_raw = pd.read_excel(archivo, sheet_name=hoja_objetivo, header=None)
            
            header_idx = 0
            for i in range(min(15, len(df_raw))):
                fila_str = " ".join([str(x).upper() for x in df_raw.iloc[i].values if pd.notna(x)])
                if any(k in fila_str for k in ["CC", "DNI", "CEDULA", "NOMBRE"]):
                    header_idx = i; break
            
            df = pd.read_excel(archivo, sheet_name=hoja_objetivo, header=header_idx)
            df.columns = df.columns.astype(str).str.strip().str.upper().str.replace('É', 'E').str.replace('Ó', 'O')
            df = df.loc[:, ~df.columns.duplicated()]
            
            cc_col = next((c for c in df.columns if any(x in c for x in ['CC', 'DNI', 'ID', 'CEDULA', 'DOCUMENTO']) and 'PASAPORTE' not in c), None)
            nom_col = next((c for c in df.columns if 'NOMBRE' in c), None)
            lid_col = next((c for c in df.columns if 'LIDER' in c), None)
            prod_col = next((c for c in df.columns if any(x in c for x in ['PRODUCTO', 'MATERIAL', 'FORMULA'])), None)
            email_col = next((c for c in df.columns if any(x in c for x in ['CORREO', 'EMAIL'])), None)
            tel_col = next((c for c in df.columns if any(x in c for x in ['TEL', 'CEL', 'MOVIL'])), None)
            
            if cc_col:
                df['ID_CLEAN'] = df[cc_col].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.lstrip('0')
                df = df[~df['ID_CLEAN'].isin(['NAN', 'nan', '', 'NONE', 'NULL', 'None'])]
                df['ID/CC/DNI'] = df['ID_CLEAN']
                df['NOMBRE COMPLETO'] = df[nom_col].fillna('NO REGISTRA').astype(str).str.strip() if nom_col else 'NO REGISTRA'
                df['LIDER'] = df[lid_col].fillna(lider_archivo).astype(str).str.strip() if lid_col else lider_archivo
                df['PRODUCTO / MATERIAL'] = df[prod_col].fillna('').astype(str).str.strip() if prod_col else ''
                df['CORREO_EXCEL'] = df[email_col].astype(str).str.strip().str.lower().replace(['nan', 'none', 'null', '<na>'], '') if email_col else ''
                df['TELEFONO'] = df[tel_col].fillna('').astype(str).str.strip() if tel_col else ''
                df['ARCHIVO_ORIGEN'] = os.path.basename(archivo)
                lista_dfs.append(df[['ID/CC/DNI', 'NOMBRE COMPLETO', 'LIDER', 'PRODUCTO / MATERIAL', 'CORREO_EXCEL', 'TELEFONO', 'ARCHIVO_ORIGEN']])
        except Exception: continue
            
    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        dict_ag = {
            'NOMBRE COMPLETO': 'first', 'LIDER': 'first',
            'CORREO_EXCEL': lambda x: next((e for e in x if isinstance(e, str) and '@' in e), ''),
            'TELEFONO': 'first',
            'PRODUCTO / MATERIAL': lambda x: '+'.join([str(i) for i in x if str(i).strip() not in ['', 'nan', 'None']]),
            'ARCHIVO_ORIGEN': 'first'
        }
        df_agrupado = df_final.groupby('ID/CC/DNI', as_index=False).agg(dict_ag)
        
        # Inyectar modificaciones manuales registradas en SQLite
        with get_db_connection() as conn:
            mods = pd.read_sql_query("SELECT dni, formula_modificada, nombre_modificado FROM modificaciones_manuales", conn)
            if not mods.empty:
                for _, m in mods.iterrows():
                    mask = df_agrupado['ID/CC/DNI'] == str(m['dni'])
                    if mask.any():
                        if m['formula_modificada']: df_agrupado.loc[mask, 'PRODUCTO / MATERIAL'] = m['formula_modificada']
                        if m['nombre_modificado']: df_agrupado.loc[mask, 'NOMBRE COMPLETO'] = m['nombre_modificado']
                    else:
                        nuevo = pd.DataFrame([{
                            'ID/CC/DNI': str(m['dni']),
                            'NOMBRE COMPLETO': m['nombre_modificado'] or 'REGISTRO DIRECTO',
                            'LIDER': 'ADMINISTRACIÓN DIRECTA',
                            'PRODUCTO / MATERIAL': m['formula_modificada'] or '',
                            'CORREO_EXCEL': '', 'TELEFONO': '', 'ARCHIVO_ORIGEN': 'CONSOLA_ADMIN'
                        }])
                        df_agrupado = pd.concat([df_agrupado, nuevo], ignore_index=True)
        try:
            df_agrupado.to_pickle('super_matriz_cache.pkl')
        except Exception: pass
        return df_agrupado
    return pd.DataFrame(columns=['ID/CC/DNI', 'NOMBRE COMPLETO', 'LIDER', 'PRODUCTO / MATERIAL', 'CORREO_EXCEL', 'TELEFONO', 'ARCHIVO_ORIGEN'])

df_usuarios = cargar_super_matriz()

def calcular_materiales(formula, catalogo):
    res = {k: 0 for k in catalogo}
    res['TOTAL_PAGO'] = 0
    if pd.isna(formula) or not isinstance(formula, str) or not formula.strip(): return res
    
    matches = re.findall(r'(\d+)\s*([A-Za-z]+)', formula.upper().replace(' ', ''))
    for cant_str, mat in matches:
        try: cant = int(cant_str)
        except ValueError: continue
        if cant <= 0: continue
        
        clave_hallada = None
        if mat in catalogo:
            clave_hallada = mat
        else:
            for k, info in sorted(catalogo.items(), key=lambda x: len(x[0]), reverse=True):
                if mat.startswith(k) or info['nombre'].upper().startswith(mat):
                    clave_hallada = k; break
        if clave_hallada:
            res[clave_hallada] += cant
            res['TOTAL_PAGO'] += (cant * catalogo[clave_hallada]['precio'])
    return res

def formato_pesos(valor): return f"$ {valor:,.0f}".replace(",", ".") if valor != 0 else "$ 0"
def formato_trm(valor): return f"$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

@st.cache_data(ttl=3600)
def obtener_trm():
    try: 
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=3).json()
        trm = float(resp['rates']['COP'])
        with open(CACHE_TRM, 'w', encoding='utf-8') as f: json.dump({'trm': trm}, f)
        return trm
    except Exception: 
        if os.path.exists(CACHE_TRM):
            try:
                with open(CACHE_TRM, 'r', encoding='utf-8') as f: return float(json.load(f)['trm'])
            except Exception: pass
        return 4180.0

def buscar_logo():
    for op in ['logo.png', 'logo.jpg', 'image_a251de.png']:
        if os.path.exists(op): return op
    return ""

