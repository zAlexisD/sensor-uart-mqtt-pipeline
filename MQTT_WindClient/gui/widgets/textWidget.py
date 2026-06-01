"""
Widget Module for displaying generic text on GUI
"""
from PyQt6.QtWidgets import QWidget,QLabel

class TextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.label = QLabel("TEXT")
        self.label.setStyleSheet("font-size: 32px;")

    def update_value(self,value:str):
        self.label.setText(value)
        #TODO: Add interaction to change display when actions happens
        # Here this widget would be mainly used for "press ENTER to start listening"