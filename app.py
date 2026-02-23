import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")
st.title("🏡 Agencia de Ventas Nueva Ilusión")
st.subheader("Simulador Pro: Turbaco y Santa Rosa")

with st.form("simulador"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nombre del Cliente")
        proyecto = st.selectbox("Proyecto", ["Turbaco", "Santa Rosa", "Cartagena"])
        precio_total = st.number_input("Precio Total ($)", min_value=0, step=1000000)
    with col2:
        cuota_inicial = st.number_input("Cuota Inicial / Bono ($)", min_value=0, step=500000)
        num_cuotas = st.number_input("Meses de plazo", min_value=1, max_value=60, value=12)
    boton = st.form_submit_button("Generar Plan de Pagos")

if boton:
    saldo = precio_total - cuota_inicial
    valor_cuota = saldo / num_cuotas
    
    st.divider()
    st.write(f"### Plan de pagos para: {cliente}")
    
    # Crear la tabla de amortización
    datos_tabla = []
    saldo_actual = saldo
    for i in range(1, num_cuotas + 1):
        saldo_actual -= valor_cuota
        datos_tabla.append({
            "Mes": i,
            "Cuota": f"${valor_cuota:,.0f}",
            "Saldo Restante": f"${max(0, saldo_actual):,.0f}"
        })
    
    df = pd.DataFrame(datos_tabla)
    st.table(df) # Muestra la tabla en la pantalla

    def generar_pdf(nombre, loc, total, inicial, saldo_fin, meses, mensualidad):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 750, "COTIZACIÓN OFICIAL - AGENCIA NUEVA ILUSIÓN")
        p.setFont("Helvetica", 11)
        p.drawString(100, 720, f"Cliente: {nombre}")
        p.drawString(100, 705, f"Ubicación: {loc}")
        p.drawString(100, 690, f"Precio Total: ${total:,.0f}")
        p.drawString(100, 675, f"Cuota Inicial: ${inicial:,.0f}")
        p.drawString(100, 660, f"Saldo a Financiar: ${saldo_fin:,.0f}")
        p.drawString(100, 645, f"Cuotas: {meses} de ${mensualidad:,.0f}")
        p.drawString(100, 600, "Firma: Luis Fernando Ortega Arteaga")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    pdf = generar_pdf(cliente, proyecto, precio_total, cuota_inicial, saldo, num_cuotas, valor_cuota)
    st.download_button("📥 Descargar PDF para el Cliente", pdf, f"Plan_{cliente}.pdf", "application/pdf")

