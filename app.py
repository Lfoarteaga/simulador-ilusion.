import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Configuración de Identidad y Estilo (Contraste Máximo)
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Forzar botones de radio (Si/No) en blanco */
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] { color: white !important; }

    /* Estilo de la Tabla: Todo visible y en blanco */
    .stTable { background-color: transparent !important; color: white !important; width: 100% !important; }
    .stTable td { color: white !important; font-size: 16px !important; border-bottom: 1px solid #19376D !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; font-size: 17px !important; }

    /* Métricas Doradas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")
st.subheader("Simulador Pro de Estructura de Negocio")

# 2. Captura de Datos con Lógica de Negocio
with st.form(key="form_cierre_ilusion_final"):
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
        proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="i_proy")

        st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
        cliente = st.text_input("  ", placeholder="Nombre del comprador", key="i_cli")

        st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
        precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

        # Bono Especial con botones Si/No en Blanco
        st.markdown('<p class="pregunta">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
        aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="i_bono")
        valor_bono = 0.0
        if aplica_bono == "Si":
            st.markdown('<p class="pregunta">Indique el valor del descuento ($)</p>', unsafe_allow_html=True)
            valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f")

    with col_b:
        st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
        v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f")

        st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
        p
