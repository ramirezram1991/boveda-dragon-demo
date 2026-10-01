# ==============================================================================
# COMPONENTES VISUALES, EMBLEMAS Y DASHBOARD INTERACTIVO
# ==============================================================================
import os
import base64
import html
import json
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from config import TEMA_COLOR, CARPETA_RECLAMOS
from database import (
    get_db_connection,
    obtener_parametros_globales,
    obtener_preferencia_usuario,
    guardar_preferencia_usuario,
    obtener_catalogo_activos,
    registrar_auditoria
)
from services import (
    buscar_logo,
    calcular_materiales,
    formato_pesos,
    formato_trm
)
from security import sanitizar_texto, generar_firma_hmac
from pdf_generator import generar_recibo_pdf

LOGO_B64 = ""
LOGO_PATH = buscar_logo()
if LOGO_PATH:
    with open(LOGO_PATH, "rb") as img_file: LOGO_B64 = base64.b64encode(img_file.read()).decode()

def render_logo_animado():
    img_tag = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:90px; filter:drop-shadow(0 0 20px rgba(234,88,12,0.6)); border-radius:50%; z-index:10; position:relative;">' if LOGO_B64 else '<div style="font-size:70px; z-index:10; position:relative;">🐉</div>'
    st.markdown(f'<div class="anillo" style="margin-bottom:1.5rem;">{img_tag}</div>', unsafe_allow_html=True)

def render_logo_pequeno():
    img_tag = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:48px; filter:drop-shadow(0 0 10px rgba(234,88,12,0.6)); border-radius:50%; z-index:10; position:relative;">' if LOGO_B64 else '<div style="font-size:38px; z-index:10; position:relative;">🐉</div>'
    return f'<div class="anillo" style="width:68px; height:68px; margin:0; flex-shrink:0;">{img_tag}</div>'

# ==============================================================================
# 6. EMBLEMA TECNOLÓGICO FUTURISTA (CYBER PLACA DORADA)
# ==============================================================================
def render_emblema_tecnologico():
    """Renderiza el recuadro holográfico con letras doradas cambiantes y silueta láser."""
    st.markdown("""
    <div class="emblema-cyber-container">
        <div class="emblema-cyber">
            <div class="scan-laser"></div>
            <div class="emblema-bracket top-left"></div>
            <div class="emblema-bracket top-right"></div>
            <div class="emblema-bracket btm-left"></div>
            <div class="emblema-bracket btm-right"></div>
            <h1 class="emblema-texto">MATRIZ OPERACIÓN DRAGÓN</h1>
            <div class="emblema-sub">✦ BÓVEDA FINANCIERA CLASIFICADA ✦</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_advertencia_forense():
    """Renderiza el recuadro pericial de advertencia legal y protocolo de seguridad (Opción 3)."""
    st.markdown("""
    <div class="panel-advertencia-forense">
        <div class="advertencia-header">
            <div class="advertencia-tag-box">
                <span class="live-dot"></span>
                <span class="advertencia-tag">SISTEMA BLINDADO // LEY 1581 DE 2012</span>
            </div>
            <span class="advertencia-status">● VIGILANCIA ACTIVA</span>
        </div>
        <div class="advertencia-titulo">
            🛡️ PROTOCOLO DE SEGURIDAD & HABEAS DATA INSTITUCIONAL
        </div>
        <div class="advertencia-cuerpo">
            Acceso estrictamente reservado a <strong>titulares verificados de la Matriz Operación Dragón</strong>.
            Toda interacción, dirección IP de origen, huella pericial y marca temporal son registradas en el libro
            mayor criptográfico inmutable. La intrusión o intento no autorizado constituye delito penal e informático
            según la Ley 1273 de 2009 y Ley 1581 de Protección de Datos Personales.
        </div>
        <div class="advertencia-footer">
            <span>✦ RESTRICCIÓN DE SEGURIDAD NIVEL IV ✦</span>
            <span>AUDITORÍA FORENSE PERICIAL EN TIEMPO REAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# CIRCUITO NEURAL CIBERNÉTICO ESTILO JARVIS (CANVAS FORENSE DE ALTA TECNOLOGÍA)
# ==============================================================================
def render_circuito_neural_jarvis():
    components.html('''
    <script>
    let oldLanding = window.parent.document.getElementById('dragon-canvas');
    if (oldLanding) { oldLanding.remove(); }

    let oldJarvis = window.parent.document.getElementById('jarvis-neural-canvas');
    if (oldJarvis) { oldJarvis.remove(); }

    const canvas = window.parent.document.createElement('canvas');
    canvas.id = 'jarvis-neural-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '0';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.72';
    window.parent.document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.parent.innerWidth;
        canvas.height = window.parent.innerHeight;
    }
    resize();
    window.parent.addEventListener('resize', resize);

    let mouse = { x: null, y: null, maxDist: 150 };
    window.parent.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    window.parent.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });

    const NODE_COUNT = Math.min(80, Math.floor((canvas.width * canvas.height) / 14000));
    const nodes = [];
    for (let i = 0; i < NODE_COUNT; i++) {
        nodes.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.85,
            vy: (Math.random() - 0.5) * 0.85,
            radius: Math.random() * 2.2 + 1.2,
            pulseSpeed: Math.random() * 0.04 + 0.02,
            pulseOffset: Math.random() * Math.PI * 2,
            colorType: Math.random() > 0.35 ? 'gold' : 'cyan'
        });
    }

    const packets = [];
    for (let i = 0; i < 18; i++) {
        packets.push({
            from: Math.floor(Math.random() * NODE_COUNT),
            to: Math.floor(Math.random() * NODE_COUNT),
            progress: Math.random(),
            speed: Math.random() * 0.015 + 0.008
        });
    }

    let tick = 0;
    function animate() {
        if (!window.parent.document.getElementById('jarvis-neural-canvas')) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        tick += 0.012;
        
        nodes.forEach((n) => {
            n.x += n.vx;
            n.y += n.vy;
            
            if (n.x < 0 || n.x > canvas.width) n.vx *= -1;
            if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
            
            if (mouse.x !== null) {
                let dx = mouse.x - n.x;
                let dy = mouse.y - n.y;
                let d = Math.sqrt(dx * dx + dy * dy);
                if (d < mouse.maxDist) {
                    let force = (mouse.maxDist - d) / mouse.maxDist;
                    n.x -= (dx / d) * force * 1.5;
                    n.y -= (dy / d) * force * 1.5;
                }
            }
            
            let pulse = Math.sin(tick * 3 + n.pulseOffset) * 0.5 + 0.5;
            let r = n.radius + pulse * 1.3;
            let isGold = n.colorType === 'gold';
            let mainColor = isGold ? `rgba(234, 179, 8, ${0.55 + pulse * 0.4})` : `rgba(0, 210, 255, ${0.55 + pulse * 0.4})`;
            let glowColor = isGold ? `rgba(234, 88, 12, ${0.28 + pulse * 0.3})` : `rgba(56, 189, 248, ${0.28 + pulse * 0.3})`;
            
            ctx.beginPath();
            ctx.arc(n.x, n.y, r * 2.8, 0, Math.PI * 2);
            ctx.fillStyle = glowColor;
            ctx.fill();
            
            ctx.beginPath();
            ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
            ctx.fillStyle = mainColor;
            ctx.fill();
        });
        
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                let dx = nodes[i].x - nodes[j].x;
                let dy = nodes[i].y - nodes[j].y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < 115) {
                    let alpha = (1 - dist / 115) * 0.28;
                    let stroke = (nodes[i].colorType === 'gold' && nodes[j].colorType === 'gold')
                        ? `rgba(234, 179, 8, ${alpha})`
                        : `rgba(0, 210, 255, ${alpha * 0.9})`;
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.strokeStyle = stroke;
                    ctx.lineWidth = 0.9;
                    ctx.stroke();
                }
            }
        }
        
        packets.forEach(p => {
            let n1 = nodes[p.from];
            let n2 = nodes[p.to];
            if (n1 && n2) {
                let dx = n2.x - n1.x;
                let dy = n2.y - n1.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 140) {
                    p.progress += p.speed;
                    if (p.progress > 1) {
                        p.progress = 0;
                        p.from = Math.floor(Math.random() * nodes.length);
                        p.to = Math.floor(Math.random() * nodes.length);
                    }
                    let px = n1.x + dx * p.progress;
                    let py = n1.y + dy * p.progress;
                    
                    ctx.beginPath();
                    ctx.arc(px, py, 2.2, 0, Math.PI * 2);
                    ctx.fillStyle = '#ffffff';
                    ctx.shadowColor = '#00d2ff';
                    ctx.shadowBlur = 8;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                } else {
                    p.from = Math.floor(Math.random() * nodes.length);
                    p.to = Math.floor(Math.random() * nodes.length);
                    p.progress = 0;
                }
            }
        });
        
        window.parent.requestAnimationFrame(animate);
    }
    animate();
    </script>
    ''', height=0)


def renderizar_dashboard_interactivo(cedula, df_bd, trm_actual):
    render_circuito_neural_jarvis()
    tema_actual = st.session_state.get('tema_actual', 'cyber_dragon')
    T_ACT = TEMA_COLOR.get(tema_actual, TEMA_COLOR['cyber_dragon'])
    u_data = df_bd[df_bd['ID/CC/DNI'] == str(cedula)]
    if u_data.empty:
        st.error("❌ Cédula no localizada en las matrices consolidadas.")
        return
        
    val_nombre = u_data['NOMBRE COMPLETO'].values[0] if 'NOMBRE COMPLETO' in u_data.columns else "NO REGISTRA"
    nombre = str(val_nombre).strip() if pd.notna(val_nombre) else "NO REGISTRA"
    
    val_lider = u_data['LIDER'].values[0] if 'LIDER' in u_data.columns else "NO ASIGNADO"
    lider = str(val_lider).strip() if pd.notna(val_lider) else "NO ASIGNADO"
    
    # Saludo formal dinámico según la hora del día (Buenos días, Buenas tardes, Buenas noches)
    hora_actual = datetime.now().hour
    if 5 <= hora_actual < 12:
        saludo_horario = "BUENOS DÍAS"
    elif 12 <= hora_actual < 19:
        saludo_horario = "BUENAS TARDES"
    else:
        saludo_horario = "BUENAS NOCHES"

    # Formateo de nombre completo formal (primer nombre y primer apellido garantizados)
    palabras_nombre = [p for p in nombre.split() if p.strip()]
    if len(palabras_nombre) >= 2:
        nombre_formal = " ".join(palabras_nombre).upper()
    elif len(palabras_nombre) == 1:
        nombre_formal = palabras_nombre[0].upper()
    else:
        nombre_formal = "TITULAR VERIFICADO"
    
    prod = u_data['PRODUCTO / MATERIAL'].values[0] if 'PRODUCTO / MATERIAL' in u_data.columns else ""
    
    catalogo = obtener_catalogo_activos()
    calc = calcular_materiales(prod, catalogo)
    params = obtener_parametros_globales()

    pct_fid, pct_nube = obtener_preferencia_usuario(cedula)
    
    t_usd = calc['TOTAL_PAGO']
    pct_desc = params.get('descuento_general', 10.0) / 100.0
    pct_banco = params.get('comision_banco', 1.0) / 100.0

    t_neto = t_usd * (1.0 - pct_desc)
    b_usd = t_neto * pct_banco
    remanente_usd = t_neto * (1.0 - pct_banco)

    f_usd_fid = remanente_usd * (pct_fid / 100.0)
    f_usd_nube = remanente_usd * (pct_nube / 100.0)
    t_cop = t_neto * trm_actual

    # Generar Firma HMAC Criptográfica
    cadena_pericial = f"{cedula}|{t_usd:.2f}|{t_neto:.2f}|{pct_fid:.1f}|{pct_nube:.1f}|{trm_actual:.2f}"
    firma_hmac = generar_firma_hmac(cadena_pericial)

    # Tarjetas de materiales
    filas_html = ""
    tiene_materiales = False
    cant_items = 0
    for k, v in catalogo.items():
        if calc.get(k, 0) > 0:
            tiene_materiales = True
            cant_items += 1
            monto_item = calc[k] * v['precio']
            filas_html += f"""
            <div class="tilt-card" style="display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:rgba(12,15,20,0.85); border:1px solid rgba(255,255,255,0.06); border-radius:10px; margin-bottom:10px; transition:transform 0.15s ease-out, box-shadow 0.15s ease-out;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.8rem;">{v['icono']}</span>
                    <div>
                        <div style="font-weight:700; font-size:1rem; color:#f8fafc;">{v['nombre']}</div>
                        <div style="color:#94a3b8; font-size:11px;">Precio unitario: {formato_pesos(v['precio'])} USD</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="color:{T_ACT['accent']}; font-weight:800; font-family:'Space Grotesk', sans-serif; font-size:1.15rem;">x{calc[k]}</div>
                    <div class="num-anim secure-blur" data-val="{monto_item}" title="Desencriptar" style="color:#10b981; font-weight:800; font-family:'Space Grotesk', sans-serif; font-size:1rem;">$ 0 USD</div>
                </div>
            </div>
            """
    if not tiene_materiales:
        filas_html = "<div style='color:#94a3b8; font-size:0.95rem; padding:16px; background:rgba(12,15,20,0.6); border-radius:8px;'>Sin activos catalogados para esta cuenta en la matriz.</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Teko:wght@500;700&family=Inter:wght@400;600;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; font-family: 'Inter', sans-serif; background: transparent; color: #f8fafc; overflow-x: hidden; }}
        .header-box {{ display: flex; align-items: center; justify-content: space-between; gap: 20px; background: {T_ACT['card']}; border: 1px solid {T_ACT['border']}; border-radius: 14px; padding: 20px 24px; margin-bottom: 2rem; box-shadow: 0 16px 40px rgba(0,0,0,0.5); }}
        .greeting {{ font-family: 'Teko', sans-serif; font-size: clamp(2.5rem, 5vw, 3.8rem); margin: 0; line-height: 1; text-transform: uppercase; color: #f8fafc; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .kpi-card {{ background: {T_ACT['card']}; border: 1px solid {T_ACT['border']}; border-radius: 12px; padding: 1.2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .kpi-label {{ font-size: 0.72rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }}
        .kpi-value {{ font-family: 'Space Grotesk', sans-serif; font-size: clamp(1.2rem, 2.4vw, 1.6rem); font-weight: 800; }}
        .main-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.8rem; }}
        .panel {{ background: {T_ACT['card']}; border: 1px solid {T_ACT['border']}; border-radius: 14px; padding: 1.8rem; box-shadow: 0 12px 36px rgba(0,0,0,0.4); }}
        .panel-title {{ font-family: 'Teko', sans-serif; font-size: 2rem; margin: 0 0 1.2rem 0; text-transform: uppercase; color: #f8fafc; }}
        .summary-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
        .anillo {{ width: 68px; height: 68px; margin: 0; border-radius: 50%; position: relative; display: grid; place-items: center; flex-shrink: 0; }}
        .anillo::before {{ content: ""; position: absolute; inset: 0; border-radius: 50%; padding: 3px; background: conic-gradient(from 0deg, transparent, {T_ACT['accent']}, {T_ACT['sub_accent']}, transparent 60%, {T_ACT['accent']}); -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; animation: gira 4s linear infinite; }}
        @keyframes gira {{ to {{ transform: rotate(360deg); }} }}

        /* OPTIMIZACIÓN RESPONSIVA MÓVIL */
        @media (max-width: 768px) {{
            body {{ padding: 2px; }}
            .header-box {{ flex-direction: column; align-items: flex-start; padding: 14px 16px; gap: 10px; margin-bottom: 1.2rem; }}
            .greeting {{ font-size: 2.2rem; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr) !important; gap: 0.6rem !important; margin-bottom: 1.2rem !important; }}
            .kpi-card {{ padding: 0.9rem 0.5rem !important; }}
            .kpi-label {{ font-size: 0.65rem !important; }}
            .kpi-value {{ font-size: 1.15rem !important; }}
            .main-grid {{ grid-template-columns: 1fr !important; gap: 1.2rem !important; }}
            .panel {{ padding: 1.1rem !important; border-radius: 12px !important; }}
            .panel-title {{ font-size: 1.6rem !important; margin-bottom: 0.8rem !important; }}
            .tilt-card {{ padding: 9px 12px !important; margin-bottom: 8px !important; }}
            .summary-row {{ padding-bottom: 6px !important; margin-bottom: 8px !important; font-size: 0.88rem !important; }}
        }}
    </style>
    </head>
    <body>
        <div class="header-box">
            <div style="display:flex; align-items:center; gap:18px;">
                {render_logo_pequeno()}
                <div>
                    <h2 class="greeting">{saludo_horario}, {nombre_formal}</h2>
                    <div style="color:#94a3b8; font-size:0.95rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;">
                        LÍDER ASIGNADO: <strong style="color:{T_ACT['accent']};">{lider.upper()}</strong> &nbsp;|&nbsp; CÉDULA/ID: <strong style="color:white;">{cedula}</strong>
                    </div>
                </div>
            </div>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">PAGO BRUTO (USD)</div>
                <div id="kpi1" class="kpi-value num-anim secure-blur" title="Pase el cursor para desencriptar" data-val="{t_usd}" style="color: #f8fafc;">$ 0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">TOTAL NETO (-{pct_desc*100:.0f}%)</div>
                <div id="kpi2" class="kpi-value num-anim secure-blur" title="Pase el cursor para desencriptar" data-val="{t_neto}" style="color: {T_ACT['accent']};">$ 0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">COMISIÓN BANCO ({pct_banco*100:.0f}%)</div>
                <div id="kpi3" class="kpi-value num-anim secure-blur" title="Pase el cursor para desencriptar" data-val="{b_usd}" style="color: #ef4444;">$ 0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">TOTAL FINAL (COP)</div>
                <div id="kpi4" class="kpi-value num-anim secure-blur" title="Pase el cursor para desencriptar" data-val="{t_cop}" style="color: #10b981;">$ 0</div>
            </div>
        </div>

        <div class="main-grid">
            <div class="panel">
                <h4 class="panel-title">TUS ACTIVOS ASIGNADOS</h4>
                {filas_html}
            </div>

            <div class="panel">
                <h4 class="panel-title">ESTRUCTURA DE DESEMBOLSO</h4>
                <div class="summary-row">
                    <span style="color:#94a3b8; font-weight:600;">TRM APLICADA EN VIVO</span>
                    <span style="font-family:'Space Grotesk'; font-weight:700;">{formato_trm(trm_actual)}</span>
                </div>
                <div class="summary-row">
                    <span style="color:#ef4444; font-weight:600;">BANCO INICIAL (1%)</span>
                    <span class="num-anim" data-val="{b_usd * trm_actual}" style="font-family:'Space Grotesk'; font-weight:700; color:#ef4444;">$ 0</span>
                </div>
                <div class="summary-row">
                    <span style="color:#38bdf8; font-weight:600;">🏛️ FIDUCIA ASIGNADA ({pct_fid:.0f}%)</span>
                    <span class="num-anim" data-val="{f_usd_fid * trm_actual}" style="font-family:'Space Grotesk'; font-weight:700; color:#38bdf8;">$ 0</span>
                </div>
                <div class="summary-row">
                    <span style="color:#a855f7; font-weight:600;">☁️ NUBE ASIGNADA ({pct_nube:.0f}%)</span>
                    <span class="num-anim" data-val="{f_usd_nube * trm_actual}" style="font-family:'Space Grotesk'; font-weight:700; color:#a855f7;">$ 0</span>
                </div>
                <div class="summary-row" style="border:none; margin-top:1.5rem;">
                    <span style="font-weight:800; font-size:1.1rem; color:white;">VALOR A DESEMBOLSAR</span>
                    <span class="num-anim" data-val="{t_cop}" style="font-family:'Space Grotesk'; font-weight:800; font-size:1.8rem; color:#10b981;">$ 0</span>
                </div>
            </div>
        </div>

        <script>
        function animarOdometer(el, endVal, prefix, suffix="") {{
            const dur = 1500;
            let start = null;
            const step = (t) => {{
                if (!start) start = t;
                const p = Math.min((t - start) / dur, 1);
                const ease = 1 - Math.pow(1 - p, 4);
                el.textContent = prefix + Math.floor(ease * endVal).toLocaleString('es-CO') + suffix;
                if (p < 1) window.requestAnimationFrame(step);
            }};
            window.requestAnimationFrame(step);
        }}

        document.querySelectorAll('.tilt-card').forEach(card => {{
            card.addEventListener('mousemove', e => {{
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                card.style.transform = `perspective(600px) rotateX(${{-y / 15}}deg) rotateY(${{x / 20}}deg) translateY(-2px)`;
                card.style.boxShadow = `0 12px 28px rgba(0,0,0,0.6), 0 0 15px rgba(234, 88, 12, 0.25)`;
            }});
            card.addEventListener('mouseleave', () => {{
                card.style.transform = 'perspective(600px) rotateX(0deg) rotateY(0deg) translateY(0)';
                card.style.boxShadow = 'none';
            }});
        }});

        let tiempoInactivo = 0;
        const resetTimer = () => tiempoInactivo = 0;
        window.addEventListener('mousemove', resetTimer);
        window.addEventListener('keydown', resetTimer);
        setInterval(() => {{
            tiempoInactivo++;
            if (tiempoInactivo >= 300) {{
                alert("⚠️ Sesión cerrada por inactividad prolongada (Protección de Bóveda).");
                window.parent.location.reload();
            }}
        }}, 1000);

        document.addEventListener("DOMContentLoaded", () => {{
            document.querySelectorAll('.num-anim').forEach(el => {{
                const val = parseFloat(el.getAttribute('data-val'));
                const isUSD = el.textContent.includes('USD');
                animarOdometer(el, val, '$ ', isUSD ? ' USD' : '');
            }});
        }});
        </script>
        
        <div style="text-align:center; font-family:'Space Grotesk', monospace; font-size:10px; color:#64748b; margin-top:25px; border-top:1px dashed {T_ACT['border']}; padding-top:10px;">
            SELLO DE SEGURIDAD HMAC-SHA256 (INMUTABLE):<br/>{firma_hmac}
        </div>
    </body>
    </html>
    """
    altura_dinamica = max(1120, 680 + (cant_items * 65))
    components.html(html_content, height=altura_dinamica, scrolling=False)

    # --- CONTROL DE FIDUCIA VS NUBE PARA EL CLIENTE (SELECTOR TÁCTICO OPCIÓN 1) ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card-custom'>", unsafe_allow_html=True)
        st.markdown("<h4 class='font-teko' style='font-size:1.8rem; margin-top:0; color:white;'>⚙️ TU PREFERENCIA DE DESEMBOLSO (REMANENTE 99%)</h4>", unsafe_allow_html=True)
        st.caption("Elige libremente qué porcentaje deseas recibir a través de Fiducia Bancaria y cuánto a través de la Nube.")
        
        key_fid_state = f"pct_fid_{cedula}"
        if key_fid_state not in st.session_state:
            st.session_state[key_fid_state] = int(pct_fid)

        st.markdown("<p style='color:#94a3b8; font-size:0.88rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;'>Selección rápida de 1 clic:</p>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            if st.button("🏛️ 100% Fiducia", use_container_width=True, key=f"btn_100_{cedula}"):
                st.session_state[key_fid_state] = 100
                st.rerun()
        with b_col2:
            if st.button("🏛️ 80% / ☁️ 20%", use_container_width=True, key=f"btn_80_{cedula}"):
                st.session_state[key_fid_state] = 80
                st.rerun()
        with b_col3:
            if st.button("⚖️ 50% / ☁️ 50%", use_container_width=True, key=f"btn_50_{cedula}"):
                st.session_state[key_fid_state] = 50
                st.rerun()
        with b_col4:
            if st.button("☁️ 100% Nube", use_container_width=True, key=f"btn_0_{cedula}"):
                st.session_state[key_fid_state] = 0
                st.rerun()

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        c_num1, c_num2 = st.columns([2.5, 1.2])
        with c_num1:
            val_actual = int(st.session_state[key_fid_state])
            nuevo_pct_fid = st.number_input(
                "O ajusta el % exacto para Fiducia Bancaria:",
                min_value=0, max_value=100, value=val_actual, step=5,
                key=f"num_input_{cedula}"
            )
            st.session_state[key_fid_state] = nuevo_pct_fid
            nuevo_pct_nube = 100 - nuevo_pct_fid
            
            f_usd_fid_dyn = remanente_usd * (nuevo_pct_fid / 100.0)
            f_usd_nube_dyn = remanente_usd * (nuevo_pct_nube / 100.0)
            
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(15,23,42,0.75); padding:10px 16px; border-radius:10px; border:1px solid rgba(255,255,255,0.08); margin-top:8px; font-family:'Space Grotesk', sans-serif; font-size:0.92rem;">
                <div>🏛️ <strong style="color:#f8fafc;">Fiducia: {nuevo_pct_fid}%</strong> <span style="color:#10b981; font-weight:700;">({formato_pesos(f_usd_fid_dyn * trm_actual)} COP)</span></div>
                <div style="color:#64748b;">•</div>
                <div>☁️ <strong style="color:#f8fafc;">Nube: {nuevo_pct_nube}%</strong> <span style="color:#38bdf8; font-weight:700;">({formato_pesos(f_usd_nube_dyn * trm_actual)} COP)</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with c_num2:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("💾 Guardar Mi Preferencia", type="primary", use_container_width=True, key=f"btn_save_{cedula}"):
                guardar_preferencia_usuario(cedula, nuevo_pct_fid, nuevo_pct_nube)
                registrar_auditoria(cedula, "CAMBIO_DISTRIBUCION_FIDUCIA_NUBE", f"Fiducia:{nuevo_pct_fid}% Nube:{nuevo_pct_nube}%")
                st.success("✅ Tu distribución ha sido guardada y tu recibo actualizado.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- MÓDULO DE DISCREPANCIAS Y RECLAMACIONES CON EVIDENCIA ---
    with st.expander("📬 ¿Tu valor es diferente o te hace falta una nota/voucher? Reportar aquí", expanded=False):
        st.markdown("""
        <div style='background:rgba(234, 88, 12, 0.08); border-left:4px solid var(--accent); padding:14px 18px; border-radius:8px; margin-bottom:15px;'>
            <strong style='color:#f8fafc; font-size:1.05rem;'>¿El valor es diferente al que tenías pensado o te falta registrar algún activo o nota?</strong><br/>
            <span style='color:#cbd5e1; font-size:0.9rem;'>
                Adjunta aquí tu comprobante (voucher, foto, imagen o documento PDF) y explícanos qué tienes o qué consideras que te hace falta.
                Tu solicitud y las imágenes serán enviadas de inmediato al equipo administrativo para su auditoría y ajuste en caliente.
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"form_reclamo_{cedula}"):
            c_f1, c_f2 = st.columns([1.6, 1])
            with c_f1:
                msj_reclamo = st.text_area(
                    "Explícanos tu situación (¿Qué tienes o qué crees que hace falta?):",
                    placeholder="Ejemplo: 'Tengo este voucher por 1 Quintillion adicional que no veo reflejado en mi balance...', o 'Creo que me queda haciendo falta registrar una nota de compra...'",
                    height=130
                )
            with c_f2:
                evidencia = st.file_uploader(
                    "Sube tu comprobante, voucher o foto:",
                    type=["pdf", "jpg", "jpeg", "png", "webp"],
                    help="Formatos aceptados: Imágenes (JPG, PNG, WEBP) o documento PDF."
                )
            
            btn_reclamo = st.form_submit_button("📤 Enviar Solicitud y Adjuntar Evidencia", type="primary", use_container_width=True)
            if btn_reclamo:
                if not msj_reclamo.strip() and not evidencia:
                    st.error("⚠️ Por favor ingresa una breve descripción o adjunta un archivo/foto.")
                else:
                    path_evidencia = ""
                    if evidencia is not None:
                        import uuid
                        nombre_limpio = os.path.basename(evidencia.name)
                        ext = str(nombre_limpio).split('.')[-1].lower() if '.' in nombre_limpio else ""
                        if ext not in ['pdf', 'jpg', 'jpeg', 'png', 'webp']:
                            st.error("❌ Formato de archivo no válido. Solo se admiten JPG, PNG, WEBP o PDF.")
                            st.stop()
                        nombre_archivo = f"{cedula}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.{ext}"
                        path_evidencia = os.path.join(CARPETA_RECLAMOS, nombre_archivo)
                        with open(path_evidencia, "wb") as f:
                            f.write(evidencia.getbuffer())
                    
                    with get_db_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO reclamaciones (fecha, cedula, mensaje, archivo_path, estado) VALUES (datetime('now', 'localtime'), ?, ?, ?, 'PENDIENTE')",
                            (cedula, msj_reclamo.strip(), path_evidencia)
                        )
                        nuevo_id = cur.lastrowid
                    registrar_auditoria(cedula, "RECLAMACION_ENVIADA", f"Radicado #{nuevo_id} - Evidencia: {bool(evidencia)}")
                    st.success(f"✅ ¡Solicitud radicada con éxito bajo el Radicado #{nuevo_id}! El equipo administrativo ya tiene acceso inmediato a tu soporte y a tu mensaje.")
                    st.rerun()

        # Historial de solicitudes radicadas por este usuario
        with get_db_connection() as conn:
            mis_reclamos = pd.read_sql_query("SELECT id, fecha, mensaje, archivo_path, estado FROM reclamaciones WHERE cedula=? ORDER BY id DESC", conn, params=(str(cedula),))
        if not mis_reclamos.empty:
            st.markdown("<h5 class='font-teko' style='font-size:1.4rem; color:#f8fafc; margin-top:1.2rem; margin-bottom:0.5rem;'>HISTORIAL DE TUS SOLICITUDES ENVIADAS</h5>", unsafe_allow_html=True)
            for _, r in mis_reclamos.iterrows():
                badge_bg = "rgba(234, 179, 8, 0.15)" if r['estado'] == 'PENDIENTE' else ("rgba(56, 189, 248, 0.15)" if r['estado'] == 'EN REVISIÓN' else "rgba(16, 185, 129, 0.15)")
                badge_color = "#facc15" if r['estado'] == 'PENDIENTE' else ("#38bdf8" if r['estado'] == 'EN REVISIÓN' else "#10b981")
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <strong style='color:white;'>Radicado #{r['id']}</strong> &nbsp;|&nbsp; <span style='color:#94a3b8; font-size:0.85rem;'>{r['fecha']}</span>
                        <div style='color:#cbd5e1; font-size:0.9rem; margin-top:4px;'>{html.escape(str(r['mensaje']))}</div>
                    </div>
                    <span style='background:{badge_bg}; color:{badge_color}; border:1px solid {badge_color}55; padding:4px 10px; border-radius:6px; font-weight:700; font-size:0.8rem;'>{r['estado']}</span>
                </div>
                """, unsafe_allow_html=True)

    # --- DESCARGA DE RECIBO OFICIAL EN PDF ---
    col_pdf1, col_pdf2 = st.columns([2.5, 1.5])
    with col_pdf2:
        try:
            pdf_bytes = generar_recibo_pdf(
                cedula, nombre, lider, prod, calc, catalogo,
                t_usd, t_neto, b_usd, f_usd_fid, f_usd_nube,
                pct_fid, pct_nube, t_cop, trm_actual, firma_hmac
            )
            st.download_button(
                label="📄 Descargar Recibo Oficial (PDF)",
                data=pdf_bytes,
                file_name=f"Liquidacion_Dragon_{cedula}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

# ==============================================================================
