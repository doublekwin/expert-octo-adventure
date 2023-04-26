from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox

import sys

class AverageSpeedCalc(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Average Speed")
        grid = QGridLayout()

        # Create Widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        time_Label = QLabel("Time(Hours):")
        self.time_line_edit = QLineEdit()

        calculator_button = QPushButton("Calculate")
        calculator_button.clicked.connect(self.calculate_speed)

        self.unitmeasure = QComboBox()
        self.unitmeasure.addItems(['Metric (km)', 'Imperial (miles)'])

        self.distance_speed_label = QLabel("")



        # Add Widgets row, column, span row, span column
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(time_Label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculator_button, 2, 1)
        grid.addWidget(self.distance_speed_label, 3, 0, 1, 2)
        grid.addWidget(self.unitmeasure, 0, 3)

        self.setLayout(grid)

    def calculate_speed(self):
        # Option 1
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())

        speed = distance/time

        if self.unitmeasure.currentText() == 'Metric (km)':
            speed = round(speed, 2)
            unit = 'km/h'
        if self.unitmeasure.currentText() == 'Imperial (miles)':
            speed = round(speed * 0.621371, 2)
            unit = 'mph'

        self.distance_speed_label.setText(f"Average Speed {speed} {unit}")

        # Option 2
        #if self.unitmeasure.currentText() == 'Metric (km)':
        #    khm = int(self.distance_line_edit.text()) / int(self.time_line_edit.text())
        #    self.distance_speed_label.setText(f"Average speed: {khm:.2f} km/h")

        #if self.unitmeasure.currentText() == 'Imperial (miles)':
        #    mph = int(self.distance_line_edit.text()) / int(self.time_line_edit.text()) / 1.6093440006147
        #    self.distance_speed_label.setText(f"Average speed: {mph:.2f} mph")

app = QApplication(sys.argv)
age_calculator = AverageSpeedCalc()
age_calculator.show()
sys.exit(app.exec())


