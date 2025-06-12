import json
import requests
from datetime import datetime

def link_ativo(url):
    try:
        resposta = requests.get(url, timeout=5, stream=True)
        return resposta.status_code == 200
    except:
        return False

def normalizar_nome(nome):
    return nome.strip().lower().replace(" hd", "").replace("  ", " ")

with open("canais.json", "r", encoding="utf-8") as f:
    canais = json.load(f)

# Verificações
nomes_normalizados = {}
links_usados = set()
duplicados = []
links_repetidos = []
sem_links = []

for nome, urls in canais.items():
    norm = normalizar_nome(nome)
    if norm in nomes_normalizados:
        duplicados.append((nome, nomes_normalizados[norm]))
    else:
        nomes_normalizados[norm] = nome

    if not urls:
        sem_links.append(nome)
        continue

    for url in urls:
        if url in links_usados:
            links_repetidos.append((nome, url))
        else:
            links_usados.add(url)

print("✅ Verificação concluída:")
if duplicados:
    print(f"⚠️ Canais com nomes parecidos/iguais:")
    for a, b in duplicados:
        print(f"   - '{a}' e '{b}'")
if links_repetidos:
    print(f"⚠️ Links usados em mais de um canal:")
    for nome, url in links_repetidos:
        print(f"   - {url} em '{nome}'")
if sem_links:
    print(f"⚠️ Canais sem nenhum link:")
    for nome in sem_links:
        print(f"   - {nome}")
if not (duplicados or links_repetidos or sem_links):
    print("🎉 Nenhum problema encontrado.")

# Geração da M3U
with open("lista.m3u", "w", encoding="utf-8") as m3u:
    m3u.write(f"#EXTM3U\n# Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for nome, urls in canais.items():
        if isinstance(urls, list) and urls:
            for url in urls:
                if link_ativo(url):
                    m3u.write(f'#EXTINF:-1,{nome}\n{url}\n')
                    break
