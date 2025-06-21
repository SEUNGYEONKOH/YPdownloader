import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
import os
import yt_dlp
import requests

class YouTubeThumbnailDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Thumbnail Downloader")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter YouTube URL:")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Download Thumbnail")
        self.download_button.clicked.connect(self.download_thumbnail)
        layout.addWidget(self.download_button)

        self.video_button = QPushButton("다운로드")
        self.video_button.clicked.connect(self.download_video)
        layout.addWidget(self.video_button)

        self.thumbnail_label = QLabel()
        layout.addWidget(self.thumbnail_label)

        self.thumbnail_path = os.path.join(os.getcwd(), "thumbnail.jpg")
        self.setLayout(layout)

    def download_thumbnail(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL.")
            return
        try:
            ydl_opts = {
                'skip_download': True,
                'quiet': True,
                'force_generic_extractor': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                if thumbnail_url:
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:
                        with open(self.thumbnail_path, 'wb') as f:
                            f.write(response.content)
                        self.update_thumbnail_image()
                        QMessageBox.information(self, "Success", "Thumbnail downloaded successfully.")
                    else:
                        QMessageBox.warning(self, "Error", "Failed to download thumbnail image.")
                else:
                    QMessageBox.warning(self, "Error", "Could not retrieve thumbnail.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_thumbnail_image(self):
        pixmap = QPixmap(self.thumbnail_path)
        self.thumbnail_label.setPixmap(pixmap.scaled(320, 180))

    def download_video(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL.")
            return
        try:
            ydl_opts = {
                'ffmpeg_location': r'C:\Users\user\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin',
                'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, "Success", "Video downloaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeThumbnailDownloader()
    window.show()
    sys.exit(app.exec_())