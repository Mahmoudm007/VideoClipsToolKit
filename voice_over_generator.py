import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QFileDialog,
    QMessageBox, QTabWidget, QComboBox, QHBoxLayout, QTextEdit
)
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array, AudioFileClip
import pyttsx3
import os
from merge_videos import *


class VoiceOverWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(QLabel("Enter Text for Voice-Over:"))
        layout.addWidget(self.text_edit)

        self.select_video_btn = QPushButton('Select Video to Add Voice-Over')
        self.select_video_btn.clicked.connect(self.load_video)
        layout.addWidget(self.select_video_btn)

        self.create_voiceover_btn = QPushButton('Create Voice-Over and Merge with Video')
        self.create_voiceover_btn.clicked.connect(self.create_voiceover)
        layout.addWidget(self.create_voiceover_btn)

        self.setLayout(layout)

    def load_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.video = VideoFileClip(file_path)
            QMessageBox.information(self, "Video Loaded", f"Loaded video: {file_path}")

    def create_voiceover(self):
        if not self.video:
            QMessageBox.warning(self, "No Video", "Please load a video first.")
            return

        text = self.text_edit.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "No Text", "Please enter text for the voice-over.")
            return

        # Generate voice-over using pyttsx3
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)

        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume - 0.25)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # changing index changes voices but ony 0 and 1 are working here

        output_audio_path = "voiceover.mp3"
        engine.save_to_file(text, output_audio_path)
        engine.runAndWait()

        # Add the generated voice-over to the video
        audio_clip = AudioFileClip(output_audio_path)
        final_video = self.video.set_audio(audio_clip)

        # Save the final video to the "stories" directory
        output_dir = "stories"
        os.makedirs(output_dir, exist_ok=True)
        output_video_path = os.path.join(output_dir, "video_with_voiceover.mp4")
        final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

        QMessageBox.information(self, "Voice-Over Added", f"Voice-over added and saved to: {output_video_path}")
        final_video.close()
        os.remove(output_audio_path)

    def closeEvent(self, event):
        if self.video:
            self.video.close()
        event.accept()

class VideoEditorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(VideoSplitterWidget(), "Split Video")
        self.tabs.addTab(VideoMergerWidget(), "Merge Videos")
        self.tabs.addTab(VoiceOverWidget(), "Add Voice-Over")
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setWindowTitle('Video Editor')
        self.setGeometry(300, 300, 500, 400)

def main():
    app = QApplication(sys.argv)
    ex = VideoEditorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
