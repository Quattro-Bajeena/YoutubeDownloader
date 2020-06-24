from pytube import YouTube, Playlist, Stream
from os import path, remove, rename
import time
from shutil import move
from moviepy.audio.io.AudioFileClip import AudioFileClip


def convert_to_mp3(file_path: str):
    file_name_ext = path.basename(file_path)
    file_name = path.splitext(file_name_ext)[0]
    new_filename = file_name + ".mp3"

    if not path.exists(new_filename):
        rename(file_name_ext, new_filename)

    print(f"renamed: {new_filename}")
    return new_filename


def show_progress_bar(stream: Stream, chunk: bytes, bytes_remaining: int):
    print(bytes_remaining)
    return


def move_file(org_path: str, new_path: str):
    file_name = path.basename(org_path)
    print(f"Moving file '{file_name}' from {org_path} to {new_path}")
    move(org_path, new_path + "/" + file_name)


def download_to_mp3(url: str, path: str):
    start = time.time()
    video = YouTube(url)
    title = video.title
    print(f"Title: {title}")
    # After download finishes it will be converted to mp3 and org file deleted
    #video.register_on_complete_callback(convert_to_mp3)

    # Only streams with audio, with mp4 extension, highest bitrate first
    audio_streams = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
    if audio_streams:
        org_path = audio_streams[0].download()
        print("Orginal path: ", org_path)
        convert_path = convert_to_mp3(org_path)
        move_file(convert_path, path)
        end = time.time()
        print(f"Time elapsed: {round(end - start, 1)} s")
    else:
        print("There were no audio streams")
