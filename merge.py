import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, clips_array
from PIL import Image

# If using a newer version of Pillow, replace ANTIALIAS with Resampling.LANCZOS
if hasattr(Image, 'Resampling'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Directories containing the video clips
video_clips_dir = "Ages 1 _ 100 Fight For 500_000"
satysfiy_dir = "satisfy_2min"
output_dir = "merged_videos_1"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop over all 32 clips
for i in range(1, 13):
    video_clip_path = os.path.join(video_clips_dir, f"clip_{i}.mp4")
    sat_clip_path = os.path.join(satysfiy_dir, f"clip_{i}.mp4")
    print(sat_clip_path)

    if os.path.exists(video_clip_path) and os.path.exists(sat_clip_path):
        video_clip = VideoFileClip(video_clip_path)
        sat_clip = VideoFileClip(sat_clip_path)

        # Make the shorter video repeat until it matches the length of the longer video
        if video_clip.duration > sat_clip.duration:
            sat_clip = sat_clip.loop(duration=video_clip.duration)
        else:
            video_clip = video_clip.loop(duration=sat_clip.duration)

        # Resize both videos to have the same width based on the larger one
        max_width = max(video_clip.w, sat_clip.w)
        video_clip_resized = video_clip.resize(width=max_width)
        sat_clip_resized = sat_clip.resize(width=max_width)

        # Further resize to match the 2/3 and 1/3 height ratio based on the max width
        total_height = video_clip_resized.h + sat_clip_resized.h
        print(f"Total height: {total_height}")
        print(f"video height: {video_clip_resized.h}")
        print(f"Stat height: {sat_clip_resized.h}")
        ##
        # From vertically to horizontally change videos height
        ##
        video_clip_resized = video_clip_resized.resize(height=int(1160))
        sat_clip_resized = sat_clip_resized.resize(height=int(1160))
        print(f"video height: {video_clip_resized.h}")
        print(f"Stat height: {sat_clip_resized.h}")

        if sat_clip_path == "satisfy_2min\clip_6.mp4" or "satisfy_2min\clip_7.mp4" or "satisfy_2min\clip_8.mp4" or "satisfy_2min\clip_9.mp4" or "satisfy_2min\clip_10.mp4" or "satisfy_2min\clip_11.mp4":
            # Merge the two videos ## horizontally ## using clips_array
            merged_clip = clips_array([[video_clip_resized, sat_clip_resized]])
        else:
            # Merge the two videos vertically using clips_array
            merged_clip = clips_array([[video_clip_resized], [sat_clip_resized]])

        # Set the audio of the merged video to be the audio from the video clip
        merged_clip = merged_clip.set_audio(video_clip.audio)

        # Save the merged video
        output_path = os.path.join(output_dir, f"merged_clip_{i}.mp4")
        merged_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Close the clips to release resources
        video_clip.close()
        sat_clip.close()
        merged_clip.close()

print("Merging complete!")
