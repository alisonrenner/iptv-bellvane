import requests
from bs4 import BeautifulSoup
import json


def verificar_link_funcional(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10, stream=True)

        if res.status_code == 200 and int(res.headers.get('Content-Length', 1)) > 0:
            print(f"✅ Link funcional: {url}")
            return True
        else:
            print(f"❌ Link não funcional (Status: {res.status_code}): {url}")
            return False
    except Exception as e:
        print(f"❌ Erro verificando {url}: {e}")
        return False


def extrair_links(site_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(site_url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Erro acessando {site_url}: {e}")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    links = []

    for tag in soup.find_all(['a', 'iframe', 'source', 'script', 'video', 'meta']):
        link = tag.get('href') or tag.get('src') or tag.get('content')
        if link:
            if not link.startswith('http'):
                link = requests.compat.urljoin(site_url, link)
            links.append(link)

    return links


def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, 'r') as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split('/')[-1].split('.')[0].upper()
        print(f"\n🔍 PROCESSANDO {nome}")

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
                    print(f"✅ LINK SALVO: {link}")
                    break
            else:
                print(f"❌ Nenhum link funcional encontrado para {nome}")
        else:
            print(f"❌ Nenhum link encontrado em {url}")

    with open('canais_temp.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print("\n✅ canais_temp.json GERADO COM SUCESSO!")


if __name__ == "__main__":
    processar_fontes('fontes.txt')
