"""
PyQt Module - GUI Main Window
"""
from PyQt6.QtWidgets import QMainWindow,QStackedWidget

from gui.screens.startScreen import StartPage
from gui.screens.mainScreen import DashboardPage
from mqtt.handlers import TopicSelectController

class MainWindow(QMainWindow):
    def __init__(self,controller:TopicSelectController):
        super().__init__()
        self.controller = controller
        
        self.stack = QStackedWidget()
        self.setGeometry(100, 60, 1000, 500)

        self.start_page = StartPage(controller)
        self.stack.addWidget(self.start_page)      # index 0

        self.setCentralWidget(self.stack)

        # Connect controller signal to page switch
        self.controller.topic_selection.connect(self.on_topics_selected)

    def on_topics_selected(self, topics):
        # Create dashboard widget here to avoid launching before topic selection
        self.dashboard_page = DashboardPage(self.controller)
        self.stack.addWidget(self.dashboard_page)  # index 1
        # Switch to next page
        self.stack.setCurrentIndex(1)