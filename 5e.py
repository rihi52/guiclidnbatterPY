from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
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
        width = 720
        height = 480

        self.setWindowTitle("5E Encounter Builder")

        layout = QGridLayout()

        self.creatures = QListWidget()
        self.creatures.setFixedWidth(int((width/2)-10))
        self.search = QLineEdit()
        self.search.setFixedWidth(int((width/2)-10))
        
        layout.addWidget(self.search, 0, 0)
        layout.addWidget(self.creatures, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.populate_list()
        self.setFixedSize(QSize(width, height))
        self.setCentralWidget(widget)
        
        # Connect the search input to the filter method
        self.search.textChanged.connect(self.filter_creatures)
        
    def populate_list(self):
        # add creatures to list
        items = []
        cr = []
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name, cr FROM MONSTERS"))
            for rows in result:
                items.append(rows[0])
                cr.append(rows[1])
                
            widget = QWidget()
            grid_layout = QGridLayout()
            
            grid_layout = QGridLayout()
            
            name_label = QLabel("Name")
            grid_layout.addWidget(name_label, 0, 0)
            
            cr_label = QLabel("CR")
            grid_layout.addWidget(cr_label, 0, 1)
            
            widget.setLayout(grid_layout)
            
            # Set a minimum size for the widget to ensure it renders
            widget.setMinimumSize(100, 30)

            # Create a QListWidgetItem (empty item for custom widget)
            list_item = QListWidgetItem()

            # Add the empty QListWidgetItem to the QListWidget
            self.creatures.addItem(list_item)

            # Set the custom widget for the QListWidgetItem
            self.creatures.setItemWidget(list_item, widget)
        
        # Populate the QListWidget with custom grid-aligned items
        for name, challenge_rating in zip(items, cr):
            # Create a custom widget with grid layout
            widget = QWidget()
            grid_layout = QGridLayout()

            # Add name to the first column
            name_label = QLabel(name)
            grid_layout.addWidget(name_label, 0, 0)

            # Add Challenge Rating (CR) to the second column
            cr_label = QLabel(f"{challenge_rating}")
            grid_layout.addWidget(cr_label, 0, 1)

            # Set the custom widget's layout
            widget.setLayout(grid_layout)
            
            # Set a minimum size for the widget to ensure it renders
            widget.setMinimumSize(100, 30)

            # Create a QListWidgetItem (empty item for custom widget)
            list_item = QListWidgetItem()

            # Add the empty QListWidgetItem to the QListWidget
            self.creatures.addItem(list_item)

            # Set the custom widget for the QListWidgetItem
            self.creatures.setItemWidget(list_item, widget)
            
    def filter_creatures(self, text):
        """Filter the items in the QListWidget based on search text."""
        for i in range(self.creatures.count()):
            item = self.creatures.item(i)
            widget = self.creatures.itemWidget(item)

            # Get the text from the widget's labels to compare against the search text
            name_label = widget.layout().itemAt(0).widget()  # Access the first QLabel (name)
            item.setHidden(text.lower() not in name_label.text().lower())
            
            cr_label = widget.layout().itemAt(1).widget()  # Access the second QLabel (CR)
            item.setHidden(text.lower() not in cr_label.text().lower())
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()