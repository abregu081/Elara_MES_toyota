import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import MESxLog as mes
from datetime import datetime
import csv

class HermanacionApp(tk.Tk):
    def __init__(self):
        version = "1.1 06-05-2025"
        super().__init__()
        self.title(f"Elara - v{version}")
        self.state("zoomed")
        self.configure(bg="white")
        mes.load_settings()  # Carga la configuración desde MESxLog
        mes.load_titles()  # Carga los títulos desde Labels.cfg
        settings = mes.setting   #Traigo la data del archivo settings.cfg
        titulos = mes.titulos    #Traigo la data del archivo Labels.ini
        
        # Debounces para evitar múltiples validaciones
        self._debounce_id = None
        self._debounce_id_sn2 = None

        # BANDERA PARA LA HERMANACIÓN
        self.hermanacion_realizada = False
        # -----------------------
        # Contadores y cronómetro
        # -----------------------
        self.pass_count = 0
        self.fail_count = 0
        self.test_time_seconds = 0
        self._timer_job = None  # Guarda el id del after() para el cronómetro
        self.timer_started = False  # Indica si el cronómetro ya inició
        # -----------------------
        # Estilos de Entry (usando tema "clam")
        # -----------------------
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Normal.TEntry", fieldbackground="white")
        self.style.configure("Error.TEntry", fieldbackground="red")
        self.style.configure("Valid.TEntry", fieldbackground="lightgreen")

        # -----------------------
        # Layout principal
        # -----------------------
        # Filas del root:
        #   fila 0: top_frame (logos)
        #   fila 1: main_frame (contenido principal)
        #   fila 2: stats_frame (estadísticas)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)  # main_frame se expande
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        # ----------------------------------------------------------------
        # FRAME SUPERIOR (Logos / Título) – fondo blanco
        # ----------------------------------------------------------------
        top_frame = tk.Frame(self, bg="white")
        top_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=5)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        mirgor_path = os.path.join("assets", "Logo_Mirgor.png")
        if os.path.exists(mirgor_path):
            original_image = Image.open(mirgor_path)
            resized_image = original_image.resize((300, 100), Image.LANCZOS)
            self.logo_mirgor = ImageTk.PhotoImage(resized_image)
            logo_label_img = tk.Label(top_frame, image=self.logo_mirgor, bg="white")
            logo_label_img.grid(row=0, column=0, sticky="w", padx=10)

        title_font = ("Montserrat", 32, "bold")
        title_label = tk.Label(top_frame, text="TESTING UNAE", font=title_font, bg="white")
        title_label.grid(row=0, column=1, sticky="nsew", padx=10)

        clare_path = os.path.join("assets", "Elara Logo.png")
        if os.path.exists(clare_path):
            clare_logo = Image.open(clare_path)
            resized_clare = clare_logo.resize((150, 150), Image.LANCZOS)
            self.logo_clare = ImageTk.PhotoImage(resized_clare)
            logo_clare_label = tk.Label(top_frame, image=self.logo_clare, bg="white")
            logo_clare_label.grid(row=0, column=2, sticky="e", padx=10)

        # ----------------------------------------------------------------
        # FRAME PRINCIPAL (Entradas + Chat y Botones) – fondo blanco
        # ----------------------------------------------------------------
        main_frame = tk.Frame(self, bg="white")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=5)
        # main_frame se divide en dos filas:
        #   fila 0: content_frame (Entradas)
        #   fila 1: chat_buttons_frame (Chat y panel derecho)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # ---- FRAME DE ENTRADAS ----
        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.grid(row=0, column=0, sticky="ew", pady=5)
        content_frame.columnconfigure(0, weight=0)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=0)

        label_font = ("Montserrat", 16, "bold")
        entry_font = ("Montserrat", 20)

        self.sn1_var = tk.StringVar()
        self.sn2_var = tk.StringVar()
        self.SN1 = tk.Label(content_frame, text=titulos.get('SN1',''),font=label_font, bg="white")
        self.SN1.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        self.SN1_entry = ttk.Entry(content_frame, width=50, font=entry_font,
                                       textvariable=self.sn1_var, justify="center",
                                       style="Normal.TEntry")
        self.SN1_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.status_circle_housing = tk.Label(content_frame, text="●", font=("Arial", 20, "bold"),
                                              fg="gray", bg="white")
        self.status_circle_housing.grid(row=0, column=2, sticky="ew", padx=5, pady=2)

        self.SN2 = tk.Label(content_frame, text=titulos.get("SN2",""), font=label_font, bg="white")
        self.SN2.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        self.pcb_entry = ttk.Entry(content_frame, width=50, font=entry_font,
                                   textvariable=self.sn2_var, justify="center",
                                   style="Normal.TEntry")
        self.pcb_entry.config(state='disabled')
        self.pcb_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.status_circle_pcb = tk.Label(content_frame, text="●", font=("Arial", 20, "bold"),
                                          fg="gray", bg="white")
        self.status_circle_pcb.grid(row=1, column=2, sticky="ew", padx=5, pady=2)

        self.SN1_entry.bind("<KeyRelease>", self.check_sn1)
        self.pcb_entry.bind("<KeyRelease>", self.check_sn2)

        # ---- FRAME Chat + Botones + Config ----
        chat_buttons_frame = tk.Frame(main_frame, bg="white")
        chat_buttons_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        chat_buttons_frame.rowconfigure(0, weight=1)
        chat_buttons_frame.columnconfigure(0, weight=4)
        chat_buttons_frame.columnconfigure(1, weight=1)

        # Área de Chat (columna 0)
        self.chat_text = tk.Text(chat_buttons_frame, bg="white")
        self.chat_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_text.config(state="disabled")

        # Scrollbar vertical
        chat_scroll = ttk.Scrollbar(
            chat_buttons_frame,
            orient="vertical",
            command=self.chat_text.yview
        )
        chat_scroll.grid(row=0, column=0, sticky="nse", padx=(0,5), pady=5)
        self.chat_text.configure(yscrollcommand=chat_scroll.set)

        # Colores de log
        self.chat_text.tag_configure("outgoing", foreground="green")
        self.chat_text.tag_configure("incoming", foreground="blue")
        self.chat_text.tag_configure("default",  foreground="black")
        self.chat_text.config(state="disabled")

        # Panel derecho (columna 1)
        right_side_frame = tk.Frame(chat_buttons_frame, bg="white")
        right_side_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # Dividimos el panel derecho en tres filas:
        #   fila 0: Configuración (Modo, Unlock, settings)
        #   fila 1: Botones PASS y FAIL
        #   fila 2: Botón RESET
        right_side_frame.rowconfigure(0, weight=0)
        right_side_frame.rowconfigure(1, weight=0)
        right_side_frame.rowconfigure(2, weight=0)
        right_side_frame.columnconfigure(0, weight=1)

        # --- FRAME CONFIGURACIÓN (fila 0 del panel derecho)
        config_frame = tk.Frame(right_side_frame, bg="white", bd=2, relief="solid")
        config_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        config_frame.columnconfigure(0, weight=0)
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(2, weight=0)
        config_frame.columnconfigure(3, weight=0)

        # Etiqueta "Modo:"
        modo_label = tk.Label(config_frame, text="Modo:", font=("Montserrat", 12, "bold"), bg="white")
        modo_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Combobox para seleccionar el modo
        self.modo_var = tk.StringVar()
        self.modo_combobox = ttk.Combobox(config_frame, textvariable=self.modo_var,
                                          values=["Hermanado", "Hermanado Manual","Envio BCMP"], state="readonly", width=10)
        self.modo_combobox.current(0)
        self.modo_combobox.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # Al cambiar de modo, llamamos a la función para habilitar/deshabilitar PASS/FAIL
        self.modo_combobox.bind("<<ComboboxSelected>>", self._on_modo_changed)

        self.unlock_button = tk.Button(config_frame, text="Unlock", font=("Montserrat", 10), foreground="white", bg="blue",
                                       command=self.unlock_config)
        self.unlock_button.grid(row=0, column=2, sticky="w", padx=2, pady=2)

        self.save_button = tk.Button(config_frame, text="save", font=("Montserrat", 10, "bold"),
                                     command=self.guardar_config, foreground="white", bg="blue", state="disabled")
        self.save_button.grid(row=0, column=3, sticky="w", padx=2, pady=2)

        # Settings (fila 1 del config_frame)
        settings_frame = tk.Frame(config_frame, bg="white")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        settings_frame.columnconfigure(1, weight=1)

        self.ip_var = tk.StringVar()
        self.port_var = tk.StringVar()
        self.station_var = tk.StringVar()
        self.process_var = tk.StringVar()
        self.timeout_var = tk.StringVar()

        self.ip_var.set(settings.get("ip", ""))
        self.port_var.set(settings.get("port", ""))
        self.station_var.set(settings.get("station", ""))
        self.process_var.set(settings.get("process", ""))
        self.timeout_var.set(settings.get("timeout_mes", "6"))
        self.mensajeKey = settings.get("mensajeKey", "")
        self.SN1_text = titulos.get("SN1","")
        self.SN2_text = titulos.get("SN2","")

        config_labels = ["IP:", "Port:", "Station:", "Process:", "Timeout:"]
        config_vars = [self.ip_var, self.port_var, self.station_var, self.process_var, self.timeout_var]
        self.config_entries = {}
        for i, (lab_text, var) in enumerate(zip(config_labels, config_vars)):
            lbl = tk.Label(settings_frame, text=lab_text, font=("Montserrat", 12), bg="white")
            lbl.grid(row=i, column=0, sticky="nsew", padx=5, pady=2)
            ent = tk.Entry(settings_frame, textvariable=var, font=("Montserrat", 12), state="disabled")
            ent.grid(row=i, column=1, sticky="nsew", padx=5, pady=2)
            self.config_entries[lab_text] = ent

        # --- FRAME BOTONES PASS y FAIL (fila 1 del panel derecho)
        botones_frame = tk.Frame(right_side_frame, bg="white", bd=2, relief="solid")
        botones_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)

        titulo_botones_label = tk.Label(
            botones_frame, text="USER-BCMP", font=("Montserrat", 12, "bold"),
            bg="white", anchor="center"
        )
        titulo_botones_label.grid(
            row=0, column=0, columnspan=2, sticky="ew",
            padx=10, pady=10, ipadx=10, ipady=5
        )

        # Botones PASS y FAIL manual
        self.manual_pass_button = tk.Button(botones_frame, text="PASS", foreground="white", bg="green",
                                            command=lambda: self.manual_bcmp("PASS"))
        self.manual_pass_button.grid(row=1, column=0, sticky="ew", padx=10, pady=10, ipadx=10, ipady=5)

        self.manual_fail_button = tk.Button(botones_frame, text="FAIL", foreground="white", bg="red",
                                            command=lambda: self.manual_bcmp("FAIL"))
        self.manual_fail_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10, ipadx=10, ipady=5)

        # Por defecto, modo=Auto => deshabilitados
        self.manual_pass_button.config(state="disabled")
        self.manual_fail_button.config(state="disabled")

        # --- BOTÓN RESET (fila 2 del panel derecho)
        reset_button = tk.Button(right_side_frame, text="RESET", foreground="white", bg="blue" , command=self.reset_entries)
        reset_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10, ipadx=10, ipady=5)

        # ----------------------------------------------------------------
        # FRAME DE ESTADÍSTICAS – fondo blanco (Fila 3)
        # ----------------------------------------------------------------
        stats_frame = tk.Frame(self, bg="white")
        stats_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=5)
        for i in range(5):
            stats_frame.columnconfigure(i, weight=1)

        pass_box = tk.Frame(stats_frame, relief="solid", borderwidth=1, bg="white")
        pass_box.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.pass_label = tk.Label(pass_box, text="Pass: 0", font=("Montserrat", 12, "bold"), bg="white")
        self.pass_label.pack(expand=True, fill="both", padx=10, pady=10)

        fail_box = tk.Frame(stats_frame, relief="solid", borderwidth=1, bg="white")
        fail_box.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.fail_label = tk.Label(fail_box, text="Fail: 0", font=("Montserrat", 12, "bold"), bg="white")
        self.fail_label.pack(expand=True, fill="both", padx=10, pady=10)

        fail_rate_box = tk.Frame(stats_frame, relief="solid", borderwidth=1, bg="white")
        fail_rate_box.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.fail_rate_label = tk.Label(fail_rate_box, text="Failure Rate: 0%", font=("Montserrat", 12, "bold"), bg="white")
        self.fail_rate_label.pack(expand=True, fill="both", padx=10, pady=10)

        reset_box = tk.Frame(stats_frame, relief="solid", borderwidth=1, bg="white")
        reset_box.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        reset_counters_button = tk.Button(reset_box, text="Reset Counters", foreground="white", bg="blue", command=self.reset_counters)
        reset_counters_button.pack(expand=True, fill="both", padx=10, pady=10)

        test_time_box = tk.Frame(stats_frame, relief="solid", borderwidth=1, bg="white")
        test_time_box.grid(row=0, column=4, sticky="ew", padx=5, pady=5)
        self.test_time_label = tk.Label(test_time_box, text="Test Time: 00:00",
                                        font=("Montserrat", 12, "bold"), bg="white")
        self.test_time_label.pack(expand=True, fill="both", padx=10, pady=10)
    

    #  Funcion de cursor
    def auto_cursor(self,ventana):
        banderaa_do_check1 = 0
        self.focus_set(ventana)
        if banderaa_do_check1 == 0:
            self.after(1000, lambda: self.focus_set(ventana))
            self._debounce_id = self.after(0.5, self._do_check_sn1)
            banderaa_do_check1 = 1
        else:
            bandeera_do_check1 = 0
    # ----------------------------------------------------------------
    # Centrar popups para pass/fail/timeout
    # ----------------------------------------------------------------
    def _center_popup(self, win):
        # Llamado en cada popup para forzar centrado
        self.update_idletasks()
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

    # ----------------------------------------------------------------
    # Selector de modos
    # ----------------------------------------------------------------
    def _on_modo_changed(self, event=None):
        modo_actual = self.modo_var.get()
        if modo_actual == "Hermanado Manual":
            self.manual_pass_button.config(state="normal")
            self.manual_fail_button.config(state="normal")
            self.SN1.config(text=f"{self.SN1_text}")
            self.SN2.config(text=f"{self.SN2_text}")
            self.pcb_entry.grid()
            self.SN2.grid()

        elif modo_actual == "Envio BCMP":
            self.pcb_entry.grid_remove()
            self.SN2.grid_remove()
            self.SN1.config(text=f"{self.SN1_text}")
            self.manual_pass_button.config(state="disabled")
            self.manual_fail_button.config(state="disabled")
        else:
            self.manual_pass_button.config(state="disabled")
            self.manual_fail_button.config(state="disabled")
            self.SN1.config(text=f"{self.SN1_text}")
            self.SN2.config(text=f"{self.SN2_text}")
            self.pcb_entry.grid()
            self.SN2.grid()

        self.SN1_entry.focus_set()

    # ----------------------------------------------------------------
    # BCMP manual con status=PASS o FAIL
    # ----------------------------------------------------------------
    def manual_bcmp(self, status="PASS"):
        """
        Envía BCMP manual con el status indicado (PASS o FAIL).
        Actualiza contadores y popups según la respuesta BACK.
        """
        sn1 = self.SN1_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()

        if not sn1 or not sn2:
            self._log_message("No hay SN1 o SN2 para enviar BCMP manual.")
            return

        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", ""))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "")
        mensajeKey = mes.setting.get("mensajeKey", "")


        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn2}|pid={sn1}|status={status}|msgT={mensajeKey}"
        self._log_message(f"To SIM (Manual BCMP): {bcmp_msg}")

        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            self._log_message("From SIM: Tiempo de conexion agotado. (Manual BCMP)")
            self.show_timeout_popup()
            self.fail_count += 1
            self.stop_test_time()
            self.timer_started = False
            self.update_stats()
            return

        self._log_message(f"From SIM: {resp}")

        # Validamos “BACK|id=sn1|status=PASS”
        if self.check_back_response(resp, sn1):
            # PASÓ
            self.show_pass_popup(auto_close_ms=3000)
            self._log_message("Manual BCMP => PASS.")
            self.hermanacion_realizada = True
            self.pass_count += 1
        else:
            # FALLÓ
            self.show_fail_popup()
            self._log_message("Manual BCMP => FAIL.")
            self.fail_count += 1

        self.stop_test_time()
        self.timer_started = False
        self.update_stats()

        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)

    # ----------------------------------------------------------------
    # Función para desbloquear/lockear la configuración
    # (Sin cambios en la lógica.)
    # ----------------------------------------------------------------
    def unlock_config(self):
        current_state = self.config_entries["IP:"].cget("state")
        if current_state == "disabled":
            for ent in self.config_entries.values():
                ent.config(state="normal")
            self.save_button.config(state="normal")
            self.unlock_button.config(text="Lock")
        else:
            for ent in self.config_entries.values():
                ent.config(state="disabled")
            self.save_button.config(state="disabled")
            self.unlock_button.config(text="Unlock")

    #limpiar el chat
    def _clear_log(self):
        """Limpia todo el histórico del chat."""
        self.chat_text.config(state="normal")
        self.chat_text.delete("1.0", "end")
        self.chat_text.config(state="disabled")
    # ----------------------------------------------------------------
    # Función para guardar la configuración en setting.cfg
    # (Sin cambios en la lógica.)
    # ----------------------------------------------------------------
    def guardar_config(self):
        """
        Guarda la configuración en setting.cfg y recarga los valores en la app.
        """
        config_data = (
            f"ip={self.ip_var.get()}\n"
            f"port={self.port_var.get()}\n"
            f"station={self.station_var.get()}\n"
            f"process={self.process_var.get()}\n"
            f"timeout_mes={self.timeout_var.get()}\n"
            f"modo={self.modo_var.get()}\n"
        )

        try:
            with open("setting.cfg", "w") as f:
                f.write(config_data)
            
            
            mes.load_settings() 
            mes.setting.update({
                "ip": self.ip_var.get(),
                "port": self.port_var.get(),
                "station": self.station_var.get(),
                "process": self.process_var.get(),
                "timeout_mes": self.timeout_var.get(),
                "modo": self.modo_var.get()
            })

            self._log_message("Configuración guardada y recargada correctamente.")
        except Exception as e:
            self._log_message(f"Error al guardar configuración: {e}")

    # ----------------------------------------------------------------
    # Cronómetro (Test Time)
    # (Sin cambios en la lógica.)
    # ----------------------------------------------------------------
    def update_test_time(self):
        minutes = self.test_time_seconds // 60
        seconds = self.test_time_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.test_time_label.config(text=f"Test Time: {time_str}")
        self.test_time_seconds += 1
        self._timer_job = self.after(1000, self.update_test_time)

    def stop_test_time(self):
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    # ----------------------------------------------------------------
    # Funciones para actualizar contadores de estadísticas
    # (Sin cambios en la lógica.)
    # ----------------------------------------------------------------
    def update_stats(self):
        total = self.pass_count + self.fail_count
        if total > 0:
            failure_rate = (self.fail_count / total) * 100
        else:
            failure_rate = 0
        self.pass_label.config(text=f"Pass: {self.pass_count}")
        self.fail_label.config(text=f"Fail: {self.fail_count}")
        self.fail_rate_label.config(text=f"Failure Rate: {failure_rate:.0f}%")

    def reset_counters(self):
        self.pass_count = 0
        self.fail_count = 0
        self.test_time_seconds = 0
        self.update_stats()

    # ----------------------------------------------------------------
    # Validación BREQ (Leo la respuesta del BNCF BUSCANDO el PASS)
    # ----------------------------------------------------------------
    def check_breq_response(self, respuesta, sn):
        if respuesta.startswith("BCNF"):
            partes = respuesta.split('|')
            if len(partes) >= 2:
                if "status=PASS" in partes[2]: 
                    return True
        return False

    # ----------------------------------------------------------------
    # Popup PASS
    # + Centramos con _center_popup
    # ----------------------------------------------------------------
    def show_pass_popup(self, auto_close_ms=None):
        pass_win = tk.Toplevel(self)
        pass_win.title("PASS")
        pass_win.configure(bg="black")
        pass_win.transient(self)
        pass_win.grab_set()

        green_frame = tk.Frame(pass_win, bg="green", padx=20, pady=20)
        green_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_pass = tk.Label(green_frame, text="PASS", bg="green", fg="white", font=("Arial", 24, "bold"))
        label_pass.pack(expand=True)

        close_button = ttk.Button(pass_win, text="Cerrar", command=lambda: [pass_win.destroy(), self.SN1_entry.focus_set()])
        close_button.pack(pady=10)

        # Forzamos centrado
        self._center_popup(pass_win)

        if auto_close_ms is not None:
            pass_win.after(auto_close_ms, lambda: [pass_win.destroy(), self.SN1_entry.focus_set()])


    # ----------------------------------------------------------------
    # Popup FAIL
    # + Centramos con _center_popup
    # ----------------------------------------------------------------
    def show_fail_popup(self):
        fail_win = tk.Toplevel(self)
        fail_win.title("FAIL")
        fail_win.configure(bg="black")
        fail_win.transient(self)
        fail_win.grab_set()

        red_frame = tk.Frame(fail_win, bg="red", padx=20, pady=20)
        red_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_fail = tk.Label(red_frame, text="FAIL", bg="red", fg="white", font=("Arial", 24, "bold"))
        label_fail.pack(expand=True)
        
        def close_popup():
            self.reset_entries()
            fail_win.destroy()
            self.SN1_entry.focus_set()

        close_button = ttk.Button(fail_win, text="Cerrar", command=close_popup)
        close_button.pack(pady=10)
        
        # Forzamos centrado del popup
        self._center_popup(fail_win)
    # ----------------------------------------------------------------
    # Popup TIMEOUT
    # + Centramos con _center_popup
    # ----------------------------------------------------------------
    def show_timeout_popup(self):
        timeout_win = tk.Toplevel(self)
        timeout_win.title("TIMEOUT")
        timeout_win.configure(bg="black")
        timeout_win.transient(self)
        timeout_win.grab_set()

        yellow_frame = tk.Frame(timeout_win, bg="yellow", padx=20, pady=20)
        yellow_frame.pack(expand=True, fill="both", padx=50, pady=50)

        label_timeout = tk.Label(yellow_frame, text="TimeOut", bg="yellow", fg="black", font=("Arial", 24, "bold"))
        label_timeout.pack(expand=True)

        def close_popup():
            self.reset_entries()
            timeout_win.destroy()
            self.SN1_entry.focus_set()

        close_button = ttk.Button(timeout_win, text="Cerrar", command=close_popup)
        close_button.pack(pady=10)
        
        # Forzamos centrado del popup
        self._center_popup(timeout_win)
        
    # ----------------------------------------------------------------
    # Lógica check_sn1 / check_sn2 (BREQ) + hermanación = auto
    # ----------------------------------------------------------------
    def check_sn1(self, event):
        if self._debounce_id:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(300, self._do_check_sn1)

    def _do_check_sn1(self):
        modo_actual = self.modo_var.get()
        sn1 = self.SN1_entry.get().strip()
        self.pcb_entry.focus_set()
        if not sn1:
            self.status_circle_housing.config(fg="gray")
            return
        if len(sn1) >= 25:
            self.chat_text.see("end")
            if not self.timer_started:
                self.test_time_seconds = 0
                self.update_test_time()
                self.timer_started = True

            # Realizamos BREQ
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", ""))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "")
            mensajeKey = mes.setting.get("mensajeKey", "")

            breq_sn1 = f"BREQ|process={process}|station={station}|id={sn1}|msgT={mensajeKey}"
            self._log_message(f"To SIM: {breq_sn1}")

            try:
                resp = mes.send_message(ip, port, breq_sn1)
            except TimeoutError:
                self._log_message("From SIM: Tiempo de conexion agotado.")
                self.show_timeout_popup()
                self.status_circle_housing.config(fg="red")
                self.SN1.configure(style="Error.TEntry")
                self.fail_count += 1
                self.stop_test_time()
                self.timer_started = False
                self.update_stats()
                return

            self._log_message(f"From SIM: {resp}")

            # Validamos la respuesta BREQ
            if self.check_breq_response(resp, sn1):
                self.status_circle_housing.config(fg="green")
                self.SN1_entry.configure(style="Valid.TEntry")
                self.SN1_entry.config(state="readonly")

                # ---------------------------
                #  DIFERENCIA AQUI:
                #  Si el modo es Version Simple => pasamos DIRECTO a BCMP
                # ---------------------------
                if modo_actual == "Envio BCMP":
                    self.ejecutar_bcmp_simple(sn1)
                else:
                    # Modo "Auto" => habilitar PCB
                    # Modo "Manual" => habilitar PCB y/o otras lógicas
                    self.pcb_entry.config(state="normal")
                    self.pcb_entry.focus_set()
            else:
                self.show_fail_popup()
                self.status_circle_housing.config(fg="red")
                self.SN1_entry.configure(style="Error.TEntry", state="normal")
                self.pcb_entry.config(state="disabled")
                self.fail_count += 1
                self.update_stats()

    def check_sn2(self, event):
        if self._debounce_id_sn2:
            self.after_cancel(self._debounce_id_sn2)
        self._debounce_id_sn2 = self.after(300, self._do_check_sn2)
        

    def _do_check_sn2(self):
        if self.pcb_entry.cget("state") == "disabled":
            return

        current = self.pcb_entry.get().strip()
        if not current:
            self.status_circle_pcb.config(fg="gray")
            return

        if len(current) >= 25:
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", ""))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "")
            mensajeKey = mes.setting.get("mensajeKey", "")

            breq_sn2 = f"BREQ|process={process}|station={station}|id={current}|msgT={mensajeKey}"
            self._log_message(f"To SIM: {breq_sn2}")

            try:
                resp = mes.send_message(ip, port, breq_sn2)
            except TimeoutError:
                self._log_message("From SIM: Tiempo de conexion agotado.")
                self.show_timeout_popup()
                self.status_circle_pcb.config(fg="red")
                self.pcb_entry.configure(style="Error.TEntry")
                self.fail_count += 1
                self.stop_test_time()
                self.timer_started = False
                self.update_stats()
                return

            self._log_message(f"From SIM: {resp}")

            if self.check_breq_response(resp, current):
                self.status_circle_pcb.config(fg="green")
                self.pcb_entry.configure(style="Valid.TEntry")
                self.pcb_entry.config(state="readonly")
                # Modo AUTO => se llama a ejecutar_bc_mp con PASS
                self.ejecutar_bc_mp()
            else:
                self.show_fail_popup()
                self.status_circle_pcb.config(fg="red")
                self.pcb_entry.configure(style="Error.TEntry", state="normal")
                self.fail_count += 1
            self.update_stats()

    # ----------------------------------------------------------------
    #                       Hermanación de dos SN
    # ----------------------------------------------------------------
    def ejecutar_hermanacion(self):
        sn1 = self.SN1_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()
        if len(sn1) < 25 or len(sn2) < 25:
            self.show_fail_popup()
            return
        self.ejecutar_bc_mp()

    def ejecutar_bc_mp(self):
        if self.hermanacion_realizada:
            return
        sn1 = self.SN1_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()
        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", ""))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "")
        mensajeKey = mes.setting.get("mensajeKey", "")
        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn2}|pid={sn1}|status=PASS|msgT={mensajeKey}"
        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            self._log_message("From SIM: Tiempo de conexion agotado.")
            self.show_timeout_popup()
            self.fail_count += 1
            self.stop_test_time()
            self.timer_started = False
            self.update_stats()
            return
        
        self._log_message(f"To SIM: {bcmp_msg}")
        self._log_message(f"From SIM: {resp}")

        if self.check_back_response(resp, sn1):
            self._log_message("Hermanación exitosa.")
            self.show_pass_popup(auto_close_ms=3000)
            self.hermanacion_realizada = True
            self.pass_count += 1
            self.stop_test_time()
            self.timer_started = False
            self.update_stats()
            self.guardar_log_csv(sn1, "PASS", bcmp_msg, resp)
        else:
            self._log_message("Fallo en la Hermanacion.")
            self.show_fail_popup()
            self.fail_count += 1
            self.stop_test_time()
            self.timer_started = False
            self.update_stats()
            self.guardar_log_csv(sn1, "FAIL", bcmp_msg, resp)

        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)

    def check_back_response(self, respuesta, sn1):
        if respuesta.startswith("BACK"):
            partes = respuesta.split('|')
            if len(partes) >= 1 and "status=PASS" in partes[2]:
                return True
        return False
    
    # ----------------------------------------------------------------
    # Ejecutar bcmp para version simple / un solo sn de Envio BCMP
    # ----------------------------------------------------------------
    def ejecutar_bcmp_simple(self, sn1):
        """
        Envía BCMP en modo 'Versión Simple' y procesa la respuesta usando check_back_response.
        BCMP|process={process}|station={station}|id={sn1}|status=PASS
        """
        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", ""))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "")
        mensajeKey = mes.setting.get("mensajeKey", "")

        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn1}|status=PASS|msgT={mensajeKey}"
        self._log_message(f"To SIM: {bcmp_msg}")

        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            self._log_message("From SIM: Tiempo de conexion agotado")
            self.show_timeout_popup()
            self.fail_count += 1
            self.stop_test_time()
            self.timer_started = False
            self.update_stats()
            return

        self._log_message(f"From SIM: {resp}")
        self.SN1_entry.focus_force()

        # Verificamos la respuesta con check_back_response en lugar de check_bcmp_response
        if self.check_back_response(resp, sn1):
            # PASS
            self.show_pass_popup(auto_close_ms=3000)
            self.pass_count += 1
            self.guardar_log_csv(sn1, "PASS", bcmp_msg, resp)
        else:
            # FAIL
            self.show_fail_popup()
            self.fail_count += 1
            self.guardar_log_csv(sn1, "FAIL", bcmp_msg, resp)

        self.stop_test_time()
        self.timer_started = False
        self.update_stats()

        # Espera de N segundos y reset
        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)
        self.pcb_entry.focus_set()

    # ----------------------------------------------------------------
    # Reset- metodo para validar las secuencias y metodos
    # ----------------------------------------------------------------
    def reset_entries(self):
        self.sn1_var.set("")
        self.sn2_var.set("")
        self.status_circle_housing.config(fg="gray")
        self.status_circle_pcb.config(fg="gray")
        self.SN1_entry.configure(style="Normal.TEntry", state="normal")
        self.pcb_entry.configure(style="Normal.TEntry", state="disabled")
        self.hermanacion_realizada = False
        self.test_time_seconds = 0
        self.timer_started = False
        self.stop_test_time()
        self.SN1.focus_set()

    # ----------------------------------------------------------------
    # Log - muestra los mensajes en tiempo real y en directo
    # ----------------------------------------------------------------
    def _log_message(self, msg: str):
        """
        • T<S  (verde)   → envíos
        • S>T  (azul)    → respuestas
        • Negro          → otros
        Autoscroll solo si el usuario está al final.
        """
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if msg.startswith("To SIM:"):
            contenido = msg[len("To SIM:"):].strip()
            linea, tag = f"T<S {contenido} {ts}", "outgoing"
        elif msg.startswith("From SIM:"):
            contenido = msg[len("From SIM:"):].strip()
            linea, tag = f"S>T {contenido} {ts}", "incoming"
        else:
            linea, tag = f"{msg} {ts}", "default"

        # ¿El visor ya está en la parte inferior?
        autoscroll = self.chat_text.yview()[1] >= 0.999

        self.chat_text.config(state="normal")
        self.chat_text.insert("end", linea + "\n", tag)
        if autoscroll:
            self.chat_text.see("end")
        self.chat_text.config(state="disabled")

    def update_stats(self):
        total = self.pass_count + self.fail_count
        if total > 0:
            rate = (self.fail_count / total) * 100
        else:
            rate = 0
        self.pass_label.config(text=f"Pass: {self.pass_count}")
        self.fail_label.config(text=f"Fail: {self.fail_count}")
        self.fail_rate_label.config(text=f"Failure Rate: {rate:.0f}%")

    #Funcion para guardar los log
    def guardar_log_csv(self, sn1, resultado, envio_sim, devolucion_sim):
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        carpeta_base = os.path.join("C:\\DGS\\Log", resultado.upper())
        os.makedirs(carpeta_base, exist_ok=True)
        archivo_nombre = f"{sn1}_{fecha_hora}.csv"
        ruta_completa = os.path.join(carpeta_base, archivo_nombre)

        with open(ruta_completa, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["SN1", "Resultado", "Fecha", "Hora", "Envio a SIM", "Devolucion de SIM"])
            writer.writerow([
                sn1,
                resultado,
                datetime.now().strftime("%Y-%m-%d"),
                datetime.now().strftime("%H:%M:%S"),
                envio_sim,
                devolucion_sim
            ])

if __name__ == "__main__":
    app = HermanacionApp()
    app.pass_count = 0
    app.fail_count = 0
    app.test_time_seconds = 0
    app.update_stats()
    app.mainloop()
