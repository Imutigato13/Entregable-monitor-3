import json

class Pacientes:
    def __init__(self, ruta='data.json'):
        self.ruta = ruta
        self.cargar_pacientes()
    
    def validacion(self,usuario,contraseña):
        if usuario == 'admin123' and contraseña == 'contraseña123':
            return True
        else:
            return False

    def cargar_pacientes(self):
        try:
            with open(self.ruta, 'r') as file:
                self.pacientes = json.load(file)
        except FileNotFoundError:
            with open(self.ruta, 'w') as file:
                json.dump([], file)
            with open(self.ruta, 'r') as file:
                self.pacientes = json.load(file)

    def guardar_pacientes(self):
        with open(self.ruta, 'w') as file:
            json.dump(self.pacientes, file)

    def agregar_paciente(self, paciente):
        if any(p['cedula'] == paciente['cedula'] for p in self.pacientes):
            raise ValueError
        self.pacientes.append(paciente)
        self.guardar_pacientes()

    def eliminar_paciente(self, cedula):
        self.pacientes = [p for p in self.pacientes if p['cedula'] != cedula]
        self.guardar_pacientes()

    def buscar_paciente(self, busqueda):
        busqueda = busqueda.lower()
        return [p for p in self.pacientes if p['nombre'].lower().startswith(busqueda)]

    def get_pacientes(self):
        return self.pacientes 