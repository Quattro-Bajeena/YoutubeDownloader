from pytube import YouTube, Playlist, Stream
import time
import os
import shutil
import moviepy.editor as mpe
import subprocess
from ffmpy import FFmpeg


def convert_to_mp3(stream: Stream, file_path: str) -> str:
    folder = os.path.dirname(file_path)
    filename_ext = os.path.basename(file_path)
    filename_mp3 = os.path.splitext(filename_ext)[0] + ".mp3"

    new_path = folder + "\\" + filename_mp3
    os.rename(folder + "\\" + filename_ext, new_path)
    return new_path


def append_to_filename(file_path: str, append_str: str) -> str:
    folder = os.path.dirname(file_path)
    filename_ext = os.path.basename(file_path)
    filename = os.path.splitext(filename_ext)[0]
    ext = os.path.splitext(filename_ext)[1]

    path_appended = folder + "\\" + filename + append_str + ext
    os.rename(file_path, path_appended)
    return path_appended


def combine_video_audio(video_path: str, audio_path: str, output_path: str):
    try:
        # Using raw FFmpeg
        cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}"'
        # subprocess.call(cmd, shell=True)

        # using wrapper around FFmpeg
        ff = FFmpeg(
            inputs={video_path: None, audio_path: None},
            outputs={output_path: '-c:v copy -c:a aac'}
        )
        # ff.cmd = cmd
        ff.run()
    except:
        print("Couldn't find FFmpeg, converting by moviepy")
        video = mpe.VideoFileClip(video_path)
        audio = mpe.AudioFileClip(audio_path)
        final_clip = video.set_audio(audio)
        final_clip.write_videofile(output_path)
    finally:
        os.remove(video_path)
        os.remove(audio_path)


def show_progress_bar(stream: Stream, chunk: bytes, bytes_remaining: int):
    print(bytes_remaining)
    return


def move_file(org_path: str, new_path: str):
    file_name = os.path.basename(org_path)
    print(f"Moving file '{file_name}' from {org_path} to {new_path}")
    shutil.move(org_path, new_path + "/" + file_name)


def download_to_mp3(url: str, path: str) -> (bool, str):
    start = time.time()
    try:
        video = YouTube(url)
    except:
        print("Couldn't get video, bad url")
        return (False, "Invalid URL")
    title = video.title
    print(f"Title: {title}")

    # After download finishes it will be converted to mp3 and org file deleted
    video.register_on_complete_callback(convert_to_mp3)

    # Only streams with audio, with mp4 extension, highest bitrate first
    audio_streams = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
    if audio_streams:
        if not os.path.exists(path + "\\" + title + ".mp3"):
            audio_streams[0].download(path)
            end = time.time()
            return (True, f"Downloaded video in {round(end - start, 1)} s")
        else:
            return(False, "File already exists")
    else:
        return (False, "There were no audio streams")



def download_video(url: str, path: str) -> (bool, str):

    start = time.time()
    try:
        video = YouTube(url)
    except:
        return (False, "Invalid URL")

    title = video.title
    print(f"Title: {title}")

    if not os.path.exists(path + "\\" + title + ".mp4"):
        video_stream = video.streams.filter(file_extension='mp4').order_by('resolution').desc()[0]
        try:
            if video_stream.is_adaptive:
                audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()[0]

                audio_path = audio_stream.download(path)
                audio_path = convert_to_mp3(None, audio_path)
                audio_path_tmp = append_to_filename(audio_path, "_audio")

                video_path = video_stream.download(path)
                video_path_tmp = append_to_filename(video_path, "_video")
                print("Video path: ",video_path)
                combine_video_audio(video_path_tmp, audio_path_tmp, video_path)

                end = time.time()
                return (True, f"Downloaded video in {round(end - start, 1)} s")
            else:
                video.streams.get_highest_resolution().download(path)
                end = time.time()
                return (True, f"Downloaded video in {round(end - start, 1)} s")
        except:
            return(False, "Couldn't download video")
    else:
        return (False, "File already exists")
