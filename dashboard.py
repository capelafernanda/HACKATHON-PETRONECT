import streamlit as st
import pandas as pd


# CONFIGURAÇÃO
st.set_page_config(
    page_title="Petronect Inteligente",
    page_icon="📊",
    layout="wide"
)


# =========================
# ESTILO VISUAL
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #EEF3F9;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* TÍTULOS */

h1 {
    color: #123B66 !important;
    font-size: 32px;
    font-weight: 700;
}

h2 {
    color: #123B66 !important;
    font-size: 24px;
    font-weight: 700;
}

h3 {
    color: #123B66 !important;
    font-size: 20px;
    font-weight: 700;
}


/* TEXTO NORMAL */

p {
    color: #263746;
}


/* TEXTO SECUNDÁRIO */

[data-testid="stCaptionContainer"] {
    color: #5F6F7E !important;
}


/* CARDS DE MÉTRICAS */

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #D7E2EE;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 6px 18px rgba(18, 59, 102, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #123B66 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #123B66 !important;
    font-weight: 700;
}


/* LABELS DOS FILTROS */

.stSelectbox label {
    color: #123B66 !important;
    font-weight: 600;
}


/* SELECTBOX */

[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #B9CBE0;
}

[data-baseweb="select"] * {
    color: #263746;
}


/* BOTÕES */

//* BOTÕES */

.stButton > button {
    background-color: #123B66 !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 45px !important;
    font-weight: 600 !important;
    width: 100% !important;
}

/* Texto do botão */
.stButton > button,
.stButton > button *,
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #000000 !important;
}

/* Quando passar o mouse */
.stButton > button:hover,
.stButton > button:hover *,
.stButton > button:hover p,
.stButton > button:hover span,
.stButton > button:hover div {
    color: #000000 !important;
}

/* Quando clicar/focar */
.stButton > button:focus,
.stButton > button:focus *,
.stButton > button:focus p,
.stButton > button:focus span,
.stButton > button:focus div,
.stButton > button:active,
.stButton > button:active *,
.stButton > button:active p,
.stButton > button:active span,
.stButton > button:active div {
    color: #000000 !important;
}

/* TABELA */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* ALERTAS */

.stAlert {
    border-radius: 10px;
}


/* DIVISORES */

hr {
    border-color: #C9D6E4;
}

</style>
""", unsafe_allow_html=True)


# =========================
# CARREGAR DADOS
# =========================

df = pd.read_csv("dados_fornecedores.csv")
resumo = pd.read_csv("resumo_fornecedores.csv")


# =========================
# CABEÇALHO
# =========================

st.title("Petronect")

st.caption(
    "Inteligência de comportamento e reengajamento de fornecedores"
)

st.header("Dashboard de Inteligência")

st.caption(
    "Transformando comportamento em oportunidades de negócio"
)

st.divider()


# =========================
# VISÃO GERAL
# =========================

st.subheader("Visão geral")


total_acessos = len(df)

propostas_iniciadas = (
    df["iniciou_proposta"] == "Sim"
).sum()

propostas_abandonadas = (
    df["abandonou_proposta"] == "Sim"
).sum()

propostas_enviadas = (
    df["enviou_proposta"] == "Sim"
).sum()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total de acessos",
        total_acessos
    )


with col2:
    st.metric(
        "Propostas iniciadas",
        propostas_iniciadas
    )


with col3:
    st.metric(
        "Propostas abandonadas",
        propostas_abandonadas
    )


with col4:
    st.metric(
        "Propostas enviadas",
        propostas_enviadas
    )


st.divider()


# =========================
# COMPORTAMENTO
# =========================

st.subheader("Comportamento dos fornecedores")


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


# =========================
# FORNECEDORES
# =========================

st.subheader("Fornecedores")


col1, col2 = st.columns(2)


with col1:

    estado_filtro = st.selectbox(
        "Filtrar por estado",
        ["Todos"] + sorted(
            df["estado"].unique().tolist()
        )
    )


with col2:

    segmento_filtro = st.selectbox(
        "Filtrar por segmento",
        ["Todos"] + sorted(
            df["segmento"].unique().tolist()
        )
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


# =========================
# REENGAJAMENTO
# =========================

st.subheader("Reengajamento")


engajados = (
    resumo["status"] == "Engajado"
).sum()

em_risco = (
    resumo["status"] == "Em risco"
).sum()

inativos = (
    resumo["status"] == "Inativo"
).sum()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Engajados",
        engajados
    )


with col2:

    st.metric(
        "Em risco",
        em_risco
    )


with col3:

    st.metric(
        "Inativos",
        inativos
    )


fornecedores_acao = resumo[
    resumo["status"].isin(
        ["Em risco", "Inativo"]
    )
]


st.metric(
    "Total para reengajamento",
    len(fornecedores_acao)
)


st.divider()


# =========================
# FORNECEDOR EM ATENÇÃO
# =========================

st.subheader("Fornecedor em atenção")


if len(tabela) > 0:

    ids_filtrados = tabela[
        "id_fornecedor"
    ].tolist()


    resumo_filtrado = resumo[
        resumo["id_fornecedor"].isin(
            ids_filtrados
        )
    ].copy()


    resumo_filtrado["prioridade"] = (
        resumo_filtrado["status"].map({
            "Inativo": 1,
            "Em risco": 2,
            "Engajado": 3
        })
    )


    fornecedores_prioridade = (
        resumo_filtrado.sort_values(
            ["prioridade", "dias_sem_acesso"],
            ascending=[True, False]
        )
    )


    fornecedor_id = st.selectbox(
        "Selecione um fornecedor",
        fornecedores_prioridade[
            "id_fornecedor"
        ].tolist()
    )


    fornecedor = resumo_filtrado[
        resumo_filtrado["id_fornecedor"]
        == fornecedor_id
    ].iloc[0]


    col1, col2 = st.columns(2)


    # =========================
    # PERFIL DO FORNECEDOR
    # =========================

    with col1:

        st.markdown(
            "### Perfil do fornecedor"
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Empresa:</span>** "
            f"<span style='color:#263746;'>{fornecedor['nome']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Segmento:</span>** "
            f"<span style='color:#263746;'>{fornecedor['segmento']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Estado:</span>** "
            f"<span style='color:#263746;'>{fornecedor['estado']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Interesse declarado:</span>** "
            f"<span style='color:#263746;'>{fornecedor['interesse_declarado']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Interesse identificado:</span>** "
            f"<span style='color:#263746;'>{fornecedor['interesse_real']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Frequência de acessos:</span>** "
            f"<span style='color:#263746;'>{fornecedor['frequencia']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Dias sem acesso:</span>** "
            f"<span style='color:#263746;'>{fornecedor['dias_sem_acesso']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Score:</span>** "
            f"<span style='color:#263746;'>{fornecedor['score']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"**<span style='color:#123B66;'>Status:</span>** "
            f"<span style='color:#263746;'>{fornecedor['status']}</span>",
            unsafe_allow_html=True
        )


    # =========================
    # DIAGNÓSTICO
    # =========================

    with col2:

        st.markdown(
            "### Diagnóstico"
        )


        if fornecedor[
            "dias_sem_acesso"
        ] >= 15:

            st.warning(
                f"Fornecedor está há "
                f"{fornecedor['dias_sem_acesso']} dias "
                "sem acessar o portal."
            )


        elif fornecedor[
            "propostas_abandonadas"
        ] > 0:

            st.warning(
                f"Fornecedor abandonou "
                f"{fornecedor['propostas_abandonadas']} "
                "proposta(s)."
            )


        elif fornecedor[
            "comportamento"
        ] == "Divergente":

            st.info(
                "Comportamento de navegação "
                "diferente do interesse declarado."
            )


        elif fornecedor[
            "frequencia"
        ] >= 8:

            st.success(
                "Fornecedor apresenta alta "
                "frequência de acesso."
            )


        else:

            st.info(
                "Monitorar comportamento para "
                "identificar novas oportunidades."
            )


        st.markdown(
            "### Ação recomendada"
        )

        st.info(
            fornecedor["acao_recomendada"]
        )


        # =========================
        # COMUNICAÇÃO
        # =========================

        if st.button(
            "ENVIAR COMUNICAÇÃO",
            key="enviar_comunicacao"
        ):


            if fornecedor[
                "dias_sem_acesso"
            ] >= 15:

                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Sentimos sua falta no Portal "
                    "Petronect. Confira as novas "
                    "oportunidades disponíveis "
                    "para sua empresa."
                )


            elif fornecedor[
                "propostas_abandonadas"
            ] > 0:

                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Você iniciou uma proposta "
                    "recentemente. Que tal retomar "
                    "de onde parou?"
                )


            elif fornecedor[
                "comportamento"
            ] == "Divergente":

                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Identificamos interesses "
                    "diferentes dos cadastrados "
                    "no seu perfil. Confira novas "
                    "oportunidades que podem ser "
                    "relevantes para sua empresa."
                )


            else:

                mensagem = (
                    f"Olá, {fornecedor['nome']}! "
                    "Confira as novas oportunidades "
                    "disponíveis no Portal Petronect."
                )


            st.success(
                "Comunicação enviada com sucesso!"
            )

            st.write("**Mensagem:**")

            st.info(mensagem)


else:

    st.warning(
        "Nenhum fornecedor encontrado para "
        "os filtros selecionados."
    )