import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Configuración de Identidad y Estilo Visual
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Estilo de los números grandes (Métricas) */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    
    /* Estilo de la tabla para quitar el índice y mejorar visibilidad */
    .stDataFrame { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")
st.subheader("Simulador Pro de Estructura de Negocio")

# 2. Captura de Datos con Lógica Condicional y Fecha Digitada
with st.form(key="form_ilusion_v7"):
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="f_proy")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="f_cliente")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

    # Lógica de Descuento con botones Si/No
    st.markdown('<p class="pregunta">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    aplica_descuento = st.radio("    ", ["No", "Si"], horizontal=True, key="f_radio")
    
    valor_descuento = 0.0
    if aplica_descuento == "Si":
        st.markdown('<p class="pregunta">Indique el valor del descuento ($)</p>', unsafe_allow_html=True)
        valor_descuento = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_separacion = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
    p_inicial = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0)

    st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p>', unsafe_allow_html=True)
    m_ini_fin = st.number_input("        ", min_value=1, value=12)

    st.markdown('<p class="pregunta">8. Meses a financiar saldo del lote</p>', unsafe_allow_html=True)
    m_lote_fin = st.number_input("         ", min_value=1, value=36)

    # Fecha digitada por el usuario
    st.markdown('<p class="pregunta">9. Fecha de la primera cuota</p>', unsafe_allow_html=True)
    fecha_inicio = st.date_input("          ", value=datetime.date.today())

    btn_calc = st.form_submit_button(label="GENERAR ESTRUCTURA DE NEGOCIO")

# 3. Lógica de Negocio y Presentación de Resultados
if btn_calc:
    precio_base = precio_lista - valor_descuento
    v_cuota_inicial = precio_base * (p_inicial / 100)
    saldo_cuota_inicial = v_cuota_inicial - v_separacion
    valor_financiado_lote = precio_base - v_cuota_inicial

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    st.markdown(f"**Cliente:** {cliente.upper()}")

    # Métricas con los nombres solicitados
    c1, c2, c3 = st.columns(3)
    c1.metric("VALOR CUOTA INICIAL", f"${v_cuota_inicial:,.0f}")
    c2.metric("SALDO CUOTA INICIAL", f"${max(0, saldo_cuota_inicial):,.0f}")
    c3.metric("VALOR FINANCIADO LOTE", f"${valor_financiado_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma de Pagos Detallado")
    
    plan = []
    dia_fijo = fecha_inicio.day

    def calcular_fecha_pago(meses_futuros):
        mes = (fecha_inicio.month + meses_futuros - 1) % 12 + 1
        anio = fecha_inicio.year + (fecha_inicio.month + meses_futuros - 1) // 12
        ultimo_dia = calendar.monthrange(anio, mes)[1]
        dia_final = min(dia_fijo, ultimo_dia)
        return datetime.date(anio, mes, dia_final).strftime('%d/%m/%Y')

    # FASE 1: Cuotas de Pago Inicial
    if saldo_cuota_inicial > 0:
        c_ini_valor = saldo_cuota_inicial / m_ini_fin
        for i in range(1, int(m_ini_fin) + 1):
            plan.append({
                "Etapa": f"Cuota {i} de pago inicial", 
                "Fecha": calcular_fecha_pago(i-1), 
                "Valor": f"${c_ini_valor:,.0f}"
            })

    # FASE 2: Cuotas del Lote
    c_lote_valor = valor_financiado_lote / m_lote_fin
    for j in range(1, int(m_lote_fin) + 1):
        plan.append({
            "Etapa": f"Cuota {j} del lote", 
            "Fecha": calcular_fecha_pago(int(m_ini_fin) + j - 1), 
                "Valor": f"${c_lote_valor:,.0f}"
        })

    # Mostrar tabla sin el consecutivo (índice)
    st.dataframe(pd.DataFrame(plan), hide_index=True, use_container_width=True)
