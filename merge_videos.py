import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QFileDialog,
    QMessageBox, QTabWidget, QComboBox, QHBoxLayout
)
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array



class VideoSplitterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video = None
        self.initUI()

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

        output_dir = "video_clips"
        os.makedirs(output_dir, exist_ok=True)

        clip = self.video.subclip(start_time, end_time)
        clip_filename = os.path.join(output_dir,
                                     f"clip_{start_time // 60:.0f}m{start_time % 60:.0f}s_to_{end_time // 60:.0f}m{end_time % 60:.0f}s.mp4")
        clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac")

        QMessageBox.information(self, "Clip Created", f"Created clip: {clip_filename}")
        clip.close()

    def closeEvent(self, event):
        if self.video:
            self.video.close()
        event.accept()


from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array

class VideoMergerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video1 = None
        self.video2 = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_video1_btn = QPushButton('Select First Video')
        self.select_video1_btn.clicked.connect(lambda: self.load_video(1))
        layout.addWidget(self.select_video1_btn)

        self.select_video2_btn = QPushButton('Select Second Video')
        self.select_video2_btn.clicked.connect(lambda: self.load_video(2))
        layout.addWidget(self.select_video2_btn)

        self.audio_source_label = QLabel("Select Audio Source:")
        layout.addWidget(self.audio_source_label)

        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItems(["First Video", "Second Video"])
        layout.addWidget(self.audio_source_combo)

        self.merge_btn = QPushButton('Merge Videos')
        self.merge_btn.clicked.connect(self.merge_videos)
        layout.addWidget(self.merge_btn)

        self.setLayout(layout)

    def load_video(self, video_number):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            if video_number == 1:
                self.video1 = VideoFileClip(file_path)
                QMessageBox.information(self, "Video Loaded", f"Loaded first video: {file_path}")
            elif video_number == 2:
                self.video2 = VideoFileClip(file_path)
                QMessageBox.information(self, "Video Loaded", f"Loaded second video: {file_path}")

    def merge_videos(self):
        if not self.video1 or not self.video2:
            QMessageBox.warning(self, "Videos Missing", "Please load both videos before merging.")
            return

        # Repeat shorter video to match the length of the longer one
        if self.video1.duration > self.video2.duration:
            self.video2 = concatenate_videoclips([self.video2] * (int(self.video1.duration // self.video2.duration) + 1)).subclip(0, self.video1.duration)
        else:
            self.video1 = concatenate_videoclips([self.video1] * (int(self.video2.duration // self.video1.duration) + 1)).subclip(0, self.video2.duration)

        # Stack the videos vertically using clips_array
        final_clip = clips_array([[self.video1], [self.video2]])

        # Choose the audio source
        if self.audio_source_combo.currentText() == "First Video":
            final_clip = final_clip.set_audio(self.video1.audio)
        else:
            final_clip = final_clip.set_audio(self.video2.audio)

        # Save the merged video
        output_dir = "merged_videos"
        os.makedirs(output_dir, exist_ok=True)
        merged_filename = os.path.join(output_dir, "merged_video.mp4")
        final_clip.write_videofile(merged_filename, codec="libx264", audio_codec="aac")

        QMessageBox.information(self, "Video Merged", f"Merged video created: {merged_filename}")
        final_clip.close()

    def closeEvent(self, event):
        if self.video1:
            self.video1.close()
        if self.video2:
            self.video2.close()
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
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setWindowTitle('Video Editor')
        self.setGeometry(300, 300, 400, 300)


def main():
    app = QApplication(sys.argv)
    ex = VideoEditorApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
