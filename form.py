import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QStackedWidget, QTableWidget, QComboBox
)
from PySide6.QtCore import Qt

class UI_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IRA(Interval repetition app)")
        self.setWindowIcon(QIcon("C:/vnutri_vyshki_firewatch.jpg"))

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Navigation panel
        nav_widget = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)
        self.menu_button = QPushButton("Меню")
        self.words_button = QPushButton("Слова")
        self.test_button = QPushButton("Проверка")
        nav_layout.addWidget(self.menu_button)
        nav_layout.addWidget(self.words_button)
        nav_layout.addWidget(self.test_button)
        nav_widget.setLayout(nav_layout)
        main_layout.addWidget(nav_widget)

        # Navigation buttons styling
        nav_widget.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: 1px solid #388E3C;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        # Stacked widget for switching layouts
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Menu widget
        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_label = QLabel("Приложение для интервального повторения информации")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        menu_layout.addWidget(menu_label)
        menu_layout.addStretch()
        self.menu_widget.setLayout(menu_layout)

        # Words widget
        self.words_widget = QWidget()
        words_layout = QVBoxLayout()
        input_form = QFormLayout()
        self.word_edit = QLineEdit()
        self.meaning_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Слово", "Определение", "Теорема"])
        input_form.addRow("Слово:", self.word_edit)
        input_form.addRow("Значение:", self.meaning_edit)
        input_form.addRow("Вид:", self.category_combo)
        self.add_button = QPushButton("Добавить слово")
        input_form.addWidget(self.add_button)
        words_layout.addLayout(input_form)

        # Words table
        self.words_table = QTableWidget()
        self.words_table.setColumnCount(3)
        self.words_table.setHorizontalHeaderLabels(["Слово", "Значение", "Вид"])
        self.words_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: 1px solid #cccccc;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:nth-child(even) {
                background-color: #f9f9f9;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #d1e7dd;
            }
        """)
        self.words_table.setAlternatingRowColors(True)
        self.words_table.setSelectionMode(QTableWidget.SingleSelection)
        self.words_table.setSelectionBehavior(QTableWidget.SelectRows)
        words_layout.addWidget(self.words_table)
        self.delete_button = QPushButton("Удалить выбранное слово")
        words_layout.addWidget(self.delete_button)
        self.words_widget.setLayout(words_layout)

        # Words buttons styling
        self.words_widget.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: 1px solid #388E3C;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        # Testing widget
        self.testing_widget = QWidget()
        testing_layout = QVBoxLayout()
        testing_layout.setAlignment(Qt.AlignCenter)
        self.word_label = QLabel("Тестов пока нет..")
        self.word_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #4CAF50;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
            margin: 10px;
        """)
        testing_layout.addWidget(self.word_label)
        self.answer_edit = QLineEdit()
        self.answer_edit.setMaximumWidth(300)
        testing_layout.addWidget(self.answer_edit)
        self.submit_button = QPushButton("Отправить")
        self.retry_button = QPushButton("Попробовать через 5 минут")
        self.refresh_button = QPushButton("Обновить очередь")
        testing_layout.addWidget(self.submit_button)
        testing_layout.addWidget(self.retry_button)
        testing_layout.addWidget(self.refresh_button)
        self.next_test_label = QLabel("Больше тестов не запланировано")
        self.next_test_label.setStyleSheet("font-size: 12px; color: #555555; margin: 10px;")
        testing_layout.addWidget(self.next_test_label)
        testing_layout.addStretch()
        self.testing_widget.setLayout(testing_layout)

        # Testing buttons styling
        self.testing_widget.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: 1px solid #388E3C;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.words_widget)
        self.stacked_widget.addWidget(self.testing_widget)