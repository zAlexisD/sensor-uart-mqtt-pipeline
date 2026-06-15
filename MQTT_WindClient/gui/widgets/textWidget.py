"""
Widget Module for displaying simple text-based widgets on GUI
"""
from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout
import random

class TextWidget(QWidget):
    def __init__(self,topics):
        super().__init__()
        self.topics = topics
        self.labels = []

        self.textLayout = QVBoxLayout()
        self.build_ui()
        self.setLayout(self.textLayout)

    #TODO: make layout more pleasant to read
    def build_ui(self):
        for topic in self.topics:
            label = QLabel(f"{topic}: --")
            label.setStyleSheet("font-size: 16px;")
            self.labels.append(label)
            self.textLayout.addWidget(label)

    def update_data(self,values:list[str]):
        for i,label in enumerate(self.labels):
            # Unset randomness seed for string list
            random.seed(None)
            value = random.choice(values)
            label.setText(f"{self.topics[i]}: {value}")