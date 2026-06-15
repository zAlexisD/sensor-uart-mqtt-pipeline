"""
GUI Module for Logging diplay Widget
"""
from PyQt6.QtWidgets import QWidget,QPlainTextEdit
from utils.config import LogQueue
from PyQt6.QtCore import QObject,pyqtSignal,QThread
from mqtt.handlers import storeData

# Define Log manager class for real time updating
class LogManager(QObject):
    addLog = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logList = []
    
    # Callback like Qt signal to send to prompt and save log entry
    def queueToList(self):
        # Listening method to continuously copy from log queue to list
        while not LogQueue.empty():
            logContent = LogQueue.get()
            self.logList.append(logContent)
            self.addLog.emit(logContent)

    def saveLogs(self):
        logPath = f"data/logErrors.json"
        storeData(self.logList,logPath)

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        self.logPanel = QPlainTextEdit("[LOG ERROR]: --")
        self.logPanel.setReadOnly(True)
        self.logPanel.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;  /* Dark background */
                color: #d4d4d4;             /* Light gray text */
                border: none;
                padding: 5px;
                selection-background-color: #264f78; /* Selection color */
            }
        """)

        # Start thread for continuous listening + copy of logs
        self.thread = QThread()
        self.logManager = LogManager()
        self.logManager.moveToThread(self.thread)

        self.logManager.addLog.connect(self.update_entry)

        self.thread.started.connect(self.logManager.queueToList)
        self.thread.start()

    def update_entry(self,entry:str):
        self.logPanel.appendPlainText(f"[LOG ERROR]: {entry}")