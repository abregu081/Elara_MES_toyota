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

        # Configurar la ventana para que se adapte al tamaño
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # ----------------------------------------------------------------
        # FRAME SUPERIOR (Logotipos, Título, etc.)
        # ----------------------------------------------------------------
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=10)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        # Cargar y redimensionar imágenes
        mirgor_path = os.path.join("assets", "Logo_Mirgor.png")
        original_image = Image.open(mirgor_path)
        resized_image = original_image.resize((300, 100), Image.LANCZOS)
        self.logo_mirgor = ImageTk.PhotoImage(resized_image)

        clare_path = os.path.join("assets", "Logo Clare.png")
        clare_logo = Image.open(clare_path)
        resized_clare = clare_logo.resize((200, 150), Image.LANCZOS)
        self.logo_clare = ImageTk.PhotoImage(resized_clare)

        logo_label_img = ttk.Label(top_frame, image=self.logo_mirgor)
        logo_label_img.grid(row=0, column=0, sticky="w", padx=10)
        title_font = ("Montserrat", 32, "bold")
        title_label = ttk.Label(top_frame, text="TESTING UNAE", font=title_font)
        title_label.grid(row=0, column=1, sticky="nsew", padx=10)
        logo_clare_label = ttk.Label(top_frame, image=self.logo_clare)
        logo_clare_label.grid(row=0, column=2, sticky="e", padx=10)

        # ----------------------------------------------------------------
        # FRAME INFERIOR (Housing, PCB, Respuesta y Botón)
        # ----------------------------------------------------------------
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=1)

        content_frame = ttk.Frame(bottom_frame)
        content_frame.grid(row=0, column=0, sticky="nsew", pady=20)
        # Ajustar pesos para expandir
        content_frame.columnconfigure(0, weight=0)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=0)

        label_font = ("Montserrat", 16, "bold")
        entry_font = ("Montserrat", 9)

        # Variables asociadas a los seriales
        self.sn1_var = tk.StringVar()
        self.sn2_var = tk.StringVar()

        # -- Fila 0: Housing (SN1)
        housing_label = ttk.Label(content_frame, text="Housing:", font=label_font)
        housing_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.housing_entry = ttk.Entry(content_frame, width=50, font=entry_font, textvariable=self.sn1_var)
        self.housing_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.status_circle_housing = ttk.Label(content_frame, text="●", font=("Arial", 20, "bold"), foreground="gray")
        self.status_circle_housing.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # -- Fila 1: PCB (SN2)
        pcb_label = ttk.Label(content_frame, text="PCB:", font=label_font)
        pcb_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.pcb_entry = ttk.Entry(content_frame, width=50, font=entry_font, textvariable=self.sn2_var)
        self.pcb_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.status_circle_pcb = ttk.Label(content_frame, text="●", font=("Arial", 20, "bold"), foreground="gray")
        self.status_circle_pcb.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # -- Fila 2: Respuesta
        resp_label = ttk.Label(content_frame, text="Respuesta:", font=label_font)
        resp_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.resp_textbox = tk.Text(content_frame, width=50, height=2, font=entry_font)
        self.resp_textbox.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.status_circle_resp = ttk.Label(content_frame, text="●", font=("Arial", 20, "bold"), foreground="gray")
        self.status_circle_resp.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # -- Fila 3: Botón "Hermanar"
        self.hermanar_button = ttk.Button(content_frame, text="Hermanar", command=self.ejecutar_hermanacion)
        self.hermanar_button.grid(row=3, column=0, columnspan=3, pady=15)

        #Frame pensado para las Respuestas del servidor.
        history_frame = ttk.Frame(self)
        history_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)

        # Configuramos dos filas: fila 0 para la cabecera y fila 1 para el Treeview
        history_frame.rowconfigure(1, weight=1)  # Le damos menos peso para achicarlo
        history_frame.columnconfigure(0, weight=1)

        tree_frame = ttk.Frame(history_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=("Fecha_Hora", "Estacion", "Tipo", "Serie", "Mensaje"),
            show="headings",
            height=5  # Ajusta 'height' para achicar el cuadro
        )

        # Vincular validación en tiempo real (opcional)
        self.housing_entry.bind("<KeyRelease>", self.check_sn1)
        self.pcb_entry.bind("<KeyRelease>", self.check_sn2)
    
    def Show_pass_popup(self, message= ""):
        """
        Funcion para la creacion del pop pass para la validacion de placas de las mismas
        -Agregar la funcion de concatenado para la misma

        """
        pass_win = tk.Toplevel(self)
        pass_win.title("PASS")
        pass_win.configure(bg="black")
        pass_win.transient(self)
        pass_win.grab_set()

        # ----- Contenido del popup -----
        # Usamos pack para que el toplevel se ajuste según el contenido.
        label_fail = tk.Label(pass_win, text="PASS", bg="black", fg="green", font=("Arial", 24, "bold"))
        label_fail.pack(pady=(10, 5), padx=10)

        if message:
            label_msg = tk.Label(pass_win, text=message, bg="black", fg="white", font=("Arial", 12), wraplength=300)
            label_msg.pack(pady=5, padx=10)

        close_button = ttk.Button(pass_win, text="Salir", command=pass_win.destroy)
        close_button.pack(pady=(5, 10))


    def show_fail_popup(self, message=""):
        """
        Popup centrado en la ventana principal, sin tamaño fijo,
        que se adapta automáticamente al contenido.

        - Muestra "FAIL" en grande
        - Muestra 'message' debajo (si existe).
        - Tiene un botón "Cerrar" para que el usuario lo cierre.
        """
        fail_win = tk.Toplevel(self)
        fail_win.title("FAIL")
        fail_win.configure(bg="black")
        fail_win.transient(self)
        fail_win.grab_set()

        # ----- Contenido del popup -----
        # Usamos pack para que el toplevel se ajuste según el contenido.
        label_fail = tk.Label(fail_win, text="FAIL", bg="black", fg="red", font=("Arial", 24, "bold"))
        label_fail.pack(pady=(10, 5), padx=10)

        if message:
            label_msg = tk.Label(fail_win, text=message, bg="black", fg="white", font=("Arial", 12), wraplength=300)
            label_msg.pack(pady=5, padx=10)

        close_button = ttk.Button(fail_win, text="Salir", command=fail_win.destroy)
        close_button.pack(pady=(5, 10))

        # ----- Calcular tamaño requerido y centrarlo -----
        fail_win.update_idletasks()  # Calcula dimensiones requeridas
        win_width = fail_win.winfo_reqwidth()
        win_height = fail_win.winfo_reqheight()

        # Coordenadas para centrar en la ventana principal
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (win_width // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (win_height // 2)

        # Ajustamos posición (sin forzar ancho/alto, así se mantiene flexible)
        fail_win.geometry(f"+{x}+{y}")

    def check_sn1(self, event):
        """
        Valida el contenido del Entry de Housing (sn1).
        Si tiene >= 25 chars, se envía BREQ y se actualiza el estado.
        """
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
            try:
                resp = mes.send_message(ip, port, breq_sn1)
            except TimeoutError:
                msg = f"Tiempo de espera agotado al conectar para Housing {current}.\nBorre el contenido para reintentar."
                self.resp_textbox.delete("1.0", "end")
                self.resp_textbox.insert("1.0", msg)
                self.show_fail_popup(msg)
                self.status_circle_housing.config(foreground="red")
                return

            if mes.check_breq_response(resp, current):
                self.status_circle_housing.config(foreground="green")
                # Opcionalmente, mover foco a SN2
                self.pcb_entry.focus_set()
            else:
                msg = f"BREQ para Housing {current} FALLÓ.\nBorre el contenido para reintentar."
                self.resp_textbox.delete("1.0", "end")
                self.resp_textbox.insert("1.0", msg)
                self.show_fail_popup(msg)
                self.status_circle_housing.config(foreground="red")

    def check_sn2(self, event):
        """
        Valida el contenido del Entry de PCB (sn2).
        Si tiene >= 25 chars, se envía BREQ y, si pasa, llama a BCMP.
        """
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
            try:
                resp = mes.send_message(ip, port, breq_sn2)
            except TimeoutError:
                msg = f"Tiempo de espera agotado al conectar para PCB {current}.\nBorre el contenido para reintentar."
                self.resp_textbox.delete("1.0", "end")
                self.resp_textbox.insert("1.0", msg)
                self.show_fail_popup(msg)
                self.status_circle_pcb.config(foreground="red")
                return

            if mes.check_breq_response(resp, current):
                self.status_circle_pcb.config(foreground="green")
                # Cuando SN2 está OK, se hace BCMP
                self.ejecutar_bc_mp()
            else:
                msg = f"BREQ para PCB {current} FALLÓ.\nBorre el contenido para reintentar."
                self.resp_textbox.delete("1.0", "end")
                self.resp_textbox.insert("1.0", msg)
                self.show_fail_popup(msg)
                self.status_circle_pcb.config(foreground="red")

    def ejecutar_hermanacion(self):
        """
        Al presionar el botón 'Hermanar':
        - Verifica manualmente si ambos SN tienen la longitud mínima (25 chars).
        - Si no, muestra fail_popup con mensaje de error.
        - Si sí, llama a ejecutar_bc_mp().
        """
        sn1 = self.housing_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()

        # Limpiar la respuesta previa
        self.resp_textbox.delete("1.0", "end")

        if len(sn1) < 25:
            error_msg = f"Housing serial inválido: {sn1}\nDebe tener al menos 25 caracteres."
            self.resp_textbox.insert("1.0", error_msg)
            self.show_fail_popup(error_msg)
            return

        if len(sn2) < 25:
            error_msg = f"PCB serial inválido: {sn2}\nDebe tener al menos 25 caracteres."
            self.resp_textbox.insert("1.0", error_msg)
            self.show_fail_popup(error_msg)
            return

        # Si ambos son válidos, llamamos a ejecutar_bc_mp directamente.
        self.ejecutar_bc_mp()

    def ejecutar_bc_mp(self):
        """
        Envía BCMP con id=sn2 y pid=sn1, y verifica la respuesta.
        """
        sn1 = self.housing_entry.get().strip()
        sn2 = self.pcb_entry.get().strip()
        ip = mes.setting.get("ip", "")
        port = int(mes.setting.get("port", "0"))
        process = mes.setting.get("process", "")
        station = mes.setting.get("station", "STATION1")

        bcmp_msg = f"BCMP|process={process}|station={station}|id={sn2}|pid={sn1}|status=PASS"
        try:
            resp = mes.send_message(ip, port, bcmp_msg)
        except TimeoutError:
            error_msg = "Tiempo de espera agotado al conectar para BCMP.\nIntente nuevamente."
            self.resp_textbox.delete("1.0", "end")
            self.resp_textbox.insert("1.0", error_msg)
            self.show_fail_popup(error_msg)
            return

        if mes.check_bcmp_response(resp, sn1, sn2):
            self.status_circle_resp.config(foreground="green")
            self.resp_textbox.delete("1.0", "end")
            self.resp_textbox.insert("1.0", "Hermanación exitosa.\n")
        else:
            self.status_circle_resp.config(foreground="red")
            error_msg = f"Hermanación FALLÓ.\nConsola: {resp}\n"
            self.resp_textbox.delete("1.0", "end")
            self.resp_textbox.insert("1.0", error_msg)
            self.show_fail_popup(error_msg)

        # Reset automático después de un periodo
        periodo = int(mes.setting.get("periodo", 10)) * 1000
        self.after(periodo, self.reset_entries)

    def reset_entries(self):
        """
        Reinicia los campos y el estado de los indicadores.
        """
        self.sn1_var.set("")
        self.sn2_var.set("")
        self.resp_textbox.delete("1.0", "end")
        self.status_circle_housing.config(foreground="gray")
        self.status_circle_pcb.config(foreground="gray")
        self.status_circle_resp.config(foreground="gray")
        self.housing_entry.focus_set()

if __name__ == "__main__":
    app = HermanacionApp()
    app.mainloop()
