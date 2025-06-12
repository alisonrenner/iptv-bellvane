import json

with open("canais.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

with open("lista.m3u", "w", encoding="utf-8") as m3u:
    m3u.write("#EXTM3U\n")
    for canal in dados["canais"]:
        if isinstance(canal, dict):
            url = None
            if isinstance(canal["url"], list):
                for u in canal["url"]:
                    if u:  # usa o primeiro válido
                        url = u
                        break
            else:
                url = canal["url"]

            if url:
                m3u.write(f'#EXTINF:-1 tvg-id="{canal["id"]}" group-title="{canal["grupo"]}",{canal["nome"]}\n')
                m3u.write(f"{url}\n")
