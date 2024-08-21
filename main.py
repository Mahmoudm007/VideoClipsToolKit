from moviepy.editor import TextClip

# Simple test to create an image with text
text_clip = TextClip("Hello, World!", fontsize=70, color='yellow', font='Arial-Bold')
text_clip.save_frame("test_image.png")
