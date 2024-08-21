import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
from pydub.playback import play
import os

# Set the path to ffmpeg
# AudioSegment.converter = "C://ffmpeg//bin//ffmpeg.exe"  # Adjust the path accordingly


# Step 1: Extract Audio from Video
def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio_path = tempfile.mktemp(suffix='.wav')
    video.audio.write_audiofile(audio_path)
    print("extract_audio_from_video, done")
    return audio_path, video


# Step 2: Speech Recognition
def recognize_speech(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    print(f"Speech{text}")
    return text


# Step 3: Translation to Arabic
from translate import Translator

# Step 3: Translation to Arabic using Translate library
def translate_text(text):
    translator = Translator(to_lang="ar")
    translation = translator.translate(text)
    print(f"Translated text {translation}")
    return translation


# Step 4: Text-to-Speech for Voice Over
def generate_voiceover(text, lang='ar', speaker_id=1):
    tts = gTTS(text=text, lang=lang)
    audio_path = tempfile.mktemp(suffix='.mp3')
    tts.save(audio_path)
    print("Audio path")
    return audio_path


# Step 5: Adjust Speech Rate
# def match_speech_rate(original_audio_path, generated_audio_path):
#     original_audio = AudioSegment.from_file(original_audio_path)
#     generated_audio = AudioSegment.from_file(generated_audio_path)
#
#     original_duration = len(original_audio)
#     generated_duration = len(generated_audio)
#
#     rate = original_duration / generated_duration
#     generated_audio = generated_audio.speedup(playback_speed=rate)
#
#     temp_output = tempfile.mktemp(suffix='.wav')
#     generated_audio.export(temp_output, format="wav")
#     print(f"match speech rate {temp_output}")
#     return temp_output


# Step 6: Merge Voice-Over with Video
def add_voiceover_to_video(video, voiceover_path, output_path):
    voiceover = mp.AudioFileClip(voiceover_path)
    final_video = video.set_audio(voiceover)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("Add voiceover to video")


# Example usage
video_path = 'clip_5.mp4'
output_path = 'output_video.mp4'

# Extract audio from video
audio_path, video = extract_audio_from_video(video_path)

# Recognize speech
recognized_text = recognize_speech(audio_path)

# Translate text to Arabic
translated_text = translate_text(recognized_text)

# Generate voice-over
voiceover_path = generate_voiceover(translated_text)

# Match speech rate
# adjusted_voiceover_path = match_speech_rate(audio_path, voiceover_path)

# Add voice-over to video
add_voiceover_to_video(video, voiceover_path, output_path)
