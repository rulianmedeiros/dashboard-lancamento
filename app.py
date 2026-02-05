import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Lançamento BI - Rulian", layout="wide", page_icon="📈")

# Estilo Customizado (Dark Mode Friendly)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("📊 Gestão Estratégica de Lançamento")
st.markdown("---")

# --- SIDEBAR (FILTROS) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1998/1998592.png", width=100)
st.sidebar.header("Filtros Globais")
data_range = st.sidebar.date_input("Período do Lançamento", [])
canal_filtro = st.sidebar.multiselect("Origem do Tráfego", ["Facebook Ads", "Instagram Ads", "Google Ads"], ["Facebook Ads", "Instagram Ads"])

# --- SIMULAÇÃO DE DADOS ROBUSTOS ---
# Criando 100 leads fictícios para o visual
np.random.seed(42)
utm_options = ['Criativo_01_Video', 'Criativo_02_Imagem', 'Criativo_03_Carrossel']
data_leads = pd.DataFrame({
    'Data': pd.date_range(start='2026-01-01', periods=100, freq='H'),
    'UTM_Content': np.random.choice(utm_options, 100),
    'Qualificacao': np.random.choice(['Alta (Fatura > 10k)', 'Média', 'Baixa'], 100, p=[0.2, 0.5, 0.3]),
    'Resposta_Pesquisa': np.random.choice(['Confeitaria', 'Pizzaria', 'Hamburgueria', 'Outros'], 100),
    'Custo_Anuncio': np.random.uniform(5, 15, 100)
})

# --- LINHA 1: KPIs PRINCIPAIS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Investimento Meta", "R$ 4.250,00", "+R$ 150 hoje")
with col2:
    st.metric("Total de Leads", len(data_leads), "12% vs ontem")
with col3:
    st.metric("CPL Médio", "R$ 4,25", "-R$ 0,50")
with col4:
    st.metric("ROI Estimado", "3.4x", "📈 Saudável")

st.markdown("### 🎯 Qualidade por Origem de Anúncio (UTM)")

# --- LINHA 2: GRÁFICOS DE CRUZAMENTO ---
c1, c2 = st.columns([2, 1])

with c1:
    # Gráfico de barras empilhadas: UTM vs Qualificação
    chart_data = data_leads.groupby(['UTM_Content', 'Qualificacao']).size().unstack().fillna(0)
    fig_leads = px.bar(chart_data, barmode='group', color_discrete_sequence=['#2ecc71', '#f1c40f', '#e74c3c'],
                       title="Quais anúncios trazem os leads mais qualificados?")
    st.plotly_chart(fig_leads, use_container_width=True)

with c2:
    # Gráfico de Pizza: Perfil do Cliente (Respostas da Pesquisa)
    fig_pizza = px.pie(data_leads, names='Resposta_Pesquisa', title="Nicho dos Leads (Pesquisa)",
                       color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pizza, use_container_width=True)

# --- LINHA 3: TABELA DETALHADA ---
st.markdown("### 📋 Visão Detalhada dos leads")
st.dataframe(data_leads.sort_values(by='Data', ascending=False), use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Sistema de Análise de Dados desenvolvido para estratégias de lançamento. VPS Hetzner Status: Online.")