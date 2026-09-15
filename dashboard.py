import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Petronect",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("dados_fornecedores.csv")
resumo = pd.read_csv("resumo_fornecedores.csv")

st.title("Dashboard Petronect")
st.caption("Inteligência de comportamento e reengajamento de fornecedores")

st.divider()

st.subheader("VISÃO GERAL")

total_acessos = len(df)
propostas_iniciadas = (df["iniciou_proposta"] == "Sim").sum()
propostas_abandonadas = (df["abandonou_proposta"] == "Sim").sum()
propostas_enviadas = (df["enviou_proposta"] == "Sim").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de acessos", total_acessos)
col2.metric("Propostas iniciadas", propostas_iniciadas)
col3.metric("Propostas abandonadas", propostas_abandonadas)
col4.metric("Propostas enviadas", propostas_enviadas)

st.divider()

st.subheader("COMPORTAMENTO DOS FORNECEDORES")

col1, col2 = st.columns(2)

with col1:
    st.write("**Telas mais acessadas**")
    telas = df["tela_acessada"].value_counts()
    st.bar_chart(telas)

with col2:
    st.write("**Nível de engajamento**")
    engajamento = resumo["status"].value_counts()
    st.bar_chart(engajamento)

col1, col2 = st.columns(2)

with col1:
    st.write("**Principais buscas**")
    buscas = df["buscou"].value_counts()
    st.bar_chart(buscas)

with col2:
    st.write("**Acessos por estado**")
    estados = df["estado"].value_counts()
    st.bar_chart(estados)

st.divider()

st.subheader("FORNECEDORES")

col1, col2 = st.columns(2)

with col1:
    estado_filtro = st.selectbox(
        "Filtrar por estado",
        ["Todos"] + sorted(df["estado"].unique().tolist())
    )

with col2:
    segmento_filtro = st.selectbox(
        "Filtrar por segmento",
        ["Todos"] + sorted(df["segmento"].unique().tolist())
    )

df_filtrado = df.copy()

if estado_filtro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["estado"] == estado_filtro
    ]

if segmento_filtro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["segmento"] == segmento_filtro
    ]

tabela = df_filtrado[
    [
        "id_fornecedor",
        "nome",
        "segmento",
        "estado"
    ]
].drop_duplicates()

tabela = tabela.merge(
    resumo[
        [
            "id_fornecedor",
            "frequencia",
            "dias_sem_acesso",
            "score",
            "status",
            "comportamento",
            "acao_recomendada"
        ]
    ],
    on="id_fornecedor",
    how="left"
)

st.dataframe(
    tabela,
    width="stretch",
    height=400
)

st.divider()

st.subheader("REENGAJAMENTO")

engajados = (resumo["status"] == "Engajado").sum()
em_risco = (resumo["status"] == "Em risco").sum()
inativos = (resumo["status"] == "Inativo").sum()

col1, col2, col3 = st.columns(3)

col1.metric("Engajados", engajados)
col2.metric("Em risco", em_risco)
col3.metric("Inativos", inativos)

fornecedores_acao = resumo[
    resumo["status"].isin(["Em risco", "Inativo"])
]

st.metric(
    "Total para reengajamento",
    len(fornecedores_acao)
)

st.divider()

st.subheader("FORNECEDOR EM ATENÇÃO")

if len(tabela) > 0:

    ids_filtrados = tabela["id_fornecedor"].tolist()

    resumo_filtrado = resumo[
        resumo["id_fornecedor"].isin(ids_filtrados)
    ].copy()

    resumo_filtrado["prioridade"] = resumo_filtrado["status"].map({
        "Inativo": 1,
        "Em risco": 2,
        "Engajado": 3
    })

    fornecedores_prioridade = resumo_filtrado.sort_values(
        ["prioridade", "dias_sem_acesso"],
        ascending=[True, False]
    )

    fornecedor_id = st.selectbox(
        "Selecione um fornecedor",
        fornecedores_prioridade["id_fornecedor"].tolist()
    )

    fornecedor = resumo_filtrado[
        resumo_filtrado["id_fornecedor"] == fornecedor_id
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{fornecedor['nome']}**")
        st.write(f"Segmento: {fornecedor['segmento']}")
        st.write(f"Estado: {fornecedor['estado']}")
        st.write(f"Interesse declarado: {fornecedor['interesse_declarado']}")
        st.write(f"Interesse identificado: {fornecedor['interesse_real']}")
        st.write(f"Frequência de acessos: {fornecedor['frequencia']}")
        st.write(f"Dias sem acesso: {fornecedor['dias_sem_acesso']}")
        st.write(f"Score: {fornecedor['score']}")
        st.write(f"Status: {fornecedor['status']}")

    with col2:
        st.write("**DIAGNÓSTICO**")

        if fornecedor["dias_sem_acesso"] >= 15:
            st.warning(
                f"Fornecedor está há {fornecedor['dias_sem_acesso']} dias sem acessar o portal."
            )

        elif fornecedor["propostas_abandonadas"] > 0:
            st.warning(
                f"Fornecedor abandonou {fornecedor['propostas_abandonadas']} proposta(s)."
            )

        elif fornecedor["comportamento"] == "Divergente":
            st.info(
                "Comportamento de navegação diferente do interesse declarado."
            )

        elif fornecedor["frequencia"] >= 8:
            st.success(
                "Fornecedor apresenta alta frequência de acesso."
            )

        else:
            st.info(
                "Monitorar comportamento para identificar novas oportunidades."
            )

        st.write("**AÇÃO RECOMENDADA**")
        st.info(fornecedor["acao_recomendada"])

        if st.button(
            "ENVIAR COMUNICAÇÃO",
            key="enviar_comunicacao"
        ):

            if fornecedor["dias_sem_acesso"] >= 15:
                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Sentimos sua falta no Portal Petronect. "
                    "Confira as novas oportunidades disponíveis para sua empresa."
                )

            elif fornecedor["propostas_abandonadas"] > 0:
                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Você iniciou uma proposta recentemente. "
                    "Que tal retomar de onde parou?"
                )

            elif fornecedor["comportamento"] == "Divergente":
                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Identificamos interesses diferentes dos cadastrados no seu perfil. "
                    "Confira novas oportunidades que podem ser relevantes para sua empresa."
                )

            else:
                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Confira as novas oportunidades disponíveis no Portal Petronect."
                )

            st.success("Comunicação enviada com sucesso!")
            st.write("**Mensagem:**")
            st.info(mensagem)

else:
    st.warning(
        "Nenhum fornecedor encontrado para os filtros selecionados."
    )