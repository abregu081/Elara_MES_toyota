import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import MESxLog as mes

class HermanacionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Elara - v1.0.0")
        self.state("zoomed")
        
        mes.load_settings()  # Carga la configuración desde MESxLog

        # Atributo para debounce de check_sn1
        self._debounce_id = None

        # Configurar estilos para los Entry
        self.style = ttk.Style()
        # Estilo normal (blanco)
        self.style.configure("Normal.TEntry", fieldbackground="white")
        # Estilo de error (rojo)
        self.style.configure("Error.TEntry", fieldbackground="red")
        # Estilo válido (verde)
        self.style.configure("Valid.TEntry", fieldbackground="lightgreen")

        # Configurar la ventana
        self.rowconfigure(1, weight=1)  # Fila 1 se expande
        self.rowconfigure(2, weight=0)  # Fila 2 fija (stats)
        self.columnconfigure(0, weight=1)

        # ----------------------------------------------------------------
        # FRAME SUPERIOR (Logotipos, Título, etc.) -> fila=0
        # ----------------------------------------------------------------
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=5)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        # Cargar y redimensionar imágenes
        mirgor_path = os.path.join("assets", "Logo_Mirgor.png")
        original_image = Image.open(mirgor_path)
        resized_image = original_image.resize((300, 100), Image.LANCZOS)
        self.logo_mirgor = ImageTk.PhotoImage(resized_image)

        clare_path = os.path.join("assets", "Elara Logo.png")
        clare_logo = Image.open(clare_path)
        resized_clare = clare_logo.resize((150, 150), Image.LANCZOS)
        self.logo_clare = ImageTk.PhotoImage(resized_clare)

        logo_label_img = ttk.Label(top_frame, image=self.logo_mirgor, anchor="center")
        logo_label_img.grid(row=0, column=0, sticky="w", padx=10)
        title_font = ("Montserrat", 32, "bold")
        title_label = ttk.Label(top_frame, text="TESTING UNAE", font=title_font, anchor="center")
        title_label.grid(row=0, column=1, sticky="nsew", padx=10)
        logo_clare_label = ttk.Label(top_frame, image=self.logo_clare, anchor="center")
        logo_clare_label.grid(row=0, column=2, sticky="e", padx=10)

        # ----------------------------------------------------------------
        # FRAME INFERIOR PRINCIPAL (fila=1)
        # ----------------------------------------------------------------
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=5)
        bottom_frame.rowconfigure(0, weight=0)
        bottom_frame.rowconfigure(1, weight=1)
        bottom_frame.columnconfigure(0, weight=1)

        # FRAME de Entradas (Housing, PCB) -> fila=0
        content_frame = ttk.Frame(bottom_frame)
        content_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        content_frame.columnconfigure(0, weight=0)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=0)

        label_font = ("Montserrat", 16, "bold")
        entry_font = ("Montserrat", 20)

        self.sn1_var = tk.StringVar()
        self.sn2_var = tk.StringVar()

        housing_label = ttk.Label(content_frame, text="Housing:", font=label_font, anchor="center")
        housing_label.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        # Se asigna el estilo normal al crear el Entry
        self.housing_entry = ttk.Entry(content_frame, width=50, font=entry_font,
                                       textvariable=self.sn1_var, justify="center",
                                       style="Normal.TEntry")
        self.housing_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.status_circle_housing = ttk.Label(content_frame, text="●", font=("Arial", 20, "bold"),
                                               foreground="gray", anchor="center")
        self.status_circle_housing.grid(row=0, column=2, sticky="ew", padx=5, pady=2)

        pcb_label = ttk.Label(content_frame, text="PCB:", font=label_font, anchor="center")
        pcb_label.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        self.pcb_entry = ttk.Entry(content_frame, width=50, font=entry_font,
                                   textvariable=self.sn2_var, justify="center",
                                   style="Normal.TEntry")
        self.pcb_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.status_circle_pcb = ttk.Label(content_frame, text="●", font=("Arial", 20, "bold"),
                                           foreground="gray", anchor="center")
        self.status_circle_pcb.grid(row=1, column=2, sticky="ew", padx=5, pady=2)

        # Vincular validación (debounce para check_sn1)
        self.housing_entry.bind("<KeyRelease>", self.check_sn1)
        self.pcb_entry.bind("<KeyRelease>", self.check_sn2)

        # FRAME Chat y Botones -> fila=1
        chat_buttons_frame = ttk.Frame(bottom_frame)
        chat_buttons_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        chat_buttons_frame.columnconfigure(0, weight=3)
        chat_buttons_frame.columnconfigure(1, weight=1)
        chat_buttons_frame.rowconfigure(0, weight=1)

        self.chat_text = tk.Text(chat_buttons_frame, width=50, height=6, state="normal")
        self.chat_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_text.config(state="disabled")

        buttons_frame = ttk.Frame(chat_buttons_frame)
        buttons_frame.grid(row=0, column=1, sticky="n", padx=5, pady=5)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        reset_chat_button = ttk.Button(buttons_frame, text="RESET", command=...)
        reset_chat_button.grid(row=0, column=0, columnspan=2, sticky="ew",
                                padx=10, pady=10, ipadx=10, ipady=5)
        chat_status_label = ttk.Label(buttons_frame, text="User-BCNF", font=("Montserrat", 10))
        chat_status_label.grid(row=1, column=0, columnspan=2, sticky="ew",
                                padx=10, pady=10)
        pass_button = ttk.Button(buttons_frame, text="PASS", command=...)
        pass_button.grid(row=2, column=0, sticky="ew",
                         padx=10, pady=10, ipadx=10, ipady=5)
        fail_button = ttk.Button(buttons_frame, text="FAIL", command=...)
        fail_button.grid(row=2, column=1, sticky="ew",
                         padx=10, pady=10, ipadx=10, ipady=5)

        # ----------------------------------------------------------------
        # FRAME INFERIOR DE ESTADÍSTICAS -> fila=2 CON 5 COLUMNAS
        # ----------------------------------------------------------------
        stats_frame = ttk.Frame(self)
        stats_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=5)
        for i in range(5):
            stats_frame.columnconfigure(i, weight=1)

        pass_box = ttk.Frame(stats_frame, relief="solid", borderwidth=1)
        pass_box.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        pass_label = ttk.Label(pass_box, text="Pass: 0", font=("Montserrat", 12, "bold"))
        pass_label.pack(expand=True, fill="both", padx=10, pady=10)

        fail_box = ttk.Frame(stats_frame, relief="solid", borderwidth=1)
        fail_box.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        fail_label = ttk.Label(fail_box, text="Fail: 0", font=("Montserrat", 12, "bold"))
        fail_label.pack(expand=True, fill="both", padx=10, pady=10)

        fail_rate_box = ttk.Frame(stats_frame, relief="solid", borderwidth=1)
        fail_rate_box.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        fail_rate_label = ttk.Label(fail_rate_box, text="Failure Rate: 0%", font=("Montserrat", 12, "bold"))
        fail_rate_label.pack(expand=True, fill="both", padx=10, pady=10)

        reset_box = ttk.Frame(stats_frame, relief="solid", borderwidth=1)
        reset_box.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        reset_counters_button = ttk.Button(reset_box, text="Reset Counters")
        reset_counters_button.pack(expand=True, fill="both", padx=10, pady=10)

        test_time_box = ttk.Frame(stats_frame, relief="solid", borderwidth=1)
        test_time_box.grid(row=0, column=4, sticky="ew", padx=5, pady=5)
        test_time_label = ttk.Label(test_time_box, text="Test Time: 00:00", font=("Montserrat", 12, "bold"))
        test_time_label.pack(expand=True, fill="both", padx=10, pady=10)

    # ----------------------------------------------------------------
    # Método para validar la respuesta a BREQ
    # ----------------------------------------------------------------
    def check_breq_response(self, respuesta, sn):
        if respuesta.startswith("BCNF"):
            partes = respuesta.split('|')
            if len(partes) < 3:
                print("Respuesta BREQ incompleta:", partes)
                return False
            if f"id={sn}" in partes[1] and "status=PASS" in partes[2]:
                print(f"BREQ para {sn}: PASS")
                return True
            else:
                print(f"BREQ para {sn}: FAIL (ID o STATUS no coinciden)")
                return False
        else:
            print("Respuesta desconocida para BREQ:", respuesta)
            return False

    # ----------------------------------------------------------------
    # POPUP para PASS: Ventana negra con cuadro verde ("PASS") y botón "Cerrar"
    # ----------------------------------------------------------------
    def show_pass_popup(self):
        self.update_idletasks()
        pass_win = tk.Toplevel(self)
        pass_win.title("PASS")
        pass_win.configure(bg="black")
        pass_win.transient(self)
        pass_win.grab_set()

        green_frame = tk.Frame(pass_win, bg="green", padx=20, pady=20)
        green_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_pass = tk.Label(green_frame, text="PASS", bg="green", fg="white", font=("Arial", 24, "bold"))
        label_pass.pack(expand=True)

        close_button = ttk.Button(pass_win, text="Cerrar", command=pass_win.destroy)
        close_button.pack(pady=10)

        pass_win.update_idletasks()
        win_width = pass_win.winfo_reqwidth()
        win_height = pass_win.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        pass_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # ----------------------------------------------------------------
    # POPUP para FALLO: Ventana negra con cuadro rojo ("FAIL") y botón "Cerrar"
    # ----------------------------------------------------------------
    def show_fail_popup(self):
        self.update_idletasks()
        fail_win = tk.Toplevel(self)
        fail_win.title("FAIL")
        fail_win.configure(bg="black")
        fail_win.transient(self)
        fail_win.grab_set()

        red_frame = tk.Frame(fail_win, bg="red", padx=20, pady=20)
        red_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_fail = tk.Label(red_frame, text="FAIL", bg="red", fg="white", font=("Arial", 24, "bold"))
        label_fail.pack(expand=True)

        close_button = ttk.Button(fail_win, text="Cerrar", command=fail_win.destroy)
        close_button.pack(pady=10)

        fail_win.update_idletasks()
        win_width = fail_win.winfo_reqwidth()
        win_height = fail_win.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        fail_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # ----------------------------------------------------------------
    # POPUP para TIMEOUT: Ventana negra con cuadro amarillo ("TimeOut") y botón "Cerrar"
    # ----------------------------------------------------------------
    def show_timeout_popup(self):
        self.update_idletasks()
        timeout_win = tk.Toplevel(self)
        timeout_win.title("TIMEOUT")
        timeout_win.configure(bg="black")
        timeout_win.transient(self)
        timeout_win.grab_set()

        yellow_frame = tk.Frame(timeout_win, bg="yellow", padx=20, pady=20)
        yellow_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_timeout = tk.Label(yellow_frame, text="TimeOut", bg="yellow", fg="black", font=("Arial", 24, "bold"))
        label_timeout.pack(expand=True)

        close_button = ttk.Button(timeout_win, text="Cerrar", command=timeout_win.destroy)
        close_button.pack(pady=10)

        timeout_win.update_idletasks()
        win_width = timeout_win.winfo_reqwidth()
        win_height = timeout_win.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        timeout_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # ----------------------------------------------------------------
    # Debounce en check_sn1 para evitar múltiples ejecuciones
    # ----------------------------------------------------------------
    def check_sn1(self, event):
        if self._debounce_id:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(300, self._do_check_sn1)

    def _do_check_sn1(self):
        current = self.housing_entry.get().strip()
        if current == "":
            self.status_circle_housing.config(foreground="gray")
            return

        if len(current) >= 25:
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", "0"))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "STATION1")
            breq_sn1 = f"BREQ|process={process}|station={station}|id={current}"
            
            self.chat_text.config(state="normal")
            self.chat_text.insert("end", f"To SIM: {breq_sn1}\n")
            self.chat_text.see("end")
            
            try:
                resp = mes.send_message(ip, port, breq_sn1)
            except TimeoutError:
                self.chat_text.insert("end", "From SIM: Tiempo de conexion agotado.\n")
                self.chat_text.see("end")
                self.chat_text.config(state="disabled")
                self.show_timeout_popup()
                self.status_circle_housing.config(foreground="red")
                self.housing_entry.configure(style="Error.TEntry")
                return

            self.chat_text.insert("end", f"From SIM: {resp}\n")
            self.chat_text.see("end")
            self.chat_text.config(state="disabled")
            
            if self.check_breq_response(resp, current):
                self.status_circle_housing.config(foreground="green")
                self.housing_entry.configure(style="Valid.TEntry")
                self.pcb_entry.focus_set()
            else:
                self.show_fail_popup()
                self.status_circle_housing.config(foreground="red")
                self.housing_entry.configure(style="Error.TEntry")

    def check_sn2(self, event):
        current = self.pcb_entry.get().strip()
        if current == "":
            self.status_circle_pcb.config(foreground="gray")
            return

        if len(current) >= 25:
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", "0"))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "STATION1")
            breq_sn2 = f"BREQ|process={process}|station={station}|id={current}"
            
            self.chat_text.config(state="normal")
            self.chat_text.insert("end", f"To SIM: {breq_sn2}\n")
            self.chat_text.see("end")
            
            try:
                resp = mes.send_message(ip, port, breq_sn2)
            except TimeoutError:
                self.chat_text.insert("end", "From SIM: Tiempo de conexion agotado.\n")
                self.chat_text.see("end")
                self.chat_text.config(state="disabled")
                self.show_timeout_popup()
                self.status_circle_pcb.config(foreground="red")
                self.pcb_entry.configure(style="Error.TEntry")
                return

            self.chat_text.insert("end", f"From SIM: {resp}\n")
            self.chat_text.see("end")
            self.chat_text.config(state="disabled")
            
            if self.check_breq_response(resp, current):
                self.status_circle_pcb.config(foreground="green")
                self.pcb_entry.configure(style="Valid.TEntry")
                self.ejecutar_bc_mp()
            else:
                self.show_fail_popup()
                self.status_circle_pcb.config(foreground="red")
                self.pcb_entry.configure(style="Error.TEntry")

    def ejecutar_hermanacion(self):
        sn1 = self.housing_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()

        if len(sn1) < 25:
            self.show_fail_popup()
            return

        if len(sn2) < 25:
            self.show_fail_popup()
            return

        self.ejecutar_bc_mp()

    def ejecutar_bc_mp(self):
        sn1 = self.housing_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()
        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", ""))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "")
        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn2}|pid={sn1}|status=PASS"
        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            self.show_timeout_popup()
            return

        if self.check_breq_response(resp, sn1):
            self.status_circle_resp.config(foreground="green")
            self.chat_text.config(state="normal")
            self.chat_text.insert("end", "Hermanación exitosa.\n")
            self.chat_text.see("end")
            self.chat_text.config(state="disabled")
        else:
            self.status_circle_resp.config(foreground="red")
            self.chat_text.config(state="normal")
            self.chat_text.insert("end", "Hermanación FALLÓ.\n")
            self.chat_text.see("end")
            self.chat_text.config(state="disabled")
            self.show_fail_popup()

        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)

    def reset_entries(self):
        self.sn1_var.set("")
        self.sn2_var.set("")
        self.status_circle_housing.config(foreground="gray")
        self.status_circle_pcb.config(foreground="gray")
        self.status_circle_resp.config(foreground="gray")
        self.housing_entry.configure(style="Normal.TEntry")
        self.pcb_entry.configure(style="Normal.TEntry")
        self.housing_entry.focus_set()

if __name__ == "__main__":
    # Configuración de estilos para los Entry
    app = HermanacionApp()
    app.style.configure("Normal.TEntry", fieldbackground="white")
    app.style.configure("Error.TEntry", fieldbackground="red")
    app.style.configure("Valid.TEntry", fieldbackground="lightgreen")
    app.mainloop()
