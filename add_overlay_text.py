import sys
import os
import speech_recognition as sr
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
from moviepy.config import change_settings
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from voice_over_generator import *

# Replace with your actual path to magick.exe
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})


class TextOverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_video_btn = QPushButton('Select Video to Convert Audio to Text')
        self.select_video_btn.clicked.connect(self.load_video)
        layout.addWidget(self.select_video_btn)

        self.add_text_overlay_btn = QPushButton('Add Text Overlay from Audio')
        self.add_text_overlay_btn.clicked.connect(self.add_text_overlay)
        layout.addWidget(self.add_text_overlay_btn)

        self.setLayout(layout)

    def load_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.video = VideoFileClip(file_path)
            QMessageBox.information(self, "Video Loaded", f"Loaded video: {file_path}")

    def add_text_overlay(self):
        if not self.video:
            QMessageBox.warning(self, "No Video", "Please load a video first.")
            return

        # Extract audio from video
        audio_path = "extracted_audio.wav"
        self.video.audio.write_audiofile(audio_path)

        # Convert audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                QMessageBox.information(self, "Audio to Text", f"Recognized text: {text}")
            except sr.UnknownValueError:
                QMessageBox.warning(self, "Error", "Could not understand audio.")
                return
            except sr.RequestError as e:
                QMessageBox.warning(self, "Error", f"Could not request results; {e}")
                print(e)
                return

        # Define font properties and fallback font
        font = 'Arial-Bold'  # Replace with an anime-style font if available
        fontsize = 28
        color = 'yellow'

        # Split text into chunks of up to 5 words
        words = text.split()
        max_words_per_frame = 5
        chunks = [words[i:i + max_words_per_frame] for i in range(0, len(words), max_words_per_frame)]

        # Create a list to store text clips
        text_clips = []

        # Create a text clip for each chunk
        for i, chunk in enumerate(chunks):
            chunk_text = ' '.join(chunk)
            try:
                text_clip = TextClip(
                    chunk_text, fontsize=fontsize, color=color, font=font,
                    stroke_color="black", stroke_width=2
                ).set_position('center').set_duration(self.video.duration / len(chunks)).set_start(i * (self.video.duration / len(chunks)))
                text_clips.append(text_clip)
            except Exception as e:
                QMessageBox.warning(self, "Font Error", f"Error using the specified font: {str(e)}. Trying fallback font.")
                print("Font Error", f"Error using the specified font: {str(e)}. Trying fallback font.")
                font = 'Arial'  # Fallback font
                text_clip = TextClip(
                    chunk_text, fontsize=fontsize, color=color, font=font,
                    stroke_color="black", stroke_width=2
                ).set_position('center').set_duration(self.video.duration / len(chunks)).set_start(i * (self.video.duration / len(chunks)))
                text_clips.append(text_clip)

        # Overlay text on the video
        try:
            final_clip = CompositeVideoClip([self.video] + text_clips)

            # Save the final video with a unique name
            output_dir = "stories"
            os.makedirs(output_dir, exist_ok=True)
            output_video_path = os.path.join(output_dir, "video_with_text_overlay.mp4")
            final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

            QMessageBox.information(self, "Text Overlay Added", f"Text overlay added and saved to: {output_video_path}")
            final_clip.close()
            os.remove(audio_path)
        except Exception as e:
            QMessageBox.warning(self, "Video Processing Error", f"An error occurred while processing the video: {str(e)}")
            print("Video Processing Error", f"An error occurred while processing the video: {str(e)}")

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
        self.tabs.addTab(TextOverlayWidget(), "Add Text Overlay")
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setWindowTitle('Video Editor')
        self.setGeometry(300, 300, 600, 400)

def main():
    app = QApplication(sys.argv)
    ex = VideoEditorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
