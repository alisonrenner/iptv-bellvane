import requests
from bs4 import BeautifulSoup
import json


def verificar_link_funcional(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10, stream=True)
        if res.status_code == 200 and int(res.headers.get('Content-Length', 1)) > 0:
            return True
        else:
            return False
    except:
        return False


def link_parece_stream_ao_vivo(link):
    palavras_ao_vivo = ['.m3u8', '/live/', '/hls/', '/stream/', '/index.m3u8', '/playlist.m3u8']
    palavras_de_videos_normais = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

    if any(p in link.lower() for p in palavras_de_videos_normais):
        return False

    return any(p in link.lower() for p in palavras_ao_vivo)


def extrair_links(site_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(site_url, headers=headers, timeout=10)
        res.raise_for_status()
    except:
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    links = []

    for tag in soup.find_all(['a', 'iframe', 'source', 'video', 'script']):
        link = tag.get('href') or tag.get('src')
        if link:
            if not link.startswith('http'):
                link = requests.compat.urljoin(site_url, link)
            if link_parece_stream_ao_vivo(link):
                links.append(link)

    return links


def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, 'r') as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split('/')[-1].split('.')[0].upper()
        links_encontrados = extrair_links(url)

        if links_encontrados:
            for link in links_encontrados:
                if verificar_link_funcional(link):
                    resultado[nome] = {
                        "site_fonte": url,
                        "grupo": "Sem Grupo",
                        "logo": "",
                        "links": [link]
                    }
                    break
        else:
            resultado[nome] = {
                "site_fonte": url,
                "grupo": "Sem Grupo",
                "logo": "",
                "links": []
            }

    with open('canais_temp.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    processar_fontes('fontes.txt')
