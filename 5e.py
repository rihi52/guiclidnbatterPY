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

        self.creatures_list = QListWidget()
        self.creatures_list.setFixedWidth(700)
        self.search = QLineEdit()
        self.search.setFixedWidth(700)
        
        self.list_header_name = QLabel()
        self.list_header_name.setText("Name")
        self.list_header_name.setFixedWidth(int((width/4)-20))
        
        self.list_header_cr = QLabel()
        self.list_header_cr.setText("CR")
        self.list_header_cr.setFixedWidth(int((width/4)-20))
        
        self.list_header_type = QLabel()
        self.list_header_type.setText("Type")
        self.list_header_type.setFixedWidth(int((width/4)-20))
        
        self.list_header_size = QLabel()
        self.list_header_size.setText("Size")
        self.list_header_size.setFixedWidth(int((width/4)-20))
        
        layout.addWidget(self.search, 0, 0, 1, 2)        
        layout.addWidget(self.list_header_name, 1, 0)
        layout.addWidget(self.list_header_type, 1, 1)
        layout.addWidget(self.list_header_size, 1, 2)
        layout.addWidget(self.list_header_cr, 1, 3)
        layout.addWidget(self.creatures_list, 2, 0, 1, 2)

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
        type = []
        size = []
        cr = []
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name, type, size, cr FROM MONSTERS"))
            for rows in result:
                items.append(rows[0])
                type.append(rows[1])
                size.append(rows[2])
                cr.append(rows[3])
        
        # Populate the QListWidget with custom grid-aligned items
        for name, type, size, challenge_rating in zip(items, type, size, cr):
            # Create a custom widget with grid layout
            widget = QWidget()
            grid_layout = QGridLayout()

            # Add name to the first column
            name_label = QLabel(name)
            grid_layout.addWidget(name_label, 0, 0)
            
            type_label = QLabel(type)
            grid_layout.addWidget(type_label, 0, 1)
            
            size_label = QLabel(size)
            grid_layout.addWidget(size_label, 0, 2)

            # Add Challenge Rating (CR) to the second column
            cr_label = QLabel(f"{challenge_rating}")
            grid_layout.addWidget(cr_label, 0, 3)
            
            

            # Set the custom widget's layout
            widget.setLayout(grid_layout)
            
            # Set a minimum size for the widget to ensure it renders
            widget.setMinimumSize(100, 30)

            # Create a QListWidgetItem (empty item for custom widget)
            list_item = QListWidgetItem()

            # Add the empty QListWidgetItem to the QListWidget
            self.creatures_list.addItem(list_item)

            # Set the custom widget for the QListWidgetItem
            self.creatures_list.setItemWidget(list_item, widget)
            
    def filter_creatures(self, text):
        """Filter the items in the QListWidget based on search text."""
        for i in range(self.creatures_list.count()):
            item = self.creatures_list.item(i)
            widget = self.creatures_list.itemWidget(item)

            # Get the text from the widget's labels to compare against the search text
            name_label = widget.layout().itemAt(0).widget()  # Access the first QLabel (name)
            
            size_label = widget.layout().itemAt(1).widget()  # Access the second QLabel (CR)
            
            type_label = widget.layout().itemAt(2).widget()  # Access the second QLabel (CR)
            
            cr_label = widget.layout().itemAt(3).widget()  # Access the second QLabel (CR)
            
            # Get the text from both labels
            name_text = name_label.text().lower()
            size_text = size_label.text().lower()
            type_text = type_label.text().lower()
            cr_text = cr_label.text().lower()

            # Set hidden only if the search text is NOT in either the name or the CR
            item.setHidden(text.lower() not in name_text and text.lower() not in cr_text and text.lower() not in size_text and text.lower() not in type_text)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()