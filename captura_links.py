import json
import re
import requests
from bs4 import BeautifulSoup

ARQUIVO_CANAIS = "canais.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def extrair_m3u8_do_site(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        matches = re.findall(r'https?://[^\s"']+\.m3u8', resp.text)
        return matches[0] if matches else None
    except Exception as e:
        print(f"[ERRO] Falha ao capturar de {url}: {e}")
        return None

def atualizar_canais_com_links(canais):
    atualizados = {}
    for canal, info in canais.items():
        if isinstance(info, dict) and "site_fonte" in info:
            print(f"🔍 Capturando link para {canal} de {info['site_fonte']}...")
            m3u8_link = extrair_m3u8_do_site(info["site_fonte"])
            if m3u8_link:
                print(f"✅ Encontrado: {m3u8_link}")
                streams = info.get("streams", [])
                if m3u8_link not in streams:
                    streams.insert(0, m3u8_link)
                atualizados[canal] = {**info, "streams": streams}
            else:
                print(f"⚠️ Nenhum link encontrado para {canal}")
                atualizados[canal] = info
        else:
            atualizados[canal] = info
    return atualizados

if __name__ == "__main__":
    canais = carregar_json(ARQUIVO_CANAIS)
    canais_atualizados = atualizar_canais_com_links(canais)
    salvar_json(canais_atualizados, ARQUIVO_CANAIS)
    print("\n📦 canais.json atualizado com os novos links capturados.")
