import streamlit as st
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo de la Agencia
st.set_page_config(page_title="Agencia de Ventas Nueva Ilusión", page_icon="🏡", layout="centered")

# Estilo visual: Fondo azul oscuro y acentos dorados
st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    h1, h2, h3 { color: #C5A880 !important; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #C5A880; color: white; font-weight: bold; }
    label { font-size: 18px !important; color: #C5A880 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA DE VENTAS NUEVA ILUSIÓN")
st.subheader("Simulador Inmobiliario Profesional")

# 2. Formulario de Entrada de Datos
with st.form("simulador_form"):
    nombre_cliente = st.text_input("Nombre del Cliente")
    # Ubicaciones clave de tu operación
    ubicacion = st.selectbox("Ubicación del Proyecto", ["Santa Rosa, Bolívar", "Turbaco, Bolívar", "Cartagena"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        precio_total = st.number_input("Precio del Lote ($)", min_value=0.0, step=1000000.0)
        cuota_inicial = st.number_input("Cuota Inicial ($)", min_value=0.0, step=1000000.0)
    
    with col_b:
        plazo_meses = st.number_input("Plazo a financiar (meses)", min_value=1, value=36)
        tasa_interes = st.number_input("Tasa mensual (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
    
    # Botón principal dentro del formulario
    btn_estructura = st.form_submit_button("Generar estructura de negocio")

# 3. Lógica de Cálculo
saldo_financiar = precio_total - cuota_inicial

# Fórmula financiera para la cuota mensual amortizada
if tasa_interes > 0:
    i = tasa_interes / 100
    cuota_mensual = saldo_financiar * ( (i * (1 + i)**plazo_meses) / ((1 + i)**plazo_meses - 1) )
else:
    cuota_mensual = saldo_financiar / plazo_meses

# 4. Visualización de Resultados
if btn_estructura:
    st.write("---")
    st.markdown(f"### Resumen para: {nombre_cliente}")
    st.success(f"Estructura calculada correctamente para {ubicacion}")
    
    c1, c2 = st.columns(2)
    c1.metric("Saldo a Financiar", f"${saldo_financiar:,.0f}")
    c2.metric("Cuota Mensual", f"${cuota_mensual:,.0f}")

# 5. Fila de Botones Adicionales (Solicitud del Usuario)
st.write("---")
col_pdf, col_nuevo = st.columns(2)

with col_pdf:
    if st.button("Generar PDF"):
        if nombre_cliente == "":
            st.error("Por favor, ingresa el nombre del cliente primero.")
        else:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="AGENCIA DE VENTAS NUEVA ILUSIÓN", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                pdf.ln(10)
                pdf.cell(200, 10, txt=f"COTIZACIÓN PARA: {nombre_cliente}", ln=True)
                pdf.cell(200, 10, txt=f"Ubicación: {ubicacion}", ln=True)
                pdf.cell(200, 10, txt=f"Fecha: {datetime.date.today()}", ln=True)
                pdf.ln(5)
                pdf.cell(200, 10, txt=f"Precio Total: ${precio_total:,.0f}", ln=True)
                pdf.cell(200, 10, txt=f"Cuota Inicial: ${cuota_inicial:,.0f}", ln=True)
                pdf.cell(200, 10, txt=f"Saldo a Financiar: ${saldo_financiar:,.0f}", ln=True)
                pdf.cell(200, 10, txt=f"Plazo: {plazo_meses} meses", ln=True)
                pdf.cell(200, 10, txt=f"Cuota Mensual: ${cuota_mensual:,.0f}", ln=True)
                
                # Generación del archivo para descarga
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.download_button(label="📥 Descargar Cotización", data=pdf_output, 
                                 file_name=f"Cotizacion_{nombre_cliente}.pdf", mime='application/pdf')
            except Exception as e:
                st.error(f"Error: Asegúrate de que 'fpdf' esté en requirements.txt")

with col_nuevo:
    # Este botón limpia todo y reinicia la aplicación
    if st.button("Borrar"):
        st.rerun()
