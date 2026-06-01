"""
Screen Module to define starting screen
"""
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt6.QtCore import Qt

class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        #TODO: Make the start screen better looking
        label = QLabel("Press Enter to start listening")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)