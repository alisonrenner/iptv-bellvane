import json
import os

def merge_canais(temp_path, final_path):
    with open(temp_path, 'r', encoding='utf-8') as f:
        canais_temp = json.load(f)
    with open(final_path, 'r', encoding='utf-8') as f:
        canais = json.load(f)

    for canal_temp in canais_temp:
        nome_temp = canal_temp.get("nome", "").lower()
        existente = next((c for c in canais if c.get("nome", "").lower() == nome_temp), None)
        if existente:
            links_existentes = {l["url"] for l in existente.get("links", [])}
            novos_links = [l for l in canal_temp.get("links", []) if l["url"] not in links_existentes]
            existente["links"].extend(novos_links)
        else:
            canais.append(canal_temp)

    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(canais, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    merge_canais("canais_temp.json", "canais.json")