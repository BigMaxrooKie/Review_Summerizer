# worker.py
from PyQt5.QtCore import QObject, pyqtSignal
from sentiment import score_comments, map_score_to_verdict
from similarity_check import average_lcs_similarity
from config import API_KEY
import requests
import re

class ReviewWorker(QObject):
    finished = pyqtSignal(list, str, float)
    error = pyqtSignal(str)

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url

    def extract_video_id(self, url):
        match = re.search(r"v=([^&]+)", url)
        return match.group(1) if match else None

    def fetch_comments(self, video_id):
        comments = []
        url = (
            "https://www.googleapis.com/youtube/v3/commentThreads"
            f"?part=snippet&videoId={video_id}&maxResults=100&key={API_KEY}"
        )

        while True:
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["message"])

            for item in data.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(text)

                # Stop after 500 (good balance for speed)
                if len(comments) >= 500:
                    return comments

            next_token = data.get("nextPageToken")
            if not next_token:
                break

            url = (
                "https://www.googleapis.com/youtube/v3/commentThreads"
                f"?part=snippet&videoId={video_id}"
                f"&maxResults=100&pageToken={next_token}&key={API_KEY}"
            )

        return comments

    def run(self):
        try:
            video_id = self.extract_video_id(self.video_url)
            if not video_id:
                self.error.emit("Invalid YouTube URL")
                return

            comments = self.fetch_comments(video_id)

            if not comments:
                self.error.emit("No comments found (maybe disabled?)")
                return

            verdict = map_score_to_verdict(score_comments(comments))
            similarity = average_lcs_similarity(comments)

            self.finished.emit(comments, verdict, similarity)

        except Exception as e:
            self.error.emit(f"Failed to fetch comments:\n{str(e)}")
