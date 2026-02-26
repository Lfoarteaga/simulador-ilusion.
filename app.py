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
    
    /* Forzar botones de radio (Si/No) en blanco y más grandes */
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
st.markdown('<p class="pregunta-blanca">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="k_radio_b")

valor_bono = 0.0
# El cuadro SOLO aparece si marcas "Si"
if aplica_bono == "Si":
    st.markdown('<p class="pregunta-blanca">Digite Valor del Bono</p>', unsafe_allow_html=True)
    valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="k_val_b")

st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f", key="k_s")

st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
p_ini = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0, key="k_pct")

st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p>', unsafe_allow_html=True)
m_ini = st.number_input("        ", min_value=1, value=12, key="k_mi")

st.markdown('<p class="pregunta">8. Meses a financiar saldo del lote</p>', unsafe_allow_html=True)
m_lote = st.number_input("         ", min_value=1, value=36, key="k_ml")

st.markdown('<p class="pregunta">9. Fecha de negociacion</p>', unsafe_allow_html=True)
f_negociacion = st.date_input("          ", value=datetime.date.today(), key="k_fn")

st.markdown("<br>", unsafe_allow_html=True)
btn_ejecutar = st.button("GENERAR ESTRUCTURA DE NEGOCIO")

if btn_ejecutar:
    st.session_state['mostrar_resultados'] = True

# 3. Presentación de Resultados y Cronograma
if st.session_state.get('mostrar_resultados', False):
    # LA MATEMÁTICA EXACTA QUE PEDISTE
    base = precio_lista - valor_bono
    v_cuota_inicial_total = base * (p_ini / 100)
    saldo_cuota_inicial = v_cuota_inicial_total - v_sep
    valor_financiado_lote = base - v_cuota_inicial_total
    
    c_mensual_ini = saldo_cuota_inicial / m_ini if m_ini > 0 else 0
    c_mensual_lote = valor_financiado_lote / m_lote if m_lote > 0 else 0

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("VALOR CUOTA INICIAL", f"${v_cuota_inicial_total:,.0f}")
        st.metric("SALDO CUOTA INICIAL", f"${max(0, saldo_cuota_inicial):,.0f}")
    with col_m2:
        st.metric("CUOTA MENSUAL INICIAL", f"${c_mensual_ini:,.0f}")
        st.metric("VALOR FINANCIADO LOTE", f"${valor_financiado_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma de Pago Detallado")
    
    plan_pagos = []
    dia_fijo = f_negociacion.day

    def calcular_fecha(meses_adelante):
        m_p = (f_negociacion.month + meses_adelante - 1) % 12 + 1
        a_p = f_negociacion.year + (f_negociacion.month + meses_adelante - 1) // 12
        max_d = calendar.monthrange(a_p, m_p)[1]
        return datetime.date(a_p, m_p, min(dia_fijo, max_d)).strftime('%d/%m/%Y')

    if saldo_cuota_inicial > 0:
        for i in range(1, int(m_ini) + 1):
            plan_pagos.append({"Etapa": f"Cuota {i} de pago inicial", "Fecha": calcular_fecha(i), "Valor": f"${c_mensual_ini:,.0f}"})
    
    if m_lote > 0:
        for j in range(1, int(m_lote) + 1):
            plan_pagos.append({"Etapa": f"Cuota {j} del lote", "Fecha": calcular_fecha(int(m_ini) + j), "Valor": f"${c_mensual_lote:,.0f}"})

    st.table(pd.DataFrame(plan_pagos))
