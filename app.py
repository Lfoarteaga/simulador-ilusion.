import streamlit as st
import pandas as pd
import datetime
import calendar

# 1. Estilo de Marca (Visibilidad Total y Colores Corporativos)
st.set_page_config(page_title="AGENCIA DE VENTAS NUEVA ILUSION", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    .pregunta-blanca { font-weight: bold; font-size: 19px; color: #FFFFFF; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* Forzar visibilidad de métricas y tablas */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 28px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    .stDataFrame { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")
st.subheader("Estructura de Negocio Profesional")

# 2. Formulario de Captura con Lógica Condicional
with st.form(key="form_final_ilusion_v8"):
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="f_p")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="f_c")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

    # Lógica de Bono Condicional
    st.markdown('<p class="pregunta-blanca">4. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    aplica_bono = st.radio("    ", ["No", "Si"], horizontal=True, key="f_r")
    
    valor_bono = 0.0
    if aplica_bono == "Si":
        st.markdown('<p class="pregunta-blanca">Indique el valor del bono ($)</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_separacion = st.number_input("      ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
    p_inicial = st.number_input("       ", min_value=0.0, max_value=100.0, value=30.0)

    st.markdown('<p class="pregunta">7. Meses por financiar cuota inicial</p>', unsafe_allow_html=True)
    m_ini_fin = st.number_input("        ", min_value=1, value=12)

    st.markdown('<p class="pregunta">8. Meses a financiar saldo del lote</p>', unsafe_allow_html=True)
    m_lote_fin = st.number_input("         ", min_value=1, value=36)

    st.markdown('<p class="pregunta">9. Fecha de negociación</p>', unsafe_allow_html=True)
    fecha_negociacion = st.date_input("          ", value=datetime.date.today())

    btn_calc = st.form_submit_button(label="GENERAR ESTRUCTURA DE NEGOCIO")

# 3. Lógica de Negocio y Presentación de Resultados
if btn_calc:
    precio_base = precio_lista - valor_bono
    valor_cuota_inicial_total = precio_base * (p_inicial / 100)
    saldo_cuota_inicial = valor_cuota_inicial_total - v_separacion
    valor_financiado_lote = precio_base - valor_cuota_inicial_total
    
    # Cálculos de cuotas mensuales
    cuota_mensual_inicial = saldo_cuota_inicial / m_ini_fin if saldo_cuota_inicial > 0 else 0
    cuota_mensual_lote = valor_financiado_lote / m_lote_fin

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    st.markdown(f"**Cliente:** {cliente.upper()}")
    st.markdown(f"**Fecha de Negociación:** {fecha_negociacion.strftime('%d/%m/%Y')}")

    # Resumen de Cierre con las métricas solicitadas
    c1, c2 = st.columns(2)
    with c1:
        st.metric("VALOR CUOTA INICIAL", f"${valor_cuota_inicial_total:,.0f}")
        st.metric("SALDO CUOTA INICIAL", f"${max(0, saldo_cuota_inicial):,.0f}")
    with c2:
        st.metric("CUOTA MENSUAL INICIAL", f"${cuota_mensual_inicial:,.0f}")
        st.metric("VALOR FINANCIADO LOTE", f"${valor_financiado_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma de Pagos")
    
    plan = []
    dia_fijo = fecha_negociacion.day

    def calcular_fecha_pago(meses_futuros):
        mes = (fecha_negociacion.month + meses_futuros - 1) % 12 + 1
        anio = fecha_negociacion.year + (fecha_negociacion.month + meses_futuros - 1) // 12
        ultimo_dia = calendar.monthrange(anio, mes)[1]
        dia_final = min(dia_fijo, ultimo_dia)
        return datetime.date(anio, mes, dia_final).strftime('%d/%m/%Y')

    # FASE 1: Cuotas de Pago Inicial
    if saldo_cuota_inicial > 0:
        for i in range(1, int(m_ini_fin) + 1):
            plan.append({
                "Etapa": f"Cuota {i} de pago inicial", 
                "Fecha": calcular_fecha_pago(i), 
                "Valor": f"${cuota_mensual_inicial:,.0f}"
            })

    # FASE 2: Cuotas del Lote
    for j in range(1, int(m_lote_fin) + 1):
        plan.append({
            "Etapa": f"Cuota {j} del lote", 
            "Fecha": calcular_fecha_pago(int(m_ini_fin) + j), 
            "Valor": f"${cuota_mensual_lote:,.0f}"
        })

    # Reporte sin consecutivo lateral
    st.dataframe(pd.DataFrame(plan), hide_index=True, use_container_width=True)
