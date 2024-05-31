from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
                             QMessageBox, QApplication)
import sys

class QTlogin(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.QTlog()

    def QTlog(self):
        self.setWindowTitle("Login")
        self.display = QVBoxLayout()

        self.usuario_t = QLabel("Usuario:")
        self.usuario_r = QLineEdit()
        self.contraseña_t = QLabel("Contraseña:")
        self.contraseña_r = QLineEdit()
        self.contraseña_r.setEchoMode(QLineEdit.Password)
        self.boton_login = QPushButton("Login")
        self.boton_login.clicked.connect(self.login)

        self.display.addWidget(self.usuario_t)
        self.display.addWidget(self.usuario_r)
        self.display.addWidget(self.contraseña_t)
        self.display.addWidget(self.contraseña_r)
        self.display.addWidget(self.boton_login)

        self.setLayout(self.display)

    def login(self):
        usuario = self.usuario_r.text()
        contraseña = self.contraseña_r.text()
        if self.controlador.validacion(usuario, contraseña):
            self.close()
            self.controlador.ventana_principal()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        

class QTprincipal(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.QTprincipal()

    def QTprincipal(self):
        self.setWindowTitle("Gestión de Pacientes")
        self.setGeometry(100, 100, 720, 480)

        self.widget_principal = QWidget()
        self.setCentralWidget(self.widget_principal)
        self.display = QVBoxLayout()
        
        self.HUD_superior = QHBoxLayout()
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")
        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")
        self.edad = QLineEdit()
        self.edad.setPlaceholderText("Edad")
        self.cedula = QLineEdit()
        self.cedula.setPlaceholderText("Cedula")

        self.boton_agregar = QPushButton("Agregar Paciente")
        self.boton_agregar.clicked.connect(self.agregar_paciente)

        self.HUD_superior.addWidget(self.nombre)
        self.HUD_superior.addWidget(self.apellido)
        self.HUD_superior.addWidget(self.edad)
        self.HUD_superior.addWidget(self.cedula)
        self.HUD_superior.addWidget(self.boton_agregar)
        self.display.addLayout(self.HUD_superior)

        self.busqueda = QHBoxLayout()
        self.busqueda_r = QLineEdit()
        self.busqueda_r.setPlaceholderText("Buscar por nombre")
        self.boton_busqueda = QPushButton("Buscar")
        self.boton_busqueda.clicked.connect(self.buscar_paciente)

        self.busqueda.addWidget(self.busqueda_r)
        self.busqueda.addWidget(self.boton_busqueda)

        self.display.addLayout(self.busqueda)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Apellido", "Edad", "Cedula","Eliminar"])
        

        self.boton_logout = QPushButton("Logout")
        self.boton_logout.clicked.connect(self.logout)

        self.display.addWidget(self.boton_logout)
        
        self.widget_principal.setLayout(self.display)
        self.cargar_pacientes()

    def cargar_pacientes(self):
        self.tabla.setRowCount(0)
        pacientes = self.controlador.get_pacientes()
        for paciente in pacientes:
            self.tabla_pacientes(paciente)

    def agregar_paciente(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        edad = self.edad.text()
        cedula = self.cedula.text()
        if not (nombre and apellido and edad and cedula):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return
        else:
            paciente = self.controlador.agregar_paciente(nombre,apellido,edad,cedula)
            if paciente == False:
                QMessageBox.warning(self, "Error", str(ValueError('Cedula ya registrada')))
            else:
                self.nombre.clear()
                self.apellido.clear()
                self.edad.clear()
                self.cedula.clear()
                QMessageBox.information(self, "Operacion exitosa", "Se agrego al paciente correctamente")
                self.tabla_pacientes(paciente)

    def buscar_paciente(self):
        busqueda = self.busqueda_r.text()
        encuentro = self.controlador.buscar_paciente(busqueda)
        self.tabla.setRowCount(0)
        for paciente in encuentro:
            self.tabla_pacientes(paciente)
        self.display.addWidget(self.tabla)
    
    def tabla_pacientes(self, paciente):
        posicion = self.tabla.rowCount()
        self.tabla.insertRow(posicion)
        self.tabla.setItem(posicion, 0, QTableWidgetItem(paciente['nombre']))
        self.tabla.setItem(posicion, 1, QTableWidgetItem(paciente['apellido']))
        self.tabla.setItem(posicion, 2, QTableWidgetItem(paciente['edad']))
        self.tabla.setItem(posicion, 3, QTableWidgetItem(paciente['cedula']))
        self.tabla.setCellWidget(posicion, 4, self.boton_eliminar(paciente['cedula']))

    def boton_eliminar(self, cedula):
        boton = QPushButton("Eliminar")
        boton.clicked.connect(lambda: self.eliminar_paciente(cedula))
        return boton

    def eliminar_paciente(self, cedula):
        self.controlador.eliminar_paciente(cedula)
        self.cargar_pacientes()
        self.tabla.clearContents()
        self.tabla.setRowCount(0)

    def logout(self):
        self.controlador.logout()
        self.close()