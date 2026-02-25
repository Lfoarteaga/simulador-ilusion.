import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import io

st.set_page_config(page_title="Agencia Nueva Ilusión", page_icon="🏡")

# Diseño de marca
COLOR_FONDO = "#0B2447"
COLOR_ACENTO = "#C5A880"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_FONDO}; color: white; }}
    .stButton>button {{ background-color: {COLOR_ACENTO}; color: black; border-radius: 10px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 AGENCIA NUEVA ILUSIÓN")
st.subheader("Simulador Pro de Estructura de Negocio")

with st.form("simulador_guiado"):
    col1, col2 = st.columns(2)
    with col1:
        # Guía para el Proyecto
        proyecto = st.text_input("Proyecto / Ubicación", 
                                placeholder="Ej: Turbaco - Sector Campestre",
                                help="Escribe aquí si el lote está en Turbaco, Santa Rosa o Cartagena.")
        
        # Guía para el Cliente
        cliente = st.text_input("Nombre del Cliente", 
                               placeholder="Nombre completo del comprador",
                               help="Para que la cotización salga personalizada con su nombre.")
        
        # Guía para el Precio
        precio_lista = st.number_input("Precio Lista ($)", min_value=0, step=1000000,
                                     help="Coloca el valor total del terreno según la lista de precios.")
        
        bono = st.number_input("Bono Especial ($)", min_value=0, step=500000,
                             help="Si hay un descuento o bono promocional, colócalo aquí.")
    
    with col2:
        separacion = st.number_input("Valor Separación ($)", min_value=0, step=500000,
                                   help="Monto que el cliente entrega para apartar el lote.")
        
        pct_ini = st.number_input("% Cuota Inicial", min_value=1, max_value=100, value=30,
                                 help="Porcentaje del valor total que se pagará como inicial.")
        
        # Guía para los Meses
        meses_ini = st.number_input("Meses Inicial", min_value=1, value=12,
                                   help="Plazo en meses para completar el pago de la cuota inicial.")
        
        meses_lote = st.number_input("Meses Financiación Lote", min_value=0, value=36,
                                    help="Plazo para pagar el saldo restante del lote.")
    
    dia_fijo = st.slider("Día de Pago Fijo", 1, 30, 10,
                        help="Día del mes en que el cliente prefiere realizar sus pagos.")
    
    boton = st.form_submit_button("CALCULAR Y GENERAR GUÍA DE PAGOS")

if boton:
    base_calculo = precio_lista - bono
    val_ini_total = base_calculo * (pct_ini / 100)
    restante_inicial = val_ini_total - separacion
    saldo_final_lote = base_calculo - val_ini_total
    
    st.divider()
    st.info(f"📍 Negocio para {cliente} en {proyecto}")
    
    # Tabla de pagos automática
    datos_tabla = []
    hoy = datetime.date.today()
    cuota_ini = restante_inicial / meses_ini
    cuota_lote = saldo_final_lote / meses_lote if meses_lote > 0 else 0

    for i in range(1, meses_ini + 1):
        datos_tabla.append({"Cuota": f"Inicial {i}", "Monto": f"${cuota_ini:,.0f}"})
    for j in range(1, meses_lote + 1):
        datos_tabla.append({"Cuota": f"Lote {j}", "Monto": f"${cuota_lote:,.0f}"})

    st.table(pd.DataFrame(datos_tabla))
