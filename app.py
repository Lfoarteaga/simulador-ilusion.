import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def formato_co(v):
    return "$" + format(v, ",.0f").replace(",", ".")

st.title("AGENCIA NUEVA ILUSIÓN")

# Entradas simples
proy = st.text_input("Proyecto", "AMARU")
cli = st.text_input("Cliente")
pre = st.number_input("Precio Lista", 0.0)
bon = st.number_input("Bono", 0.0)
sep = st.number_input("Separación", 0.0)
pct = st.number_input("% Inicial", 30)

# Cálculos
base = pre - bon
v_ini = base * (pct / 100)
r_ini = v_ini - sep
s_lot = base - v_ini

if st.button("GENERAR REPORTE"):
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=letter)
    p.drawString(100, 750, f"COTIZACION: {proy}")
    p.drawString(100, 730, f"Cliente: {cli}")
    p.drawString(100, 710, f"Precio: {formato_co(pre)}")
    p.drawString(100, 690, f"Base: {formato_co(base)}")
    p.drawString(100, 670, f"Total Inicial: {formato_co(v_ini)}")
    p.drawString(100, 650, f"Saldo Lote: {formato_co(s_lot)}")
    p.save()
    
    st.download_button("📥 DESCARGAR PDF", buf.getvalue(), f"{cli}.pdf", "application/pdf")
