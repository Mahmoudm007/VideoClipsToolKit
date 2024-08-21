from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def split_video_into_clips(input_video_path, clip_length=30):
    # Load the video file
    video = VideoFileClip(input_video_path)

    # Calculate the number of clips
    video_duration = video.duration  # Duration in seconds
    num_clips = int(video_duration // clip_length)

    # Create an output directory if it doesn't exist
    output_dir = "1,000 Blind People See For The First Time/30sec"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_clips + 1):
        start_time = i * clip_length
        end_time = min((i + 1) * clip_length, video_duration)

        # Generate the clip
        clip = video.subclip(start_time, end_time)

        # Define output filename
        clip_filename = os.path.join(output_dir, f"clip_{i + 1}.mp4")

        # Write the clip to a file
        clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac")

        print(f"Created clip: {clip_filename}")

    # Close the video file to release resources
    video.close()


# Example usage
input_video = "long_videos/1,000 Blind People See For The First Time.mp4"  # Replace with your video path
split_video_into_clips(input_video)
