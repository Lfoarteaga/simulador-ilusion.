import streamlit as st
import pandas as pd
import datetime

# 1. Configuración de Marca y Visibilidad (Fondo Oscuro / Letras Claras)
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    
    /* Preguntas en Dorado */
    .pregunta { font-weight: bold; font-size: 19px; color: #C5A880; margin-top: 15px; margin-bottom: 5px; display: block; }
    
    /* FORZAR COLOR BLANCO EN LA TABLA */
    .stTable td { color: white !important; font-size: 16px !important; }
    .stTable th { color: #C5A880 !important; background-color: #19376D !important; }

    /* Indicadores de Resultados (Métricas) */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 32px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador de Estructura de Negocio")

# 2. Formulario de Captura (Pregunta arriba, cuadro abajo)
with st.form(key="form_cierre_ilusion"):
    st.markdown('<p class="pregunta">1. Nombre del proyecto o ubicación</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ej. Lotes Cartagena Este", key="val_proy")

    st.markdown('<p class="pregunta">2. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("  ", min_value=0.0, step=1000000.0, format="%.0f", key="val_precio")

    st.markdown('<p class="pregunta">3. ¿Aplica algún bono de descuento?</p>', unsafe_allow_html=True)
    check_bono = st.radio("   ", ["No", "Sí"], horizontal=True, key="val_check")
    v_bono = 0.0
    if check_bono == "Sí":
        st.markdown('<p class="pregunta">Valor del bono ($)</p>', unsafe_allow_html=True)
        v_bono = st.number_input("    ", min_value=0.0, step=100000.0, format="%.0f", key="val_bono")

    st.markdown('<p class="pregunta">4. Valor de separación ($)</p>', unsafe_allow_html=True)
    v_sep = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="val_sep")

    st.markdown('<p class="pregunta">5. Porcentaje de cuota inicial (%)</p>', unsafe_allow_html=True)
    p_ini = st.number_input("      ", min_value=0.0, max_value=100.0, value=30.0, key="val_pct")

    st.markdown('<p class="pregunta">6. Meses para pagar la diferencia de inicial</p>', unsafe_allow_html=True)
    m_ini = st.number_input("       ", min_value=1, value=12, key="val_mini")

    st.markdown('<p class="pregunta">7. Meses para financiar el saldo del lote</p>', unsafe_allow_html=True)
    m_lote = st.number_input("        ", min_value=1, value=36, key="val_mlote")

    btn_generar = st.form_submit_button(label="GENERAR PLAN DE NEGOCIO")

# 3. Lógica y Visualización de las 3 Cifras Clave
if btn_generar:
    base = precio_lista - v_bono
    v_ini_total = base * (p_ini / 100)
    diferencia_a_financiar = v_ini_total - v_sep
    saldo_final_lote = base - v_ini_total

    st.divider()
    st.markdown(f"## 📍 NEGOCIO: {proyecto.upper()}")

    # LAS 3 CIFRAS QUE NECESITAS MOSTRAR CLARAMENTE
    c1, c2, c3 = st.columns(3)
    c1.metric("CUOTA INICIAL TOTAL", f"${v_ini_total:,.0f}")
    c2.metric("INICIAL A FINANCIAR", f"${max(0, diferencia_a_financiar):,.0f}")
    c3.metric("SALDO FINAL LOTE", f"${saldo_final_lote:,.0f}")

    st.write("---")
    st.write("### 📅 Cronograma de Pagos (Letras en Blanco)")
    
    plan = []
    hoy = datetime.datetime.now()
    
    # Cuotas de la inicial
    if diferencia_a_financiar > 0:
        c_ini_mes = diferencia_a_financiar / m_ini
        for i in range(1, int(m_ini) + 1):
            f = hoy + datetime.timedelta(days=30 * i)
            plan.append({"Etapa": "1. Diferencia Inicial", "Fecha": f.strftime('%d/%m/%Y'), "Valor": f"${c_ini_mes:,.0f}"})
    
    # Cuotas del saldo del lote
    c_lote_mes = saldo_final_lote / m_lote
    for j in range(1, int(m_lote) + 1):
        f = hoy + datetime.timedelta(days=30 * (m_ini + j))
        plan.append({"Etapa": "2. Saldo del Lote", "Fecha": f.strftime('%d/%m/%Y'), "Valor": f"${c_lote_mes:,.0f}"})

    st.table(pd.DataFrame(plan))
    st.caption("Estructura calculada profesionalmente para la Agencia Nueva Ilusión.")
