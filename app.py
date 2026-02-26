import streamlit as st
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="Agencia de Ventas Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    h1, h2, h3 { color: #C5A880 !important; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #C5A880; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA DE VENTAS NUEVA ILUSIÓN")
st.subheader("Simulador de Negocios Inmobiliarios")

# 2. Entrada de Datos (Lotes en Santa Rosa y Turbaco)
with st.container():
    nombre = st.text_input("Nombre del Cliente")
    ubicacion = st.selectbox("Ubicación del Lote", ["Santa Rosa, Bolívar", "Turbaco, Bolívar", "Cartagena"])
    precio = st.number_input("Precio Total ($)", min_value=0.0, step=1000000.0)
    inicial = st.number_input("Cuota Inicial ($)", min_value=0.0, step=500000.0)
    meses = st.number_input("Plazo (Meses)", min_value=1, value=36)

# 3. Cálculos
saldo = precio - inicial
cuota = saldo / meses if meses > 0 else 0

# 4. Botones Organizados (Solicitud del Usuario)
st.write("---")

# Botón Principal
if st.button("Generar estructura de negocio"):
    st.success(f"Estructura lista para {nombre}")
    st.write(f"**Ubicación:** {ubicacion}")
    st.write(f"**Saldo a Financiar:** ${saldo:,.2f}")
    st.write(f"**Cuota Mensual:** ${cuota:,.2f}")

# Fila de botones secundarios
col1, col2 = st.columns(2)

with col1:
    if st.button("Generar PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="AGENCIA DE VENTAS NUEVA ILUSIÓN", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Cliente: {nombre}", ln=True)
            pdf.cell(200, 10, txt=f"Ubicación: {ubicacion}", ln=True)
            pdf.cell(200, 10, txt=f"Cuota Mensual: ${cuota:,.2f}", ln=True)
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="📥 Descargar PDF", data=pdf_output, file_name=f"Cotizacion_{nombre}.pdf", mime='application/pdf')
        except Exception as e:
            st.error(f"Error: Asegúrate de que 'fpdf' esté en tu requirements.txt")

with col2:
    # Este es el botón de reinicio que limpia todo
    if st.button("Nuevo cálculo"):
        st.rerun()
