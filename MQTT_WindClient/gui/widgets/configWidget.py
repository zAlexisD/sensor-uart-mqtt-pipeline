"""
Widget Module for Configuration display 
"""
from PyQt6.QtWidgets import QWidget,QLabel,QGridLayout

class ConfigWidget(QWidget):
    def __init__(self,title:str,configs:dict):
        super().__init__()
        self.title = title
        self.configs = configs
        self.build_ui()
    
    def build_ui(self):
        layout = QGridLayout()
        rowIndex = 0

        # Title
        titleLabel = QLabel(self.title)
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(titleLabel,rowIndex,0)

        # Configs display
        for key,value in self.configs.items():
            rowIndex += 1
            row = QLabel(f"{key}: {value}")
            row.setStyleSheet("font-size: 12px;")
            layout.addWidget(row,rowIndex,0)

        self.setLayout(layout)