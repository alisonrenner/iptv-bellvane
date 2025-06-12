import json

with open("canais.json", "r", encoding="utf-8") as f:
    canais = json.load(f)

with open("lista.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for nome, links in canais.items():
        if links:
            f.write(f"#EXTINF:-1,{nome}\n{links[0]}\n")
