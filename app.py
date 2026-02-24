import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime
import io

# Configuración de Marca
COLOR_FONDO = "#0B2447"
COLOR_ACENTO = "#C5A880"

st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

# Estilo personalizado para imitar tu diseño
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_FONDO}; color: white; }}
    .stButton>button {{ background-color: {COLOR_ACENTO}; color: black; border-radius: 10px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador Pro de Estructura de Negocio")

# Formulario de Entrada
with st.form("simulador_avanzado"):
    col1, col2 = st.columns(2)
    with col1:
        proyecto = st.text_input("Proyecto / Ubicación")
        cliente = st.text_input("Nombre del Cliente")
        precio_lista = st.number_input("Precio Lista ($)", min_value=0, step=1000000)
        bono = st.number_input("Bono Especial ($)", min_value=0, step=500000)
    with col2:
        separacion = st.number_input("Valor Separación ($)", min_value=0, step=500000)
        pct_ini = st.number_input("% Cuota Inicial", min_value=1, max_value=100, value=30)
        meses_ini = st.number_input("Meses para pagar la Inicial", min_value=0, value=12)
        meses_lote = st.number_input("Meses Financiación Lote", min_value=0, value=36)
    
    dia_fijo = st.slider("Día de Pago Fijo", 1, 30, 10)
    asesor = st.selectbox("Asesor Comercial", ["LUIS FERNANDO ORTEGA ARTEAGA", "YERLIS PAREDES BRONDY"])
    
    boton = st.form_submit_button("CALCULAR PLAN DE NEGOCIO")

if boton:
    # Cálculos Lógicos
    base_calculo = precio_lista - bono
    val_ini_total = base_calculo * (pct_ini / 100)
    restante_inicial = val_ini_total - separacion
    saldo_final_lote = base_calculo - val_ini_total
    
    cuota_ini_mes = restante_inicial / meses_ini if meses_ini > 0 else 0
    cuota_lote_mes = saldo_final_lote / meses_lote if meses_lote > 0 else 0

    # Resumen Visual
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Base de Cálculo", f"${base_calculo:,.0f}")
    c2.metric("Saldo Inicial", f"${restante_inicial:,.0f}")
    c3.metric("Saldo Lote", f"${saldo_final_lote:,.0f}")

    # Generación de la Tabla
    hoy = datetime.date.today()
    datos_tabla = []
    
    # Cuotas Iniciales
    for i in range(1, meses_ini + 1):
        fecha = (hoy + datetime.timedelta(days=30*i)).replace(day=dia_fijo)
        datos_tabla.append({"Cuota": f"Inicial {i}", "Fecha": fecha.strftime("%d/%m/%Y"), "Monto": f"${cuota_ini_mes:,.0f}"})
    
    # Cuotas de Lote
    for j in range(1, meses_lote + 1):
        fecha = (hoy + datetime.timedelta(days=30*(meses_ini + j))).replace(day=dia_fijo)
        datos_tabla.append({"Cuota": f"Lote {j}", "Fecha": fecha.strftime("%d/%m/%Y"), "Monto": f"${cuota_lote_mes:,.0f}"})

    df = pd.DataFrame(datos_tabla)
    st.table(df)

    # Función PDF (Simplificada para Web)
    def generar_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, f"COTIZACIÓN: {proyecto}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Cliente: {cliente}")
        c.drawString(50, 715, f"Precio Lista: ${precio_lista:,.0f}")
        c.drawString(50, 700, f"Bono: -${bono:,.0f}")
        c.drawString(50, 685, f"Saldo Lote: ${saldo_final_lote:,.0f}")
        c.drawString(50, 650, f"Asesor: {asesor}")
        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    st.download_button("📥 DESCARGAR PDF PROFESIONAL", generar_pdf(), f"Cotizacion_{cliente}.pdf", "application/pdf")
