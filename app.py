import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import calendar

# 1. Configuración de Colores de la Agencia
COLOR_FONDO = "#0B2447"
COLOR_DORADO = "#C5A880"
COLOR_BLANCO = "#FFFFFF"

def limpiar_num(texto):
    if not texto: return 0.0
    return float(texto.replace("$", "").replace(".", "").replace(",", "").strip())

# Función para habilitar el cuadro de Bono solo si marcas "Si"
def toggle_bono():
    if var_bono.get() == "Si":
        ent_val_bono.config(state="normal")
        ent_val_bono.focus()
    else:
        ent_val_bono.delete(0, tk.END)
        ent_val_bono.insert(0, "0")
        ent_val_bono.config(state="disabled")

def generar_negocio_pc():
    try:
        # Captura de datos
        precio = limpiar_num(ent_precio.get())
        v_bono = limpiar_num(ent_val_bono.get()) if var_bono.get() == "Si" else 0
        v_sep = limpiar_num(ent_sep.get())
        p_ini = limpiar_num(ent_pct.get())
        m_ini = int(limpiar_num(ent_m_ini.get()))
        m_lote = int(limpiar_num(ent_m_lote.get()))
        
        f_texto = ent_fecha.get() # DD/MM/AAAA
        d, m, a = map(int, f_texto.split('/'))
        f_neg = datetime.date(a, m, d)

        # Cálculos de la Agencia Nueva Ilusión
        base_calc = precio - v_bono
        v_inicial_total = base_calc * (p_ini / 100)
        saldo_inicial = v_inicial_total - v_sep
        v_fin_lote = base_calc - v_inicial_total
        
        c_ini_mes = saldo_inicial / m_ini if m_ini > 0 else 0
        c_lote_mes = v_fin_lote / m_lote if m_lote > 0 else 0

        # Mostrar métricas doradas
        lbl_v_ini.config(text=f"VALOR CUOTA INICIAL: ${v_inicial_total:,.0f}")
        lbl_s_ini.config(text=f"SALDO CUOTA INICIAL: ${max(0, saldo_inicial):,.0f}")
        lbl_c_ini.config(text=f"CUOTA MENSUAL INICIAL: ${c_ini_mes:,.0f}")
        lbl_v_lote.config(text=f"VALOR FINANCIADO LOTE: ${v_fin_lote:,.0f}")

        # Llenar cronograma sin índices laterales
        for row in tabla.get_children(): tabla.delete(row)
        
        for i in range(1, m_ini + 1):
            f_p = (f_neg + datetime.timedelta(days=30*i)).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {i} de pago inicial", f_p, f"${c_ini_mes:,.0f}"))
            
        for j in range(1, m_lote + 1):
            f_p = (f_neg + datetime.timedelta(days=30*(m_ini+j))).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {j} del lote", f_p, f"${c_lote_mes:,.0f}"))

    except Exception:
        messagebox.showerror("Revisa los números", "Asegúrate de:\n1. No dejar campos vacíos.\n2. Fecha como DD/MM/AAAA.\n3. Usar solo números.")

# --- INTERFAZ PC ---
root = tk.Tk()
root.title("AGENCIA DE VENTAS NUEVA ILUSION")
root.geometry("600x850")
root.configure(bg=COLOR_FONDO)

def q(t, c=COLOR_DORADO):
    return tk.Label(root, text=t, bg=COLOR_FONDO, fg=c, font=("Arial", 10, "bold"))

q("1. Nombre del proyecto:").pack(pady=2)
ent_proy = tk.Entry(root, justify='center'); ent_proy.pack()

q("2. Nombre del Cliente:").pack(pady=2)
ent_cli = tk.Entry(root, justify='center'); ent_cli.pack()

q("3. Precio de lista del lote ($):").pack(pady=2)
ent_precio = tk.Entry(root, justify='center'); ent_precio.pack()

q("4. ¿Aplica bono de descuento especial?", COLOR_BLANCO).pack(pady=2)
var_bono = tk.StringVar(value="No")
tk.Radiobutton(root, text="No", variable=var_bono, value="No", command=toggle_bono, bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()
tk.Radiobutton(root, text="Si", variable=var_bono, value="Si", command=toggle_bono, bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()

q("Digite el valor del bono ($):", COLOR_BLANCO).pack()
ent_val_bono = tk.Entry(root, justify='center', state="disabled"); ent_val_bono.insert(0, "0"); ent_val_bono.pack()

q("5. Valor de Separación (Abono hoy) ($):").pack(pady=2)
ent_sep = tk.Entry(root, justify='center'); ent_sep.pack()

q("6. Porcentaje de Cuota Inicial (%):").pack(pady=2)
ent_pct = tk.Entry(root, justify='center'); ent_pct.insert(0, "30"); ent_pct.pack()

q("7. Meses por financiar cuota inicial:").pack(pady=2)
ent_m_ini = tk.Entry(root, justify='center'); ent_m_ini.pack()

q("8. Meses a financiar saldo del lote:").pack(pady=2)
ent_m_lote = tk.Entry(root, justify='center'); ent_m_lote.pack()

q("9. Fecha de negociacion (DD/MM/AAAA):").pack(pady=2)
ent_fecha = tk.Entry(root, justify='center'); ent_fecha.insert(0, datetime.date.today().strftime("%d/%m/%Y")); ent_fecha.pack()

tk.Button(root, text="GENERAR ESTRUCTURA DE NEGOCIO", command=generar_negocio_pc, bg=COLOR_DORADO, font=("Arial", 10, "bold")).pack(pady=15)

# Cifras de Cierre
lbl_v_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_ini.pack(); lbl_s_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_s_ini.pack(); lbl_c_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_c_ini.pack(); lbl_v_lote = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_lote.pack()

# Cronograma
tabla = ttk.Treeview(root, columns=("E", "F", "V"), show="headings", height=8)
tabla.heading("E", text="ETAPA DE PAGO"); tabla.heading("F", text="FECHA"); tabla.heading("V", text="VALOR")
tabla.pack(pady=10, fill="x", padx=20)

root.mainloop()
