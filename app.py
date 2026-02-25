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
    /* Forzar visibilidad de la tabla en blanco */
    .stTable td { color: white !important; font-size: 16px !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; }
    /* Estilo de los números grandes (Métricas) */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AGENCIA DE VENTAS NUEVA ILUSION")
st.subheader("Simulador de Estructura de Negocio")

# 2. Captura de Datos con Preguntas Claras
with st.form(key="form_final_ilusion"):
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ubicación del lote", key="p_loc")

    st.markdown('<p class="pregunta">2. Nombre del Cliente</p>', unsafe_allow_html=True)
    cliente = st.text_input("  ", placeholder="Nombre del comprador", key="p_cli")

    st.markdown('<p class="pregunta">3. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("   ", min_value=0.0, step=1000000.0, format="%.0f")

    st.markdown('<p class="pregunta">4. Valor del Bono de Descuento ($)</p>', unsafe_allow_html=True)
    v_bono = st.number_input("    ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">5. Valor de Separación (Abono hoy) ($)</p>', unsafe_allow_html=True)
    v_sep = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f")

    st.markdown('<p class="pregunta">6. Porcentaje de Cuota Inicial (%)</p>', unsafe_allow_html=True)
    p_ini = st.number_input("      ", min_value=0.0, max_value=100.0, value=30.0)

    st.markdown('<p class="pregunta">7. Meses para pagar el resto de la inicial</p>', unsafe_allow_html=True)
    m_ini = st.number_input("       ", min_value=1, value=12)

    st.markdown('<p class="pregunta">8. Meses para financiar el valor del lote</p>', unsafe_allow_html=True)
    m_lote = st.number_input("        ", min_value=1, value=36)

    btn_calc = st.form_submit_button(label="CALCULAR PLAN DE PAGOS")

# 3. Lógica de Negocio y Resultados
if btn_calc:
    base = precio_lista - v_bono
    v_ini_total = base * (p_ini / 100)
    # Valor a financiar después del abono (separación)
    dif_inicial_financiar = v_ini_total - v_sep
    saldo_lote = base - v_ini_total

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    st.markdown(f"**Cliente:** {cliente.upper()}")

    # Visualización de valores solicitados
    c1, c2, c3 = st.columns(3)
    c1.metric("CUOTA INICIAL TOTAL", f"${v_ini_total:,.0f}")
    c2.metric("INICIAL POR PAGAR", f"${max(0, dif_inicial_financiar):,.0f}")
    c3.metric("VALOR FINANCIADO LOTE", f"${saldo_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma con Fechas de Pago Fijas")
    
    plan = []
    fecha_hoy = datetime.datetime.now()
    dia_pago = fecha_hoy.day # El día de hoy define el día de todos los pagos futuros

    def calcular_fecha(meses_adelante):
        mes = (fecha_hoy.month + meses_adelante - 1) % 12 + 1
        anio = fecha_hoy.year + (fecha_hoy.month + meses_adelante - 1) // 12
        # Ajustar si el día no existe en el mes futuro (ej: 31 de febrero)
        ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
        dia_ajustado = min(dia_pago, ultimo_dia_mes)
        return datetime.date(anio, mes, dia_ajustado).strftime('%d/%m/%Y')

    # FASE 1: Diferencia de la Inicial
    if dif_inicial_financiar > 0:
        cuota_ini = dif_inicial_financiar / m_ini
        for i in range(1, int(m_ini) + 1):
            plan.append({
                "Etapa": "1. Diferencia Inicial", 
                "Fecha": calcular_fecha(i), 
                "Valor Cuota": f"${cuota_ini:,.0f}"
            })

    # FASE 2: Saldo del Lote
    cuota_lote = saldo_lote / m_lote
    for j in range(1, int(m_lote) + 1):
        plan.append({
            "Etapa": "2. Valor Lote", 
            "Fecha": calcular_fecha(int(m_ini) + j), 
            "Valor Cuota": f"${cuota_lote:,.0f}"
        })

    st.table(pd.DataFrame(plan))
    st.success(f"Día de pago establecido: todos los {dia_pago} de cada mes.")
