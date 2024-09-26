from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QGridLayout,
    QWidget,
)
from PyQt6.QtCore import QSize, Qt
from sqlalchemy import create_engine, text

import sys

# Database
engine = create_engine("sqlite:///monsters.db", echo=True)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("5E Encounter Builder")

        layout = QGridLayout()

        self.creatures = QListWidget()
        self.search = QLineEdit()
        
        layout.addWidget(self.search, 0, 0)
        layout.addWidget(self.creatures, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.populate_list()
        self.setFixedSize(QSize(400, 300))
        self.setCentralWidget(widget)
        
        # Connect the search input to the filter method
        self.search.textChanged.connect(self.filter_creatures)
        
    def populate_list(self):
        # add creatures to list
        items = []
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM MONSTERS"))
            for rows in result:
                items.append(rows[0])
        
        for item in items:
            self.creatures.addItem(item)
            
    def filter_creatures(self, text):
        for i in range(self.creatures.count()):
            item = self.creatures.item(i)
            item.setHidden(text.lower() not in item.text().lower())
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()