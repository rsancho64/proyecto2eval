import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
import re

class Circuito:
    def __init__(self):
        """Inicializa la clase Circuito y carga las reservas desde un archivo JSON."""
        self.reservas = []  # Lista para almacenar las reservas
        self.cargar_reservas()

    def cargar_reservas(self):
        """Carga las reservas desde un archivo JSON si existe."""
        if os.path.exists("reservas.json"):
            with open("reservas.json", "r") as file:
                try:
                    self.reservas = json.load(file)
                except json.JSONDecodeError:
                    self.reservas = []

    def guardar_reservas(self):
        """Guarda las reservas en un archivo JSON."""
        with open("reservas.json", "w") as file:
            json.dump(self.reservas, file, indent=4)

    def mostrar_reservas(self):
        """Devuelve una cadena con todas las reservas actuales."""
        if not self.reservas:
            return "No hay reservas en este momento."
        else:
            return "\n".join(
                f"Fecha: {reserva['fecha']}, Hora: {reserva['hora']}, Cliente: {reserva['nombre']}"
                for reserva in self.reservas
            )

    def agregar_reserva(self, fecha, hora, nombre):
        """Agrega una nueva reserva si la fecha y la hora son válidas y no están ocupadas."""
        if not fecha or not hora or not nombre:
            return "Todos los campos son obligatorios."

        if not self.validar_fecha(fecha):
            return "Formato de fecha inválido. Usa DD/MM/AAAA."
        if not self.validar_hora(hora):
            return "Formato de hora inválido. Usa HH:MM."

        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        if datetime.strptime(fecha, "%d/%m/%Y") < datetime.strptime(fecha_actual, "%d/%m/%Y"):
            return "No se pueden hacer reservas en fechas pasadas."

        hora_actual = datetime.now().strftime("%H:%M")
        if fecha == fecha_actual and datetime.strptime(hora, "%H:%M") < datetime.strptime(hora_actual, "%H:%M"):
            return "No se pueden hacer reservas en horas pasadas."

        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                return "La hora ya está reservada. Por favor, elige otra."

        self.reservas.append({'fecha': fecha, 'hora': hora, 'nombre': nombre})
        self.guardar_reservas()
        return "Reserva añadida con éxito."

    def cancelar_reserva(self, fecha, hora):
        """Cancela una reserva existente si coincide con la fecha y hora dadas."""
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                self.reservas.remove(reserva)
                self.guardar_reservas()
                return "Reserva cancelada con éxito."
        return "No se encontró ninguna reserva para cancelar."

    def validar_fecha(self, fecha):
        """Valida que la fecha tenga el formato DD/MM/AAAA."""
        return bool(re.match(r'^\d{2}/\d{2}/\d{4}$', fecha))

    def validar_hora(self, hora):
        """Valida que la hora tenga el formato HH:MM."""
        return bool(re.match(r'^\d{2}:\d{2}$', hora))

class App:
    def __init__(self, root):
        """Inicializa la interfaz gráfica del programa."""
        self.circuito = Circuito()
        self.root = root
        self.root.title("Agenda de Citas para Circuito de Velocidad")
        self.root.geometry("500x400")
        self.root.configure(bg="#80DEEA")

        # Configurar estilos de los widgets
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10, background="#388E3C", foreground="white")
        style.configure("TLabel", font=("Arial", 14), background="#80DEEA", foreground="#004D40")

        # Título
        self.label = ttk.Label(root, text="Bienvenido a la Agenda de Citas", font=("Arial", 20, "bold"), background="#80DEEA", foreground="#004D40")
        self.label.pack(pady=20)

        # Botones
        self.mostrar_btn = ttk.Button(root, text="Mostrar Reservas", command=self.mostrar_reservas, style="TButton")
        self.mostrar_btn.pack(pady=10, padx=20, fill=tk.X)

        self.agregar_btn = ttk.Button(root, text="Agregar Reserva", command=self.agregar_reserva, style="TButton")
        self.agregar_btn.pack(pady=10, padx=20, fill=tk.X)

        self.cancelar_btn = ttk.Button(root, text="Cancelar Reserva", command=self.cancelar_reserva, style="TButton")
        self.cancelar_btn.pack(pady=10, padx=20, fill=tk.X)

    def mostrar_reservas(self):
        """Muestra las reservas en una ventana emergente."""
        reservas = self.circuito.mostrar_reservas()
        messagebox.showinfo("Reservas", reservas)

    def agregar_reserva(self):
        """Abre el formulario para agregar una reserva."""
        self.abrir_formulario("Agregar Reserva", self.procesar_agregar)

    def cancelar_reserva(self):
        """Abre el formulario para cancelar una reserva."""
        self.abrir_formulario("Cancelar Reserva", self.procesar_cancelar, cancelar=True)

    def abrir_formulario(self, titulo, callback, cancelar=False):
        """Abre un formulario emergente para ingresar datos de reserva o cancelación."""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("300x200")
        ventana.configure(bg="#B2DFDB")

        ttk.Label(ventana, text="Fecha (DD/MM/AAAA):").pack(pady=5)
        fecha_entry = ttk.Entry(ventana)
        fecha_entry.pack(pady=5)

        ttk.Label(ventana, text="Hora (HH:MM):").pack(pady=5)
        hora_entry = ttk.Entry(ventana)
        hora_entry.pack(pady=5)

        if not cancelar:
            ttk.Label(ventana, text="Nombre:").pack(pady=5)
            nombre_entry = ttk.Entry(ventana)
            nombre_entry.pack(pady=5)

        def confirmar():
            fecha = fecha_entry.get()
            hora = hora_entry.get()
            if cancelar:
                mensaje = self.circuito.cancelar_reserva(fecha, hora)
            else:
                nombre = nombre_entry.get()
                mensaje = self.circuito.agregar_reserva(fecha, hora, nombre)
            messagebox.showinfo(titulo, mensaje)
            ventana.destroy()

        ttk.Button(ventana, text="Confirmar", command=confirmar, style="TButton").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
