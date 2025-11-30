# main.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QLineEdit, QLabel, QMessageBox,
    QHBoxLayout, QFrame
)
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QFont
from worker import ReviewWorker


class ReviewChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Review Summarizer")  # ← UPDATED TITLE HERE
        self.resize(950, 720)

        # Modern background color
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F2F5;
                font-family: 'Segoe UI';
            }
        """)

        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # ---------- HEADER ----------
        header = QLabel("📊 Review Summarizer")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff5f6d, stop:1 #ffc371
                );
                color: white;
                padding: 20px;
                font-size: 26px;
                font-weight: bold;
                border-radius: 18px;
            }
        """)

        # ---------- INPUT CARD ----------
        input_card = QFrame()
        input_card.setFrameShape(QFrame.StyledPanel)
        input_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 18px;
                border: 1px solid #E0E0E0;
            }
        """)

        input_layout = QVBoxLayout()
        input_layout.setSpacing(12)

        label = QLabel("Paste YouTube URL:")
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=xxxx")
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 12px;
                border: 2px solid #ddd;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #ff6a88;
            }
        """)

        self.button = QPushButton("Analyze Comments")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #ff6a88;
                color: white;
                padding: 12px;
                border-radius: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff3e60;
            }
            QPushButton:pressed {
                background-color: #d92d4e;
            }
        """)
        self.button.clicked.connect(self.start_analysis)

        input_layout.addWidget(label)
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.button)
        input_card.setLayout(input_layout)

        # ---------- RESULT CARD ----------
        result_card = QFrame()
        result_card.setFrameShape(QFrame.StyledPanel)
        result_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 20px;
                border: 1px solid #E0E0E0;
            }
        """)

        result_layout = QVBoxLayout()

        self.result_label = QLabel("Result will appear here")
        self.result_label.setFont(QFont("Segoe UI", 14))
        self.result_label.setStyleSheet("color: #333;")

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background: #FAFAFA;
                border: none;
                padding: 14px;
                border-radius: 12px;
                font-size: 14px;
            }
        """)

        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.text_area)
        result_card.setLayout(result_layout)

        # Add widgets to main layout
        main_layout.addWidget(header)
        main_layout.addWidget(input_card)
        main_layout.addWidget(result_card)

        self.setLayout(main_layout)

    # ---------------- Logic unchanged ----------------
    def start_analysis(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Empty URL", "Please paste a link first")
            return

        self.button.setEnabled(False)
        self.result_label.setText("Fetching comments… Please wait")
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
        self.text_area.setText("\n\n".join(comments[:100]))
        total = len(comments)

        self.result_label.setText(
            f"<b>Sentiment:</b> {verdict}<br>"
            f"<b>Average Similarity:</b> {similarity}<br>"
            f"<b>Total Comments Analyzed:</b> {total}"
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
