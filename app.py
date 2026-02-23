import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def formato_co(v):
    return "$" + format(v, ",.0f").replace(",", ".")

st.title("AGENCIA NUEVA ILUSIÓN")

# Entradas para Luis Fer
proy = st.text_input("Proyecto", "AMARU")
cli = st.text_input("Cliente")
pre = st.number_input("Precio Lista", 0.0)
bon = st.number_input("Bono Especial", 0.0)
sep = st.number_input("Separación", 0.0)
pct = st.number_input("% Inicial", 30)

# Cálculos automáticos
base = pre - bon
v_ini = base * (pct / 10) # Ajuste para el simulador
r_ini = v_ini - sep
s_lot = base - v_ini

if st.button("GENERAR COTIZACIÓN"):
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=letter)
    p.drawString(100, 750, f"PROYECTO: {proy}")
    p.drawString(100, 730, f"CLIENTE: {cli}")
    p.drawString(100, 710, f"PRECIO LISTA: {formato_co(pre)}")
    p.drawString(100, 690, f"BASE CÁLCULO: {formato_co(base)}")
    p.drawString(100, 670, f"TOTAL INICIAL: {formato_co(v_ini)}")
    p.drawString(100, 650, f"SALDO LOTE: {formato_co(s_lot)}")
    p.save()
    st.download_button("📥 DESCARGAR PDF", buf.getvalue(), f"Cotizacion_{cli}.pdf", "application/pdf")
