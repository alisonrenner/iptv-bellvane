import json

def merge_canais(arquivo_temp, arquivo_final):
    try:
        with open(arquivo_temp, "r", encoding="utf-8") as f:
            canais_temp = json.load(f)
    except Exception as e:
        print(f"[ERRO] Não foi possível abrir {arquivo_temp}: {e}")
        return

    try:
        with open(arquivo_final, "r", encoding="utf-8") as f:
            canais_final = json.load(f)
    except:
        print("[INFO] Arquivo canais.json não encontrado ou vazio. Criando um novo.")
        canais_final = {}

    for nome, dados_temp in canais_temp.items():
        print(f"[✔] Processando canal: {nome}")
        
        if nome not in canais_final:
            canais_final[nome] = {
                "site_fonte": dados_temp.get("site_fonte", ""),
                "grupo": dados_temp.get("grupo", "Sem Grupo"),
                "logo": dados_temp.get("logo", ""),
                "links": []
            }

        # Adiciona links novos sem duplicar
        links_existentes = set(canais_final[nome].get("links", []))
        novos_links = set(dados_temp.get("links", []))
        canais_final[nome]["links"] = list(links_existentes.union(novos_links))

    with open(arquivo_final, "w", encoding="utf-8") as f:
        json.dump(canais_final, f, indent=2, ensure_ascii=False)
        print(f"[✔] Merge concluído! {arquivo_final} atualizado.")

if __name__ == "__main__":
    merge_canais("canais_temp.json", "canais.json")
