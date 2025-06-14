from playwright.sync_api import sync_playwright
import json


def capturar_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        links = []

        def handle_request(request):
            if (
                ".m3u8" in request.url
                or "/live/" in request.url
                or "/hls/" in request.url
                or "/playlist" in request.url
                or "/index.m3u" in request.url
            ):
                print(f"🎯 LINK ENCONTRADO: {request.url}")
                links.append(request.url)

        page.on("request", handle_request)

        try:
            print(f"🌐 Acessando: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(15000)  # Espera 15 segundos
        except Exception as e:
            print(f"❌ Erro ao acessar {url}: {e}")

        browser.close()
        return links


def processar_fontes(arquivo_fontes):
    with open(arquivo_fontes, "r") as f:
        urls = f.read().splitlines()

    resultado = {}

    for url in urls:
        nome = url.strip().split("/")[-1].split(".")[0].upper()
        links_encontrados = capturar_links(url)

        resultado[nome] = {
            "site_fonte": url,
            "grupo": "Sem Grupo",
            "logo": "",
            "links": links_encontrados if links_encontrados else [],
        }

    with open("canais_temp.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    processar_fontes("fontes.txt")
