from modelo import *
from vista import *
from PyQt5.QtWidgets import QApplication

class Controlador:
    def __init__(self):
        self.modelo = Pacientes()
        self.aplicacion = QApplication([])

    def inicio(self):
        self.ventana_log_in()

    def ventana_log_in(self):
        self.log_in = QTlogin(self.login)
        self.log_in.show()
        self.aplicacion.exec_()

    def login(self, usuario, contraseña):
        if usuario == 'admin123' and contraseña == 'contraseña123':
            self.ventana_principal()
            return True
        return False

    def ventana_principal(self):
        self.principal = QTprincipal(self.modelo, self.logout)
        self.principal.show()

    def logout(self):
        self.ventana_log_in()