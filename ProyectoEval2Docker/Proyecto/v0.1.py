class Circuito:
    def __init__(self):
        self.reservas = []  # Lista para almacenar las reservas

    def mostrar_reservas(self):
        if not self.reservas:
            print("No hay reservas en este momento.")
        else:
            print("Reservas actuales:")
            for reserva in self.reservas:
                print(f"Fecha: {reserva['fecha']}, Hora: {reserva['hora']}, Cliente: {reserva['nombre']}")

    def agregar_reserva(self, fecha, hora, nombre):
        # Verificar si la hora ya está reservada
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                print("La hora ya está reservada. Por favor, elige otra.")
                return
        
        # Agregar la nueva reserva
        self.reservas.append({'fecha': fecha, 'hora': hora, 'nombre': nombre})
        print("Reserva añadida con éxito.")

    def cancelar_reserva(self, fecha, hora):
        for reserva in self.reservas:
            if reserva['fecha'] == fecha and reserva['hora'] == hora:
                self.reservas.remove(reserva)
                print("Reserva cancelada con éxito.")
                return
        print("No se encontró ninguna reserva para cancelar.")

def main():
    circuito = Circuito()
    
    while True:
        print("\n--- Agenda de Citas para Circuito de Velocidad ---")
        print("1. Mostrar reservas")
        print("2. Agregar reserva")
        print("3. Cancelar reserva")
        print("4. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            circuito.mostrar_reservas()
        elif opcion == '2':
            fecha = input("Ingresa la fecha (DD/MM/AAAA): ")
            hora = input("Ingresa la hora (HH:MM): ")
            nombre = input("Ingresa tu nombre: ")
            circuito.agregar_reserva(fecha, hora, nombre)
        elif opcion == '3':
            fecha = input("Ingresa la fecha de la reserva a cancelar (DD/MM/AAAA): ")
            hora = input("Ingresa la hora de la reserva a cancelar (HH:MM): ")
            circuito.cancelar_reserva(fecha, hora)
        elif opcion == '4':
            print("Saliendo de la agenda.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()