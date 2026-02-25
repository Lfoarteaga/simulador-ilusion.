import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime
import io

# Configuración visual de la Agencia
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 18px; color: #C5A880; margin-bottom: 5px; display: block; }
    input { border-radius: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador Pro de Estructura de Negocio")

with st.form("simulador_completo"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="pregunta">1. ¿En qué proyecto está el lote?</p>', unsafe_allow_html=True)
        proyecto = st.text_input("", placeholder="Ej. Campestre Real", key="p1")

        st.markdown('<p class="pregunta">2. ¿Nombre del Cliente?</p>', unsafe_allow_html=True)
        cliente = st.text_input("", placeholder="Nombre completo", key="p2")

        st.markdown('<p class="pregunta">3. Precio de Lista ($)</p>', unsafe_allow_html=True)
        precio_lista = st.number_input("", min_value=0.0, step=1000000.0, key="p3")

        st.markdown('<p class="pregunta">4. Bono Especial ($)</p>', unsafe_allow_html=True)
        bono = st.number_input("", min_value=0.0, step=500000.0, key="p4")

        st.markdown('<p class="pregunta">5. Valor de Separación ($)</p>', unsafe_allow_html=True)
        separacion = st.number_input("", min_value=0.0, step=500000.0, key="p5")

    with col2:
        st.markdown('<p class="pregunta">6. % de Cuota Inicial</p>', unsafe_allow_html=True)
        pct_ini = st.number_input("", min_value=1.0, max_value=100.0, value=30.0, key="p6")

        st.markdown('<p class="pregunta">7. Meses para la Inicial</p>', unsafe_allow_html=True)
        meses_ini = st.number_input("", min_value=1, value=12, key="p7")

        st.markdown('<p class="pregunta">8. Meses para el Lote</p>', unsafe_allow_html=True)
        meses_lote = st.number_input("", min_value=0, value=36, key="p8")

        st.markdown('<p class="pregunta">9. Día de Pago Fijo</p>', unsafe_allow_html=True)
        dia_fijo = st.slider("", 1, 30, 10, key="p9")

        st.markdown('<p class="pregunta">Asesor Comercial</p>', unsafe_allow_html=True)
        asesor = st.selectbox("", ["LUIS FERNANDO ORTEGA ARTEAGA", "YERLIS PAREDES BRONDY"])

    calcular = st.form_submit_button("CALCULAR ESTRUCTURA DE NEGOCIO")

if calcular:
    # Lógica de cálculo idéntica a tu código original
    base_calculo = precio_lista - bono
    val_ini_total = base_calculo * (pct_ini / 100)
    restante_inicial = val_ini_total - separation
    saldo_lote_total = base_calculo - val_ini_total
    
    cuota_ini_mes = restante_inicial / meses_ini if meses_ini > 0 else 0
    cuota_lote_mes = saldo_lote_total / meses_lote if meses_lote > 0 else 0

    st.divider()
    st.write(f"### Resumen: {proyecto}")
    st.info(f"Base: ${base_calculo:,.0f} | Saldo Inicial: ${restante_inicial:,.0f} | Saldo Lote: ${saldo_final_lote:,.0f}")

    # Generación de tabla de amortización
    datos_tabla = []
    hoy = datetime.date.today()
    
    def ajustar_fecha(n):
        mes_futuro = (hoy.month + n - 1) % 12 + 1
        anio_futuro = hoy.year + (hoy.month + n - 1) // 12
        dia = min(dia_fijo, 28) # Simplificado para estabilidad
        return f"{dia}/{mes_futuro}/{anio_futuro}"

    for i in range(1, int(meses_ini) + 1):
        datos_tabla.append({"Cuota": f"Inicial {i}", "Fecha": ajustar_fecha(i), "Valor": f"${cuota_ini_mes:,.0f}"})
    
    for j in range(1, int(meses_lote) + 1):
        datos_tabla.append({"Cuota": f"Lote {j}", "Fecha": ajustar_fecha(int(meses_ini) + j), "Valor": f"${cuota_lote_mes:,.0f}"})

    st.table(pd.DataFrame(datos_tabla))

    # Función para el PDF
    def crear_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "AGENCIA NUEVA ILUSIÓN - COTIZACIÓN")
        c.setFont("Helvetica", 11)
        c.drawString(50, 720, f"Proyecto: {proyecto}")
        c.drawString(50, 705, f"Cliente: {cliente}")
        c.drawString(50, 690, f"Precio Lista: ${precio_lista:,.0f}")
        c.drawString(50, 675, f"Asesor: {asesor}")
        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    st.download_button("📥 DESCARGAR COTIZACIÓN EN PDF", crear_pdf(), f"Plan_{cliente}.pdf", "application/pdf")
