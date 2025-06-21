import sys
import numpy as np
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import QTimer, QElapsedTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from diode_widget import DiodeWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacja naziemna")
        self.setGeometry(100, 100, 1400, 700)

        # Konfiguracja
        self.total_duration = 15.0
        self.sample_rate = 100

        # Dane - #TODO Należy to poprawić
        self.time_data = np.array([])
        self.y1_data = np.array([])
        self.y2_data = np.array([])
        self.y3_data = np.array([])

        # Timer
        self.real_timer = QElapsedTimer()

        # UI
        self.init_ui()

        # Timery
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.generate_data)
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)


        self.diode_states = [0, 1, 2]

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel wykresów (80%)
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)

        # Wykres 1 - Zwiększony rozmiar
        self.figure1 = Figure(figsize=(10, 3.5), tight_layout=True)
        self.canvas1 = FigureCanvasQTAgg(self.figure1)
        self.ax1 = self.figure1.add_subplot(111)
        self.line1, = self.ax1.plot([], [], 'b-', linewidth=1.8)
        self.ax1.set_title("Wykres wysokości", pad=20)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_xlabel("Czas [s]", fontsize=10)
        self.ax1.set_ylabel("Wysokość  [m]", fontsize=10)

        # Wykres 2
        self.figure2 = Figure(figsize=(10, 3.5), tight_layout=True)
        self.canvas2 = FigureCanvasQTAgg(self.figure2)
        self.ax2 = self.figure2.add_subplot(111)
        self.line2, = self.ax2.plot([], [], 'r-', linewidth=1.8)
        self.ax2.set_title("Wykres prędkości", pad=20)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_xlabel("Czas [s]", fontsize=10)
        self.ax2.set_ylabel("Prędkość [m/s]", fontsize=10)

        # Wykres 3
        self.figure3 = Figure(figsize=(10, 3.5), tight_layout=True)
        self.canvas3 = FigureCanvasQTAgg(self.figure3)
        self.ax3 = self.figure3.add_subplot(111)
        self.line3, = self.ax3.plot([], [], 'g-', linewidth=1.8)
        self.ax3.set_title("Wykreś przyspieszenia", pad=20)
        self.ax3.grid(True, alpha=0.3)
        self.ax3.set_xlabel("Czas [s]", fontsize=10)
        self.ax3.set_ylabel("Przyspieszenie [m/s^2]", fontsize=10)

        plot_layout.addWidget(self.canvas1)
        plot_layout.addWidget(self.canvas2)
        plot_layout.addWidget(self.canvas3)

        # Panel czatu (20%)
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)

        # Diode panel at the top
        diode_panel = QWidget()
        diode_layout = QHBoxLayout(diode_panel)
        diode_layout.setContentsMargins(0, 0, 0, 0)

        # Create three diodes
        self.diode1 = DiodeWidget("START",0)
        self.diode2 = DiodeWidget("APOGEUM",1)
        self.diode3 = DiodeWidget("UTRATA SYGNAŁU",2)

        diode_layout.addWidget(self.diode1)
        diode_layout.addWidget(self.diode2)
        diode_layout.addWidget(self.diode3)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(
            "background-color: #c0c0c0;")
        separator.setFixedHeight(2)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.append("> SYSTEM: Uruchomienie stacji naziemnej")

        chat_layout.addWidget(diode_panel)
        chat_layout.addWidget(separator)
        chat_layout.addWidget(self.chat_box, 1)

        # input_widget = QWidget()
        # input_layout = QHBoxLayout(input_widget)

        # self.message_input = QLineEdit()
        # self.message_input.setPlaceholderText("Wpisz wiadomość...")
        # self.send_button = QPushButton("WYŚLIJ")
        # self.send_button.setFixedWidth(120)
        # self.send_button.clicked.connect(self.send_message)

        # input_layout.addWidget(self.message_input)
        # input_layout.addWidget(self.send_button)


        main_layout.addWidget(plot_widget, 80)
        main_layout.addWidget(chat_widget, 20)

    def start_simulation(self):
        # Reset danych
        self.time_data = np.array([])
        self.y1_data = np.array([])
        self.y2_data = np.array([])
        self.y3_data = np.array([])

        # Uruchomienie
        self.real_timer.start()
        self.data_timer.start(20)
        self.plot_timer.start(30)

        self.chat_box.append(f"\n> Rozpoczęto {self.total_duration}s symulacji")

        QTimer.singleShot(int(self.total_duration * 1000), self.stop_simulation)

    def generate_data(self):
        elapsed = self.real_timer.elapsed() / 1000.0
        if elapsed >= self.total_duration:
            return

        new_time = elapsed
        freq = 0.5  # Hz

        noise = 0.1 * random.random()
        new_y1 = np.sin(2 * np.pi * freq * new_time) + noise
        new_y2 = np.cos(2 * np.pi * freq * new_time) + noise
        new_y3 = random.uniform(-1, 1)

        # Zapisz dane
        self.time_data = np.append(self.time_data, new_time)
        self.y1_data = np.append(self.y1_data, new_y1)
        self.y2_data = np.append(self.y2_data, new_y2)
        self.y3_data = np.append(self.y3_data, new_y3)

        # Raport co 1s
        if abs(new_time - round(new_time)) < 0.02:
            self.chat_box.append(f"> Czas: {new_time:.1f}s | Próbek: {len(self.time_data)}")

    def update_plots(self):
        if len(self.time_data) == 0:
            return

        current_time = self.time_data[-1]

        x_min = 0
        time_margin = 0.1
        x_max = (1+time_margin)*current_time

        # Aktualizuj wszystkie wykresy
        for ax, line, y_data in zip(
                [self.ax1, self.ax2, self.ax3],
                [self.line1, self.line2, self.line3],
                [self.y1_data, self.y2_data, self.y3_data]
        ):
            line.set_data(self.time_data, y_data)

            # Skalowanie osi Y
            if len(y_data) > 0:
                value_margin = 0.1
                y_min = (1+value_margin)*min(y_data)
                y_max = (1+value_margin)*max(y_data)
                ax.set_ylim(y_min, y_max)

            ax.set_xlim(x_min, x_max)
            ax.figure.canvas.draw()

    def stop_simulation(self):
        self.data_timer.stop()
        self.plot_timer.stop()
        elapsed = self.real_timer.elapsed() / 1000.0
        self.chat_box.append(f"\n> Zakończono symulację (czas: {elapsed:.2f}s)")
        self.chat_box.append(f"> Zebrano {len(self.time_data)} próbek")

    # def send_message(self):
    #     message = self.message_input.text()
    #     if message:
    #         self.chat_box.append(f"TY: {message}")
    #         self.message_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Rozpocznij symulację po 1s
    QTimer.singleShot(1000, window.start_simulation)

    window.show()
    sys.exit(app.exec())