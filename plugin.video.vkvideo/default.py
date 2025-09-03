import sys
import json
import urllib.request
import urllib.parse
import xbmcplugin
import xbmcgui

BASE_API = "https://live.vkvideo.ru/api/v1/live"

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Kodi"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def list_categories(addon_handle):
    url = f"{BASE_API}/categories"
    data = get_json(url)

    for cat in data.get("data", []):
        cat_id = cat.get("id")
        name = cat.get("title", "Без названия")
        icon = cat.get("cover", {}).get("url")

        u = f"{sys.argv[0]}?mode=category&cat_id={cat_id}"
        li = xbmcgui.ListItem(label=name)
        if icon:
            li.setArt({"thumb": icon, "icon": icon, "poster": icon})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

def list_streams(addon_handle, cat_id):
    url = f"{BASE_API}/category/{cat_id}/streams"
    data = get_json(url)

    for stream in data.get("data", []):
        title = stream.get("title", "Без названия")
        username = stream.get("user", {}).get("name", "Неизвестный")
        playback = stream.get("playback_url") or stream.get("hls_url")
        thumb = stream.get("preview", {}).get("url")

        li = xbmcgui.ListItem(label=f"{title} [{username}]")
        li.setInfo("video", {"title": title, "genre": "VK Video Live"})
        if thumb:
            li.setArt({"thumb": thumb, "icon": thumb, "poster": thumb})

        if playback:
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=playback, listitem=li, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == "__main__":
    addon_handle = int(sys.argv[1])
    args = urllib.parse.parse_qs(sys.argv[2][1:])

    mode = args.get("mode", [None])[0]

    if mode == "category":
        cat_id = args.get("cat_id", [None])[0]
        if cat_id:
            list_streams(addon_handle, cat_id)
    else:
        list_categories(addon_handle)
