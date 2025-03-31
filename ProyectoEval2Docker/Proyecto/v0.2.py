import tkinter as tk
from tkinter import messagebox, simpledialog

class Circuito:
    def __init__(self):
        self.reservas = []  # Lista para almacenar las reservas

    def mostrar_reservas(self):
        if not self.reservas:
            return "No hay reservas en este momento."
        else:
            reservas_str = "Reservas actuales:\n"
            for reserva in self.reservas:
                reservas_str += f"Fecha: {reserva['fecha']}, Hora: {reserva['hora']}, Cliente: {reserva['nombre']}\n"
            return reservas_str.strip()

    def agregar_reserva(self, fecha, hora, nombre):
        # Verificar si la hora ya está reservada
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                return "La hora ya está reservada. Por favor, elige otra."
        
        # Agregar la nueva reserva
        self.reservas.append({'fecha': fecha, 'hora': hora, 'nombre': nombre})
        return "Reserva añadida con éxito."

    def cancelar_reserva(self, fecha, hora):
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                self.reservas.remove(reserva)
                return "Reserva cancelada con éxito."
        return "No se encontró ninguna reserva para cancelar."

class App:
    def __init__(self, root):
        self.circuito = Circuito()
        self.root = root
        self.root.title("Agenda de Citas para Circuito de Velocidad")

        self.label = tk.Label(root, text="Bienvenido a la Agenda de Citas", font=("Arial", 16))
        self.label.pack(pady=10)

        self.mostrar_btn = tk.Button(root, text="Mostrar Reservas", command=self.mostrar_reservas)
        self.mostrar_btn.pack(pady=5)

        self.agregar_btn = tk.Button(root, text="Agregar Reserva", command=self.agregar_reserva)
        self.agregar_btn.pack(pady=5)

        self.cancelar_btn = tk.Button(root, text="Cancelar Reserva", command=self.cancelar_reserva)
        self.cancelar_btn.pack(pady=5)

        self.salir_btn = tk.Button(root, text="Salir", command=root.quit)
        self.salir_btn.pack(pady=5)

    def mostrar_reservas(self):
        reservas = self.circuito.mostrar_reservas()
        messagebox.showinfo("Reservas", reservas)

    def agregar_reserva(self):
        fecha = simpledialog.askstring("Fecha", "Ingresa la fecha (DD/MM/AAAA):")
        hora = simpledialog.askstring("Hora", "Ingresa la hora (HH:MM):")
        nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        resultado = self.circuito.agregar_reserva(fecha, hora, nombre)
        messagebox.showinfo("Resultado", resultado)

    def cancelar_reserva(self):
        fecha = simpledialog.askstring("Fecha", "Ingresa la fecha de la reserva a cancelar (DD/MM/AAAA):")
        hora = simpledialog.askstring("Hora", "Ingresa la hora de la reserva a cancelar (HH:MM):")
        resultado = self.circuito.cancelar_reserva(fecha, hora)
        messagebox.showinfo("Resultado", resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()