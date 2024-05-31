from modelo import *
from vista import *

class Controlador:
    def __init__(self) -> None:
        self.modelo = Pacientes()
        self.aplicacion = QApplication([])

    def inicio(self):
        self.ventana_log_in()

    def ventana_log_in(self):
        self.log_in = QTlogin(self)
        self.log_in.show()
        self.aplicacion.exec_()
    
    def validacion(self,usuario,contraseña):
        if self.modelo.validacion(usuario,contraseña) == True:
            return True

    def ventana_principal(self):
        self.principal = QTprincipal(self)
        self.principal.show()

    def agregar_paciente(self,nombre,apellido,edad,cedula):
        try:
            paciente = {
                'nombre': nombre,
                'apellido': apellido,
                'edad': edad,
                'cedula': cedula
            }
            self.modelo.agregar_paciente(paciente)
            return paciente
        except ValueError:
            return False
    
    def buscar_paciente(self,busqueda):
        return self.modelo.buscar_paciente(busqueda)
    
    def eliminar_paciente(self,cedula):
        self.modelo.eliminar_paciente(cedula)

    def get_pacientes(self):
        return self.modelo.get_pacientes()
    
    def logout(self):
        self.principal.close()
        self.ventana_log_in()