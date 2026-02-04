import streamlit as st
import pandas as pd
import numpy as np

# Configuração da Página
st.set_page_config(page_title="Dashboard de Lançamento", layout="wide")

st.title("🚀 Análise de Dados: Saúde do Lançamento")
st.sidebar.header("Filtros do Lançamento")

# --- SIMULAÇÃO DE DADOS (Aqui entrará sua integração depois) ---
data_leads = pd.DataFrame({
    'UTM_Content': ['AD_01', 'AD_02', 'AD_01', 'AD_03', 'AD_02', 'AD_01'],
    'Qualificacao': ['Alta', 'Baixa', 'Alta', 'Media', 'Alta', 'Alta'],
    'Faturamento': [15000, 2000, 12000, 5000, 20000, 11000]
})

# --- LINHA 1: Métricas Principais (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Investimento Total", "R$ 12.500", "+12%")
col2.metric("Total de Leads", "1.450", "8%")
col3.metric("Custo por Lead (CPL)", "R$ 8,62", "-2%")
col4.metric("Leads Qualificados (Alta)", "420", "25%")

st.divider()

# --- LINHA 2: Gráficos de Cruzamento ---
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("🎯 Leads Qualificados por Anúncio (UTM)")
    # Simulando o cruzamento que você pediu
    chart_data = data_leads.groupby(['UTM_Content', 'Qualificacao']).size().unstack().fillna(0)
    st.bar_chart(chart_data)

with right_column:
    st.subheader("📊 Performance do Tráfego (Meta)")
    # Exemplo de dados vindos do Meta
    meta_stats = pd.DataFrame({
        'Anúncio': ['AD_01', 'AD_02', 'AD_03'],
        'CTR': [2.5, 1.8, 3.2],
        'Cliques': [450, 300, 600]
    }).set_index('Anúncio')
    st.line_chart(meta_stats['CTR'])

# --- LINHA 3: Análise da Pesquisa ---
st.subheader("📋 Respostas da Pesquisa vs Origem")
st.write("Tabela cruzada para identificar qual anúncio traz o lead com maior faturamento:")
st.dataframe(data_leads.style.highlight_max(axis=0, subset=['Faturamento']))