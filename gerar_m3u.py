import json
import requests

def verificar_link(url):
    try:
        resposta = requests.get(url, timeout=5, stream=True)
        return resposta.status_code == 200
    except Exception:
        return False

def gerar_m3u(canais):
    linhas = ["#EXTM3U"]
    for nome, links in canais.items():
        contador = 0
        for link in links:
            if verificar_link(link):
                sufixo = f" ({contador})" if contador > 0 else ""
                linhas.append(f'#EXTINF:-1 tvg-name="{nome}" group-title="Canais",{nome}{sufixo}')
                linhas.append(link)
                contador += 1
    return "\n".join(linhas)

def main():
    with open("canais.json", "r", encoding="utf-8") as f:
        canais = json.load(f)

    lista = gerar_m3u(canais)

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(lista)

if __name__ == "__main__":
    main()
