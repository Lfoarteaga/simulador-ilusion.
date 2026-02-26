import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import calendar

# 1. Configuración de Marca (Visibilidad para PC)
COLOR_FONDO = "#0B2447"
COLOR_DORADO = "#C5A880"
COLOR_BLANCO = "#FFFFFF"

def limpiar_numero(texto):
    if not texto: return 0.0
    return float(texto.replace("$", "").replace(".", "").replace(",", "").strip())

# Función para habilitar/deshabilitar el cuadro de bono según tu petición
def activar_bono():
    if var_bono.get() == "Si":
        ent_val_bono.config(state="normal")
        ent_val_bono.delete(0, tk.END)
        ent_val_bono.focus()
    else:
        ent_val_bono.delete(0, tk.END)
        ent_val_bono.insert(0, "0")
        ent_val_bono.config(state="disabled")

def generar_negocio_pc():
    try:
        # Captura de datos
        precio_l = limpiar_numero(ent_precio.get())
        v_bono = limpiar_numero(ent_val_bono.get()) if var_bono.get() == "Si" else 0
        v_separacion = limpiar_numero(ent_sep.get())
        p_inicial = limpiar_numero(ent_pct.get())
        m_inicial = int(limpiar_numero(ent_m_ini.get()))
        m_lote = int(limpiar_numero(ent_m_lote.get()))
        
        # Fecha de Negociación (Formato DD/MM/AAAA)
        f_texto = ent_fecha.get()
        dia, mes, anio = map(int, f_texto.split('/'))
        fecha_neg = datetime.date(anio, mes, dia)

        # Lógica de AGENCIA DE VENTAS NUEVA ILUSION
        base_calc = precio_l - v_bono
        v_cuota_inicial = base_calc * (p_inicial / 100)
        saldo_cuota_inicial = v_cuota_inicial - v_separacion
        v_financiado_lote = base_calc - v_cuota
