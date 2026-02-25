import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Configuración de Marca y Diseño Centrado (Compacto para celular)
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    .pregunta-blanca { font-weight: bold; font-size: 19px; color: #FFFFFF; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Forzar botones de radio (Si/No) en blanco */
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    
    /* Estilo de la Tabla: Letras blancas claras y sin números laterales */
    .stTable { color: white !important; width: 100% !important; background-color: transparent !important; }
    .stTable td { color: white !important; font-size: 16px !important; border-bottom: 1px solid #19376D !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; font-size: 17px !important; }

    /* Métricas Doradas resaltadas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")

# 2. Formulario Unificado (El botón DEBE estar dentro del bloque 'with')
with st.form(key="form_ilusion_final_corregido"):
    
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="k_p")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="k_c")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f", key="k_pr")

    # Lógica de Descuento (Bono) solicitada en blanco
    st.markdown('<p class="pregunta-blanca">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="k_b")
    
    valor_bono = 0.0
    if aplica_bono == "Si":
        st.markdown('<p class="pregunta-blanca">Digite el valor del descuento ($)</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="k_vb")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f", key="k_s")

    st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
    p_ini = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0, key="k_pct")

    st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p
