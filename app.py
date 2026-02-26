import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import calendar

# 1. Configuración Visual de la Agencia
COLOR_FONDO = "#0B2447"
COLOR_DORADO = "#C5A880"
COLOR_BLANCO = "#FFFFFF"

def limpiar_dato(texto):
    if not texto: return 0.0
    return float(texto.replace("$", "").replace(".", "").replace(",", "").strip())

def calcular():
    try:
        # Captura de datos con nombres de Luis Fer
        precio = limpiar_dato(ent_precio.get())
        bono = limpiar_dato(ent_bono.get()) if var_bono.get() == "Si" else 0
        separacion = limpiar_dato(ent_sep.get())
        p_ini = limpiar_dato(ent_pct.get())
        m_ini = int(limpiar_dato(ent_m_ini.get()))
        m_lote = int(limpiar_dato(ent_m_lote.get()))
        
        # Fecha de Negociación
        f_neg = ent_fecha.get()
        dia, mes, anio = map(int, f_neg.split('/'))
        fecha_base = datetime.date(anio, mes, dia)

        # Cálculos de Negocio
        base_calc = precio - bono
        v_cuota_inicial = base_calc * (p_ini / 100)
        s_cuota_inicial = v_cuota_inicial - separacion
        v_fin_lote = base_calc - v_cuota_inicial
        
        c_mes_ini = s_cuota_inicial / m_ini if m_ini > 0 else 0
        c_mes_lote = v_fin_lote / m_lote if m_lote > 0 else 0

        # Actualizar Etiquetas de Resultados
        lbl_v_ini.config(text=f"VALOR CUOTA INICIAL: ${v_cuota_inicial:,.0f}")
        lbl_s_ini.config(text=f"SALDO CUOTA INICIAL: ${max(0, s_cuota_inicial):,.0f}")
        lbl_c_ini.config(text=f"CUOTA MENSUAL INICIAL: ${c_mes_ini:,.0f}")
        lbl_v_lote.config(text=f"VALOR FINANCIADO LOTE: ${v_fin_lote:,.0f}")

        # Llenar Cronograma sin índices laterales
        for row in tabla.get_children(): tabla.delete(row)
        
        # Fase Inicial
        for i in range(1, m_ini + 1):
            f_p = (fecha_base + datetime.timedelta(days=30*i)).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {i} de pago inicial", f_p, f"${c_mes_ini:,.0f}"))
            
        # Fase Lote
        for j in range(1, m_lote + 1):
            f_p = (fecha_base + datetime.timedelta(days=30*(m_ini+j))).strftime("%d/%m/%Y")
            tabla.insert("", "end", values=(f"Cuota {j} del lote", f_p, f"${c_mes_lote:,.0f}"))

    except Exception as e:
        messagebox.showerror("Revisa los números", "Asegúrate de:\n1. No dejar campos vacíos.\n2. Fecha en formato DD/MM/AAAA.\n3. Usar solo números.")

# Interfaz Principal
root = tk.Tk()
root.title("AGENCIA DE VENTAS NUEVA ILUSION")
root.geometry("600x850")
root.configure(bg=COLOR_FONDO)

# Campos de Entrada (Estilo compacto)
def crear_label(texto):
    return tk.Label(root, text=texto, bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 10, "bold"))

crear_label("1. Nombre del proyecto:").pack(pady=2)
ent_proy = tk.Entry(root, justify='center'); ent_proy.pack()

crear_label("2. Nombre del Cliente:").pack(pady=2)
ent_cli = tk.Entry(root, justify='center'); ent_cli.pack()

crear_label("3. Precio de lista del lote ($):").pack(pady=2)
ent_precio = tk.Entry(root, justify='center'); ent_precio.pack()

crear_label("4. ¿Aplica bono de descuento especial?").pack(pady=2)
var_bono = tk.StringVar(value="No")
tk.Radiobutton(root, text="No", variable=var_bono, value="No", bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()
tk.Radiobutton(root, text="Si", variable=var_bono, value="Si", bg=COLOR_FONDO, fg="white", selectcolor="#19376D").pack()

crear_label("Digite valor del descuento ($):").pack()
ent_bono = tk.Entry(root, justify='center'); ent_bono.insert(0, "0"); ent_bono.pack()

crear_label("5. Valor de Separación (Abono hoy) ($):").pack(pady=2)
ent_sep = tk.Entry(root, justify='center'); ent_sep.pack()

crear_label("6. Porcentaje de Cuota Inicial (%):").pack(pady=2)
ent_pct = tk.Entry(root, justify='center'); ent_pct.insert(0, "30"); ent_pct.pack()

crear_label("7. Meses por financiar cuota inicial:").pack(pady=2)
ent_m_ini = tk.Entry(root, justify='center'); ent_m_ini.pack()

crear_label("8. Meses a financiar saldo del lote:").pack(pady=2)
ent_m_lote = tk.Entry(root, justify='center'); ent_m_lote.pack()

crear_label("9. Fecha de negociacion (DD/MM/AAAA):").pack(pady=2)
ent_fecha = tk.Entry(root, justify='center'); ent_fecha.insert(0, datetime.date.today().strftime("%d/%m/%Y")); ent_fecha.pack()

tk.Button(root, text="GENERAR ESTRUCTURA DE NEGOCIO", command=calcular, bg=COLOR_DORADO, font=("Arial", 10, "bold")).pack(pady=15)

# Métricas de Resultados
lbl_v_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_ini.pack()
lbl_s_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_s_ini.pack()
lbl_c_ini = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_c_ini.pack()
lbl_v_lote = tk.Label(root, text="", bg=COLOR_FONDO, fg=COLOR_DORADO, font=("Arial", 11, "bold"))
lbl_v_lote.pack()

# Tabla de Cronograma
tabla = ttk.Treeview(root, columns=("Etapa", "Fecha", "Valor"), show="headings", height=10)
tabla.heading("Etapa", text="ETAPA DE PAGO")
tabla.heading("Fecha", text="FECHA")
tabla.heading("Valor", text="VALOR")
tabla.pack(pady=10, fill="x", padx=20)

root.mainloop()
