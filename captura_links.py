
import requests
from bs4 import BeautifulSoup
import re

def capturar_m3u8(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # Tenta encontrar diretamente .m3u8 no HTML
        encontrados = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html)
        if encontrados:
            return encontrados[0]

        # Busca por <iframe src=""> e tenta recursivamente
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

        # Busca links m3u8 dentro de scripts JavaScript
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
