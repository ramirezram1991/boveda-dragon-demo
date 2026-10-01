# ==============================================================================
# ESTILOS VISUALES SUPREMOS, TEMAS NEÓN Y RESPONSIVIDAD (UI VANGUARD)
# ==============================================================================
from config import TEMA_COLOR

def obtener_css_maestro(tema_actual: str = "cyber_dragon") -> str:
    T_ACT = TEMA_COLOR.get(tema_actual, TEMA_COLOR["cyber_dragon"])
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@500;700&family=Inter:wght@400;600;800&family=Space+Grotesk:wght@600;700;800&display=swap');

:root {{
    --accent: {T_ACT['accent']};
    --accent-glow: {T_ACT['accent_glow']};
    --sub-accent: {T_ACT['sub_accent']};
    --bg: {T_ACT['bg']};
    --card: {T_ACT['card']};
    --border: {T_ACT['border']};
    --text-sub: #94a3b8;
}}

/* CORRECCIÓN DE LA PARTE DE ARRIBA (DESPEJADO DE NAVBAR) */
.block-container,
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"] > div {{
    padding-top: 5rem !important;
    padding-bottom: 3rem !important;
    max-width: 95%;
    position: relative;
    z-index: 2;
}}

/* Barra superior fija con espaciado elegante */
.top-bar-custom {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}}

/* Fondo de Filigrana / Marca de Agua Forense */
.watermark-bg {{
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.032;
    background-image: repeating-linear-gradient(45deg, #fff 0, #fff 1px, transparent 0, transparent 48px);
}}

/* Contenedor y Placa Emblema Tecnológica */
.emblema-cyber-container {{
    display: flex;
    justify-content: center;
    margin: 1.2rem auto 2.2rem auto;
    position: relative;
    max-width: 520px;
}}

.emblema-cyber {{
    position: relative;
    width: 100%;
    padding: 16px 28px;
    background: linear-gradient(135deg, rgba(15, 17, 23, 0.95), rgba(28, 22, 14, 0.95));
    border: 1px solid rgba(234, 179, 8, 0.45);
    border-radius: 14px;
    box-shadow: 0 0 30px rgba(234, 88, 12, 0.28), inset 0 0 22px rgba(234, 179, 8, 0.12);
    text-align: center;
    overflow: hidden;
    backdrop-filter: blur(18px);
}}

/* Silueta Dorada Láser que Barre Continuamente */
.emblema-cyber .scan-laser {{
    position: absolute;
    top: 0;
    left: -120%;
    width: 65%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(234, 179, 8, 0.2), rgba(249, 115, 22, 0.5), rgba(234, 179, 8, 0.2), transparent);
    transform: skewX(-25deg);
    animation: barridoLaser 3.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    pointer-events: none;
}}

@keyframes barridoLaser {{
    0% {{ left: -120%; }}
    50%, 100% {{ left: 160%; }}
}}

/* Brackets esquineros de alta tecnología */
.emblema-bracket {{
    position: absolute;
    width: 10px;
    height: 10px;
    border-color: #ea580c;
    border-style: solid;
    pointer-events: none;
}}
.emblema-bracket.top-left {{ top: 4px; left: 4px; border-width: 2px 0 0 2px; }}
.emblema-bracket.top-right {{ top: 4px; right: 4px; border-width: 2px 2px 0 0; }}
.emblema-bracket.btm-left {{ bottom: 4px; left: 4px; border-width: 0 0 2px 2px; }}
.emblema-bracket.btm-right {{ bottom: 4px; right: 4px; border-width: 0 2px 2px 0; }}

/* Letras Doradas Cambiantes con Reflejo Líquido */
.emblema-texto {{
    font-family: 'Teko', sans-serif;
    font-size: clamp(2rem, 4vw, 2.7rem);
    font-weight: 700;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    line-height: 1;
    margin: 0;
    background: linear-gradient(90deg, #bf953f, #fcf6ba, #ea580c, #fbf5b7, #aa771c, #f97316, #bf953f);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: brilloOro 5s linear infinite;
    filter: drop-shadow(0 2px 10px rgba(234, 88, 12, 0.55));
}}

@keyframes brilloOro {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.emblema-sub {{
    font-family: 'Space Grotesk', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: #cbd5e1;
    text-transform: uppercase;
    margin-top: 6px;
    opacity: 0.9;
}}

/* Glassmorphism 3D */
.card-custom {{
    background: var(--card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 16px 40px rgba(0,0,0,0.65);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}}
.card-custom:hover {{
    border-color: rgba(234, 88, 12, 0.4);
    box-shadow: 0 20px 48px rgba(0,0,0,0.8), 0 0 25px rgba(234, 88, 12, 0.15);
}}

/* Contenedores de Formulario Nativos Blindados (Streamlit st.container border=True) */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
    background: var(--card) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 2rem !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.65) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}}
[data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
    border-color: rgba(234, 88, 12, 0.45) !important;
    box-shadow: 0 20px 48px rgba(0,0,0,0.8), 0 0 25px rgba(234, 88, 12, 0.15) !important;
}}

/* Panel de Advertencia Legal y Protocolo de Seguridad (Opción 3) */
.panel-advertencia-forense {{
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.95), rgba(12, 14, 18, 0.95));
    border: 1px solid rgba(234, 88, 12, 0.38);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 0 auto 1.5rem auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 16px rgba(234, 88, 12, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
}}

.panel-advertencia-forense::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(234, 179, 8, 0.6), transparent);
}}

.advertencia-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}}

.advertencia-tag-box {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.live-dot {{
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px #10b981;
    animation: livePulse 2s infinite ease-in-out;
}}

@keyframes livePulse {{
    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
    70% {{ transform: scale(1.2); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
}}

.advertencia-tag {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #cbd5e1;
    text-transform: uppercase;
}}

.advertencia-status {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: #10b981;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
}}

.advertencia-titulo {{
    font-family: 'Teko', sans-serif;
    font-size: 1.45rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #f8fafc;
    text-transform: uppercase;
    margin: 0 0 6px 0;
    line-height: 1.1;
}}

.advertencia-cuerpo {{
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    line-height: 1.55;
    color: #94a3b8;
    margin: 0 0 10px 0;
}}

.advertencia-cuerpo strong {{
    color: #f1f5f9;
}}

.advertencia-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Space Grotesk', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--accent);
    padding-top: 8px;
    border-top: 1px dashed rgba(255, 255, 255, 0.08);
    text-transform: uppercase;
}}


/* Botones Neón con Efecto Ripple */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, var(--accent), var(--accent-glow)) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 4px 18px rgba(234, 88, 12, 0.4) !important;
    transition: all 0.25s ease-out !important;
}}
div.stButton > button:first-child:hover {{
    box-shadow: 0 6px 25px rgba(234, 88, 12, 0.7) !important;
    transform: translateY(-2px) !important;
}}

.btn-secondary > div > button:first-child {{
    background: rgba(255,255,255,0.04) !important;
    color: #94a3b8 !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}}
.btn-secondary > div > button:first-child:hover {{
    border-color: #f8fafc !important;
    color: white !important;
    transform: none !important;
}}

/* Inputs */
.stTextInput > div > div > input {{
    background-color: #0c0f14 !important;
    color: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}}

.text-orange {{ color: var(--accent); }}
.font-teko {{ font-family: 'Teko', sans-serif; text-transform: uppercase; }}
.landing-title {{ font-family: 'Teko', sans-serif; font-size: clamp(3rem, 6.2vw, 5.2rem); font-weight: 700; line-height: 1.05; text-transform: uppercase; text-align: center; margin-bottom: 1rem; }}

/* Anillos Holográficos */
.anillo {{ width: 120px; height: 120px; margin: 0 auto; border-radius: 50%; position: relative; display: grid; place-items: center; }}
.anillo::before {{ content: ""; position: absolute; inset: 0; border-radius: 50%; padding: 3px; background: conic-gradient(from 0deg, transparent, var(--accent), var(--sub-accent), transparent 60%, var(--accent)); -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; animation: gira 4s linear infinite; }}
@keyframes gira {{ to {{ transform: rotate(360deg); }} }}

/* ================================================================== */
/* 🌌 MEJORA 1: FONDO AURORA BOREALIS ANIMADA (GLOBAL)                */
/* ================================================================== */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background: var(--bg) !important;
    position: relative;
}}
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background:
        radial-gradient(ellipse 90% 60% at 15% 15%, rgba(234, 88, 12, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse 70% 50% at 85% 85%, rgba(0, 210, 255, 0.09) 0%, transparent 55%),
        radial-gradient(ellipse 80% 60% at 50% 10%, rgba(234, 179, 8, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 45% at 50% 90%, rgba(168, 85, 247, 0.06) 0%, transparent 50%);
    animation: auroraShift 14s ease-in-out infinite alternate;
}}
@keyframes auroraShift {{
    0% {{ opacity: 0.7; filter: hue-rotate(0deg) scale(1); }}
    50% {{ opacity: 1; filter: hue-rotate(18deg) scale(1.03); }}
    100% {{ opacity: 0.8; filter: hue-rotate(-15deg) scale(0.98); }}
}}

/* ================================================================== */
/* 📟 MEJORA 2: LÍNEAS DE ESCÁNER VERTICALES MATRIX (GLOBAL)          */
/* ================================================================== */
.stApp::after {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(234, 88, 12, 0.025) 2px,
        rgba(234, 88, 12, 0.025) 4px
    );
    animation: scanDrift 10s linear infinite;
}}
@keyframes scanDrift {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(8px); }}
}}

/* ================================================================== */
/* 💎 MEJORA 3: BORDES ANIMADOS GRADIENTE CUÁNTICO EN TARJETAS        */
/* ================================================================== */
.card-custom, .panel {{
    position: relative;
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s ease, border-color 0.35s ease !important;
}}
.card-custom:hover, .panel:hover {{
    transform: translateY(-3px);
    border-color: rgba(234, 88, 12, 0.5) !important;
    box-shadow: 0 20px 48px rgba(0,0,0,0.8), 0 0 30px rgba(234, 88, 12, 0.22) !important;
}}
.card-custom::before, .panel::before {{
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg,
        var(--accent), transparent 35%,
        var(--sub-accent), transparent 60%,
        var(--accent-glow), transparent 85%,
        var(--accent));
    background-size: 400% 400%;
    animation: borderGlow 7s ease infinite;
    z-index: -1;
    border-radius: 15px;
    opacity: 0;
    transition: opacity 0.4s ease;
}}
.card-custom:hover::before, .panel:hover::before {{
    opacity: 1;
}}
@keyframes borderGlow {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* ================================================================== */
/* ⚡ MEJORA 4: BOTONES CON ONDA CUÁNTICA Y RESPLANDOR               */
/* ================================================================== */
div.stButton > button:first-child {{
    position: relative !important;
    overflow: hidden !important;
    background: linear-gradient(135deg, var(--accent), var(--accent-glow)) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 4px 18px rgba(234, 88, 12, 0.4) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}
div.stButton > button:first-child:hover {{
    box-shadow: 0 8px 32px rgba(234, 88, 12, 0.75), 0 0 65px rgba(234, 88, 12, 0.3) !important;
    transform: translateY(-3px) scale(1.02) !important;
}}
div.stButton > button:first-child:active {{
    transform: translateY(0) scale(0.98) !important;
    box-shadow: 0 0 35px rgba(234, 88, 12, 0.95), inset 0 0 15px rgba(255, 255, 255, 0.4) !important;
}}

/* ================================================================== */
/* 💡 MEJORA 5: INPUTS CON RESPLANDOR ELÉCTRICO AL FOCUS              */
/* ================================================================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {{
    background-color: #0c0f14 !important;
    color: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent), 0 0 25px rgba(234, 88, 12, 0.5), inset 0 0 8px rgba(234, 88, 12, 0.15) !important;
    outline: none !important;
}}

/* ================================================================== */
/* 📑 MEJORA 6: TABS CON ILUMINACIÓN NEÓN                             */
/* ================================================================== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px !important;
    background: rgba(15, 17, 21, 0.9) !important;
    border-radius: 12px !important;
    padding: 6px !important;
    border: 1px solid var(--border) !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.5) !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 700 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 8px 16px !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: #f8fafc !important;
    background: rgba(255, 255, 255, 0.05) !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, var(--accent), var(--accent-glow)) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(234, 88, 12, 0.6), 0 0 12px rgba(234, 88, 12, 0.35) !important;
    border-radius: 8px !important;
}}

/* ================================================================== */
/* 📜 MEJORA 7: SCROLLBAR PERSONALIZADO CYBER                         */
/* ================================================================== */
::-webkit-scrollbar {{ width: 7px; height: 7px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, var(--accent), var(--accent-glow));
    border-radius: 10px;
    box-shadow: 0 0 8px rgba(234, 88, 12, 0.4);
}}
::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(180deg, var(--accent-glow), #fbbf24);
    box-shadow: 0 0 14px rgba(234, 88, 12, 0.8);
}}

/* ================================================================== */
/* 📊 MEJORA 8: DATAFRAMES Y TABLAS BLINDADAS                         */
/* ================================================================== */
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(234, 88, 12, 0.3) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.65), 0 0 18px rgba(234, 88, 12, 0.12) !important;
    background: rgba(12, 15, 20, 0.9) !important;
    backdrop-filter: blur(12px) !important;
}}

/* ================================================================== */
/* 📂 MEJORA 9: EXPANDERS FUTURISTAS                                  */
/* ================================================================== */
[data-testid="stExpander"], .streamlit-expanderHeader {{
    background: rgba(15, 18, 24, 0.8) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
}}
[data-testid="stExpander"]:hover, .streamlit-expanderHeader:hover {{
    border-color: rgba(234, 88, 12, 0.5) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(234, 88, 12, 0.2) !important;
}}

/* Slider estilizado */
.stSlider > div > div > div > div {{
    background-color: var(--accent) !important;
}}

/* Alertas temáticas */
.stAlert {{
    border-radius: 10px !important;
    border-left: 4px solid var(--accent) !important;
}}

/* ================================================================== */
/* SAFETY NET: Asegurar visibilidad del contenido en Streamlit 1.30+  */
/* ================================================================== */
section[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.main .block-container,
.stMainBlockContainer {{
    position: relative !important;
    z-index: 2 !important;
}}
section[data-testid="stSidebar"] {{
    z-index: 3 !important;
}}
header[data-testid="stHeader"] {{
    z-index: 4 !important;
}}
/* --- NUEVAS CLASES UI VANGUARD --- */
.secure-blur {{
    filter: blur(8px) opacity(0.7);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white"><path d="M12 4.5C7 4.5 2.7 8.3 1 12c1.7 3.7 6 7.5 11 7.5s9.3-3.8 11-7.5c-1.7-3.7-6-7.5-11-7.5zm0 12c-2.5 0-4.5-2-4.5-4.5S9.5 7.5 12 7.5 16.5 9.5 16.5 12 14.5 16.5 12 16.5zm0-7.5c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3z"/></svg>') 12 12, pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    font-family: 'Space Grotesk', monospace;
    text-shadow: 0 0 10px var(--accent);
}}
.secure-blur:hover, .secure-blur:active {{
    filter: blur(0) opacity(1);
    color: var(--accent_glow) !important;
    text-shadow: 0 0 15px rgba(234,88,12,0.8);
}}

/* Radar de Auditoría */
.radar-box {{
    position: relative;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, rgba(12,15,20,0) 70%);
    border: 1px solid rgba(16,185,129,0.3);
    overflow: hidden;
    box-shadow: 0 0 15px rgba(16,185,129,0.1);
}}
.radar-sweep {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: conic-gradient(from 0deg, transparent 70%, rgba(16,185,129,0.8) 100%);
    animation: radar-spin 2s linear infinite;
    border-radius: 50%;
}}
@keyframes radar-spin {{ 100% {{ transform: rotate(360deg); }} }}

/* Honeypot invisible */
div[data-testid="stTextInput"]:has(input[aria-label="TrampaBot"]) {{
    opacity: 0 !important;
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
    z-index: -1;
    pointer-events: none;
}}

/* Fondo Aurora Dorada Segura (Puro CSS) */
@keyframes golden-aurora {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
body, .stApp {{
    background: radial-gradient(circle at top left, rgba(212, 175, 55, 0.05), transparent 40%),
                radial-gradient(circle at bottom right, rgba(212, 175, 55, 0.04), transparent 40%),
                var(--bg) !important;
}}
.watermark-bg::before {{
    content: '';
    position: fixed;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(234, 179, 8, 0.08) 0%, transparent 20%),
                radial-gradient(circle, rgba(251, 191, 36, 0.05) 0%, transparent 20%);
    background-size: 100vw 100vh;
    background-position: 0 0, 50vw 50vh;
    animation: golden-aurora 20s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
    opacity: 0.8;
}}

/* ================================================================== */
/* 🎚️ ESTILIZACIÓN PREMIUM DE LA BARRA SLIDER (FIDUCIA / NUBE)        */
/* ================================================================== */
div[data-testid="stSlider"] {{
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 14px 18px 16px 18px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    margin-bottom: 12px !important;
}}

div[data-testid="stSlider"] label {{
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #f8fafc !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}}

/* Carril / Pista de la barra */
div[data-testid="stSlider"] div[data-baseweb="slider"] {{
    padding: 12px 0 !important;
}}

div[data-testid="stSlider"] div[data-baseweb="slider"] > div {{
    height: 8px !important;
    border-radius: 9999px !important;
    background: rgba(39, 44, 53, 0.9) !important;
}}

/* Barra llena (progreso activo) */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {{
    background: linear-gradient(90deg, #ea580c 0%, #f97316 70%, #38bdf8 100%) !important;
    border-radius: 9999px !important;
    box-shadow: 0 0 14px rgba(234, 88, 12, 0.75) !important;
}}

/* Perilla circular moderna con resplandor neón */
div[data-testid="stSlider"] div[role="slider"] {{
    width: 22px !important;
    height: 22px !important;
    background: radial-gradient(circle, #ffffff 30%, #ea580c 100%) !important;
    border: 2px solid #ffffff !important;
    border-radius: 50% !important;
    box-shadow: 0 0 16px #ea580c, 0 2px 8px rgba(0,0,0,0.6) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    cursor: pointer !important;
}}

div[data-testid="stSlider"] div[role="slider"]:hover {{
    transform: scale(1.25) !important;
    box-shadow: 0 0 24px #ea580c, 0 0 35px rgba(234, 88, 12, 0.9) !important;
}}

/* Ocultar las cajas cuadradas feas con fondo naranja pegadas a los números */
div[data-testid="stSlider"] div[role="slider"] > div {{
    display: none !important;
}}

/* Números de los extremos (0 y 100) en formato limpio y sutil */
div[data-testid="stSlider"] [data-testid="stSliderTickBar"] > div,
div[data-testid="stSlider"] div[data-baseweb="slider"] ~ div div {{
    background: transparent !important;
    color: #94a3b8 !important;
    font-family: 'Space Grotesk', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: none !important;
}}

/* ================================================================== */
/* 📱 OPTIMIZACIÓN RESPONSIVA DEFINITIVA PARA SMARTPHONES / MÓVILES    */
/* ================================================================== */
@media (max-width: 768px) {{
    .block-container,
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    section[data-testid="stMain"] > div {{
        padding-top: 2.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        max-width: 100% !important;
    }}

    [data-testid="stTabs"] [role="tablist"] {{
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        scrollbar-width: none !important;
        gap: 6px !important;
        padding-bottom: 6px !important;
    }}

    [data-testid="stTabs"] button {{
        white-space: nowrap !important;
        padding: 0.5rem 0.9rem !important;
        font-size: 0.88rem !important;
    }}

    .card-custom, [data-testid="stVerticalBlockBorderWrapper"] > div {{
        padding: 1.1rem !important;
        border-radius: 12px !important;
    }}

    iframe {{
        width: 100% !important;
        border: none !important;
    }}
}}

</style>
<div class="watermark-bg"></div>

"""
