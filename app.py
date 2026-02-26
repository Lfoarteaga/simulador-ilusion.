import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import calendar

# 1. Configuración de Marca (Agencia de Ventas Nueva Ilusión)
COLOR_FONDO = "#0B2447"
COLOR_DORADO = "#C5A880"
COLOR_BLANCO = "#FFFFFF"

def limpiar_num(texto):
    if not texto: return 0.0
    # Limpia puntos, comas y símbolos para que el PC no se bloquee
    return float(texto.replace("$", "").replace(".", "").replace(",", "").strip())

# 2. Lógica para habilitar el cuadro de Bono
def toggle_bono():
    if var_aplica_bono.get() == "Si":
        ent_val_bono.config(state="normal")
        ent_val_bono.delete(0, tk.END)
        ent_val_bono.focus()
    else:
        ent_val_bono.delete(0, tk.END)
        ent_val_bono.insert(0, "0")
        ent_val_bono.config(state="disabled")

def generar_negocio():
    try:
        # Captura de datos
        precio_lista = limpiar_num(ent_precio.get())
        v_bono = limpiar_num(ent_val_bono.get()) if var_aplica_bono.get() == "Si" else 0
        v_sep = limpiar_num(ent_sep.get())
        pct_ini = limpiar_num(ent_pct.get())
        m_ini = int(limpiar_num(ent_m_ini.get()))
        m_lote = int(limpiar_num(ent_m_lote.get()))
        
        # Fecha de Negociación (Debe ser DD/MM/AAAA)
        f_texto = ent_fecha.get()
        d, m, a = map(int, f_texto.split('/'))
        fecha_ini = datetime.date(a, m, d)

        # Cálculos de la Agencia
        base_calc = precio_lista - v_bono
        v_cuota_inicial = base_calc * (pct_ini / 100)
        saldo_cuota_inicial = v_cuota_inicial - v_sep
        v_financiado_lote = base_calc - v_cuota_inicial
        
        c_mensual_ini = saldo_cuota_inicial / m_ini if m_ini > 0 else 0
        c_mensual_lote = v_financiado_lote / m_lote if m_lote > 0 else 0

        # Mostrar métricas doradas (Cifras de cierre)
        lbl_v_ini.config(text=f"VALOR CUOTA INICIAL: ${v_cuota_inicial:,.0f}")
        lbl_s_ini.config(text=f"SALDO CUOTA INICIAL: ${max(0, saldo_cuota_inicial):,.0f}")
        lbl_c_ini.config(text=f"CUOTA MENSUAL INICIAL: ${c_mensual_ini:,.0f}")
        lbl_v_lote.config(text=f"VALOR FINANCIADO LOTE: ${v_financiado_lote:,.0f}")

        # Llenar el cronograma sin números laterales
        for row in tabla.get_children(): tabla.delete(row)
        
        # Etapa 1: Pago Inicial
        for i in range(1, m_ini + 1):
            f_p = (fecha_ini + datetime.timedelta(days=30*i)).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {i} de pago inicial", f_p, f"${c_mensual_ini:,.0f}"))
            
        # Etapa 2: Saldo Lote
        for j in range(1, m_lote + 1):
            f_p = (fecha_ini + datetime.timedelta(days=30*(m_ini+j))).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {j} del lote", f_p, f"${c_mensual_lote:,.0f}"))

    except Exception as e:
        messagebox.showerror("Error", "Revisa los números. No dejes campos vacíos y usa la fecha como DD/MM/AAAA.")

# 3. Interfaz del PC
root = tk.Tk()
root.title("AGENCIA DE VENTAS NUEVA ILUSION")
root.geometry("600x850")
root.configure(bg=COLOR_FONDO)

def lbl(t, c=COLOR_DORADO):
    return tk.Label(root, text=t, bg=COLOR_FONDO, fg=c, font=("Arial", 10, "bold"))

lbl("1. Nombre del proyecto:").pack(pady=2)
ent_proy = tk.Entry(root, justify='center'); ent_proy.pack()

lbl("2. Nombre del Cliente:").pack(pady=2)
ent_cli = tk.Entry(root, justify='center'); ent_cli.pack()

lbl("3. Precio de lista del lote ($):").pack(pady=2)
ent_precio = tk.Entry(root, justify='center'); ent_precio.pack()

# Item de Bono Especial (Dígitalo cuando aplique)
lbl("4. ¿Aplica bono de descuento especial?", COLOR_BLANCO).pack(pady=2)
var_aplica_bono = tk.StringVar(value="No")
tk.Radiobutton(root, text="No", variable=var_aplica_bono, value="No", command=toggle_bono, bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()
tk.Radiobutton(root, text="Si", variable=var_aplica_bono, value="Si", command=toggle_bono, bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()

lbl("Digite el valor del bono ($):", COLOR_BLANCO).pack()
ent_val_bono = tk.Entry(root, justify='center', state="disabled"); ent_val_bono.insert(0, "0"); ent_val_bono.pack()

lbl("5. Valor de Separación (Abono hoy) ($):").pack(pady=2)
ent_sep = tk.Entry(root, justify='center'); ent_sep.pack()

lbl("6. Porcentaje de Cuota Inicial (%):").pack(pady=2)
ent_pct = tk.Entry(root, justify='center'); ent_pct.insert(0, "30"); ent_pct.pack()

lbl("7. Meses por financiar cuota inicial:").pack(pady=2)
ent_m_ini = tk.Entry(root, justify='center'); ent_m_ini.pack()

lbl("8. Meses a financiar saldo del lote:").pack(pady=2)
ent_m_lote = tk.Entry(root, justify='center'); ent_m_lote.pack()

lbl("9. Fecha de negociacion (DD/MM/AAAA):").pack(pady=2)
ent_fecha = tk.Entry(root, justify='center'); ent_fecha.insert(0, datetime.date.today().strftime("%d/%m/%Y")); ent_fecha.pack()

tk.Button(root, text="GENERAR ESTRUCTURA DE NEGOCIO", command=generar_negocio, bg=COLOR_DORADO, font=("Arial", 10, "bold")).pack(pady=15)

# Cifras de Cierre Visibles
lbl_v_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_ini.pack(); lbl_s_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_s_ini.pack(); lbl_c_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_c_ini.pack(); lbl_v_lote = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_lote.pack()

# Cronograma Profesional
tabla = ttk.Treeview(root, columns=("E", "F", "V"), show="headings", height=8)
tabla.heading("E", text="ETAPA DE PAGO"); tabla.heading("F", text="FECHA"); tabla.heading("V", text="VALOR")
tabla.pack(pady=10, fill="x", padx=20)

root.mainloop()
