# worker.py

from PyQt5.QtCore import QObject, pyqtSignal
from sentiment import score_comments, map_score_to_verdict
from similarity_check import average_lcs_similarity

class ReviewWorker(QObject):
    finished = pyqtSignal(str, float)  # verdict, similarity

    def __init__(self, comments):
        super().__init__()
        self.comments = comments

    def run(self):
        score = score_comments(self.comments)
        verdict = map_score_to_verdict(score)
        similarity = average_lcs_similarity(self.comments)
        self.finished.emit(verdict, similarity)