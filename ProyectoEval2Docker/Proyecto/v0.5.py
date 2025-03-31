import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class Circuito:
    def __init__(self):
        self.reservas = []  # Lista para almacenar las reservas
        self.cargar_reservas()

    def cargar_reservas(self):
        if os.path.exists("reservas.json"):
            with open("reservas.json", "r") as file:
                self.reservas = json.load(file)

    def guardar_reservas(self):
        with open("reservas.json", "w") as file:
            json.dump(self.reservas, file)

    def mostrar_reservas(self):
        if not self.reservas:
            return "No hay reservas en este momento."
        else:
            reservas_str = "Reservas actuales:\n"
            for reserva in self.reservas:
                reservas_str += f"Fecha: {reserva['fecha']}, Hora: {reserva['hora']}, Cliente: {reserva['nombre']}\n"
            return reservas_str.strip()

    def agregar_reserva(self, fecha, hora, nombre):
        if not fecha or not hora or not nombre:
            return "Todos los campos son obligatorios."
        
        # Verificar si la fecha es válida y no está en el pasado
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        if datetime.strptime(fecha, "%d/%m/%Y") < datetime.strptime(fecha_actual, "%d/%m/%Y"):
            return "No se pueden hacer reservas en fechas pasadas."

        # Verificar si la hora es válida
        hora_actual = datetime.now().strftime("%H:%M")
        if fecha == fecha_actual and datetime.strptime(hora, "%H:%M") < datetime.strptime(hora_actual, "%H:%M"):
            return "No se pueden hacer reservas en horas pasadas."

        # Verificar si ya hay una reserva en la misma fecha y hora
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                return "La hora ya está reservada. Por favor, elige otra."
        
        # Agregar la nueva reserva
        self.reservas.append({'fecha': fecha, 'hora': hora, 'nombre': nombre})
        self.guardar_reservas()  # Guardar reservas al agregar
        return "Reserva añadida con éxito."

    def cancelar_reserva(self, fecha, hora):
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                self.reservas.remove(reserva)
                self.guardar_reservas()  # Guardar reservas al cancelar
                return "Reserva cancelada con éxito."
        return "No se encontró ninguna reserva para cancelar."

class App:
    def __init__(self, root):
        self.circuito = Circuito()
        self.root = root
        self.root.title("Agenda de Citas para Circuito de Velocidad")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.label = tk.Label(root, text="Bienvenido a la Agenda de Citas", font=("Arial", 16), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.mostrar_btn = tk.Button(root, text="Mostrar Reservas", command=self.mostrar_reservas, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.mostrar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.agregar_btn = tk.Button(root, text="Agregar Reserva", command=self.agregar_reserva, bg="#2196F3", fg="white", font=("Arial", 12))
        self.agregar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.cancelar_btn = tk.Button(root, text="Cancelar Reserva", command=self.cancelar_reserva, bg="#f44336", fg="white", font=("Arial", 12))
        self.cancelar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.salir_btn = tk.Button(root, text="Salir", command=self.salir, bg="#9E9E9E", fg="white", font=("Arial",  12))
        self.salir_btn.pack(pady=5, padx=20, fill=tk.X)

    def mostrar_reservas(self):
        reservas = self.circuito.mostrar_reservas()
        messagebox.showinfo("Reservas", reservas)

    def agregar_reserva(self):
        self.ventana_agregar = tk.Toplevel(self.root)
        self.ventana_agregar.title("Agregar Reserva")
        self.ventana_agregar.geometry("300x250")
        self.ventana_agregar.configure(bg="#f0f0f0")

        tk.Label(self.ventana_agregar, text="Fecha (DD/MM/AAAA):", bg="#f0f0f0").pack(pady=5)
        self.fecha_entry = tk.Entry(self.ventana_agregar)
        self.fecha_entry.pack(pady=5)
        self.fecha_entry.focus_set()

        tk.Label(self.ventana_agregar, text="Hora (HH:MM):", bg="#f0f0f0").pack(pady=5)
        self.hora_entry = tk.Entry(self.ventana_agregar)
        self.hora_entry.pack(pady=5)

        tk.Label(self.ventana_agregar, text="Nombre:", bg="#f0f0f0").pack(pady=5)
        self.nombre_entry = tk.Entry(self.ventana_agregar)
        self.nombre_entry.pack(pady=5)

        tk.Button(self.ventana_agregar, text="Agregar", command=self.confirmar_agregar, bg="#2196F3", fg="white").pack(pady=10)

    def confirmar_agregar(self):
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()
        nombre = self.nombre_entry.get()
        resultado = self.circuito.agregar_reserva(fecha, hora, nombre)
        messagebox.showinfo("Resultado", resultado)
        self.ventana_agregar.destroy()

    def cancelar_reserva(self):
        self.ventana_cancelar = tk.Toplevel(self.root)
        self.ventana_cancelar.title("Cancelar Reserva")
        self.ventana_cancelar.geometry("300x200")
        self.ventana_cancelar.configure(bg="#f0f0f0")

        tk.Label(self.ventana_cancelar, text="Fecha (DD/MM/AAAA):", bg="#f0f0f0").pack(pady=5)
        self.fecha_cancelar_entry = tk.Entry(self.ventana_cancelar)
        self.fecha_cancelar_entry.pack(pady=5)
        self.fecha_cancelar_entry.focus_set()

        tk.Label(self.ventana_cancelar, text="Hora (HH:MM):", bg="#f0f0f0").pack(pady=5)
        self.hora_cancelar_entry = tk.Entry(self.ventana_cancelar)
        self.hora_cancelar_entry.pack(pady=5)

        tk.Button(self.ventana_cancelar, text="Cancelar", command=self.confirmar_cancelar, bg="#f44336", fg="white").pack(pady=10)

    def confirmar_cancelar(self):
        fecha = self.fecha_cancelar_entry.get()
        hora = self.hora_cancelar_entry.get()
        resultado = self.circuito.cancelar_reserva(fecha, hora)
        messagebox.showinfo("Resultado", resultado)
        self.ventana_cancelar.destroy()

    def salir(self):
        self.circuito.guardar_reservas()  # Guardar reservas al salir
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop() 