# ==============================================================================
# MOTOR GENERADOR DE REPORTES OFICIALES PDF REPORTLAB CON SELLO HMAC
# ==============================================================================
import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from services import formato_pesos, formato_trm

def generar_recibo_pdf(cedula, nombre, lider, prod, calc, catalogo, t_usd, t_neto, b_usd, f_usd_fid, f_usd_nube, pct_fid, pct_nube, t_cop, trm_actual, firma_hmac):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=colors.HexColor('#ea580c'), alignment=1)
    sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#64748b'), alignment=1)
    cell_bold = ParagraphStyle('CBold', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor('#0f172a'))
    cell_norm = ParagraphStyle('CNorm', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#334155'))
    cell_green = ParagraphStyle('CGreen', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#16a34a'))
    cell_head = ParagraphStyle('CHead', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)

    if os.path.exists('logo.png'):
        try:
            elements.append(RLImage('logo.png', width=50, height=50))
            elements.append(Spacer(1, 6))
        except Exception: pass

    elements.append(Paragraph("OPERACIÓN DRAGÓN — COMPROBANTE OFICIAL DE BÓVEDA", titulo_style))
    elements.append(Paragraph("SISTEMA DE ASIGNACIÓN PATRIMONIAL Y DISTRIBUCIÓN ELECTRÓNICA", sub_style))
    elements.append(Spacer(1, 12))

    info_data = [
        [Paragraph("<b>BENEFICIARIO:</b>", cell_bold), Paragraph(str(nombre).upper(), cell_norm),
         Paragraph("<b>FECHA EMISIÓN:</b>", cell_bold), Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), cell_norm)],
        [Paragraph("<b>DOCUMENTO (CC) / ID:</b>", cell_bold), Paragraph(str(cedula), cell_norm),
         Paragraph("<b>TRM APLICADA:</b>", cell_bold), Paragraph(formato_trm(trm_actual) + " COP", cell_norm)],
        [Paragraph("<b>LÍDER ASIGNADO:</b>", cell_bold), Paragraph(str(lider).upper(), cell_norm),
         Paragraph("<b>ESTADO CUENTA:</b>", cell_bold), Paragraph("VERIFICADA Y CERTIFICADA", cell_green)]
    ]
    t_info = Table(info_data, colWidths=[110, 160, 110, 160])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 12))

    mat_rows = [[Paragraph("MATERIAL / ACTIVO", cell_head), Paragraph("CANT", cell_head), Paragraph("VALOR UNITARIO (USD)", cell_head), Paragraph("TOTAL (USD)", cell_head)]]
    for k, v in catalogo.items():
        if calc.get(k, 0) > 0:
            monto_row = calc[k] * v['precio']
            mat_rows.append([
                Paragraph(f"{v['icono']} {v['nombre']}", cell_bold),
                Paragraph(f"x{calc[k]}", cell_norm),
                Paragraph(formato_pesos(v['precio']) + " USD", cell_norm),
                Paragraph(formato_pesos(monto_row) + " USD", cell_bold)
            ])
    if len(mat_rows) == 1:
        mat_rows.append([Paragraph("Sin materiales activos", cell_norm), Paragraph("-", cell_norm), Paragraph("-", cell_norm), Paragraph("-", cell_norm)])

    t_mat = Table(mat_rows, colWidths=[200, 60, 140, 140])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ea580c')),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_mat)
    elements.append(Spacer(1, 12))

    monto_descuento = max(0.0, t_usd - t_neto)
    pct_desc_real = (monto_descuento / t_usd * 100.0) if t_usd > 0 else 10.0
    pct_neto_real = 100.0 - pct_desc_real
    pct_banco_real = (b_usd / t_neto * 100.0) if t_neto > 0 else 1.0

    fin_rows = [
        [Paragraph("<b>CONCEPTO DE LIQUIDACIÓN</b>", cell_head), Paragraph("<b>VALOR EN USD</b>", cell_head), Paragraph("<b>VALOR EN PESOS (COP)</b>", cell_head)],
        [Paragraph("PAGO TOTAL BRUTO", cell_norm), Paragraph(formato_pesos(t_usd) + " USD", cell_norm), Paragraph(formato_pesos(t_usd * trm_actual), cell_norm)],
        [Paragraph(f"DESCUENTO GASTOS OPERATIVOS (-{pct_desc_real:.0f}%)", cell_norm), Paragraph("- " + formato_pesos(monto_descuento) + " USD", cell_norm), Paragraph("- " + formato_pesos(monto_descuento * trm_actual), cell_norm)],
        [Paragraph(f"TOTAL NETO LIQUIDADO ({pct_neto_real:.0f}%)", cell_bold), Paragraph(formato_pesos(t_neto) + " USD", cell_bold), Paragraph(formato_pesos(t_cop), cell_bold)],
        [Paragraph(f"{pct_banco_real:.1f}% PAGO INICIAL BANCO", cell_norm), Paragraph(formato_pesos(b_usd) + " USD", cell_norm), Paragraph(formato_pesos(b_usd * trm_actual), cell_norm)],
        [Paragraph(f"FIDUCIA ({pct_fid:.0f}% Remanente)", cell_norm), Paragraph(formato_pesos(f_usd_fid) + " USD", cell_norm), Paragraph(formato_pesos(f_usd_fid * trm_actual), cell_norm)],
        [Paragraph(f"NUBE ({pct_nube:.0f}% Remanente)", cell_norm), Paragraph(formato_pesos(f_usd_nube) + " USD", cell_norm), Paragraph(formato_pesos(f_usd_nube * trm_actual), cell_norm)],
        [Paragraph("<b>TOTAL FINAL A DESEMBOLSAR</b>", cell_green), Paragraph("<b>" + formato_pesos(t_neto) + " USD</b>", cell_green), Paragraph("<b>" + formato_pesos(t_cop) + "</b>", cell_green)]
    ]
    t_fin = Table(fin_rows, colWidths=[230, 155, 155])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#dcfce7')),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_fin)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>SELLO CRIPTOGRÁFICO HMAC-SHA256 (INMUTABLE):</b><br/><code>{firma_hmac}</code>", sub_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

