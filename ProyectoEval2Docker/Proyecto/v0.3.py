import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

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
        
        # Verificar si la hora ya está reservada
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                return "La hora ya está reservada. Por favor, elige otra."
        
        # Agregar la nueva reserva
        self.reservas.append({'fecha': fecha, 'hora': hora, 'nombre': nombre})
        self.guardar_reservas()  # Guardar reservas al agregar
        return "Reserva añadida con éxito."

    def cancelar_reservas(self, fecha, hora):
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

        self.mostrar_btn = tk.Button(root, text="Mostrar Reservas", command=self.mostrar_reservas, bg="#4CAF50", fg="white")
        self.mostrar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.agregar_btn = tk.Button(root, text="Agregar Reserva", command=self.agregar_reserva, bg="#2196F3", fg="white")
        self.agregar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.cancelar_btn = tk.Button(root, text="Cancelar Reserva", command=self.cancelar_reservas, bg="#f44336", fg="white")
        self.cancelar_btn.pack(pady=5, padx=20, fill=tk.X)

        self.salir_btn = tk.Button(root, text="Salir", command=self.salir, bg="#9E9E9E", fg="white")
        self.salir_btn.pack(pady=5, padx=20, fill=tk.X)

    def mostrar_reservas(self):
        reservas = self.circuito.mostrar_reservas()
        messagebox.showinfo("Reservas", reservas)

    def agregar_reserva(self):
        fecha = simpledialog.askstring("Fecha", "Ingresa la fecha (DD/MM/AAAA):")
        hora = simpledialog.askstring("Hora", "Ingresa la hora (HH:MM):")
        nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        resultado = self.circuito.agregar_reserva(fecha, hora, nombre)
        messagebox.showinfo("Resultado", resultado)

    def cancelar_reservas(self):
        fecha = simpledialog.askstring("Fecha", "Ingresa la fecha de la reserva a cancelar (DD/MM/AAAA):")
        hora = simpledialog.askstring("Hora", "Ingresa la hora de la reserva a cancelar (HH:MM):")
        resultado = self.circuito.cancelar_reservas(fecha, hora)
        messagebox.showinfo("Resultado", resultado)

    def salir(self ):
        self.circuito.guardar_reservas()  # Guardar reservas al salir
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()