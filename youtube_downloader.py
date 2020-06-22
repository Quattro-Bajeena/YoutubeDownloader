from pytube import YouTube, Playlist, Stream
from os import path, remove, rename
import time
from moviepy.audio.io.AudioFileClip import AudioFileClip


def convert_to_mp3(stream: Stream, file_path: str):
    file_name_ext = path.basename(file_path)
    file_name = path.splitext(file_name_ext)[0]

    if not path.exists(file_name + ".mp3"):
        rename(file_name_ext, file_name + ".mp3")

    # clip = AudioFileClip(file_name_ext)
    # clip.write_audiofile(file_name + ".mp3")
    # remove(file_name_ext)
    return


def show_progress_bar(stream: Stream, chunk: bytes, bytes_remaining: int):
    print(bytes_remaining)
    return


def download_to_mp3(url: str):
    start = time.time()
    video = YouTube(url)
    title = video.title
    print(f"Title: {title}")
    # After download finishes it will be converted to mp3 and org file deleted
    video.register_on_complete_callback(convert_to_mp3)

    # Only streams with audio, with mp4 extension, highest bitrate first
    audio_streams = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
    if audio_streams:
        audio_streams[0].download()
        end = time.time()
        print(f"Time elapsed: {round(end - start, 1)} s")
    else:
        print("There were no audio streams")
