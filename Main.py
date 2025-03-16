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

        self._debounce_id = None

        # -----------------------
        # Estilos de Entry
        # -----------------------
        self.style = ttk.Style()
        self.style.configure("Normal.TEntry", fieldbackground="white")
        self.style.configure("Error.TEntry", fieldbackground="red")
        self.style.configure("Valid.TEntry", fieldbackground="lightgreen")

        # -----------------------
        # Layout principal
        # -----------------------
        self.rowconfigure(1, weight=1)  # Fila 1 se expande
        self.rowconfigure(2, weight=0)  # Fila 2 fija (stats)
        self.columnconfigure(0, weight=1)

        # ----------------------------------------------------------------
        # FRAME SUPERIOR (Logotipos, Título, etc.)
        # ----------------------------------------------------------------
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=5)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        mirgor_path = os.path.join("assets", "Logo_Mirgor.png")
        if os.path.exists(mirgor_path):
            original_image = Image.open(mirgor_path)
            resized_image = original_image.resize((300, 100), Image.LANCZOS)
            self.logo_mirgor = ImageTk.PhotoImage(resized_image)
            logo_label_img = ttk.Label(top_frame, image=self.logo_mirgor, anchor="center")
            logo_label_img.grid(row=0, column=0, sticky="w", padx=10)

        title_font = ("Montserrat", 32, "bold")
        title_label = ttk.Label(top_frame, text="TESTING UNAE", font=title_font, anchor="center")
        title_label.grid(row=0, column=1, sticky="nsew", padx=10)

        clare_path = os.path.join("assets", "Elara Logo.png")
        if os.path.exists(clare_path):
            clare_logo = Image.open(clare_path)
            resized_clare = clare_logo.resize((150, 150), Image.LANCZOS)
            self.logo_clare = ImageTk.PhotoImage(resized_clare)
            logo_clare_label = ttk.Label(top_frame, image=self.logo_clare, anchor="center")
            logo_clare_label.grid(row=0, column=2, sticky="e", padx=10)

        # ----------------------------------------------------------------
        # FRAME PRINCIPAL (fila=1): Entradas + Chat + Botones
        # ----------------------------------------------------------------
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=5)
        bottom_frame.rowconfigure(0, weight=0)
        bottom_frame.rowconfigure(1, weight=1)
        bottom_frame.columnconfigure(0, weight=1)

        # FRAME de Entradas (Housing, PCB)
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

        self.housing_entry = ttk.Entry(
            content_frame, width=50, font=entry_font,
            textvariable=self.sn1_var, justify="center",
            style="Normal.TEntry"
        )
        self.housing_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        self.status_circle_housing = ttk.Label(
            content_frame, text="●", font=("Arial", 20, "bold"),
            foreground="gray", anchor="center"
        )
        self.status_circle_housing.grid(row=0, column=2, sticky="ew", padx=5, pady=2)

        pcb_label = ttk.Label(content_frame, text="PCB:", font=label_font, anchor="center")
        pcb_label.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

        self.pcb_entry = ttk.Entry(
            content_frame, width=50, font=entry_font,
            textvariable=self.sn2_var, justify="center",
            style="Normal.TEntry"
        )
        # Lo creamos "disabled" hasta que SN1 sea PASS
        self.pcb_entry.config(state='disabled')
        self.pcb_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        self.status_circle_pcb = ttk.Label(
            content_frame, text="●", font=("Arial", 20, "bold"),
            foreground="gray", anchor="center"
        )
        self.status_circle_pcb.grid(row=1, column=2, sticky="ew", padx=5, pady=2)

        # Vincular validaciones (debounce)
        self.housing_entry.bind("<KeyRelease>", self.check_sn1)
        self.pcb_entry.bind("<KeyRelease>", self.check_sn2)

        # FRAME Chat y Botones
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

        reset_chat_button = ttk.Button(buttons_frame, text="RESET", command=self.reset_entries)
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
        # FRAME DE ESTADÍSTICAS (fila=2)
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
    # BREQ => BCNF
    # ----------------------------------------------------------------
    def check_breq_response(self, respuesta, sn):
        """
        Espera: BCNF|id=<sn>|status=PASS
        """
        if respuesta.startswith("BCNF"):
            partes = respuesta.split('|')
            if len(partes) >= 3:
                if f"id={sn}" in partes[1] and "status=PASS" in partes[2]:
                    return True
        return False

    # ----------------------------------------------------------------
    # Popups (Pass, Fail, Timeout)
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

        close_button = ttk.Button(pass_win, text="Cerrar", command=pass_win.destroy)
        close_button.pack(pady=10)

        # Centrado
        self.after(0, lambda: self._center_popup(pass_win))

        # Cierre automático si se desea
        if auto_close_ms is not None:
            pass_win.after(auto_close_ms, pass_win.destroy)

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

        close_button = ttk.Button(fail_win, text="Cerrar", command=fail_win.destroy)
        close_button.pack(pady=10)

        self.after(0, lambda: self._center_popup(fail_win))

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

        close_button = ttk.Button(timeout_win, text="Cerrar", command=timeout_win.destroy)
        close_button.pack(pady=10)

        self.after(0, lambda: self._center_popup(timeout_win))

    # ----------------------------------------------------------------
    # Centrar Popups
    # ----------------------------------------------------------------
    def _center_popup(self, popup_win):
        self.update_idletasks()
        popup_win.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        win_width = popup_win.winfo_width()
        win_height = popup_win.winfo_height()

        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2

        popup_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # ----------------------------------------------------------------
    # Debounce SN1
    # ----------------------------------------------------------------
    def check_sn1(self, event):
        if self._debounce_id:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(300, self._do_check_sn1)

    def _do_check_sn1(self):
        current = self.housing_entry.get().strip()
        if not current:
            self.status_circle_housing.config(foreground="gray")
            return

        if len(current) >= 25:
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", "0"))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "STATION1")
            breq_sn1 = f"BREQ|process={process}|station={station}|id={current}"

            self._log_message(f"To SIM: {breq_sn1}")

            try:
                resp = mes.send_message(ip, port, breq_sn1)
            except TimeoutError:
                # Timeout => NO pintamos ni en rojo ni nada
                self._log_message("From SIM: Tiempo de conexion agotado.")
                self.show_timeout_popup()
                return

            self._log_message(f"From SIM: {resp}")

            if self.check_breq_response(resp, current):
                # SN1 OK => pintamos Housing en verde
                self.status_circle_housing.config(foreground="green")
                self.housing_entry.configure(style="Valid.TEntry")
                # Habilitar SN2
                self.pcb_entry.config(state='normal')
                self.pcb_entry.focus_set()
            else:
                # SN1 FAIL => popup fail, pintamos en rojo
                self.show_fail_popup()
                self.status_circle_housing.config(foreground="red")
                self.housing_entry.configure(style="Error.TEntry")
                # Asegurarnos de que SN2 siga deshabilitado
                self.pcb_entry.config(state='disabled')

    # ----------------------------------------------------------------
    # Debounce SN2
    # ----------------------------------------------------------------
    def check_sn2(self, event):
        current = self.pcb_entry.get().strip()
        if not current:
            self.status_circle_pcb.config(foreground="gray")
            return

        if len(current) >= 25:
            ip = mes.setting.get("ip", "")
            port = int(mes.setting.get("port", "0"))
            process = mes.setting.get("process", "")
            station = mes.setting.get("station", "STATION1")
            breq_sn2 = f"BREQ|process={process}|station={station}|id={current}"

            self._log_message(f"To SIM: {breq_sn2}")

            try:
                resp = mes.send_message(ip, port, breq_sn2)
            except TimeoutError:
                # Timeout => NO se pinta en rojo
                self._log_message("From SIM: Tiempo de conexion agotado.")
                self.show_timeout_popup()
                return

            self._log_message(f"From SIM: {resp}")

            if self.check_breq_response(resp, current):
                # SN2 PASS => pintamos en verde y lanzamos BCMP
                self.status_circle_pcb.config(foreground="green")
                self.pcb_entry.configure(style="Valid.TEntry")
                # Ejecutamos hermanación SOLO si SN1 y SN2 = PASS
                self.ejecutar_bc_mp()
            else:
                # SN2 FAIL => popup fail y pintamos en rojo
                self.show_fail_popup()
                self.status_circle_pcb.config(foreground="red")
                self.pcb_entry.configure(style="Error.TEntry")

    # ----------------------------------------------------------------
    # Verificar BACK (respuesta a BCMP)
    # ----------------------------------------------------------------
    def check_back_response(self, respuesta, sn1):
        """
        Esperamos: BACK|id=<sn1>|status=PASS
        """
        if respuesta.startswith("BACK"):
            partes = respuesta.split('|')
            if len(partes) >= 3:
                if f"id={sn1}" in partes[1] and "status=PASS" in partes[2]:
                    return True
        return False

    # ----------------------------------------------------------------
    # Ejecutar BCMP (hermanación)
    # ----------------------------------------------------------------
    def ejecutar_bc_mp(self):
        sn1 = self.housing_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()

        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", "0"))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "STATION1")
        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn2}|pid={sn1}|status=PASS"

        self._log_message(f"To SIM: {bcmp_msg}")

        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            self._log_message("From SIM: Tiempo de conexion agotado.")
            self.show_timeout_popup()
            return

        self._log_message(f"From SIM: {resp}")

        # Validamos "BACK|id=sn1|status=PASS"
        if self.check_back_response(resp, sn1):
            # Hermanación exitosa => PASS popup (3s)
            self._log_message("Hermanación exitosa.")
            self.show_pass_popup(auto_close_ms=3000)
        else:
            self._log_message("Hermanación FALLÓ.")
            self.show_fail_popup()

        # Limpieza tras periodo
        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)

    # ----------------------------------------------------------------
    # Reset
    # ----------------------------------------------------------------
    def reset_entries(self):
        self.sn1_var.set("")
        self.sn2_var.set("")

        self.status_circle_housing.config(foreground="gray")
        self.status_circle_pcb.config(foreground="gray")

        self.housing_entry.configure(style="Normal.TEntry")
        self.pcb_entry.configure(style="Normal.TEntry", state='disabled')
        # Al resetear, SN2 vuelve a estar deshabilitado hasta que sn1 pase

        self.chat_text.config(state="normal")
        self.chat_text.delete("1.0", tk.END)
        self.chat_text.config(state="disabled")

        self.housing_entry.focus_set()

    # ----------------------------------------------------------------
    # Log a chat_text
    # ----------------------------------------------------------------
    def _log_message(self, msg):
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", msg + "\n")
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")
        
if __name__ == "__main__":
    app = HermanacionApp()
    app.mainloop()
