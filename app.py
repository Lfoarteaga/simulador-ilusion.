import streamlit as st
import pandas as pd

# Configuración profesional de la Agencia Nueva Ilusión
st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

# Estilo de marca: Fondo azul oscuro y letras doradas para las preguntas
st.markdown("""
    <style>
    .stApp { background-color: #0B2447; color: white; }
    .titulo-pregunta { 
        font-weight: bold; 
        font-size: 20px; 
        color: #C5A880; 
        margin-top: 20px;
        margin-bottom: 5px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.write("### Cotizador Multizona Profesional")

with st.form("cotizador_universal"):
    
    # 1. UBICACIÓN (Pregunta arriba, cuadro abajo)
    st.markdown('<label class="titulo-pregunta">1. ¿En qué ciudad o proyecto está el lote?</label>', unsafe_allow_html=True)
    proyecto = st.text_input("", placeholder="Escribe la ubicación aquí...", key="loc")

    # 2. CLIENTE
    st.markdown('<label class="titulo-pregunta">2. ¿Cuál es el nombre del cliente?</label>', unsafe_allow_html=True)
    cliente = st.text_input("", placeholder="Nombre completo del interesado", key="nom")

    # 3. PRECIO
    st.markdown('<label class="titulo-pregunta">3. ¿Cuál es el precio total de venta?</label>', unsafe_allow_html=True)
    precio = st.number_input("", min_value=0, step=500000, key="pre")

    # 4. PLAZO
    st.markdown('<label class="titulo-pregunta">4. ¿En cuántos meses se va a financiar?</label>', unsafe_allow_html=True)
    meses = st.number_input("", min_value=1, max_value=120, value=36, key="mes")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón de cálculo
    boton_calcular = st.form_submit_button("CALCULAR PLAN DE PAGOS")

if boton_calcular:
    if precio > 0:
        cuota_mensual = precio / meses
        st.divider()
        st.success(f"✅ Plan generado para el proyecto en: {proyecto}")
        
        col1, col2 = st.columns(2)
        col1.metric("Cliente", cliente)
        col2.metric("Cuota Mensual", f"${cuota_mensual:,.0f}")
        
        st.info("Este cálculo es una base comercial para iniciar el cierre de venta.")
    else:
        st.error("Por favor, ingresa un precio de venta válido.")
