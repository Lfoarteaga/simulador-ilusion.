import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Configuración de Marca y Diseño Centrado
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    .pregunta-blanca { font-weight: bold; font-size: 19px; color: #FFFFFF; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* FORZAR BLANCO Y TAMAÑO EN LAS OPCIONES SI Y NO */
    div[role="radiogroup"] label div { color: white !important; font-size: 18px !important; }
    div[role="radiogroup"] label p { color: white !important; font-size: 18px !important; }
    
    /* Estilo de la Tabla: Letras blancas claras y sin números laterales */
    .stTable { color: white !important; width: 100% !important; background-color: transparent !important; }
    .stTable td { color: white !important; font-size: 16px !important; border-bottom: 1px solid #19376D !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; font-size: 17px !important; }

    /* Métricas Doradas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 30px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 15px !important; }
    
    /* Estilo del botón principal */
    div.stButton > button:first-child { background-color: #C5A880; color: #0B2447; font-weight: bold; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")

# 2. Captura de Datos Dinámica
st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="k_p")

st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
cliente = st.text_input("  ", placeholder="Nombre del comprador", key="k_c")

st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f", key="k_pr")

# LÓGICA DE BONO DINÁMICA
st.markdown('<p class="pregunta-blanca">4. ¿A
