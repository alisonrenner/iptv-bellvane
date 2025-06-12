import json

# Arquivos de entrada
ARQUIVO_ORIGINAL = "canais.json"
ARQUIVO_TEMP = "canais_temp.json"
ARQUIVO_SAIDA = "canais_atualizado.json"

def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def merge_canais(orig, novo):
    resultado = orig.copy()
    for canal, links in novo.items():
        if canal in resultado:
            # Adiciona apenas os links que ainda não estão na lista
            for link in links:
                if link not in resultado[canal]:
                    resultado[canal].append(link)
        else:
            resultado[canal] = links
    return resultado

if __name__ == "__main__":
    canais_originais = carregar_json(ARQUIVO_ORIGINAL)
    canais_novos = carregar_json(ARQUIVO_TEMP)

    canais_merged = merge_canais(canais_originais, canais_novos)
    salvar_json(canais_merged, ARQUIVO_SAIDA)

    print(f"Merged com sucesso! Arquivo salvo como: {ARQUIVO_SAIDA}")
