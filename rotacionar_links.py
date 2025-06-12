import json
import requests
import time

ARQUIVO_CANAIS = "canais.json"
ARQUIVO_FALHAS = "_falhas.json"
FALHAS_LIMITE = 3
TIMEOUT = 5

def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def testar_link(url):
    try:
        r = requests.head(url, timeout=TIMEOUT)
        return r.status_code == 200
    except:
        return False

def rotacionar_links(canais, falhas):
    atualizados = {}
    for canal, dados in canais.items():
        links = dados if isinstance(dados, list) else dados.get("streams", [])
        if not links: continue

        link_principal = links[0]
        ok = testar_link(link_principal)

        if ok:
            falhas[link_principal] = 0  # zera falhas se o link voltou
        else:
            falhas[link_principal] = falhas.get(link_principal, 0) + 1
            if falhas[link_principal] >= FALHAS_LIMITE:
                # move o link para o final
                links.append(links.pop(0))
                falhas[links[-1]] = 0  # zera falha do que subiu

        atualizados[canal] = links
    return atualizados, falhas

if __name__ == "__main__":
    canais = carregar_json(ARQUIVO_CANAIS)
    falhas = carregar_json(ARQUIVO_FALHAS)

    canais_atualizados, falhas_atualizadas = rotacionar_links(canais, falhas)

    salvar_json(canais_atualizados, ARQUIVO_CANAIS)
    salvar_json(falhas_atualizadas, ARQUIVO_FALHAS)

    print("Links rotacionados com base em falhas detectadas.")
