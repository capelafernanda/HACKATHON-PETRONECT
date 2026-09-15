import pandas as pd
import random
from datetime import datetime, timedelta

quantidade_fornecedores = 50
acessos_por_fornecedor = 6

nomes = [
    "Empresa Alpha", "Empresa Beta", "Empresa Gamma",
    "Empresa Delta", "Empresa Omega"
]

segmentos = [
    "Construção", "Engenharia", "Tecnologia",
    "Logística", "Serviços"
]

estados = ["RJ", "SP", "MG", "BA", "RS"]

telas = [
    "Home",
    "Oportunidades",
    "Minha Área de Interesse",
    "Propostas",
    "Treinamentos"
]

buscas = [
    "FPSO",
    "Manutenção",
    "Engenharia",
    "Equipamentos",
    "Nenhuma"
]

interesses = [
    "Licitações",
    "Leilões",
    "Treinamentos",
    "Cadastro Petrobras",
    "Oportunidades"
]

data_final = datetime(2026, 9, 15)
dados = []

for fornecedor in range(quantidade_fornecedores):

    id_fornecedor = f"FORN{fornecedor + 1:03d}"
    nome = random.choice(nomes)
    segmento = random.choice(segmentos)
    estado = random.choice(estados)
    interesse_declarado = random.choice(interesses)

    perfil = random.choice(["frequente", "recente", "inativo", "risco"])

    if perfil == "frequente":
        quantidade_acessos = random.randint(8, 12)
        dias_maximos = 7

    elif perfil == "recente":
        quantidade_acessos = random.randint(4, 7)
        dias_maximos = 3

    elif perfil == "inativo":
        quantidade_acessos = random.randint(1, 3)
        dias_maximos = 30

    else:
        quantidade_acessos = random.randint(4, 8)
        dias_maximos = 10

    for _ in range(quantidade_acessos):

        data_acesso = data_final - timedelta(
            days=random.randint(0, dias_maximos)
        )

        iniciou = random.choice(["Sim", "Não"])

        if iniciou == "Sim":
            abandonou = random.choice(["Sim", "Não"])

            if abandonou == "Sim":
                enviou = "Não"
            else:
                enviou = random.choice(["Sim", "Não"])
        else:
            abandonou = "Não"
            enviou = "Não"

        dados.append({
            "id_fornecedor": id_fornecedor,
            "nome": nome,
            "segmento": segmento,
            "estado": estado,
            "interesse_declarado": interesse_declarado,
            "data_acesso": data_acesso.date(),
            "hora": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}",
            "tela_acessada": random.choice(telas),
            "tempo_segundos": random.randint(20, 600),
            "buscou": random.choice(buscas),
            "clicou_oportunidade": random.choice(["Sim", "Não"]),
            "iniciou_proposta": iniciou,
            "abandonou_proposta": abandonou,
            "enviou_proposta": enviou
        })

df = pd.DataFrame(dados)

df.to_csv(
    "dados_fornecedores.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Base criada com sucesso!")
print(len(df), "registros criados.")
print(df["id_fornecedor"].nunique(), "fornecedores criados.")