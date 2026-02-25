import streamlit as st
import pandas as pd
import datetime

# Configuración de estilos para máxima visibilidad y contraste
st.set_page_config(page_title="Simulador de Pagos", page_icon="🏡")

st.markdown("""
    <style>
    /* Fondo principal del simulador */
    .stApp {
        background-color: #0B2447;
        color: white;
    }
    
    /* Selector específico para forzar el color blanco en las celdas de la tabla */
    .stTable td {
        color: white !important;
        font-weight: 400;
        font-size: 16px;
    }
    
    /* Estilo para los encabezados de la tabla con color de acento */
    .stTable th {
        color: #C5A880 !important;
        background-color: #19376D !important;
        font-weight: bold;
    }
    
    /* Diseño de las etiquetas de las preguntas */
    .pregunta {
        font-weight: bold;
        font-size: 19px;
        color: #C5A880;
        margin-top: 15px;
        margin-bottom: 5px;
        display: block;
    }
    
    /* Ajuste de métricas para mayor visibilidad */
    [data-testid="stMetricValue"] {
        color: #C5A880 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Simulador de Estructura de Negocio")

with st.form(key="simulador_negocio_v6"):
    st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
    proyecto = st.text_input(" ", placeholder="Ingrese el nombre...", key="f_proy")

    st.markdown('<p class="pregunta">2. Precio de lista del lote ($)</p>', unsafe_allow_html=True)
    precio_lista = st.number_input("  ", min_value=0.0, step=1000000.0, format="%.0f", key="f_precio")

    st.markdown('<p class="pregunta">3. ¿Aplica bono de descuento?</p>', unsafe_allow_html=True)
    tiene_bono = st.radio("   ", ["No", "Sí"], horizontal=True, key="f_bono_check")
    
    v_bono = 0.0
    if tiene_bono == "Sí":
        st.markdown('<p class="pregunta">Valor del bono ($)</p>', unsafe_allow_html=True)
        v_bono = st.number_input("    ", min_value=0.0, step=100000.0, format="%.0f", key="f_bono_val")

    st.markdown('<p class="pregunta">4. Valor de separación ($)</p>', unsafe_allow_html=True)
    v_separacion = st.number_input("     ", min_value=0.0, step=100000.0, format="%.0f", key="f_sep")

    st.markdown('<p class="pregunta">5. Porcentaje de cuota inicial</p>', unsafe_allow_html=True)
    pct_ini = st.number_input("      ", min_value=0.0, max_value=100.0, value=30.0, key="f_pct")

    st.markdown('<p class="pregunta">6. Meses para completar la inicial</p>', unsafe_allow_html=True)
    m_ini = st.number_input("       ", min_value=1, value=12, key="f_meses_ini")

    st.markdown('<p class="pregunta">7. Cuotas para el saldo del lote</p>', unsafe_allow_html=True)
    m_lote = st.number_input("        ", min_value=1, value=36, key="f_meses_lote")

    btn_calc = st.form_submit_button(label="CALCULAR")

if btn_calc:
    base = precio_lista - v_bono
    v_ini_total = base * (pct_ini / 100)
    d_ini = v_ini_total - v_separacion
    
    c_ini = d_ini / m_ini if d_ini > 0 else 0
    s_lote = base - v_ini_total
    c_lote = s_lote / m_lote

    st.divider()
    st.header(f"Proyecto: {proyecto.upper()}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Base Cálculo", f"${base:,.0f}")
    c2.metric("Inicial Restante", f"${max(0, d_ini):,.0f}")
    c3.metric("Saldo Lote", f"${s_lote:,.0f}")

    st.write("### Plan de Pagos Detallado")
    
    cronograma = []
    hoy = datetime.datetime.now()
    
    if d_ini > 0:
        for i in range(1, int(m_ini) + 1):
            fecha = hoy + datetime.timedelta(days=30 * i)
            cronograma.append({
                "Fase": "1. Cuota Inicial", 
                "Fecha": fecha.strftime('%d/%m/%Y'), 
                "Monto": f"${c_ini:,.0f}"
            })
    
    for j in range(1, int(m_lote) + 1):
        fecha = hoy + datetime.timedelta(days=30 * (m_ini + j))
        cronograma.append({
            "Fase": "2. Saldo Lote", 
            "Fecha": fecha.strftime('%d/%m/%Y'), 
            "Monto": f"${c_lote:,.0f}"
        })

    st.table(pd.DataFrame(cronograma))
