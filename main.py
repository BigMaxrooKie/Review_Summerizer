# main.py

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtCore import QThread
from utilities import load_comments
from worker import ReviewWorker


class ReviewChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_area = QTextEdit()
        self.result_label = QLabel("Sentiment Result Will Appear Here")
        self.button = QPushButton('Load and Analyze Reviews')
        self.button.clicked.connect(self.load_and_analyze)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)
        self.setWindowTitle('Review Sentiment Analyzer')

    def load_and_analyze(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Review File', '', 'Text Files (*.txt)')
        if file_path:
            comments = load_comments(file_path)
            self.text_area.setText('\n'.join(comments))
            self.result_label.setText("Analyzing...")

            self.thread = QThread()
            self.worker = ReviewWorker(comments)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.display_result)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

    def display_result(self, verdict, similarity):
        self.result_label.setText(f"Sentiment result: {verdict}\nComment Similarity: {similarity}")


if __name__ == "__main__":
    app = QApplication([])
    window = ReviewChecker()
    window.show()
    app.exec_()  # For PyQt5
