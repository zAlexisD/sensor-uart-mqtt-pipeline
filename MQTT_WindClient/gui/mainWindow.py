"""
PyQt Module - GUI Main Window
"""
from PyQt6.QtWidgets import QMainWindow,QStackedWidget,QApplication
from screens.startScreen import StartPage
from screens.mainScreen import DashboardPage
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()

        self.start_page = StartPage()
        self.dashboard_page = DashboardPage()

        self.stack.addWidget(self.start_page)      # index 0
        self.stack.addWidget(self.dashboard_page)  # index 1

        self.setCentralWidget(self.stack)

    # Overwrite ENTER pressed event to change stack (page)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.stack.setCurrentIndex(1)

# For debug
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())