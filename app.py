import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Configuración de Marca y Diseño Centrado (Compacto)
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Forzar botones de radio (Si/No) en color blanco */
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    
    /* Estilo de la Tabla: Letras blancas claras y sin números laterales */
    .stTable { color: white !important; width: 100% !important; background-color: transparent !important; }
    .stTable td { color: white !important; font-size: 16px !important; border-bottom: 1px solid #19376D !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; font-size: 17px !important; }

    /* Métricas Doradas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")

# 2. Formulario Unificado (El botón DEBE estar dentro del bloque 'with')
with st.form(key="form_ilusion_final_definitivo"):
    
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="k_proy")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="k_cli")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f", key="k_precio")

    # Lógica de Descuento (Bono) solicitada
    st.markdown('<p class="pregunta" style="color:white;">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="k_radio")
    
    valor_bono = 0.0
    if aplica_bono == "Si":
        st.markdown('<p class="pregunta" style="color:white;">Digite el valor del descuento ($)</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="k_val_bono")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_sep = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f", key="k_sep")

    st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
    p_ini = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0, key="k_pct")

    st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p>', unsafe_allow_html=True)
    m_ini = st.number_input("        ", min_value=1, value=12, key="k_m_ini")

    st.markdown('<p class="pregunta">8. Meses a financiar saldo del lote</p>', unsafe_allow_html=True)
    m_lote = st.number_input("         ", min_value=1, value=36, key="k_m_lote")

    st.markdown('<p class="pregunta">9. Fecha de negociacion</p>', unsafe_allow_html=True)
    f_negociacion = st.date_input("          ", value=datetime.date.today(), key="k_fecha")

    # BOTÓN DENTRO DEL FORMULARIO (Elimina el error rojo)
    btn_ejecutar = st.form_submit_button(label="GENERAR ESTRUCTURA DE NEGOCIO")

# 3. Presentación de Resultados y Cronograma
if btn_ejecutar:
    base_calculo = precio_lista - valor_bono
    v_cuota_inicial_total = base_calculo * (p_ini / 100)
    saldo_cuota_inicial = v_cuota_inicial_total - v_sep
    valor_financiado_lote = base_calculo - v_cuota_inicial_total
    
    cuota_mensual_ini = saldo_cuota_inicial / m_ini if saldo_cuota_inicial > 0 else 0
    cuota_mensual_lote = valor_financiado_lote / m_lote

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    
    # Métricas con los nombres solicitados
    c1, c2 = st.columns(2)
    with c1:
        st.metric("VALOR CUOTA INICIAL", f"${v_cuota_inicial_total:,.0f}")
        st.metric("SALDO CUOTA INICIAL", f"${max(0, saldo_cuota_inicial):,.0f}")
    with c2:
        st.metric("CUOTA MENSUAL INICIAL", f"${cuota_mensual_ini:,.0f}")
        st.metric("VALOR FINANCIADO LOTE", f"${valor_financiado_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma de Pago Detallado (Letras en Blanco)")
    
    plan_pagos = []
    dia_fijo = f_negociacion.day

    def calcular_fecha(meses_futuros):
        mes_p = (f_negociacion.month + meses_futuros - 1) % 12 + 1
        anio_p = f_negociacion.year + (f_negociacion.month + meses_futuros - 1) // 12
        ult_dia = calendar.monthrange(anio_p, mes_p)[1]
        return datetime.date(anio_p, mes_p, min(dia_fijo, ult_dia)).strftime('%d/%m/%Y')

    # FASE 1: Cuotas de Pago Inicial
    if saldo_cuota_inicial > 0:
        for i in range(1, int(m_ini) + 1):
            plan_pagos.append({"Etapa": f"Cuota {i} de pago inicial", "Fecha": calcular_fecha(i), "Valor": f"${cuota_mensual_ini:,.0f}"})
    
    # FASE 2: Cuotas del Lote
    for j in range(1, int(m_lote) + 1):
        plan_pagos.append({"Etapa": f"Cuota {j} del lote", "Fecha": calcular_fecha(int(m_ini) + j), "Valor": f"${cuota_mensual_lote:,.0f}"})

    # Tabla sin números laterales (index) y texto blanco
    st.table(pd.DataFrame(plan_pagos))
    st.caption("Plan de pagos generado para la AGENCIA DE VENTAS NUEVA ILUSION.")
