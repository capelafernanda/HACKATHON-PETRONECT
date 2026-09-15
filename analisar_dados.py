import pandas as pd

df = pd.read_csv("dados_fornecedores.csv")

print("\nTelas mais acessadas:")
print(df["tela_acessada"].value_counts())

print("\nBuscas mais realizadas:")
print(df["buscou"].value_counts())

print("\nPropostas iniciadas:")
print(df["iniciou_proposta"].value_counts())

print("\nPropostas abandonadas:")
print(df["abandonou_proposta"].value_counts())

print("\nPropostas enviadas:")
print(df["enviou_proposta"].value_counts())

print("\nAcessos por estado:")
print(df["estado"].value_counts())

print("\nAcessos por segmento:")
print(df["segmento"].value_counts())

def classificar_engajamento(linha):
    if linha["iniciou_proposta"] == "Sim" and linha["enviou_proposta"] == "Sim":
        return "Engajado"
    elif linha["abandonou_proposta"] == "Sim":
        return "Em risco"
    else:
        return "Inativo"


df["engajamento"] = df.apply(classificar_engajamento, axis=1)

df["data_acesso"] = pd.to_datetime(df["data_acesso"])

resumo_fornecedores = df.groupby(
    ["id_fornecedor", "nome", "segmento", "estado", "interesse_declarado"]
).agg(
    frequencia=("id_fornecedor", "count"),
    ultimo_acesso=("data_acesso", "max"),
    propostas_iniciadas=("iniciou_proposta", lambda x: (x == "Sim").sum()),
    propostas_abandonadas=("abandonou_proposta", lambda x: (x == "Sim").sum()),
    propostas_enviadas=("enviou_proposta", lambda x: (x == "Sim").sum())
).reset_index()

data_referencia = df["data_acesso"].max()

resumo_fornecedores["dias_sem_acesso"] = (
    data_referencia - resumo_fornecedores["ultimo_acesso"]
).dt.days

resumo_fornecedores["score"] = 0

resumo_fornecedores.loc[
    resumo_fornecedores["frequencia"] >= 8,
    "score"
] += 25

resumo_fornecedores.loc[
    resumo_fornecedores["frequencia"].between(4, 7),
    "score"
] += 15

resumo_fornecedores.loc[
    resumo_fornecedores["dias_sem_acesso"] <= 3,
    "score"
] += 25

resumo_fornecedores.loc[
    resumo_fornecedores["dias_sem_acesso"].between(4, 10),
    "score"
] += 15

resumo_fornecedores.loc[
    resumo_fornecedores["propostas_iniciadas"] > 0,
    "score"
] += 15

resumo_fornecedores.loc[
    resumo_fornecedores["propostas_enviadas"] > 0,
    "score"
] += 20

resumo_fornecedores.loc[
    resumo_fornecedores["propostas_abandonadas"] > 0,
    "score"
] -= 15

resumo_fornecedores["score"] = resumo_fornecedores["score"].clip(0, 100)

def classificar_score(score):
    if score >= 70:
        return "Engajado"
    elif score >= 40:
        return "Em risco"
    else:
        return "Inativo"

resumo_fornecedores["status"] = resumo_fornecedores["score"].apply(
    classificar_score
)

print("\nScore dos fornecedores:")

print(
    resumo_fornecedores[
        [
            "id_fornecedor",
            "nome",
            "frequencia",
            "dias_sem_acesso",
            "score",
            "status"
        ]
    ]
)

mapa_interesses = {
    "FPSO": "Oportunidades",
    "Manutenção": "Oportunidades",
    "Engenharia": "Oportunidades",
    "Equipamentos": "Oportunidades",
    "Nenhuma": "Nenhum"
}

df["interesse_real"] = df["buscou"].map(mapa_interesses)

interesse_real = df.groupby("id_fornecedor")["interesse_real"].agg(
    lambda x: x.mode()[0]
).reset_index()

resumo_fornecedores = resumo_fornecedores.merge(
    interesse_real,
    on="id_fornecedor",
    how="left"
)

resumo_fornecedores["comportamento"] = "Divergente"

resumo_fornecedores.loc[
    resumo_fornecedores["interesse_real"] == resumo_fornecedores["interesse_declarado"],
    "comportamento"
] = "Alinhado"

resumo_fornecedores.loc[
    resumo_fornecedores["interesse_real"] == "Nenhum",
    "comportamento"
] = "Sem interação"

resumo_fornecedores.to_csv(
    "resumo_fornecedores.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nComportamento real x declarado:")
print(
    resumo_fornecedores[
        [
            "id_fornecedor",
            "interesse_declarado",
            "interesse_real",
            "comportamento"
        ]
    ]
)

def definir_acao(linha):
    if linha["dias_sem_acesso"] >= 15:
        return "Enviar comunicação de retorno"
    elif linha["propostas_abandonadas"] > 0:
        return "Incentivar retomada da proposta"
    elif linha["comportamento"] == "Divergente":
        return "Atualizar recomendações"
    elif linha["frequencia"] >= 8:
        return "Enviar novas oportunidades"
    else:
        return "Acompanhar comportamento"

resumo_fornecedores["acao_recomendada"] = resumo_fornecedores.apply(
    definir_acao,
    axis=1
)

resumo_fornecedores.to_csv(
    "resumo_fornecedores.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDiagnóstico e ação:")
print(
    resumo_fornecedores[
        [
            "id_fornecedor",
            "score",
            "status",
            "dias_sem_acesso",
            "comportamento",
            "acao_recomendada"
        ]
    ]
)

print("\nNível de engajamento:")
print(df["engajamento"].value_counts())

df.to_csv("dados_fornecedores.csv", index=False, encoding="utf-8-sig")

resumo_engajamento = df["engajamento"].value_counts().reset_index()

resumo_engajamento.columns = ["engajamento", "quantidade"]

resumo_engajamento.to_csv(
    "resumo_engajamento.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nResumo de engajamento:")
print(resumo_engajamento)