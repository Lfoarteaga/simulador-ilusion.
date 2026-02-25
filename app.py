import streamlit as st
import pandas as pd
import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Configuración de Marca y Estilo (Blindaje de Visibilidad)
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

st.markdown("""
    <style>
    /* Fondo principal */
    .stApp { background-color: #0B2447; color: white; }
    
    /* Preguntas y títulos en dorado */
    .pregunta { font-weight: bold; font-size: 20px; color: #C5A880; margin-top: 25px; display: block; }
    
    /* Forzar visibilidad de Métricas (Números grandes) */
    [data-testid="stMetricValue"] { color: #C5A880 !important; font-size: 28px !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 16px !important; }
    
    /* Forzar visibilidad de la Tabla */
    .stTable td, .stTable th { color: white !important; font-size: 16px !important; }
    thead tr th { background-color: #19376D !important; color: #C5A880 !important; }
    
    /* Botón grande y visible */
    div.stButton > button:first-child {
        background-color: #C5A880; color: #0B2447; font-weight: bold;
        width: 100%; border-radius: 10px; border: none; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador Pro de Estructura de Negocio")

# 2. Formulario de Entrada
with st.form("simulador_v4"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="pregunta">1. Nombre del proyecto</p>', unsafe_allow_html=True)
        proyecto = st.text_input("", placeholder="Ej. Amaru", key="in1")
        st.markdown('<p class="pregunta">2. Precio de lista ($)</p>', unsafe_allow_html=True)
        precio_lista = st.number_input("", min_value=0.0, step=1000000.0, format="%.0f")
        st.markdown('<p class="pregunta">3. Bono Especial ($)</p>', unsafe_allow_html=True)
        bono = st.number_input("", min_value=0.0, step=100000.0, format="%.0f")
    with col2:
        st.markdown('<p class="pregunta">4. Valor de Separación ($)</p>', unsafe_allow_html=True)
        separacion = st.number_input("", min_value=0.0, step=100000.0, format="%.0f")
        st.markdown('<p class="pregunta">5. % Cuota Inicial</p>', unsafe_allow_html=True)
        pct_inicial = st.number_input("", min_value=0.0, max_value=100.0, value=30.0)
        st.markdown('<p class="pregunta">6. Meses Diferencia Inicial</p>', unsafe_allow_html=True)
        meses_ini = st.number_input("", min_value=1, value=12)
    
    st.markdown('<p class="pregunta">7. Cuotas Saldo del Lote</p>', unsafe_allow_html=True)
    num_cuotas_lote = st.number_input("", min_value=1, value=36)
    
    boton = st.form_submit_button("CALCULAR Y MOSTRAR PLAN")

# 3. Cálculos y Resultados Visibles
if boton:
    precio_base = precio_lista - bono
    v_inicial_total = precio_base * (pct_inicial / 100)
    dif_inicial = v_inicial_total - separacion
    c_inicial_mes = dif_inicial / meses_ini if dif_inicial > 0 else 0
    s_lote = precio_base - v_inicial_total
    c_lote_mes = s_lote / num_cuotas_lote

    st.divider()
    st.markdown(f"## 📍 PROYECTO: {proyecto.upper()}")
    
    # Métricas con colores forzados
    m1, m2, m3 = st.columns(3)
    m1.metric("BASE CÁLCULO", f"${precio_base:,.0f}")
    m2.metric("INICIAL TOTAL", f"${v_inicial_total:,.0f}")
    m3.metric("SALDO LOTE", f"${s_lote:,.0f}")

    st.write("### 📅 Cronograma de Pagos Detallado")
    
    plan = []
    hoy = datetime.datetime.now()
    
    # Fase 1
    if dif_inicial > 0:
        for i in range(1, int(meses_ini) + 1):
            f = hoy + datetime.timedelta(days=30 * i)
            plan.append({"Fase": "1. Inicial", "Vencimiento": f.strftime('%d/%m/%Y'), "Valor": f"${c_inicial_mes:,.0f}"})
    
    # Fase 2
    for j in range(1, int(num_cuotas_lote) + 1):
        f = hoy + datetime.timedelta(days=30 * (meses_ini + j))
        plan.append({"Fase": "2. Lote", "Vencimiento": f.strftime('%d/%m/%Y'), "Valor": f"${c_lote_mes:,.0f}"})

    st.table(pd.DataFrame(plan))
    st.caption("Estructura de negocio generada por Luis Fer.")
