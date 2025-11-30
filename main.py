# main.py
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit,
                             QVBoxLayout, QLineEdit, QLabel, QMessageBox)
from PyQt5.QtCore import QThread
from worker import ReviewWorker

class ReviewChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Comment Sentiment Analyzer")
        self.resize(900, 700)
        self.init_ui()

    def init_ui(self):
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube video URL here")

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        self.result_label = QLabel("Result will appear here")
        self.result_label.setStyleSheet("font-size: 16px; color: navy;")

        self.button = QPushButton("Fetch Comments from YouTube & Analyze")
        self.button.clicked.connect(self.start_analysis)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>YouTube Video URL:</b>"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.text_area)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def start_analysis(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Empty URL", "Please paste a YouTube link first")
            return

        self.button.setEnabled(False)
        self.result_label.setText("Fetching comments… (10–40 seconds)")
        self.text_area.clear()

        self.thread = QThread()
        self.worker = ReviewWorker(url)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.start()

    def on_finished(self, comments, verdict, similarity):
        self.text_area.setText("\n\n".join(comments[:100]))  # show first 100
        total = len(comments)
        self.result_label.setText(
            f"Sentiment: {verdict}\n"
            f"Average Comment Similarity: {similarity}\n\n"
            f"Successfully analyzed {total} comments!"
        )
        self.button.setEnabled(True)

    def on_error(self, msg):
        QMessageBox.critical(self, "Error", msg)
        self.result_label.setText("Failed")
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    window = ReviewChecker()
    window.show()
    app.exec_()