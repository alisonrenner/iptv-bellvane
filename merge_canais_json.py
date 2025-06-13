import json
from collections import defaultdict

# Carrega canais existentes
try:
    with open("canais.json", "r", encoding="utf-8") as f:
        canais_base = json.load(f)
except FileNotFoundError:
    canais_base = {}

# Carrega canais temporários
with open("canais_temp.json", "r", encoding="utf-8") as f:
    canais_temp_raw = json.load(f)

# Padroniza estrutura do canais_temp (caso venha como string)
canais_temp = {}
for nome, valor in canais_temp_raw.items():
    if isinstance(valor, str):
        canais_temp[nome] = {
            "grupo": "Sem Grupo",
            "logo": "",
            "links": [valor]
        }
    else:
        canais_temp[nome] = valor

# Junta todos os links por nome
resultado = defaultdict(list)

# Adiciona os canais antigos
for nome, dados in canais_base.items():
    resultado[nome].extend(dados["links"])

# Adiciona os canais novos
for nome, dados in canais_temp.items():
    resultado[nome].extend(dados["links"])

# Remove duplicados por canal
saida = {}
for nome, links in resultado.items():
    saida[nome] = {
        "grupo": canais_temp.get(nome, canais_base.get(nome, {})).get("grupo", "Sem Grupo"),
        "logo": canais_temp.get(nome, canais_base.get(nome, {})).get("logo", ""),
        "links": list(dict.fromkeys(links))  # remove duplicados mantendo ordem
    }

# Salva no canais.json
with open("canais.json", "w", encoding="utf-8") as f:
    json.dump(saida, f, indent=2, ensure_ascii=False)
