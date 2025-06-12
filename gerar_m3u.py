import json

with open("canais.json", "r", encoding="utf-8") as f:
    canais = json.load(f)

with open("lista.m3u", "w", encoding="utf-8") as m3u:
    m3u.write("#EXTM3U\n")
    for canal in canais:
        if isinstance(canal, dict):
            url = None
            if isinstance(canal.get("url"), list):
                for u in canal["url"]:
                    if u:
                        url = u
                        break
            elif isinstance(canal.get("url"), str):
                url = canal["url"]

            if url:
                m3u.write(f'#EXTINF:-1 tvg-id="{canal.get("id", "")}" group-title="{canal.get("grupo", "")}",{canal.get("nome", "")}\n')
                m3u.write(f"{url}\n")
