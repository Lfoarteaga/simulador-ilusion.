import streamlit as st
import pandas as pd
import datetime

# 1. Configuración de Marca y Visibilidad Total
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    /* Forzar que los números de la tabla y métricas sean blancos/dorados */
    [data-testid="stMetricValue"] { color: #C5A880 !important; }
    .stTable { color: white !important; background-color: rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador de Estructura de Negocio")

# 2. Formulario de Captura (Pregunta Arriba, Cuadro Abajo)
with st.form("simulador_final_ilusion"):
    
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input("", placeholder="Ej. Amaru", key="key_proy")

    st.markdown('<p class="pregunta">2. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("", min_value=0.0, step=1000000.0, format="%.0f", key="key_precio")

    st.markdown('<p class="pregunta">3. ¿Aplica bono de descuento especial?</p>', unsafe_allow_html=True)
    tiene_bono = st.radio("", ["No", "Sí"], horizontal=True, key="key_tiene_bono")
    
    valor_bono = 0.0
    if tiene_bono == "Sí":
        st.markdown('<p class="pregunta">Valor del bono ($)</p>', unsafe_allow_html=True)
        valor_bono = st.number_input("", min_value=0.0, step=100000.0, format="%.0f", key="key_val_bono")

    st.markdown('<p class="pregunta">4. Valor de separación ($)</p>', unsafe_allow_html=True)
    valor_separacion = st.number_input("", min_value=0.0, step=100000.0, format="%.0f", key="key_sep")

    st.markdown('<p class="pregunta">5. Porcentaje de cuota inicial (ej. 30)</p>', unsafe_allow_html=True)
    pct_inicial = st.number_input("", min_value=0.0, max_value=100.0, value=30.0, key="key_pct")

    st.markdown('<p class="pregunta">6. Meses para pagar la diferencia de la inicial</p>', unsafe_allow_html=True)
    meses_ini = st.number_input("", min_value=1, value=12, key="key_meses_ini")

    st.markdown('<p class="pregunta">7. Cuotas para el saldo restante del lote</p>', unsafe_allow_html=True)
    num_cuotas_lote = st.number_input("", min_value=1, value=36, key="key_cuotas_lote")

    st.markdown("<br>", unsafe_allow_html=True)
    # EL BOTÓN DEBE IR AQUÍ ADENTRO
    boton_ejecutar = st.form_submit_button("CALCULAR ESTRUCTURA DE NEGOCIO")

# 3. Lógica de Negocio y Presentación de Resultados
if boton_ejecutar:
    precio_base = precio_lista - valor_bono
    v_inicial_total = precio_base * (pct_inicial / 100)
    dif_inicial = v_inicial_total - valor_separacion
    
    cuota_inicial_mes = dif_inicial / meses_ini if dif_inicial > 0 else 0
    saldo_lote = precio_base - v_inicial_total
    cuota_lote_mes = saldo_lote / num_cuotas_lote

    st.divider()
    st.header(f"📍 {proyecto.upper()}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("BASE CÁLCULO", f"${precio_base:,.0f}")
    col2.metric("INICIAL RESTANTE", f"${dif_inicial:,.0f}")
    col3.metric("SALDO LOTE", f"${saldo_lote:,.0f}")

    st.write("### 📅 Plan de Pagos Detallado")
    
    # Construcción de la tabla
    cronograma = []
    hoy = datetime.datetime.now()
    
    if dif_inicial > 0:
        for i in range(1, int(meses_ini) + 1):
            fecha = hoy + datetime.timedelta(days=30 * i)
            cronograma.append({"Fase": "1. Diferencia Inicial", "Fecha": fecha.strftime('%d/%m/%Y'), "Cuota": f"${cuota_inicial_mes:,.0f}"})
    
    for j in range(1, int(num_cuotas_lote) + 1):
        fecha = hoy + datetime.timedelta(days=30 * (meses_ini + j))
        cronograma.append({"Fase": "2. Saldo Lote", "Fecha": fecha.strftime('%d/%m/%Y'), "Cuota": f"${cuota_lote_mes:,.0f}"})

    st.table(pd.DataFrame(cronograma))
    st.success("Simulación generada exitosamente. ¡A cerrar esa venta!")
