import requests
from bs4 import BeautifulSoup
import re
import json
import os

def capturar_m3u8(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        encontrados = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html)
        if encontrados:
            return encontrados[0]

        soup = BeautifulSoup(html, 'html.parser')
        iframes = soup.find_all('iframe')
        for iframe in iframes:
            src = iframe.get('src')
            if src:
                iframe_url = requests.compat.urljoin(url, src)
                resp_iframe = requests.get(iframe_url, headers=headers, timeout=10)
                if '.m3u8' in resp_iframe.text:
                    m3u8_links = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', resp_iframe.text)
                    if m3u8_links:
                        return m3u8_links[0]

        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and ".m3u8" in script.string:
                m3u8_js = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', script.string)
                if m3u8_js:
                    return m3u8_js[0]

        return None
    except Exception as e:
        print(f"[ERRO] {url} -> {e}")
        return None

def extrair_nome_canal(url):
    base = url.split("/")[-1]
    nome = re.sub(r'\.php|\.html|\.htm', '', base)
    return nome.upper().strip()

def main():
    if not os.path.exists("fontes.txt"):
        print("Arquivo fontes.txt não encontrado.")
        return

    with open("fontes.txt", "r", encoding="utf-8") as f:
        links = [linha.strip() for linha in f if linha.strip()]

    canais = {}

    for url in links:
        nome = extrair_nome_canal(url)
        print(f"[+] Processando: {nome} -> {url}")
        link_m3u8 = capturar_m3u8(url)
        if link_m3u8:
            canais[nome] = {
                "site_fonte": url,
                "grupo": "Sem Grupo",
                "logo": "",
                "links": [link_m3u8]
            }
            print(f"  ✔ Capturado: {link_m3u8}")
        else:
            print(f"  ✘ Nenhum link encontrado.")

    with open("canais_temp.json", "w", encoding="utf-8") as f:
        json.dump(canais, f, indent=2, ensure_ascii=False)
        print(f"[✔] canais_temp.json atualizado com {len(canais)} canais.")

if __name__ == "__main__":
    main()
