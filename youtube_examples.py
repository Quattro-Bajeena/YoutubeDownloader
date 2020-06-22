'''
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
yt.streams.filter(progressive=True)
yt.streams.filter(adaptive=True)
yt.streams.filter(only_audio=True)
yt.streams.filter(subtype='mp4')
yt.streams.filter(subtype='mp4', progressive=True)
yt.streams.filter(subtype='mp4').filter(progressive=True)
yt.streams.get_by_itag(22)

def convert_to_aac(stream: Stream, file_path: str):
         return  # do work
yt.register_on_complete_callback(convert_to_aac)

def show_progress_bar(stream: Stream, chunk: bytes, bytes_remaining: int):
         return  # do work

yt.register_on_progress_callback(show_progress_bar)
for video in playlist:
 	video.streams.get_highest_resolution().download()
'''