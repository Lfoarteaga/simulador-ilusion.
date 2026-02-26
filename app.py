import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    h1 { color: #C5A880; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #C5A880; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")
st.subheader("Simulador de Negocios Inmobiliarios")

# 2. Entradas de datos para los lotes en Santa Rosa y Turbaco
with st.container():
    nombre_cliente = st.text_input("Nombre del Cliente")
    ubicacion = st.selectbox("Ubicación del Lote", ["Santa Rosa, Bolívar", "Turbaco, Bolívar", "Cartagena"])
    precio_total = st.number_input("Precio Total del Lote ($)", min_value=0.0, step=1000000.0)
    cuota_inicial = st.number_input("Cuota Inicial ($)", min_value=0.0, step=500000.0)
    plazo_meses = st.number_input("Plazo en meses", min_value=1, max_value=120, value=36)
    tasa_interes = st.number_input("Tasa de interés mensual (%)", min_value=0.0, max_value=5
