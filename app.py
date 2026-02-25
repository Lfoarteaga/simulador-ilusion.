import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Estilo de Marca (Contraste y Visibilidad)
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Forzar botones de radio (Si/No) en blanco */
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    
    /* Estilo de la Tabla: Letras blancas y sin bordes oscuros */
    .stTable { color: white !important; width: 100% !important; }
    .stTable td { color: white !important; font-size: 16px !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; }

    /* Métricas Doradas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 30px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")

# 2. Formulario de Captura Unificado
with st.form(key="formulario_final_ilusion"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
        proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="f_proy")

        st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
        cliente = st.text_input("  ", placeholder="Nombre del comprador", key="f_cli")

        st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
        precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

        # Lógica de Descuento
        st.markdown('<p class="pregunta" style="color:white;">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
        aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="f_bono")
        valor_bono = 0.0
        if aplica_bono == "Si":
            st.markdown('<p class="pregunta" style="color:white;">Digite el valor del descuento ($)</p>', unsafe_allow_html=True)
            valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f")

    with col2:
        st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
        v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f")

        st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
        p_ini = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0)

        st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p>', unsafe_allow_html=True)
        m_ini = st.number_input("        ", min_value=1, value=12)

        st.markdown('<p class="pregunta">8. Meses a financiar saldo del lote</p>', unsafe_allow_html=True)
        m_lote = st.number_input("         ", min_value=1, value=36)

    st.markdown('<p class="pregunta">9. Fecha de negociacion</p>', unsafe_allow_html=True)
    f_negociacion = st.date_input("          ", value=datetime.date.today())

    # EL BOTÓN DEBE ESTAR AQUÍ D
