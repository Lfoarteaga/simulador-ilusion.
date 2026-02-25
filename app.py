import streamlit as st
import pandas as pd
import datetime

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { 
        font-weight: bold; 
        font-size: 20px; 
        color: #C5A880; 
        margin-top: 25px;
        margin-bottom: 8px;
        display: block;
    }
    div.stButton > button:first-child {
        background-color: #C5A880;
        color: #0B2447;
        font-weight: bold;
        width: 100%;
        height: 3em;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador de Estructura de Negocio Profesional")

# 2. Formulario con Pregunta Arriba y Cuadro Abajo
with st.form("simulador_v3"):
    
    st.markdown('<p class="pregunta">1. ¿Cuál es el nombre del proyecto?</p>', unsafe_allow_html=True)
    proyecto = st.text_input("", placeholder="Escribe el nombre aquí...", key="in1")

    st.markdown('<p class="pregunta">2. ¿Cuál es el precio de lista del lote?</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("", min_value=0.0, step=1000000.0, format="%.0f", key="in2")

    st.markdown('<p class="pregunta">3. ¿Aplica bono de descuento especial hoy?</p>', unsafe_allow_html=True)
    tiene_bono = st.radio("", ["No", "Sí"], horizontal=True, key="in3")
    
    valor_bono = 0.0
    if tiene_bono == "Sí":
        st.markdown('<p class="pregunta">¿De cuánto es el valor del bono?</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("", min_value=0.0, step=100000.0, format="%.0f", key="in4")

    st.markdown('<p class="pregunta">4. ¿Cuánto es el valor a separar?</p>', unsafe_allow_html=True)
    valor_separacion = st.number_input("", min_value=0.0, step=100000.0, format="%.0f", key="in5")

    st.markdown('<p class="pregunta">5. Porcentaje de cuota inicial (ej. 30)</p>', unsafe_allow_html=True)
    pct_inicial = st.number_input("", min_value=0.0, max_value=100.0, value=30.0, key="in6")

    st.markdown('<p class="pregunta">6. ¿En cuántos meses pagará la diferencia de la inicial?</p>', unsafe_allow_html=True)
    meses_inicial = st.number_input("", min_value=1, value=12, key="in7")

    st.markdown('<p class="pregunta">7. ¿En cuántas cuotas pagará el saldo del lote?</p>', unsafe_allow_html=True)
    num_cuotas_lote = st.number_input("", min_value=1, value=36, key="in8")

    st.markdown("<br>", unsafe_allow_html=True)
    boton = st.form_submit_button("GENERAR ESTRUCTURA DE NEGOCIO")

# 3. Lógica de Cálculos (Basada en tu estructura exacta)
if boton:
    precio_tras_bono = precio_lista - valor_bono
    precio_base_calculo = precio_tras_bono
    
    valor_inicial_total = precio_base_calculo * (pct_inicial / 100)
    diferencia_inicial = valor_inicial_total - valor_separacion
    
    cuota_inicial_mes = diferencia_inicial / meses_inicial if diferencia_inicial > 0 else 0
    saldo_lote = precio_base_calculo - valor_inicial_total
    cuota_lote_mes = saldo_lote / num_cuotas_lote

    # 4. Presentación de Resultados
    st.divider()
    st.header(f"📍 {proyecto.upper()}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Base de Cálculo", f"${precio_base_calculo:,.0f}")
    c2.metric("Inicial Total", f"${valor_inicial_total:,.0f}")
    c3.metric("Saldo Lote", f"${saldo_lote:,.0f}")

    # 5. Cronograma de Pagos
    st.write("### 📅 Cronograma de Pagos")
    fecha_hoy = datetime.datetime.now()
    plan_pagos = []

    # FASE 1: Inicial
    if diferencia_inicial > 0:
        for i in range(1, meses_inicial + 1):
            vencimiento = fecha_hoy + datetime.timedelta(days=30 * i)
            plan_pagos.append({
                "Fase": "1. Cuota Inicial",
                "Vencimiento": vencimiento.strftime('%d/%m/%Y'),
                "Valor": f"${cuota_inicial_mes:,.0f}"
            })

    # FASE 2: Lote
    for j in range(1, num_cuotas_lote + 1):
        vencimiento = fecha_hoy + datetime.timedelta(days=30 * (meses_inicial + j))
        plan_pagos.append({
            "Fase": "2. Saldo Lote",
            "Vencimiento": vencimiento.strftime('%d/%m/%Y'),
            "Valor": f"${cuota_lote_mes:,.0f}"
        })

    st.table(pd.DataFrame(plan_pagos))
    st.caption("Cotización generada profesionalmente por Luis Fer.")
