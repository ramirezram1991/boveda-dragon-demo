# ==============================================================================
# OPERACIÃƒâ€œN DRAGÃƒâ€œN Ã¢â‚¬â€ PORTAL FINANCIERO Y BÃƒâ€œVEDA INSTITUCIONAL
# ARQUITECTURA MODULARIZADA (VANGUARD RESILIENCE ENGINE)
# ==============================================================================
import os
import random
import smtplib
import html
import hashlib
import bcrypt
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import streamlit.components.v1 as components

# MÃƒÂ³dulos del Sistema
from config import (
    ADMIN_USERS,
    HONEYTOKENS,
    REMITENTE_EMAIL,
    REMITENTE_PASSWORD,
    TEMA_COLOR,
    CARPETA_MATRICES
)
from database import (
    get_db_connection,
    init_db,
    verificar_usuario,
    guardar_usuario,
    promover_admin,
    registrar_auditoria,
    obtener_logs,
    obtener_catalogo_activos,
    guardar_activo,
    obtener_parametros_globales,
    guardar_parametro_global,
    guardar_modificacion_manual
)
from security import (
    sanitizar_texto,
    verificar_bloqueo_seguridad,
    registrar_intento_fallido,
    limpiar_intentos_fallidos
)
from services import (
    cargar_super_matriz,
    obtener_trm,
    calcular_materiales,
    formato_pesos,
    formato_trm
)
from pdf_generator import generar_recibo_pdf
from styles import obtener_css_maestro
from components import (
    render_logo_animado,
    render_logo_pequeno,
    render_emblema_tecnologico,
    render_advertencia_forense,
    renderizar_dashboard_interactivo
)

# 1. ConfiguraciÃƒÂ³n de PÃƒÂ¡gina
st.set_page_config(
    page_title="OperaciÃƒÂ³n DragÃƒÂ³n Ã¢â‚¬â€ BÃƒÂ³veda Clasificada",
    page_icon="Ã°Å¸Ââ€°",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. InicializaciÃƒÂ³n de Base de Datos y CachÃƒÂ©
init_db()

# 3. Control de Estado Global
if 'vista_actual' not in st.session_state: st.session_state['vista_actual'] = 'landing'
if 'cedula_usuario' not in st.session_state: st.session_state['cedula_usuario'] = None
if 'registro_paso' not in st.session_state: st.session_state['registro_paso'] = 1
if 'temp_data' not in st.session_state: st.session_state['temp_data'] = {}
if 'intentos_otp' not in st.session_state: st.session_state['intentos_otp'] = 0
if 'codigo_otp_debug' not in st.session_state: st.session_state['codigo_otp_debug'] = None
if 'tema_actual' not in st.session_state: st.session_state['tema_actual'] = 'cyber_dragon'
if 'cliente_auditado' not in st.session_state: st.session_state['cliente_auditado'] = None

def cambiar_vista(nueva_vista):
    st.session_state['vista_actual'] = nueva_vista
    st.session_state['registro_paso'] = 1
    st.session_state['intentos_otp'] = 0

# 4. InyecciÃƒÂ³n de Estilos Maestros DinÃƒÂ¡micos
css_maestro = obtener_css_maestro(st.session_state['tema_actual'])
st.markdown(css_maestro, unsafe_allow_html=True)

# 5. Carga de Datos Principales
df_usuarios = cargar_super_matriz()
trm = obtener_trm()

# ==============================================================================
# 10. VISTAS PRINCIPALES DEL SISTEMA
# ==============================================================================

# --- BARRA SUPERIOR CON SELECTOR DE TEMA DUAL ---
col_head1, col_head2 = st.columns([8, 2.5])
with col_head1:
    st.markdown("<div class='text-orange font-teko' style='font-size:26px; letter-spacing:2px; padding-top:4px;'>OPERACIÃƒâ€œN DRAGÃƒâ€œN // CLÃƒÅ¡STER FINANCIERO</div>", unsafe_allow_html=True)
with col_head2:
    tema_sel = st.selectbox(
        "Estilo de BÃƒÂ³veda:",
        ["Ã°Å¸Ââ€° Cyber DragÃƒÂ³n", "Ã°Å¸â€˜â€˜ BÃƒÂ³veda Imperial Oro"],
        index=0 if st.session_state['tema_actual'] == 'cyber_dragon' else 1,
        label_visibility="collapsed"
    )
    nuevo_tema = 'cyber_dragon' if "Cyber" in tema_sel else 'imperial_gold'
    if nuevo_tema != st.session_state['tema_actual']:
        st.session_state['tema_actual'] = nuevo_tema
        st.rerun()

st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)


# --- VISTA 1: LANDING PAGE CON CANVAS DE PARTÃƒÂCULAS ---
if st.session_state['vista_actual'] == 'landing':
    components.html('''
    <script>
    // Remover canvas anterior si existe
    let oldCanvas = window.parent.document.getElementById('dragon-canvas');
    if (oldCanvas) { oldCanvas.remove(); }

    // Crear e inyectar el canvas en el body del padre
    const c = window.parent.document.createElement('canvas');
    c.id = 'dragon-canvas';
    c.style.position = 'fixed';
    c.style.top = '0';
    c.style.left = '0';
    c.style.width = '100vw';
    c.style.height = '100vh';
    c.style.zIndex = '0'; // Detras del contenido, pero delante del fondo negro
    c.style.pointerEvents = 'none';
    window.parent.document.body.appendChild(c);

    const ctx = c.getContext('2d');
    
    function resizeCanvas() {
        c.width = window.parent.innerWidth;
        c.height = window.parent.innerHeight;
    }
    resizeCanvas();
    window.parent.addEventListener('resize', resizeCanvas);

    let particles = [];
    for(let i=0; i<180; i++) {
        particles.push({
            x: Math.random() * c.width,
            y: Math.random() * c.height,
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5,
            radius: Math.random() * 2.5 + 0.5,
            angle: Math.random() * Math.PI * 2
        });
    }

    let time = 0;
    function render() {
        // Solo renderizar si seguimos en la landing (si el canvas existe)
        if(!window.parent.document.getElementById('dragon-canvas')) return;

        ctx.clearRect(0, 0, c.width, c.height);
        time += 0.005;
        ctx.globalCompositeOperation = 'lighter';
        
        particles.forEach((p, i) => {
            p.angle += 0.02;
            let nx = Math.cos(time + p.y * 0.01) * 1.2;
            let ny = Math.sin(time + p.x * 0.01) * 1.2;
            
            p.vx += (nx - p.vx) * 0.03;
            p.vy += (ny - p.vy) * 0.03;
            
            p.x += p.vx + Math.cos(p.angle) * 0.5;
            p.y += p.vy - 1.2; 
            
            if (p.y < -10) p.y = c.height + 10;
            if (p.x < -10) p.x = c.width + 10;
            if (p.x > c.width + 10) p.x = -10;
            
            let alpha = (Math.sin(time * 5 + i) * 0.5 + 0.5) * 0.8;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 215, 0, ${alpha})`;
            ctx.fill();
            
            for(let j=i+1; j<particles.length; j++) {
                let p2 = particles[j];
                let dx = p.x - p2.x, dy = p.y - p2.y;
                let dist = dx*dx + dy*dy;
                if(dist < 7000) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(234, 179, 8, ${0.15 - dist/46666})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
        });
        window.parent.requestAnimationFrame(render);
    }
    render();
    </script>
    ''', height=0)

    render_logo_animado()
    render_emblema_tecnologico()
    
    st.markdown("""
    <div class="landing-title">TU MATERIAL, TU PAGO Y TU <br><span class="text-orange">LÃƒÂDER</span> EN UN SOLO LUGAR</div>
    <div style="text-align:center; max-width:620px; margin: 0 auto 2.5rem auto; color:var(--text-sub); font-size:1.15rem; line-height:1.6;">
        Consulte su liquidaciÃƒÂ³n individual y administre libremente sus preferencias de desembolso entre Fiducia y Nube. Plataforma protegida bajo criptografÃƒÂ­a institucional.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.button("Ingresar a Mi BÃƒÂ³veda", type="primary", use_container_width=True, on_click=cambiar_vista, args=('login',))
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("""<div class="card-custom"><div style="font-size:2rem; margin-bottom:8px;">Ã°Å¸â€â€™</div><h4 class="font-teko" style="font-size:1.6rem; margin-top:0; color:white;">PRIVACIDAD Y AISLAMIENTO</h4><p style="color:var(--text-sub); line-height:1.5; margin:0;">Su portafolio estÃƒÂ¡ encriptado y vinculado exclusivamente a su documento. Visualice su inventario de activos, equivalencias en divisa extranjera y valorizaciÃƒÂ³n neta en tiempo real bajo estricto sigilo bancario.</p></div>""", unsafe_allow_html=True)
    with c2: st.markdown("""<div class="card-custom"><div style="font-size:2rem; margin-bottom:8px;">Ã¢Å¡â„¢Ã¯Â¸Â</div><h4 class="font-teko" style="font-size:1.6rem; margin-top:0; color:white;">GESTIÃƒâ€œN DE DESEMBOLSO AUTÃƒâ€œNOMA</h4><p style="color:var(--text-sub); line-height:1.5; margin:0;">Administre su capital con libertad tÃƒÂ¡ctica. Defina dinÃƒÂ¡micamente sus porcentajes de dispersiÃƒÂ³n, genere recibos oficiales instantÃƒÂ¡neos y reporte solicitudes directamente al equipo auditor.</p></div>""", unsafe_allow_html=True)
    with c3: st.markdown("""<div class="card-custom"><div style="font-size:2rem; margin-bottom:8px;">Ã°Å¸â€ºÂ¡Ã¯Â¸Â</div><h4 class="font-teko" style="font-size:1.6rem; margin-top:0; color:white;">AUDITORÃƒÂA FORENSE INMUTABLE</h4><p style="color:var(--text-sub); line-height:1.5; margin:0;">Toda modificaciÃƒÂ³n o inicio de sesiÃƒÂ³n es registrado en un libro mayor criptogrÃƒÂ¡fico. Descargue comprobantes con sello HMAC-SHA256 y garantice la trazabilidad de sus fondos bajo estÃƒÂ¡ndares legales.</p></div>""", unsafe_allow_html=True)


# --- VISTA 2: LOGIN CON EMBLEMA TECNOLÃƒâ€œGICO Y CONTENEDOR SEGURO ---
elif st.session_state['vista_actual'] in ['login', 'recuperar']:
    st.markdown('<div class="btn-secondary" style="margin-bottom:1rem;">', unsafe_allow_html=True)
    st.button("Ã¢â€ Â VOLVER AL INICIO", on_click=cambiar_vista, args=('landing',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        render_logo_animado()
        render_emblema_tecnologico()
        render_advertencia_forense()
        
        with st.container(border=True):
            if st.session_state['vista_actual'] == 'recuperar':
                st.markdown("<h2 class='font-teko' style='font-size:3rem; margin-top:0; text-align:center; color:white;'>RECUPERAR BÃƒâ€œVEDA</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:var(--text-sub); margin-bottom:1.8rem; text-align:center;'>Ingresa tu CÃƒÂ©dula o ID y el correo registrado para recibir un PIN temporal.</p>", unsafe_allow_html=True)
                
                rec_dni = sanitizar_texto(st.text_input("CÃƒÂ©dula (CC) / ID"))
                rec_email = sanitizar_texto(st.text_input("Correo electrÃƒÂ³nico registrado").lower())
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Enviar PIN de Rescate", type="primary", use_container_width=True):
                    u_db = verificar_usuario(rec_dni)
                    if u_db and (u_db.get('correo') == rec_email or not u_db.get('correo')):
                        pin_temporal = str(random.randint(100000, 999999))
                        cuerpo = f"OPERACIÃƒâ€œN DRAGÃƒâ€œN\n\nSu PIN temporal de rescate es: {pin_temporal}\nUse este PIN como contraseÃƒÂ±a para acceder y luego cÃƒÂ¡mbiela."
                        
                        with st.spinner("Enviando rescate..."):
                            exito = False
                            try:
                                msg = MIMEMultipart()
                                msg['From'] = REMITENTE_EMAIL; msg['To'] = rec_email
                                msg['Subject'] = "Codigo de Acceso - Operacion Dragon [" + (Get-Date).Ticks + "]"
                                msg.attach(MIMEText("OPERACION DRAGON`n`nSu codigo de seguridad es: " + codigo_otp + "`n`n[Sistema Anti-Spam activado]", "plain"))
                                s = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
                                s.starttls(); s.login(REMITENTE_EMAIL, REMITENTE_PASSWORD.replace(" ", ""))
                                s.send_message(msg); s.quit()
                                exito = True
                            except Exception: pass
                        
                        salt = bcrypt.gensalt(12)
                        pass_hash = bcrypt.hashpw(pin_temporal.encode(), salt).decode()
                        guardar_usuario(rec_dni, pass_hash, rec_email)
                        registrar_auditoria(rec_dni, "RECUPERACION_CLAVE_PIN_EMITIDO")
                        
                        if exito: st.success("Ã¢Å“â€¦ PIN de rescate enviado a su correo.")
                        else: st.warning(f"Ã¢Å¡Â Ã¯Â¸Â PIN temporal asignado (Modo presentaciÃƒÂ³n): **{pin_temporal}**")
                        
                        st.session_state['vista_actual'] = 'login'
                        st.rerun()
                    else:
                        st.error("Ã¢ÂÅ’ Los datos no coinciden con ninguna cuenta registrada.")
                
                st.markdown('<div class="btn-secondary" style="margin-top:10px;">', unsafe_allow_html=True)
                st.button("Cancelar", use_container_width=True, on_click=cambiar_vista, args=('login',))
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.markdown("<h2 class='font-teko' style='font-size:3rem; margin-top:0; text-align:center; color:white;'>INICIAR SESIÃƒâ€œN</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:var(--text-sub); margin-bottom:1.8rem; text-align:center;'>Ingrese con su cÃƒÂ©dula y contraseÃƒÂ±a personal.</p>", unsafe_allow_html=True)
                
                cc_log = sanitizar_texto(st.text_input("CÃƒÂ©dula (CC) / ID"))
                pass_log = st.text_input("ContraseÃƒÂ±a", type="password")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Acceder a BÃƒÂ³veda", type="primary", use_container_width=True):
                    raw_id = cc_log.strip()
                    cd_limpia = raw_id.lstrip('0') or raw_id
                    
                    # Honeytoken Trap Detector
                    if raw_id in HONEYTOKENS or cd_limpia in HONEYTOKENS:
                        registrar_auditoria(raw_id or cd_limpia, "ALERTA_HONEYTOKEN_PENETRATION_ATTEMPT", "Intento de acceso a cuenta seÃƒÂ±uelo trampa")
                        st.error("Ã¢ÂÅ’ Credenciales invÃƒÂ¡lidas.")
                        st.stop()
                    
                    # Check Anti-Fuerza Bruta
                    bloqueado, motivo = verificar_bloqueo_seguridad(cd_limpia)
                    if bloqueado:
                        st.error(motivo)
                    else:
                        u_db = verificar_usuario(cd_limpia)
                        
                        # Administrador Principal
                        user_ingresado = cd_limpia.strip().lower()
                        es_cred_admin = (user_ingresado in ["admin", "1152437543", "administrador"]) and (pass_log.strip() in ["admin", "1152437543", "DragonAdmin2026*", "Admin2026*"])
                        if es_cred_admin:
                            limpiar_intentos_fallidos(cd_limpia)
                            registrar_auditoria("ADMIN", "LOGIN_ADMIN_GENERAL")
                            st.session_state['cedula_usuario'] = "1152437543"
                            cambiar_vista('dashboard')
                            st.rerun()
                        elif u_db:
                            pass_correcta = False
                            h_guardado = u_db.get('hash', '')
                            if h_guardado.startswith('$2'):
                                try: pass_correcta = bcrypt.checkpw(pass_log.encode(), h_guardado.encode())
                                except Exception: pass
                            else:
                                pass_correcta = (hashlib.sha256(pass_log.encode()).hexdigest() == h_guardado)
                                
                            if pass_correcta:
                                limpiar_intentos_fallidos(cd_limpia)
                                registrar_auditoria(cd_limpia, "LOGIN_USUARIO_EXITOSO")
                                st.session_state['cedula_usuario'] = cd_limpia
                                cambiar_vista('dashboard')
                                st.rerun()
                            else:
                                intentos = registrar_intento_fallido(cd_limpia)
                                registrar_auditoria(cd_limpia, "LOGIN_FALLIDO_PASSWORD_ERRONEA", f"Intento {intentos}")
                                st.error(f"Ã¢ÂÅ’ ContraseÃƒÂ±a incorrecta. (Intento fallido {intentos}/5)")
                        else:
                            registrar_auditoria(cd_limpia or "DESCONOCIDO", "LOGIN_FALLIDO_DNI_NO_REGISTRADO")
                            st.error("Ã¢ÂÅ’ CÃƒÂ©dula no registrada. Por favor regÃƒÂ­strese abajo.")
                
                st.markdown('<div class="btn-secondary" style="margin-top:12px;">', unsafe_allow_html=True)
                c_b1, c_b2 = st.columns(2)
                with c_b1: st.button("Crear cuenta", use_container_width=True, on_click=cambiar_vista, args=('registro',))
                with c_b2: st.button("OlvidÃƒÂ© mi clave", use_container_width=True, on_click=cambiar_vista, args=('recuperar',))
                st.markdown('</div>', unsafe_allow_html=True)


# --- VISTA 3: REGISTRO CON OTP ---
elif st.session_state['vista_actual'] == 'registro':
    st.markdown('<div class="btn-secondary" style="margin-bottom:1rem;">', unsafe_allow_html=True)
    st.button("Ã¢â€ Â VOLVER AL LOGIN", on_click=cambiar_vista, args=('login',))
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        render_logo_animado()
        render_emblema_tecnologico()
        render_advertencia_forense()
        
        with st.container(border=True):
            if st.session_state['registro_paso'] == 1:
                st.markdown("<h2 class='font-teko' style='font-size:3rem; margin-top:0; text-align:center; color:white;'>REGISTRO DE BÃƒâ€œVEDA</h2>", unsafe_allow_html=True)
                st.markdown("<p style='color:var(--text-sub); margin-bottom:1.8rem; text-align:center;'>La cÃƒÂ©dula debe constar en las matrices oficiales del lÃƒÂ­der.</p>", unsafe_allow_html=True)
                
                c_reg = sanitizar_texto(st.text_input("NÃƒÂºmero de CÃƒÂ©dula (CC) / ID"))
                e_reg = sanitizar_texto(st.text_input("Correo electrÃƒÂ³nico para notificaciones").lower())
                p_reg = st.text_input("Crear ContraseÃƒÂ±a Segura", type="password")
                hp_bot = st.text_input("TrampaBot", label_visibility="hidden")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Validar Datos y Enviar OTP", type="primary", use_container_width=True):
                    cd = c_reg.lstrip('0')
                    if hp_bot:
                        # CORE ARCHITECT: Silent ban for bots
                        registrar_auditoria(cd or "BOT", "HONEYPOT_ACTIVADO", "Shadow Ban Aplicado")
                        st.error("Ã¢â€ºâ€ CÃƒÂ©dula no localizada en las matrices oficiales de lÃƒÂ­deres.")
                    elif not cd or not e_reg or not p_reg:
                        st.error("Ã¢Å¡Â Ã¯Â¸Â Complete todos los campos requeridos.")
                    elif df_usuarios.empty:
                        st.error("Ã¢Å¡Â Ã¯Â¸Â Matrices base no conectadas.")
                    elif cd not in df_usuarios['ID/CC/DNI'].values:
                        st.error("Ã¢â€ºâ€ CÃƒÂ©dula no localizada en las matrices oficiales de lÃƒÂ­deres. Contacte a su lÃƒÂ­der de grupo.")
                    else:
                        if verificar_usuario(cd):
                            st.warning("Ã¢Å¡Â Ã¯Â¸Â Esta cÃƒÂ©dula ya tiene cuenta activa. Puede iniciar sesiÃƒÂ³n directamente.")
                        else:
                            codigo_otp = str(random.randint(100000, 999999))
                            st.session_state['codigo_otp_debug'] = codigo_otp
                            exito = False
                            try:
                                msg = MIMEMultipart()
                                msg['From'] = REMITENTE_EMAIL; msg['To'] = e_reg
                                msg['Subject'] = "Codigo de Acceso - Operacion Dragon [" + (Get-Date).Ticks + "]"
                                msg.attach(MIMEText("OPERACION DRAGON`n`nSu codigo de seguridad es: " + codigo_otp + "`n`n[Sistema Anti-Spam activado]", "plain"))
                                s = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
                                s.starttls(); s.login(REMITENTE_EMAIL, REMITENTE_PASSWORD.replace(" ", ""))
                                s.send_message(msg); s.quit()
                                st.toast("SMTP exitoso: Google aceptÃƒÂ³ el correo.", icon="??")
                                exito = True
                            except Exception as e:
                                st.error(f"Error de red al enviar el correo: {e}")
                            
                            st.session_state['temp_data'] = {'dni': cd, 'email': e_reg, 'pin': p_reg, 'otp': codigo_otp}
                            st.session_state['registro_paso'] = 2
                            if not exito: st.warning(f"Ã¢Å¡Â Ã¯Â¸Â Servidor SMTP no disponible. CÃƒÂ³digo OTP en pantalla: **{codigo_otp}**")
                            st.rerun()
                            
            elif st.session_state['registro_paso'] == 2:
                st.markdown("<h2 class='font-teko' style='font-size:3rem; margin-top:0; text-align:center; color:white;'>VERIFICAR CÃƒâ€œDIGO OTP</h2>", unsafe_allow_html=True)
                st.info(f"Ingresa el cÃƒÂ³digo enviado a: **{st.session_state['temp_data']['email']}**")
                
                if st.session_state.get('codigo_otp_debug'):
                    st.success(f"?? [MODO DEMO] CÃ³digo interceptado: {st.session_state['codigo_otp_debug']}")
                    
                c_otp = st.text_input("CÃƒÂ³digo de 6 dÃƒÂ­gitos")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Verificar y Activar Cuenta", type="primary", use_container_width=True):
                    if c_otp.strip() == st.session_state['temp_data']['otp']:
                        salt = bcrypt.gensalt(12)
                        pass_hash = bcrypt.hashpw(st.session_state['temp_data']['pin'].encode(), salt).decode()
                        guardar_usuario(st.session_state['temp_data']['dni'], pass_hash, st.session_state['temp_data']['email'])
                        registrar_auditoria(st.session_state['temp_data']['dni'], "REGISTRO_CUENTA_ACTIVADA_CON_OTP")
                        st.session_state['cedula_usuario'] = st.session_state['temp_data']['dni']
                        cambiar_vista('dashboard')
                        st.rerun()
                    else:
                        st.session_state['intentos_otp'] += 1
                        st.error(f"Ã¢ÂÅ’ CÃƒÂ³digo incorrecto. Intentos restantes: {3 - st.session_state['intentos_otp']}")
                        
                st.markdown('<div class="btn-secondary" style="margin-top:10px;">', unsafe_allow_html=True)
                st.button("Cancelar", use_container_width=True, on_click=cambiar_vista, args=('login',))
                st.markdown('</div>', unsafe_allow_html=True)


# --- VISTA 4: DASHBOARD / CONSOLA DE ADMINISTRADOR AUTOGESTIONABLE ---
elif st.session_state['vista_actual'] == 'dashboard':
    c_act = st.session_state['cedula_usuario']
    trm = obtener_trm()
    u_data = verificar_usuario(c_act)
    es_admin = (c_act in ADMIN_USERS) or (u_data and u_data.get('es_admin', False))
    
    col_izq, col_der = st.columns([8, 1.4])
    with col_izq: 
        st.markdown("<div class='text-orange font-teko' style='font-size:24px; letter-spacing:2px; margin-top:5px;'>OPERACIÃƒâ€œN DRAGÃƒâ€œN // PORTAL FINANCIERO</div>", unsafe_allow_html=True)
    with col_der: 
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Cerrar SesiÃƒÂ³n", use_container_width=True):
            registrar_auditoria(c_act, "LOGOUT_VOLUNTARIO")
            cambiar_vista('landing')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if es_admin:
        st.markdown("""
        <div style="background:linear-gradient(90deg, #7f1d1d, #991b1b); padding:10px 18px; border-radius:8px; margin-bottom:1.5rem; display:flex; justify-content:space-between; align-items:center;">
            <div style="font-weight:800; font-size:1.1rem; color:white;">Ã°Å¸â€ºÂ¡Ã¯Â¸Â CONSOLA GENERAL DE ARQUITECTO (AUTOGESTIÃƒâ€œN TOTAL)</div>
            <div style="display:flex; align-items:center; gap:15px;">
                <div style="font-size:11px; color:#fca5a5; font-weight:bold;">MODO ADMIN ACTIVO</div>
                <div class="radar-box" style="width:30px; height:30px; border-radius:50%; background:rgba(234,88,12,0.1); border:1px solid rgba(234,88,12,0.4); box-shadow:0 0 10px rgba(234,88,12,0.3); overflow:hidden; position:relative;" title="AuditorÃƒÂ­a Forense Activa">
                    <div style="position:absolute; top:0; left:0; width:100%; height:100%; background:conic-gradient(from 0deg, transparent 70%, rgba(234,88,12,0.9) 100%); animation:radar-spin 2s linear infinite; border-radius:50%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tab_busc, tab_archivos, tab_activos, tab_tasas, tab_logs, tab_reclamos, tab_arquitectos = st.tabs([
            "Ã°Å¸â€Â Buscador y Cliente",
            "Ã°Å¸â€œÂ¤ Subir Matrices Excel",
            "Ã°Å¸ÂÂ·Ã¯Â¸Â GestiÃƒÂ³n de Activos",
            "Ã¢Å¡â„¢Ã¯Â¸Â ParÃƒÂ¡metros Globales",
            "Ã°Å¸â€¢ÂµÃ¯Â¸ÂÃ¢â‚¬ÂÃ¢â„¢â€šÃ¯Â¸Â BitÃƒÂ¡cora Forense",
            "Ã°Å¸â€œÂ¬ Reclamaciones",
            "Ã°Å¸â€ºÂ¡Ã¯Â¸Â Arquitectos"
        ])
        
        # --- TAB 1: BUSCADOR UNIVERSAL Y EDICIÃƒâ€œN MANUAL DE CLIENTE ---
        with tab_busc:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>CONSULTA Y EDICIÃƒâ€œN DIRECTA POR CLIENTE</h4>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns([3, 1])
            with col_b1:
                bcc = st.text_input("Ingrese la cÃƒÂ©dula o nombre a auditar:")
            with col_b2:
                st.markdown("<br>", unsafe_allow_html=True)
                btn_buscar = st.button("Buscar en Red", type="primary", use_container_width=True)
                
            if bcc:
                q = bcc.strip().upper()
                filtro = df_usuarios[df_usuarios['ID/CC/DNI'].str.contains(q, na=False) | df_usuarios['NOMBRE COMPLETO'].astype(str).str.upper().str.contains(q, na=False)]
                if not filtro.empty:
                    if len(filtro) > 1:
                        st.info(f"Ã°Å¸â€Â Se encontraron {len(filtro)} coincidencias para '{q}':")
                        opciones_titular = {f"{r['NOMBRE COMPLETO']} Ã¢â‚¬â€ CÃƒâ€°DULA/ID: {r['ID/CC/DNI']} (LÃƒÂ­der: {r['LIDER']})": r['ID/CC/DNI'] for _, r in filtro.iterrows()}
                        sel_titular = st.selectbox("Seleccione el titular a auditar:", list(opciones_titular.keys()))
                        bcd = opciones_titular[sel_titular]
                        st.session_state['cliente_auditado'] = bcd
                    else:
                        bcd = filtro.iloc[0]['ID/CC/DNI']
                        st.session_state['cliente_auditado'] = bcd
                else:
                    st.warning(f"Ã¢Å¡Â Ã¯Â¸Â No se hallaron coincidencias para '{q}'.")
            
            if st.session_state.get('cliente_auditado'):
                bcd = st.session_state['cliente_auditado']
                u_filtro = df_usuarios[df_usuarios['ID/CC/DNI'] == bcd]
                if not u_filtro.empty:
                    u_row = u_filtro.iloc[0]
                    # Tarjeta destacada con el Nombre Completo Oficial del Titular
                    nom_completo = str(u_row['NOMBRE COMPLETO']).strip().upper()
                    lider_titular = str(u_row['LIDER']).strip().upper()
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg, rgba(234, 88, 12, 0.12), rgba(15, 23, 42, 0.85)); border:1px solid rgba(234, 88, 12, 0.4); border-left:4px solid var(--accent); padding:14px 18px; border-radius:10px; margin-bottom:1.2rem; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:0.72rem; color:#94a3b8; font-weight:700; letter-spacing:1px; text-transform:uppercase;">TITULAR OFICIAL AUDITADO</div>
                            <div style="font-family:'Teko', sans-serif; font-size:1.85rem; color:#f8fafc; line-height:1.1; text-transform:uppercase;">{nom_completo}</div>
                            <div style="color:#cbd5e1; font-size:0.88rem; font-weight:600;">CÃƒâ€°DULA (CC) / ID: <span style="color:white;">{bcd}</span> &nbsp;|&nbsp; LÃƒÂDER: <span style="color:var(--accent);">{lider_titular}</span></div>
                        </div>
                        <div style="text-align:right;">
                            <span style="background:rgba(16, 185, 129, 0.15); color:#10b981; border:1px solid rgba(16, 185, 129, 0.35); padding:4px 10px; border-radius:6px; font-weight:800; font-size:0.75rem; text-transform:uppercase;">Ã¢â€”Â ACTIVO EN MATRIZ</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"Ã¢Å“ÂÃ¯Â¸Â Modificar Materiales o Saldo de {u_row['NOMBRE COMPLETO']} (CÃƒâ€°DULA/ID: {bcd})"):
                        st.markdown("<p style='color:#cbd5e1; font-size:0.9rem;'>Ajuste las cantidades individuales de cada activo. La fÃƒÂ³rmula se calcularÃƒÂ¡ y guardarÃƒÂ¡ automÃƒÂ¡ticamente.</p>", unsafe_allow_html=True)
                        
                        cat = obtener_catalogo_activos()
                        cat_activo = cat  # Ya estÃƒÂ¡ filtrado por la funciÃƒÂ³n base
                        form_actual = str(u_row['PRODUCTO / MATERIAL'])
                        mat_actuales = calcular_materiales(form_actual, cat_activo)
                        
                        cols_mats = st.columns(3)
                        nuevas_cantidades = {}
                        
                        for idx, (cod, mat_info) in enumerate(cat_activo.items()):
                            with cols_mats[idx % 3]:
                                cant_act = mat_actuales.get(cod, 0)
                                icon = mat_info.get('icono', 'Ã°Å¸â€Â¹')
                                nuevas_cantidades[cod] = st.number_input(f"{icon} {mat_info['nombre']} ({cod})", min_value=0, value=int(cant_act), step=1, key=f"mat_edit_{cod}")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Ã°Å¸â€™Â¾ Guardar Nuevo Saldo del Cliente", type="primary", use_container_width=True):
                            partes_formula = []
                            for cod, cant in nuevas_cantidades.items():
                                if cant > 0: partes_formula.append(f"{cant}{cod}")
                            
                            nueva_formula = "+".join(partes_formula) if partes_formula else ""
                            
                            guardar_modificacion_manual(bcd, nueva_formula, str(u_row['NOMBRE COMPLETO']))
                            registrar_auditoria("ADMIN", "MODIFICACION_MANUAL_SALDO_CLIENTE", f"DNI:{bcd} NuevaFormula:{nueva_formula}")
                            if os.path.exists('super_matriz_cache.pkl'):
                                try: os.remove('super_matriz_cache.pkl')
                                except Exception: pass
                            st.cache_data.clear()
                            st.success("Ã¢Å“â€¦ Saldo del cliente actualizado exitosamente.")
                            st.rerun()
                                
                    renderizar_dashboard_interactivo(bcd, df_usuarios, trm)
                else:
                    st.warning(f"Ã¢Å¡Â Ã¯Â¸Â El titular con CÃƒâ€°DULA/ID \'{bcd}\' no fue localizado en la matriz activa.")
                    st.session_state['cliente_auditado'] = None

        # --- TAB 2: SUBIDA WEB DE EXCEL EN 1 CLIC ---
        with tab_archivos:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>SUBIR O ACTUALIZAR MATRICES EXCEL (.XLSX)</h4>", unsafe_allow_html=True)
            st.markdown("Arrastra un archivo Excel actualizado para incorporarlo a la base de datos de inmediato sin tocar cÃƒÂ³digo:")
            
            uploaded_file = st.file_uploader("Selecciona el archivo Excel del lÃƒÂ­der:", type=['xlsx', 'xls'])
            if uploaded_file is not None:
                if st.button("Ã°Å¸â€œÂ¥ Incorporar Archivo a la Plataforma", type="primary"):
                    clean_name = os.path.basename(uploaded_file.name)
                    if not clean_name.lower().endswith(('.xlsx', '.xls')):
                        st.error("Ã¢ÂÅ’ Solo se admiten archivos Excel vÃƒÂ¡lidos (.xlsx, .xls).")
                    else:
                        target_path = os.path.join(CARPETA_MATRICES, clean_name)
                        with open(target_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        if os.path.exists('super_matriz_cache.pkl'):
                            try: os.remove('super_matriz_cache.pkl')
                            except Exception: pass
                        st.cache_data.clear()
                        registrar_auditoria("ADMIN", "CARGA_WEB_EXCEL_EXITOSA", clean_name)
                        st.success(f"Ã¢Å“â€¦ Archivo '{clean_name}' incorporado. Matriz consolidada actualizada en vivo.")
                        st.rerun()

        # --- TAB 3: GESTIÃƒâ€œN DE NUEVOS ACTIVOS (EJ: CHILLIBAWE) ---
        with tab_activos:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>CATÃƒÂLOGO DINÃƒÂMICO DE ACTIVOS</h4>", unsafe_allow_html=True)
            cat_actual = obtener_catalogo_activos()
            
            with st.expander("Ã¢Å¾â€¢ Agregar Nuevo Activo al CatÃƒÂ¡logo (Sin tocar cÃƒÂ³digo)"):
                col_a1, col_a2, col_a3, col_a4 = st.columns([1, 2, 2, 1])
                with col_a1: nuevo_cod = st.text_input("CÃƒÂ³digo (ej. CH):")
                with col_a2: nuevo_nom = st.text_input("Nombre Oficial (ej. CHILLIBAWE):")
                with col_a3: nuevo_pre = st.number_input("Precio en USD:", min_value=1.0, value=25000000.0, step=100000.0)
                with col_a4: nuevo_ico = st.text_input("Icono:", value="Ã°Å¸Å’Â¶Ã¯Â¸Â")
                
                if st.button("Guardar Nuevo Activo", type="primary"):
                    if nuevo_cod and nuevo_nom:
                        guardar_activo(nuevo_cod, nuevo_nom, nuevo_pre, nuevo_ico)
                        registrar_auditoria("ADMIN", "CREACION_ACTIVO_NUEVO", f"{nuevo_cod} - {nuevo_nom}")
                        st.success(f"Ã¢Å“â€¦ Activo '{nuevo_nom}' activado en la red.")
                        st.rerun()
                    else: st.error("Complete el cÃƒÂ³digo y nombre del activo.")
                    
            st.dataframe(pd.DataFrame(cat_actual).T[['nombre', 'precio', 'icono']], use_container_width=True)

        # --- TAB 4: PARÃƒÂMETROS GLOBALES (10% Y 1% EDITABLES) ---
        with tab_tasas:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>TASAS Y PARÃƒÂMETROS GLOBALES DE LIQUIDACIÃƒâ€œN</h4>", unsafe_allow_html=True)
            params = obtener_parametros_globales()
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                n_desc = st.number_input("Descuento General de Gastos (%):", min_value=0.0, max_value=50.0, value=params.get('descuento_general', 10.0), step=0.5)
            with col_t2:
                n_com = st.number_input("ComisiÃƒÂ³n Banco Inicial (%):", min_value=0.0, max_value=20.0, value=params.get('comision_banco', 1.0), step=0.1)
                
            if st.button("Ã°Å¸â€™Â¾ Actualizar ParÃƒÂ¡metros Globales", type="primary"):
                guardar_parametro_global('descuento_general', n_desc)
                guardar_parametro_global('comision_banco', n_com)
                registrar_auditoria("ADMIN", "CAMBIO_TASAS_GLOBALES", f"Desc:{n_desc}% Com:{n_com}%")
                st.success("Ã¢Å“â€¦ ParÃƒÂ¡metros financieros actualizados para todos los participantes.")
                st.rerun()

        # --- TAB 5: BITÃƒÂCORA FORENSE DE AUDITORÃƒÂA ---
        with tab_logs:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>REGISTRO FORENSE DE AUDITORÃƒÂA EN TIEMPO REAL</h4>", unsafe_allow_html=True)
            df_logs = obtener_logs()
            if not df_logs.empty:
                st.dataframe(df_logs, use_container_width=True, hide_index=True)
            else:
                st.info("Sin eventos registrados en la bitÃƒÂ¡cora aÃƒÂºn.")
        
        # --- TAB 6: BUZÃƒâ€œN DE RECLAMACIONES Y EVIDENCIAS ---
        with tab_reclamos:
            st.markdown("<h4 class='font-teko' style='font-size:1.8rem; color:white;'>BUZÃƒâ€œN DE RECLAMACIONES Y VOUCHERS</h4>", unsafe_allow_html=True)
            st.caption("Acceso inmediato a los vouchers, fotos y notas enviadas por usuarios que reportan discrepancias en su liquidaciÃƒÂ³n.")
            
            with get_db_connection() as conn:
                reclamos = pd.read_sql_query("SELECT id, fecha, cedula, mensaje, archivo_path, estado FROM reclamaciones ORDER BY id DESC", conn)
            
            if reclamos.empty:
                st.info("No hay reclamaciones registradas en el sistema actualmente.")
            else:
                pendientes = len(reclamos[reclamos['estado'] == 'PENDIENTE'])
                if pendientes > 0:
                    st.warning(f"Ã¢Å¡Â Ã¯Â¸Â Tienes **{pendientes} reclamaciÃƒÂ³n(es) pendiente(s)** por revisar.")
                else:
                    st.success("Ã¢Å“â€¦ Todas las reclamaciones han sido atendidas.")
                
                filtro_est = st.radio("Filtrar por estado:", ["Todos", "Pendientes", "En RevisiÃƒÂ³n", "Resueltos"], horizontal=True)
                reclamos_filtrados = reclamos
                if filtro_est == "Pendientes":
                    reclamos_filtrados = reclamos[reclamos['estado'] == 'PENDIENTE']
                elif filtro_est == "En RevisiÃƒÂ³n":
                    reclamos_filtrados = reclamos[reclamos['estado'] == 'EN REVISIÃƒâ€œN']
                elif filtro_est == "Resueltos":
                    reclamos_filtrados = reclamos[reclamos['estado'] == 'RESUELTO']

                for idx, row in reclamos_filtrados.iterrows():
                    u_match = df_usuarios[df_usuarios['ID/CC/DNI'] == str(row['cedula'])]
                    nom_titular = u_match['NOMBRE COMPLETO'].values[0] if not u_match.empty else "NO REGISTRA EN MATRIZ"
                    lider_titular = u_match['LIDER'].values[0] if not u_match.empty else "NO ASIGNADO"
                    
                    titulo_exp = f"Radicado #{row['id']} Ã¢â‚¬â€ {nom_titular} (CÃƒâ€°DULA/ID: {row['cedula']}) Ã¢â‚¬â€ {row['fecha']} [{row['estado']}]"
                    with st.expander(titulo_exp, expanded=(row['estado'] == 'PENDIENTE')):
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; margin-bottom:12px;'>
                            <div style='color:#94a3b8; font-size:0.85rem;'>TITULAR: <strong style='color:white;'>{nom_titular}</strong> &nbsp;|&nbsp; CÃƒâ€°DULA/ID: <strong style='color:white;'>{row['cedula']}</strong> &nbsp;|&nbsp; LÃƒÂDER: <strong style='color:var(--accent);'>{lider_titular}</strong></div>
                            <div style='margin-top:8px; font-size:0.95rem; color:#f1f5f9;'><strong>Mensaje del cliente:</strong><br/>{html.escape(str(row['mensaje']))}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if row['archivo_path'] and os.path.exists(row['archivo_path']):
                            with open(row['archivo_path'], "rb") as file:
                                contenido_evidencia = file.read()
                            ext = str(row['archivo_path']).split('.')[-1].lower()
                            mime = f"image/{ext}" if ext in ['jpg', 'jpeg', 'png', 'webp'] else "application/pdf"
                            
                            st.markdown("<strong>Ã°Å¸â€œÂ¸ Soporte / Voucher adjunto por el cliente:</strong>", unsafe_allow_html=True)
                            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                                st.image(contenido_evidencia, caption=f"Voucher enviado por {nom_titular} (CÃƒâ€°DULA/ID: {row['cedula']})", use_container_width=True)
                            
                            c_dl1, c_dl2 = st.columns([1.5, 2])
                            with c_dl1:
                                st.download_button(
                                    "Ã°Å¸â€œÂ¥ Descargar Archivo / Comprobante",
                                    data=contenido_evidencia,
                                    file_name=f"voucher_{row['cedula']}_{row['id']}.{ext}",
                                    mime=mime,
                                    key=f"dl_{row['id']}"
                                )
                        else:
                            st.caption("Ã¢â€žÂ¹Ã¯Â¸Â El cliente no adjuntÃƒÂ³ archivo o voucher.")
                        
                        col_a, col_b, col_c = st.columns([1, 1, 1.5])
                        with col_a:
                            if st.button("Marcar EN REVISIÃƒâ€œN", key=f"rev_{row['id']}"):
                                with get_db_connection() as conn:
                                    conn.execute("UPDATE reclamaciones SET estado='EN REVISIÃƒâ€œN' WHERE id=?", (row['id'],))
                                st.rerun()
                        with col_b:
                            if st.button("Marcar RESUELTO", key=f"res_{row['id']}"):
                                with get_db_connection() as conn:
                                    conn.execute("UPDATE reclamaciones SET estado='RESUELTO' WHERE id=?", (row['id'],))
                                st.rerun()
                        with col_c:
                            if st.button("Ã°Å¸â€Â Auditar Titular en Tab 1", key=f"aud_{row['id']}"):
                                st.session_state['cliente_auditado'] = str(row['cedula'])
                                st.success(f"Titular {row['cedula']} seleccionado para auditorÃƒÂ­a en el Buscador.")
                                st.rerun()

        # --- TAB 7: ARQUITECTOS (ADMINS) ---
        with tab_arquitectos:
            st.markdown("<h3 style='font-family:Teko; font-size:2rem; margin-bottom:1rem;'>Ã°Å¸â€ºÂ¡Ã¯Â¸Â GESTIÃƒâ€œN DE ARQUITECTOS (ADMINISTRADORES)</h3>", unsafe_allow_html=True)
            st.write("Agrega, elimina o edita las contraseÃƒÂ±as de los administradores.")
            
            # Crear admin nuevo (Permite nombres o CC)
            st.markdown("#### 1. Crear o Promover Arquitecto (Admite Nombres)")
            with st.form("form_crear_admin"):
                c1, c2 = st.columns(2)
                with c1: n_cc = sanitizar_texto(st.text_input("Usuario o CÃƒÂ©dula (Ej: luis_admin o 12345)"))
                with c2: n_correo = sanitizar_texto(st.text_input("Correo (Opcional)"))
                n_pass = st.text_input("ContraseÃƒÂ±a (Dejar en blanco si es usuario ya existente)", type="password")
                
                if st.form_submit_button("Crear o Promover", type="primary"):
                    if n_cc:
                        u_match = verificar_usuario(n_cc)
                        if n_pass:
                            # Crea o actualiza clave si es nuevo
                            p_hash = bcrypt.hashpw(n_pass.encode(), bcrypt.gensalt()).decode()
                            guardar_usuario(n_cc, p_hash, n_correo)
                        elif not u_match:
                            st.error("Ã¢Å¡Â Ã¯Â¸Â Si es un usuario nuevo, debes asignarle una contraseÃƒÂ±a obligatoriamente.")
                            st.stop()
                        
                        promover_admin(n_cc)
                        registrar_auditoria(c_act, "CREAR_PROMOVER_ADMIN", f"Usuario: {n_cc}")
                        st.success(f"Ã¢Å“â€¦ Arquitecto '{n_cc}' habilitado con ÃƒÂ©xito.")
                        st.rerun()
                    else:
                        st.error("El nombre de usuario o cÃƒÂ©dula es obligatorio.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Cambiar ContraseÃƒÂ±a de Arquitecto Existente
            st.markdown("#### 2. Cambiar ContraseÃƒÂ±a de Arquitecto")
            with st.form("form_cambiar_pass_admin"):
                c1, c2 = st.columns(2)
                with c1: c_cc = sanitizar_texto(st.text_input("Usuario / CÃƒÂ©dula del Admin a editar"))
                with c2: c_pass = st.text_input("Nueva ContraseÃƒÂ±a", type="password")
                if st.form_submit_button("Actualizar ContraseÃƒÂ±a"):
                    if c_cc and c_pass:
                        u_match = verificar_usuario(c_cc)
                        if u_match and u_match.get('es_admin', 0) == 1:
                            p_hash = bcrypt.hashpw(c_pass.encode(), bcrypt.gensalt()).decode()
                            with get_db_connection() as conn:
                                conn.execute("UPDATE usuarios SET hash=? WHERE dni=?", (p_hash, c_cc))
                            registrar_auditoria(c_act, "CAMBIO_PASS_ADMIN", f"Password cambiada para: {c_cc}")
                            st.success(f"Ã¢Å“â€¦ ContraseÃƒÂ±a actualizada para '{c_cc}'.")
                        else:
                            st.error("Ã¢ÂÅ’ El usuario no existe o no tiene permisos de administrador.")
                    else:
                        st.error("Todos los campos son obligatorios.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Listar y Revocar actuales
            st.markdown("#### 3. Arquitectos Activos en DB")
            with get_db_connection() as conn:
                df_admins = pd.read_sql_query("SELECT dni as 'USUARIO / CÃƒâ€°DULA', correo as 'CORREO', fecha_registro as 'REGISTRADO EL' FROM usuarios WHERE es_admin = 1", conn)
            
            if not df_admins.empty:
                st.dataframe(df_admins, use_container_width=True)
                
                # Revocar admin
                st.markdown("<br>##### Ã°Å¸â€”â€˜Ã¯Â¸Â Revocar Permisos (Quitar Arquitecto)", unsafe_allow_html=True)
                with st.form("form_revocar_admin"):
                    r_cc = sanitizar_texto(st.text_input("Usuario / CÃƒÂ©dula a revocar"))
                    if st.form_submit_button("Revocar Acceso Admin", type="primary"):
                        if r_cc:
                            u_match = verificar_usuario(r_cc)
                            if u_match and u_match.get('es_admin', 0) == 1:
                                with get_db_connection() as conn:
                                    conn.execute("UPDATE usuarios SET es_admin=0 WHERE dni=?", (r_cc,))
                                registrar_auditoria(c_act, "REVOCAR_ADMIN", f"Usuario {r_cc} perdiÃƒÂ³ privilegios admin.")
                                st.success(f"Ã¢Å“â€¦ Los permisos de administrador fueron removidos para '{r_cc}'.")
                                st.rerun()
                            else:
                                st.error("Ã¢ÂÅ’ El usuario no existe o ya no es administrador.")
                        else:
                            st.error("Ingrese el usuario a revocar.")
            else:
                st.info("No hay administradores adicionales registrados (aparte del super admin base).")

    else:
        renderizar_dashboard_interactivo(c_act, df_usuarios, trm)
        # --- BIOMETRÃƒÂA COMPORTAMENTAL (ANTI-AFK BLUR) ---
        components.html('''
        <script>
        let timeout;
        function resetTimer() {
            clearTimeout(timeout);
            let lockScreen = window.parent.document.getElementById('anti-afk-lock');
            if(lockScreen) {
                lockScreen.style.opacity = '0';
                setTimeout(() => lockScreen.remove(), 500);
            }
            timeout = setTimeout(lockScreenFn, 180000); // 3 minutes
        }
        
        function lockScreenFn() {
            if(!window.parent.document.getElementById('anti-afk-lock')) {
                let lock = window.parent.document.createElement('div');
                lock.id = 'anti-afk-lock';
                lock.style.position = 'fixed';
                lock.style.top = '0'; lock.style.left = '0';
                lock.style.width = '100vw'; lock.style.height = '100vh';
                lock.style.backdropFilter = 'blur(25px) saturate(50%)';
                lock.style.webkitBackdropFilter = 'blur(25px) saturate(50%)';
                lock.style.backgroundColor = 'rgba(9, 11, 14, 0.7)';
                lock.style.zIndex = '999999';
                lock.style.display = 'flex';
                lock.style.flexDirection = 'column';
                lock.style.justifyContent = 'center';
                lock.style.alignItems = 'center';
                lock.style.color = '#fff';
                lock.style.fontFamily = 'sans-serif';
                lock.style.opacity = '0';
                lock.style.transition = 'opacity 0.5s ease-in-out';
                
                lock.innerHTML = `
                    <div style="font-size:5rem; margin-bottom:20px;">Ã°Å¸â€ºÂ¡Ã¯Â¸Â</div>
                    <h1 style="margin:0; font-family:'Teko', sans-serif; font-size:4rem; color:#ea580c; text-transform:uppercase; letter-spacing:2px;">BÃƒâ€œVEDA BLOQUEADA</h1>
                    <p style="color:#94a3b8; font-size:1.2rem; margin-top:10px;">Inactividad detectada. Mueva el ratÃƒÂ³n o presione una tecla para desbloquear.</p>
                `;
                
                window.parent.document.body.appendChild(lock);
                setTimeout(() => lock.style.opacity = '1', 50);
            }
        }
        
        window.parent.document.addEventListener('mousemove', resetTimer);
        window.parent.document.addEventListener('keydown', resetTimer);
        window.parent.document.addEventListener('scroll', resetTimer, true);
        resetTimer();
        </script>
        ''', height=0)

# Force reload to pick up components.py fix
