import sys
import json
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer, QDateTime
from form import UI_Form

class MemoryApp(UI_Form):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.queue = []
        self.current_test = None
        self.load_data()

        # Connect navigation buttons
        self.menu_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.words_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.test_button.clicked.connect(self.switch_to_test)

        # Connect words buttons
        self.add_button.clicked.connect(self.add_word)
        self.delete_button.clicked.connect(self.delete_selected_word)

        # Connect testing buttons
        self.submit_button.clicked.connect(self.process_answer)
        self.retry_button.clicked.connect(self.retry_later)
        self.refresh_button.clicked.connect(self.check_due_tests)

        # Setup timer
        self.timer = QTimer()
        self.timer.setInterval(60000)  # 1 minute
        self.timer.timeout.connect(self.check_due_tests)
        self.timer.start()

        # Initial setup
        self.show_word_list()
        self.check_due_tests()
        if self.queue:
            self.start_testing()

    def load_data(self):
        try:
            with open("memory_data.json", "r") as f:
                data = json.load(f)
                for item in data:
                    word = item["word"]
                    meaning = item["meaning"]
                    category = item.get("category", "Слово")
                    pending_tests = [QDateTime.fromString(t, Qt.ISODate) for t in item["pending_tests"]]
                    self.data[word] = {"meaning": meaning, "category": category, "pending_tests": pending_tests}
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        data_to_save = []
        for word, info in self.data.items():
            pending_tests = [t.toString(Qt.ISODate) for t in info["pending_tests"]]
            data_to_save.append({
                "word": word,
                "meaning": info["meaning"],
                "category": info["category"],
                "pending_tests": pending_tests
            })
        with open("memory_data.json", "w") as f:
            json.dump(data_to_save, f)

    def add_word(self):
        word = self.word_edit.text().strip()
        meaning = self.meaning_edit.text().strip()
        category = self.category_combo.currentText()
        if word and meaning:
            current_time = QDateTime.currentDateTime()
            intervals = [10, 30, 120, 360]  # 10 minutes, 30 minutes, 2 hours, 6 hours
            pending_tests = [current_time.addSecs(interval * 60) for interval in intervals]
            self.data[word] = {"meaning": meaning, "category": category, "pending_tests": pending_tests}
            self.save_data()
            self.show_word_list()
            print(f"Добавленное слово: {word}, будет проверка в {[t.toString(Qt.ISODate) for t in pending_tests]}")

    def delete_selected_word(self):
        selected_rows = self.words_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Слово не выбрано", "Пожалуйста, выберите слово для удаления.")
            return
        row = selected_rows[0].row()
        word_item = self.words_table.item(row, 0)
        if word_item:
            word = word_item.text()
            del self.data[word]
            self.queue = [(w, t) for w, t in self.queue if w != word]
            self.save_data()
            self.show_word_list()
            print(f"Удалённое слово: {word}")
            if self.current_test and self.current_test[0] == word:
                self.start_testing()

    def check_due_tests(self):
        current_time = QDateTime.currentDateTime()
        self.queue = []
        for word in self.data:
            pending_tests = self.data[word]["pending_tests"]
            due_tests = [t for t in pending_tests if t <= current_time]
            for t in due_tests:
                self.queue.append((word, t))
        if self.queue:
            print(f"Тесты будут в: {[(word, t.toString(Qt.ISODate)) for word, t in self.queue]}")
            if self.stacked_widget.currentIndex() == 2:
                self.start_testing()
        elif self.stacked_widget.currentIndex() == 2:
            self.start_testing()

    def switch_to_test(self):
        self.stacked_widget.setCurrentIndex(2)
        self.start_testing()

    def start_testing(self):
        if not self.queue:
            self.word_label.setText("Тестов ещё нет")
            self.next_test_label.setText("Больше тестов не запланировано")
            self.answer_edit.clear()
        else:
            self.current_test = self.queue[0]
            word, _ = self.current_test
            self.word_label.setText(word)
            self.answer_edit.clear()
            current_time = QDateTime.currentDateTime()
            min_time = None
            for word in self.data:
                for test_time in self.data[word]["pending_tests"]:
                    if min_time is None or test_time < min_time:
                        min_time = test_time
            if min_time:
                secs = current_time.secsTo(min_time)
                minutes = secs // 60
                seconds = secs % 60
                self.next_test_label.setText(f"Следующий тест через {minutes} минут {seconds} секунд")
            else:
                self.next_test_label.setText("Больше тестов не запланировано")

    def process_answer(self):
        if not self.current_test:
            return
        word, test_time = self.current_test
        answer = self.answer_edit.text().strip()
        correct_meaning = self.data[word]["meaning"]
        if answer == correct_meaning:
            QMessageBox.information(self, "Молодец", "Правильно!")
            self.data[word]["pending_tests"].remove(test_time)
            self.save_data()
            self.queue.pop(0)
            print(f"Правильный ответ для слова {word}, тест удалён {test_time.toString(Qt.ISODate)}")
            self.start_testing()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Неверно")
            msg_box.setWindowIcon(QIcon("C:/igra-art-firewatch-campo-santo-pozharnyi-dozor-chelovek-snuf.jpg"))
            msg_box.setText(f"Неправильно. Попробуйте снова или нажмите 'Показать значение'.")
            msg_box.addButton(QMessageBox.Ok)
            show_button = msg_box.addButton("Показать значение", QMessageBox.ActionRole)
            msg_box.exec()
            if msg_box.clickedButton() == show_button:
                QMessageBox.information(self, "Значение слова", f"Правильное значение: {correct_meaning}")
            print(f"Неправильный ответ для: {word}: {answer}")

    def retry_later(self):
        if not self.current_test:
            return
        word, test_time = self.current_test
        self.data[word]["pending_tests"].remove(test_time)
        new_test_time = QDateTime.currentDateTime().addSecs(5 * 60)
        self.data[word]["pending_tests"].append(new_test_time)
        self.save_data()
        self.queue.pop(0)
        print(f"Попробуйте {word} позже, новый тест через {new_test_time.toString(Qt.ISODate)}")
        self.start_testing()

    def show_word_list(self):
        self.words_table.setRowCount(len(self.data))
        for row, (word, info) in enumerate(self.data.items()):
            self.words_table.setItem(row, 0, QTableWidgetItem(word))
            self.words_table.setItem(row, 1, QTableWidgetItem(info["meaning"]))
            self.words_table.setItem(row, 2, QTableWidgetItem(info["category"]))
        self.words_table.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoryApp()
    window.show()
    sys.exit(app.exec())
    print(1111)