import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="LAUNCHBI - Intelligence Hub", layout="wide", page_icon="🚀")

# 2. CSS PARA O VISUAL "PRO" (DARK BLUE & NEON)
st.markdown("""
    <style>
    /* Fundo Principal */
    .main { background-color: #050810; color: #ffffff; }
    
    /* Sidebar Estilo Intelligence */
    section[data-testid="stSidebar"] {
        background-color: #0a0e1a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Cards com Efeito de Profundidade */
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* Fontes e Títulos em Itálico (Estilo LaunchBI) */
    h1, h2, h3 {
        font-family: 'Arial Black', sans-serif;
        font-style: italic;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    /* Esconder botões padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE DADOS GLOBAIS ---
@st.cache_data
def get_data():
    np.random.seed(42)
    rows = 300
    paises = ['Brasil', 'EUA', 'Portugal', 'Angola', 'Espanha', 'Japão']
    df = pd.DataFrame({
        'horario': [datetime.now() - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(rows)],
        'pais': np.random.choice(paises, rows),
        'qualificacao': np.random.choice(['Aprovado IA', 'Pendente', 'Reprovado'], rows, p=[0.4, 0.4, 0.2]),
        'origem': np.random.choice(['Instagram Ads', 'Facebook Ads', 'YouTube'], rows)
    })
    df['hora'] = df['horario'].dt.hour
    return df

df = get_data()

# 3. SIDEBAR (MENU LATERAL)
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.button("📊 DASHBOARD", use_container_width=True)
    st.button("🎯 PESQUISA LEADS", use_container_width=True, type="primary")
    st.button("📈 TRÁFEGO PAGO", use_container_width=True)
    st.markdown("---")
    st.markdown("### SEUS PROJETOS")
    st.selectbox("Selecionar Projeto", ["Projeto Rulian", "Confeitaria Pro", "Hambúrguer Gourmet"])

# 4. ÁREA PRINCIPAL
st.markdown("<h3 style='color: #3b82f6;'>PROJETO RULIAN</h3>", unsafe_allow_html=True)
st.title("INTELLIGENCE HUB")
st.caption("CAMPANHA ATIVA: LC14")

# LINHA 1: METRICAS IGUAIS À IMAGEM
m1, m2, m3, m4 = st.columns(4)
m1.metric("LEADS NA CAMPANHA", len(df), "lc14")
m2.metric("TAXA DE RESPOSTA", "42%", "85 respondentes")
m3.metric("APROVADOS IA", len(df[df['qualificacao']=='Aprovado IA']), "Score de Qualificação")
m4.metric("ACESSO GLOBAL", df['pais'].nunique(), "Detectado via UTM")

st.markdown("---")

# LINHA 2: GRÁFICOS E MAPA
g1, g2 = st.columns([1.3, 1])

with g1:
    st.subheader("🌐 MAPA DE CALOR GLOBAL")
    fig_map = px.choropleth(
        df.groupby('pais').size().reset_index(name='leads'),
        locations='pais', locationmode='country names', color='leads',
        color_continuous_scale=['#0d1221', '#3b82f6'],
        template='plotly_dark'
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

with g2:
    st.subheader("⏰ HORÁRIO DE PICO")
    hourly = df.groupby('hora').size().reset_index(name='volume')
    fig_line = px.line(hourly, x='hora', y='volume', template='plotly_dark')
    fig_line.update_traces(line_color='#3b82f6', line_width=4, mode='lines+markers')
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)

# LINHA 3: TABELA ESTILO HUB
st.subheader("⚡ LEADS DA CAMPANHA")
st.table(df[['horario', 'pais', 'qualificacao', 'origem']].head(10))