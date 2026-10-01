# ==============================================================================
# SERVICIO PROFESIONAL DE CORREO SMTP (ENVÍO DE OTP Y RECLAMACIONES CON ADJUNTOS)
# ==============================================================================
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

from database import obtener_config_sistema
from config import REMITENTE_EMAIL, REMITENTE_PASSWORD

def obtener_credenciales_smtp():
    remitente = obtener_config_sistema("correo_remitente_otp", REMITENTE_EMAIL).strip()
    password = obtener_config_sistema("password_remitente_otp", REMITENTE_PASSWORD).strip()
    servidor = obtener_config_sistema("servidor_smtp", "smtp.gmail.com").strip()
    puerto_str = obtener_config_sistema("puerto_smtp", "587").strip()
    try:
        puerto = int(puerto_str)
    except Exception:
        puerto = 587
    return remitente, password, servidor, puerto

def enviar_correo_otp(destinatario, codigo_otp):
    remitente, password, servidor, puerto = obtener_credenciales_smtp()
    if not remitente or not password:
        return False, "Credenciales SMTP no configuradas en el sistema."
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario.strip()
    msg['Subject'] = f"Código de Seguridad - Operación Dragón [{datetime.now().strftime('%H%M%S')}]"
    
    cuerpo = f"""==================================================
OPERACIÓN DRAGÓN // PORTAL FINANCIERO CLASIFICADO
==================================================

Su código de verificación OTP es:

        {codigo_otp}

• Este código tiene una validez temporal de 10 minutos.
• Es confidencial y de un solo uso.
• No lo comparta con terceros ni con su líder.

Si usted no solicitó este código, ignore este mensaje."""

    msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
    
    try:
        s = smtplib.SMTP(servidor, puerto, timeout=8)
        s.starttls()
        s.login(remitente, password.replace(" ", ""))
        s.send_message(msg)
        s.quit()
        return True, "Código enviado exitosamente al correo registrado."
    except Exception as e:
        return False, f"Error al enviar correo OTP: {e}"

def enviar_notificacion_reclamacion(cedula, mensaje, archivo_path, radicado_id):
    remitente, password, servidor, puerto = obtener_credenciales_smtp()
    destino_raw = obtener_config_sistema("correo_destino_reclamos", remitente).strip()
    notificar = obtener_config_sistema("notificar_por_correo", "1").strip()
    
    if notificar == '0' or not destino_raw or not remitente or not password:
        return False, "Notificaciones por correo desactivadas o sin destinatario configurado."
    
    destinatarios = [d.strip() for d in destino_raw.replace(';', ',').split(',') if '@' in d.strip()]
    if not destinatarios:
        return False, "No hay correos de destino válidos configurados."
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = f"🚨 NUEVA RECLAMACIÓN / VOUCHER — Radicado #{radicado_id} (Cédula: {cedula})"
    
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre_adjunto = os.path.basename(archivo_path) if archivo_path and os.path.exists(archivo_path) else "Sin archivo adjunto"
    
    cuerpo = f"""===================================================================
ALERTA FORENSE: NUEVO SOPORTE / VOUCHER RADICADO EN BÓVEDA DRAGÓN
===================================================================

• Radicado Oficial: #{radicado_id}
• Fecha y Hora: {fecha_hora}
• Cédula (CC) / ID del Titular: {cedula}
• Archivo de Evidencia: {nombre_adjunto}

-------------------------------------------------------------------
DESCRIPCIÓN / MENSAJE INGRESADO POR EL TITULAR:
-------------------------------------------------------------------
{mensaje if mensaje else '(Sin mensaje de texto adicional)'}

-------------------------------------------------------------------
Este correo contiene adjunta la imagen o documento de evidencia aportado por el titular.
Auditoría Operación Dragón 2026."""

    msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
    
    if archivo_path and os.path.exists(archivo_path):
        try:
            with open(archivo_path, 'rb') as f:
                adjunto = MIMEBase('application', 'octet-stream')
                adjunto.set_payload(f.read())
            encoders.encode_base64(adjunto)
            adjunto.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(archivo_path)}"'
            )
            msg.attach(adjunto)
        except Exception:
            pass
            
    try:
        s = smtplib.SMTP(servidor, puerto, timeout=12)
        s.starttls()
        s.login(remitente, password.replace(" ", ""))
        s.send_message(msg)
        s.quit()
        return True, f"Notificación enviada a: {', '.join(destinatarios)}"
    except Exception as e:
        return False, f"Error al notificar por correo: {e}"

def probar_conexion_smtp(correo_destino_prueba):
    remitente, password, servidor, puerto = obtener_credenciales_smtp()
    if not remitente or not password:
        return False, "Faltan credenciales de remitente o contraseña de aplicación."
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = correo_destino_prueba.strip()
    msg['Subject'] = f"✅ Test de Conexión SMTP Exitoso — Operación Dragón [{datetime.now().strftime('%H%M%S')}]"
    
    cuerpo = f"""TEST DE CONEXIÓN SMTP EXITOSO // BÓVEDA OPERACIÓN DRAGÓN

• Servidor SMTP: {servidor}:{puerto}
• Correo Remitente: {remitente}
• Destinatario de Prueba: {correo_destino_prueba}
• Fecha y Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

¡El canal de correos está 100% operativo para el envío de códigos OTP y recepción de reclamaciones!"""

    msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
    
    try:
        s = smtplib.SMTP(servidor, puerto, timeout=8)
        s.starttls()
        s.login(remitente, password.replace(" ", ""))
        s.send_message(msg)
        s.quit()
        return True, f"✅ Correo de prueba enviado con éxito a '{correo_destino_prueba}'."
    except Exception as e:
        return False, f"❌ Error de conexión SMTP: {e}"
