"""
Widget Module for displaying status widgets on GUI
"""
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QListWidget,QHBoxLayout,QPushButton

class StatusWidget(QWidget):
    def __init__(self,topics):
        super().__init__()
        # Make sure that topics includes status and timestamp
        self.topics = topics

        layout = QVBoxLayout()

        # Status list widget
        self.status_list = QListWidget()
        self.status_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)  # Read-only
        layout.addWidget(self.status_list)

        # Button
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)
        
        # Connect signal
        self.clear_btn.clicked.connect(self.status_list.clear)

        self.setLayout(layout)

    def update_data(self,topic,status):
        self.status_list.addItem(f"{topic} STATUS: {status}")
        self.status_list.scrollToBottom()  # Keep latest visible