import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


class VideoSplitterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.video = None
        self.output_dir = "video_clips"
        os.makedirs(self.output_dir, exist_ok=True)

    def initUI(self):
        layout = QVBoxLayout()

        self.select_btn = QPushButton('Select Video')
        self.select_btn.clicked.connect(self.load_video)
        layout.addWidget(self.select_btn)

        self.start_label = QLabel("Start Time (min:sec):")
        layout.addWidget(self.start_label)

        self.start_min = QSpinBox()
        self.start_min.setRange(0, 59)
        self.start_min.setPrefix("Min: ")
        layout.addWidget(self.start_min)

        self.start_sec = QSpinBox()
        self.start_sec.setRange(0, 59)
        self.start_sec.setPrefix("Sec: ")
        layout.addWidget(self.start_sec)

        self.end_label = QLabel("End Time (min:sec):")
        layout.addWidget(self.end_label)

        self.end_min = QSpinBox()
        self.end_min.setRange(0, 59)
        self.end_min.setPrefix("Min: ")
        layout.addWidget(self.end_min)

        self.end_sec = QSpinBox()
        self.end_sec.setRange(0, 59)
        self.end_sec.setPrefix("Sec: ")
        layout.addWidget(self.end_sec)

        self.split_btn = QPushButton('Split Video')
        self.split_btn.clicked.connect(self.split_video)
        layout.addWidget(self.split_btn)

        self.setLayout(layout)
        self.setWindowTitle('Video Splitter')
        self.setGeometry(300, 300, 300, 200)

    def load_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "",
                                                   "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.video = VideoFileClip(file_path)
            QMessageBox.information(self, "Video Loaded",
                                    f"Loaded video: {file_path}\nDuration: {self.video.duration // 60:.0f} min {self.video.duration % 60:.0f} sec")

    def split_video(self):
        if not self.video:
            QMessageBox.warning(self, "No Video", "Please load a video first.")
            return

        start_time = self.start_min.value() * 60 + self.start_sec.value()
        end_time = self.end_min.value() * 60 + self.end_sec.value()

        if start_time >= end_time or end_time > self.video.duration:
            QMessageBox.warning(self, "Invalid Time",
                                "End time must be greater than start time and within the video duration.")
            return

        clip = self.video.subclip(start_time, end_time)
        clip_filename = os.path.join(self.output_dir,
                                     f"clip_{start_time // 60:.0f}m{start_time % 60:.0f}s_to_{end_time // 60:.0f}m{end_time % 60:.0f}s.mp4")
        clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac")

        QMessageBox.information(self, "Clip Created", f"Created clip: {clip_filename}")
        clip.close()

    def closeEvent(self, event):
        if self.video:
            self.video.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    ex = VideoSplitterWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
