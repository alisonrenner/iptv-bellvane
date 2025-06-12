import json
import requests
from datetime import datetime

def link_ativo(url):
    try:
        resposta = requests.get(url, timeout=5, stream=True)
        return resposta.status_code == 200
    except:
        return False

with open("canais.json", "r", encoding="utf-8") as f:
    canais = json.load(f)

with open("lista.m3u", "w", encoding="utf-8") as m3u:
    m3u.write(f"#EXTM3U\n# Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for nome, urls in canais.items():
        if isinstance(urls, list) and urls:
            for url in urls:
                if link_ativo(url):
                    m3u.write(f'#EXTINF:-1,{nome}\n{url}\n')
                    break
