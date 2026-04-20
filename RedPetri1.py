import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QTimer


class RedDePetri(QWidget):
    def __init__(self):
        super().__init__()

        # -------- LUGARES --------
        self.materia_prima = 5
        self.maquina_1 = 1
        self.maquina_2 = 1
        self.producto_proceso = 0
        self.buffer = 0
        self.producto_terminado = 0

        self.inicializar_ui()

    def inicializar_ui(self):

        self.setWindowTitle("Simulador Red de Petri")
        self.resize(350, 450)

        # -------- ETIQUETAS --------
        self.label_mp = QLabel()
        self.label_m1 = QLabel()
        self.label_m2 = QLabel()
        self.label_proc = QLabel()
        self.label_buffer = QLabel()
        self.label_term = QLabel()
        self.label_estado = QLabel("Estado del Sistema: Listo")

        # -------- BOTONES --------l
        self.btn_iniciar = QPushButton("Iniciar Producción")
        self.btn_finalizar = QPushButton("Finalizar Producto")
        self.btn_reiniciar = QPushButton("Reiniciar")

        self.btn_iniciar.clicked.connect(self.transicion_iniciar)
        self.btn_finalizar.clicked.connect(self.finalizar_producto)
        self.btn_reiniciar.clicked.connect(self.reiniciar)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(self.label_mp)
        layout.addWidget(self.label_m1)
        layout.addWidget(self.label_m2)
        layout.addWidget(self.label_proc)
        layout.addWidget(self.label_buffer)
        layout.addWidget(self.label_term)
        layout.addWidget(self.label_estado)
        layout.addWidget(self.btn_iniciar)
        layout.addWidget(self.btn_finalizar)
        layout.addWidget(self.btn_reiniciar)

        self.setLayout(layout)
        self.actualizar_labels()

    # -------- TRANSICIÓN T1 --------
    def transicion_iniciar(self):

        if self.materia_prima > 0 and (self.maquina_1 > 0 or self.maquina_2 > 0):

            self.materia_prima -= 1
            self.producto_proceso += 1

            if self.maquina_1 > 0:
                self.maquina_1 -= 1
            else:
                self.maquina_2 -= 1

            self.label_estado.setText("Estado: Produciendo (3s)")

            QTimer.singleShot(3000, self.transicion_buffer)

        else:
            self.label_estado.setText("Producción detenida")

        self.actualizar_labels()

    # -------- TRANSICIÓN T2 --------
    def transicion_buffer(self):
        if self.producto_proceso > 0:
            self.producto_proceso -= 1
            self.buffer += 1

            if self.maquina_1 == 0:
                self.maquina_1 += 1
            else:
                self.maquina_2 += 1

            self.label_estado.setText("Producto en Buffer")

        self.actualizar_labels()

    # -------- TRANSICIÓN T3 --------
    def finalizar_producto(self):
        if self.buffer > 0:
            self.buffer -= 1
            self.producto_terminado += 1
            self.label_estado.setText("Producto Terminado")

        else:
            self.label_estado.setText("No hay producto en buffer")

        self.actualizar_labels()

    # -------- REINICIAR --------
    def reiniciar(self):
        self.materia_prima = 5
        self.maquina_1 = 1
        self.maquina_2 = 1
        self.producto_proceso = 0
        self.buffer = 0
        self.producto_terminado = 0
        self.label_estado.setText("Sistema Reiniciado")
        self.actualizar_labels()

    # -------- ACTUALIZAR --------
    def actualizar_labels(self):
        self.label_mp.setText(f"Materia Prima: {self.materia_prima}")
        self.label_m1.setText(f"Máquina 1 Disponible: {self.maquina_1}")
        self.label_m2.setText(f"Máquina 2 Disponible: {self.maquina_2}")
        self.label_proc.setText(f"Producto en Proceso: {self.producto_proceso}")
        self.label_buffer.setText(f"Buffer: {self.buffer}")
        self.label_term.setText(f"Producto Terminado: {self.producto_terminado}")


app = QApplication(sys.argv)
ventana = RedDePetri()
ventana.show()
sys.exit(app.exec())