import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# 1. SETUP E FONTE SUPER REDONDA (QUICKSAND)
st.set_page_config(page_title="LAUNCHBI - Full Intelligence", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
    html, body, [class*="css"], .stMetric, h1, h2, h3 { 
        font-family: 'Quicksand', sans-serif !important; 
    }
    .main { background-color: #050810; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 24px;
        padding: 20px;
    }
    h1, h2, h3 { font-style: italic; text-transform: uppercase; color: #3b82f6; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO META ADS COM CORREÇÃO DE TIPO ---
def get_meta_data(token, ad_id):
    if not token or not ad_id:
        return {'spend': 4184.56, 'impressions': 13753, 'ctr': 1.70, 'clicks': 235, 'cpm': 304.27, 'conversions': 42}
    try:
        FacebookAdsApi.init(access_token=token)
        account = AdAccount(f'act_{ad_id}')
        fields = ['spend', 'impressions', 'clicks', 'ctr', 'cpm', 'conversions']
        insights = account.get_insights(fields=fields, params={'date_preset': 'last_7d'})
        
        if insights:
            raw = dict(insights[0])
            # CORREÇÃO: Extrai apenas o número de conversões da lista do Meta
            convs = raw.get('conversions', 0)
            if isinstance(convs, list) and len(convs) > 0:
                raw['conversions'] = convs[0].get('value', 0)
            return raw
        return {}
    except Exception as e:
        return {'error': str(e)}

# --- DADOS DE LEADS (SIMULADOS PARA O VISUAL) ---
@st.cache_data
def get_leads_data():
    np.random.seed(42)
    rows = 250
    paises = ['Brazil', 'Portugal', 'United States', 'Angola', 'Japan', 'Spain']
    df = pd.DataFrame({
        'Data_Hora': [datetime.now() - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(rows)],
        'Pais': np.random.choice(paises, rows),
        'Respondeu': np.random.choice([True, False], rows, p=[0.4, 0.6])
    })
    df['Hora'] = df['Data_Hora'].dt.hour
    return df

df_leads = get_leads_data()

# 2. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    projeto = st.selectbox("PROJETO ATUAL", ["Projeto Rulian", "Alimentação Pro", "Hambúrguer Gourmet"])
    st.markdown("---")
    st.subheader("🔑 META ADS CONFIG")
    token_input = st.text_input("Access Token", type="password")
    ad_id_input = st.text_input("Ad Account ID")

meta = get_meta_data(token_input, ad_id_input)

# 3. DASHBOARD PRINCIPAL
st.title("INTELLIGENCE HUB")
st.markdown(f"#### ANÁLISE ESTRATÉGICA: {projeto}")

# --- LINHA 1: TRÁFEGO PAGO (META ADS) ---
st.subheader("📈 MÉTRICAS DE TRÁFEGO")
t1, t2, t3, t4, t5 = st.columns(5)
t1.metric("INVESTIMENTO", f"R$ {float(meta.get('spend', 0)):,.2f}")
t2.metric("IMPRESSÕES", f"{int(meta.get('impressions', 0)):,}")
t3.metric("CTR MÉDIO", f"{meta.get('ctr', 0)}%")
t4.metric("CLIQUES NO LINK", meta.get('clicks', 0))
t5.metric("CPM", f"R$ {float(meta.get('cpm', 0)):,.2f}")

# --- LINHA 2: PERFORMANCE E CONVERSÕES ---
st.subheader("👥 PERFORMANCE DE LEADS")
l1, l2, l3, l4 = st.columns(4)
total = len(df_leads)
resp = df_leads['Respondeu'].sum()
tx_resp = (resp/total)*100
conv_meta = meta.get('conversions', 0)

l1.metric("TOTAL DE LEADS", total)
l2.metric("RESPONDERAM", resp, f"{tx_resp:.1f}% Taxa")
l3.metric("CONVERSÕES (META)", conv_meta)
l4.metric("CUSTO POR CONV.", f"R$ {float(meta.get('spend', 0))/float(conv_meta if float(conv_meta)>0 else 1):.2f}")

st.markdown("---")

# --- LINHA 3: GRÁFICOS (HORA E REGIÃO) ---
g1, g2 = st.columns(2)

with g1:
    st.subheader("⏰ PICO DE ENTRADA (24H)")
    h_data = df_leads.groupby('Hora').size().reset_index(name='V')
    fig_h = px.area(h_data, x='Hora', y='V', template='plotly_dark', color_discrete_sequence=['#3b82f6'])
    fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_h, use_container_width=True)

with g2:
    st.subheader("🌎 ALCANCE GLOBAL")
    m_data = df_leads.groupby('Pais').size().reset_index(name='L')
    fig_m = px.choropleth(m_data, locations='Pais', locationmode='country names', color='L', 
                          color_continuous_scale='Blues', template='plotly_dark')
    fig_m.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_m, use_container_width=True)