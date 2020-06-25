import PySimpleGUI as sg
import youtube_downloader as ytd
import threading
import queue



def download_event(event: str, in_queue: queue.Queue):
    global values

    if values["vid_url"]:
        url = values["vid_url"]
    else:
        return None

    if values['save_folder']:
        path = values["save_folder"]
    else:
        path = sg.popup_get_folder("Choose save location")
        window["save_folder"].update(path)
        return None

    # for i in range(1, 10000):
    #     stay = sg.one_line_progress_meter('My Meter', i + 1, 10000, 'key', 'Optional message', orientation='h')
    #     if not stay:
    #         return

    if event.split()[1] == "mp3":
        thread = threading.Thread(target=ytd.download_to_mp3, args=(url, path, in_queue))
        thread.start()
        return thread

    else:
        thread = threading.Thread(target=ytd.download_video, args=(url, path, in_queue))
        thread.start()
        return thread



def download_completed(return_queue: queue.Queue):
    print("download copleted")
    status, log = return_queue.get()
    if status:
        sg.Popup(log)
    else:
        sg.Popup(log, button_color=["white", "red"])


sg.theme('Dark Blue 3')
layout = [
    [sg.Text("Youtube Link: "), sg.InputText(key="vid_url")],
    [sg.Text("Choose save location: "), sg.FolderBrowse(target=(2, 0))],
    [sg.InputText(key="save_folder", disabled=True)],
    [sg.Button("Download", key="Download mp4"), sg.Button("Download mp3"), sg.Cancel('Cancel')]
]
window = sg.Window('Youtube downloader', layout)

return_queue = queue.Queue(2)
downloading = False
#thread = threading.Thread()

while True:
    event, values = window.read(1000)
    # sg.Print("lol")
    # for x, y in values.items():
    # print(x, ": ", y)
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    if event in ("Download mp4", "Download mp3"):
        thread = download_event(event, return_queue)
        if thread:
            downloading = True

    if downloading and not thread.is_alive():
        download_completed(return_queue)
        downloading = False



window.close()
