import json
import re

ARQUIVO_FONTES = "fontes.txt"
ARQUIVO_SAIDA = "canais_temp.json"

def extrair_nome_canal(url):
    nome = url.rstrip("/").split("/")[-1]
    nome = nome.replace("-", " ").replace("_", " ").upper()
    return nome

def processar_fontes():
    canais = {}
    try:
        with open(ARQUIVO_FONTES, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"Arquivo {ARQUIVO_FONTES} não encontrado.")
        return

    for url in linhas:
        nome = extrair_nome_canal(url)
        canais[nome] = { "site_fonte": url }

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(canais, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(canais)} canais adicionados em {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    processar_fontes()
