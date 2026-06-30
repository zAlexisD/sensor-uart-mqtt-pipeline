"""
Screen Module for dynamic topic updating
"""
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QHBoxLayout,QCheckBox,QMessageBox,QInputDialog
from PyQt6.QtCore import Qt,pyqtSignal

from utils.config import topicList

class TopicWindow(QWidget):
    topic_update = pyqtSignal(str,int)

    def __init__(self,currentTopics):
        super().__init__()
        self.topics = currentTopics

        self.leftTopics = []
        self.rightTopics = []

        self.init_window()
        

    def init_window(self):
        self.mainLayout = QVBoxLayout()

        # Set a hide button
        hide_btn = QPushButton("Hide")
        hide_btn.clicked.connect(self.hide)
        self.mainLayout.addWidget(hide_btn,alignment=Qt.AlignmentFlag.AlignRight)

        # Main content Layout
        self.topicLayout = QHBoxLayout()

        # Left column displays
        self.leftCol = QVBoxLayout()
        for topic in topicList:
            cb = QCheckBox(topic)
            self.leftTopics.append(cb)
            self.leftCol.addWidget(cb)
            if topic in self.topics:
                cb.setChecked(True)
            cb.stateChanged.connect(self.on_update)
        if "Select All" not in self.topics:
            all_cb = QCheckBox("Select All")
            all_cb.stateChanged.connect(self.on_all_checked)
            self.leftCol.addWidget(all_cb)
        self.topicLayout.addLayout(self.leftCol)

        # Right column display
        self.rightCol = QVBoxLayout()
        for topic in self.topics:
            if topic != "Select All":
                cb = QCheckBox(topic)
                self.rightTopics.append(cb) 
                cb.setChecked(True)
                self.rightCol.addWidget(cb)
                cb.stateChanged.connect(self.on_update)
        self.other_cb = QCheckBox("Other")
        self.other_cb.clicked.connect(self.on_other_clicked)
        self.rightCol.addWidget(self.other_cb)
        self.topicLayout.addLayout(self.rightCol)

        self.mainLayout.addLayout(self.topicLayout)
        self.setLayout(self.mainLayout)

    # Helper : Warning popup box
    def set_warning(self,message):
        warning = QMessageBox(self)
        warning.setIcon(QMessageBox.Icon.Warning)
        warning.setText(message)
        warning.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning.exec()

    # Helper : Add checkbox in layout
    def add_checkbox(self,name,returning=False):
        cb = QCheckBox(name)
        self.rightCol.addWidget(cb)
        if returning:
            return cb

    def on_all_checked(self, state):
        if state:
            # Select all
            for cb in self.leftTopics:
                cb.setChecked(True)
        else:
            # Unselect all
            for cb in self.leftTopics:
                cb.setChecked(False)

    def on_other_clicked(self, checked):
        if checked:
            text, ok = QInputDialog.getText(
                self, "Add Custom Topic", "Enter topic name:"
            )
            # Cancel if topic already exists
            if text.strip() in self.rightTopics:
                self.set_warning("Topic already exists")
                ok = False

            # Do not accept if topic contain spaces
            if " " in text.strip():
                self.set_warning("Wrong format: No spaces allowed")
                ok = False

            if ok and text.strip():
                self.rightTopics .append(text.strip())
                # Remove "Other" widget
                self.rightCol.removeWidget(self.other_cb)
                # Add new widgets
                new_cb = self.add_checkbox(text.strip(),returning=True)
                new_cb.stateChanged.connect(self.on_update)
                # Auto check the newly added widget
                new_cb.setChecked(True)
                # Put "Other" widget back under the previous one
                self.rightCol.addWidget(self.other_cb)
                
            # Reset "other" -> after moving, cancelling, unchecking, warning,etc
            self.other_cb.setChecked(False)

    # Callback for dashboard
    def on_update(self, state):
        cb = self.sender()
        topicName = cb.objectName()
        self.topic_update.emit(topicName,state)