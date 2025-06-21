from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit,
                             QLineEdit, QPushButton,
                             QLabel, QFrame, QSizePolicy)
from PyQt6.QtCore import QTimer, QElapsedTimer, Qt


class DiodeWidget(QWidget):
    def __init__(self, name, state, parent=None):
        super().__init__(parent)
        self.name = name

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Diode indicator
        self.diode = QFrame()
        self.diode.setFixedSize(30, 30)
        self.diode.setStyleSheet(
            "background-color: gray; border-radius: 15px; border: 1px solid black;")

        # Diode label
        self.label = QLabel(name)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-weight: bold;")

        layout.addWidget(self.diode, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.set_state(state)

    def set_state(self, state):
        """Set diode state: 0=gray, 1=green, 2=red"""
        color = "gray"
        if state == 1:
            color = "green"
        elif state == 2:
            color = "red"
        self.diode.setStyleSheet(
            f"background-color: {color}; border-radius: 15px; border: 1px solid black;")
