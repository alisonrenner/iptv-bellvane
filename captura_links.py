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

        # Verifica links .m3u8 direto no HTML
        padrao_m3u8 = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html)
        if padrao_m3u8:
            return padrao_m3u8[0]

        # Verifica se tem iframe
        soup = BeautifulSoup(html, 'html.parser')
        iframe = soup.find('iframe')
        if iframe and 'src' in iframe.attrs:
            iframe_url = iframe['src']
            if not iframe_url.startswith('http'):
                iframe_url = requests.compat.urljoin(url, iframe_url)
            # Repetir captura dentro do iframe
            return capturar_m3u8(iframe_url)

        return None
    except Exception as e:
        print(f"Erro ao capturar link de {url}: {e}")
        return None
