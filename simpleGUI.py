import serial
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal

# Inits
delimiter0 = "TWR[0]."
delimiter1 = ": "
ser = serial.Serial(port="COM4", baudrate=3000000)

# Worker thread class to enhance better real time display
class SerialWorker(QObject):
    newNlos = pyqtSignal(str)
    newDist = pyqtSignal(str)
    newAzim = pyqtSignal(str)
    newElev = pyqtSignal(str)

    def update(self):
        while True:
            if ser.in_waiting:
                # note : one "line" is actually the whole block displayed
                # line format -> APP : INFO :TWR[0].measure_name : measure_value
                line = ser.readline().decode(errors="ignore").strip()
                # preprocessing : split the block and keep measure data only
                # keep only right part of line after TWR[0].
                lines = line.split(delimiter0)
                lines.pop(0)
                # parse through lines
                for measureLines in lines:
                    # keep only measure data and update widget
                    data = measureLines.split(delimiter1)
                    if data[0].startswith("nLos"):
                        self.newNlos.emit(data[1])
                    elif data[0].startswith("distance"):
                        self.newDist.emit(data[1])
                    elif data[0].startswith("aoa_azimuth"):
                        self.newAzim.emit(data[1])
                    elif data[0].startswith("aoa_elevation"):
                        self.newElev.emit(data[1])


class myWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Define labels
        self.nlos = QLabel("NLoS: --")
        self.distance = QLabel("Distance: -- cm")
        self.azimuth = QLabel("AoA Azimuth: -- °")
        self.elevation = QLabel("AoA Elevation: -- °")

        # Format
        self.nlos.setStyleSheet("font-size: 32px;")
        self.distance.setStyleSheet("font-size: 32px;")
        self.azimuth.setStyleSheet("font-size: 32px;")
        self.elevation.setStyleSheet("font-size: 32px;")

        self.setStyleSheet("background-color: #514A6A")

        # Add to window
        layout = QGridLayout()
        layout.addWidget(self.nlos,0,0)
        layout.addWidget(self.distance,0,1)
        layout.addWidget(self.azimuth,1,0)
        layout.addWidget(self.elevation,1,1)
        self.setLayout(layout)

        self.setWindowTitle("Real time Type2BP ranging values")

        # --- Start worker thread --- #
        self.thread = QThread()
        self.worker = SerialWorker()
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.newNlos.connect(self.updateNlos)
        self.worker.newDist.connect(self.updateDist)
        self.worker.newAzim.connect(self.updateAzim)
        self.worker.newElev.connect(self.updateElev)

        # Start worker loop
        self.thread.started.connect(self.worker.update)
        self.thread.start()

    def updateNlos(self,value):
        self.nlos.setText(f"NLoS: {value}")

    def updateDist(self,value):
        self.distance.setText(f"Distance: {value} cm")
    
    def updateAzim(self,value):
        self.azimuth.setText(f"AoA Azimuth: {value} °")
    
    def updateElev(self,value):
        self.elevation.setText(f"Aoa Elevation: {value} °")

app = QApplication(sys.argv)
window = myWindow()
window.show()
sys.exit(app.exec_())
