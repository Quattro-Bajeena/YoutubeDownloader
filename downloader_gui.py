import PySimpleGUI as sg
import youtube_downloader as ytd

sg.theme('Dark Blue 3')
layout = [
    [sg.Text("Youtube Link: "), sg.InputText(key="vid_url")],
    [sg.Text("Choose save location: "), sg.FolderBrowse(target=(2, 0))],
    [sg.InputText(key="save_folder", disabled=True)],
    [sg.Submit("Download"), sg.Cancel('Cancel')]
]
window = sg.Window('Youtube mp3 downloader', layout)


def download_event():
    global values

    if values["vid_url"]:
        url = values["vid_url"]
    else:
        return

    if values['save_folder']:
        path = values["save_folder"]
    else:
        path = sg.popup_get_folder("Choose save location")
        window["save_folder"].update(path)
        if not path:
            return

    print("URL: ",url)
    print("Path: ", path)

    # for i in range(1, 10000):
    #     stay = sg.one_line_progress_meter('My Meter', i + 1, 10000, 'key', 'Optional message', orientation='h')
    #     if not stay:
    #         return
    try:
        ytd.download_to_mp3(url, path)
    except:
        print("Couldn't download the video")


while True:
    event, values = window.read()
    #sg.Print("lol")
    print("event: ", event)
    for x, y in values.items():
        print(x, ": ", y)
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    if event == 'Download':
        download_event()


window.close()
