import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# 1. SETUP DA PÁGINA E FONTE ARREDONDADA
st.set_page_config(page_title="LAUNCHBI - Full Intelligence", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #050810; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
    }
    h1, h2, h3 { font-style: italic; text-transform: uppercase; color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO META ADS ---
def get_meta_data(token, ad_id):
    if not token or not ad_id:
        return {'spend': 4250, 'impressions': 150000, 'ctr': 1.85, 'clicks': 2775, 'cpm': 28.33}
    try:
        FacebookAdsApi.init(access_token=token)
        account = AdAccount(f'act_{ad_id}')
        fields = ['spend', 'impressions', 'clicks', 'ctr', 'cpm']
        insights = account.get_insights(fields=fields, params={'date_preset': 'last_7d'})
        return dict(insights[0]) if insights else {}
    except:
        return {'spend': 0, 'impressions': 0, 'ctr': 0, 'clicks': 0, 'cpm': 0}

# --- SIMULAÇÃO DE DADOS DE LEADS (HORA E REGIÃO) ---
@st.cache_data
def get_leads_data():
    np.random.seed(42)
    rows = 250
    paises = ['Brazil', 'Portugal', 'United States', 'Angola', 'Japan', 'Spain']
    df = pd.DataFrame({
        'Data_Hora': [datetime.now() - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(rows)],
        'Pais': np.random.choice(paises, rows),
        'Respondeu_Pesquisa': np.random.choice([True, False], rows, p=[0.4, 0.6])
    })
    df['Hora'] = df['Data_Hora'].dt.hour
    return df

df_leads = get_leads_data()

# 2. SIDEBAR (CONFIGURAÇÃO POR PROJETO)
with st.sidebar:
    st.title("LAUNCHBI")
    projeto = st.selectbox("PROJETO", ["Projeto Rulian", "Confeitaria Pro", "Pizzaria System"])
    st.markdown("---")
    st.subheader("🔑 META ADS CONFIG")
    token_input = st.text_input("Access Token", type="password")
    ad_id_input = st.text_input("Ad Account ID")
    st.markdown("---")
    st.info("Visual: Glassmorphism Pro")

meta_metrics = get_meta_data(token_input, ad_id_input)

# 3. DASHBOARD PRINCIPAL
st.title("INTELLIGENCE HUB")
st.markdown(f"#### STATUS ATUAL: {projeto}")

# --- LINHA 1: MÉTRICAS DE TRÁFEGO (META) ---
st.subheader("📈 MÉTRICAS DE TRÁFEGO")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("GASTO (7D)", f"R$ {float(meta_metrics.get('spend', 0)):,.2f}")
m2.metric("IMPRESSÕES", f"{int(meta_metrics.get('impressions', 0)):,}")
m3.metric("CTR", f"{meta_metrics.get('ctr', 0)}%")
m4.metric("CLIQUES", f"{meta_metrics.get('clicks', 0)}")
m5.metric("CPM", f"R$ {float(meta_metrics.get('cpm', 0)):,.2f}")

# --- LINHA 2: MÉTRICAS DE LEADS E PESQUISA ---
st.subheader("👥 PERFORMANCE DE LEADS")
l1, l2, l3, l4 = st.columns(4)
total_leads = len(df_leads)
respondentes = df_leads['Respondeu_Pesquisa'].sum()
taxa_resp = (respondentes / total_leads) * 100
custo_medio = float(meta_metrics.get('spend', 0)) / total_leads

l1.metric("TOTAL DE LEADS", total_leads)
l2.metric("RESPONDERAM", respondentes, f"{taxa_resp:.1f}% Taxa")
l3.metric("TAXA DE RESPOSTA", f"{taxa_resp:.1f}%")
l4.metric("CUSTO MÉDIO/LEAD", f"R$ {custo_medio:.2f}")

st.markdown("---")

# --- LINHA 3: GRÁFICOS (HORA E REGIÃO) ---
g1, g2 = st.columns(2)

with g1:
    st.subheader("⏰ PICO DE ENTRADA (24H)")
    hourly_data = df_leads.groupby('Hora').size().reset_index(name='Volume')
    fig_hour = px.area(hourly_data, x='Hora', y='Volume', template='plotly_dark', color_discrete_sequence=['#3b82f6'])
    fig_hour.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_hour, use_container_width=True)

with g2:
    st.subheader("🌎 DISTRIBUIÇÃO GLOBAL")
    map_data = df_leads.groupby('Pais').size().reset_index(name='Leads')
    fig_map = px.choropleth(map_data, locations='Pais', locationmode='country names', color='Leads',
                            color_continuous_scale='Blues', template='plotly_dark')
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

# TABELA DE LEADS
st.subheader("📋 REGISTROS RECENTES")
st.dataframe(df_leads.sort_values('Data_Hora', ascending=False).head(10), use_container_width=True)