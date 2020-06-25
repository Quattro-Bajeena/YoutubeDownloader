import youtube_downloader as ytd


url = "https://www.youtube.com/watch?v=wcdquhB6hT8"
result, message = ytd.download_video(url, "F:\Programowanie\Python\YoutubeDownloader\Downloads")
print("Download succed: ", result)
print("Message: ", message)
