import json
from datetime import datetime

with open('canais.json', 'r', encoding='utf-8') as f:
    canais = json.load(f)

with open('lista.m3u', 'w', encoding='utf-8') as m3u:
    m3u.write(f"# Arquivo atualizado em: {datetime.now().isoformat()}\n\n")
    for canal in canais:
        m3u.write(f"#EXTINF:-1 tvg-id=\"{canal['id']}\" group-title=\"{canal['grupo']}\",{canal['nome']}\n")
        for link in canal['links']:
            m3u.write(f"{link}\n")
        m3u.write("\n")
