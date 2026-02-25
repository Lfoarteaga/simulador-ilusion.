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
    
    /* Forzar botones de radio (Si/No) y textos en color blanco */
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    
    /* Estilo de la Tabla: Texto blanco y sin números laterales */
    .stTable { color: white !important; width: 100% !important; background-color: transparent !important; }
    .stTable td { color: white !important; font-size: 16px !important; border-bottom: 1px solid #19376D !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; font-size: 17px !important; }

    /* Métricas Doradas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 30px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")

# 2. Formulario de Captura (Todo dentro del bloque 'with' para evitar errores)
with st.form(key="form_final_ilusion_v11"):
    
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="in_p")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="in_c")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

    # Lógica de Descuento Especial
    st.markdown('<p class="pregunta" style="color:white;">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="in_b")
    
    valor_bono = 0.0
    if aplica_bono == "Si":
        st.markdown('<p class="pregunta" style="color:white;">Digite el valor del descuento ($)</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="in_vb")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">
