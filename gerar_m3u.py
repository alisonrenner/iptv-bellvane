import json
from datetime import datetime

with open("canais.json", "r", encoding="utf-8") as f:
    canais = json.load(f)

with open("lista.m3u", "w", encoding="utf-8") as m3u:
    m3u.write(f"#EXTM3U\n# Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for nome, urls in canais.items():
        if isinstance(urls, list) and urls:
            url = urls[0]  # usa o primeiro link válido
            m3u.write(f'#EXTINF:-1,{nome}\n{url}\n')
