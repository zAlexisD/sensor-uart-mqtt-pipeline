"""
Screen Module to define starting screen
"""
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QGridLayout,QLabel,QCheckBox,QPushButton,QInputDialog,QMessageBox
from PyQt6.QtCore import Qt
from mqtt.handlers import TopicSelectController
from utils.config import topicList

#TODO: separate in helpers for clarity

class StartPage(QWidget):
    def __init__(self,controller:TopicSelectController):
        super().__init__()
        self.controller = controller
        self.fullList = topicList + ["Select All"]
        self.checkboxes = []
        self.custom_topics = []
        self.leftRowCounter = 0
        self.rightRowCounter = 0

        #TODO: Make the start screen better looking
        self.setWindowTitle("MQTT Sub Client - Topic choice")
        self.setStyleSheet("background-color: #514A6A")

        mainLayout = QVBoxLayout()

        headerWidget = QLabel("  Welcome to MQTT Subscriber Client. Please select topics to subscribe to.  ")
        headerWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(headerWidget)

        self.cb_layout = QGridLayout()

        for topic in self.fullList:
            # "All" should be the last topic
            if topic == "Select All":
                self.all_cb = QCheckBox(topic,self)
                self.all_cb.stateChanged.connect(self.on_all_checked)
                self.cb_layout.addWidget(self.all_cb,self.leftRowCounter,0)
            else:
                self.add_checkbox(topic,self.leftRowCounter,0)
            self.leftRowCounter += 1

        # Pad the "Other" to get equal intiial columns length
        padding = len(max(self.fullList, key=len))
        otherPadded = "Other" + " "*padding
        # "Other" checkbox
        self.other_cb = QCheckBox(otherPadded,self)
        self.other_cb.clicked.connect(self.on_other_clicked)
        self.cb_layout.addWidget(self.other_cb,0,1)
        
        mainLayout.addLayout(self.cb_layout)

        confirm = QPushButton("Confirm")
        confirm.clicked.connect(self.on_confirm)
        mainLayout.addWidget(confirm)

        self.setLayout(mainLayout)

    # Helper : Warning popup box
    def set_warning(self,message):
        warning = QMessageBox(self)
        warning.setIcon(QMessageBox.Icon.Warning)
        warning.setText(message)
        warning.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning.exec()

    # Helper : Add checkbox in layout
    def add_checkbox(self,name,row,col,returning=False):
        cb = QCheckBox(name,self)
        self.checkboxes.append(cb)
        self.cb_layout.addWidget(cb,row,col)
        if returning:
            return cb

    def on_all_checked(self, state):
        if state:
            # Select all
            for cb in self.checkboxes:
                cb.setChecked(True)
        else:
            # Unselect all
            for cb in self.checkboxes:
                cb.setChecked(False)

    def on_other_clicked(self, checked):
        if checked:
            text, ok = QInputDialog.getText(
                self, "Add Custom Topic", "Enter topic name:"
            )
            # Cancel if topic already exists
            if text.strip() in self.custom_topics:
                self.set_warning("Topic already exists")
                ok = False

            # Do not accept if topic contain spaces
            if " " in text.strip():
                self.set_warning("Wrong format: No spaces allowed")
                ok = False

            if ok and text.strip():
                self.custom_topics.append(text.strip())
                # Remove "Other" widget
                self.cb_layout.removeWidget(self.other_cb)
                # Add new widgets
                new_cb = self.add_checkbox(text.strip(),self.rightRowCounter,1,returning=True)
                self.rightRowCounter += 1
                # Auto check the newly added widget
                new_cb.setChecked(True)
                # Put "Other" widget back under the previous one
                self.cb_layout.addWidget(self.other_cb,self.rightRowCounter,1)
                
            # Reset "other" -> after moving, cancelling, unchecking, warning,etc
            self.other_cb.setChecked(False)

    def on_confirm(self):
        # Return every checked checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        self.controller.set_topics_from_gui(selected)