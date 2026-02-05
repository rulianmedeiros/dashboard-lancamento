import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# 1. ESTILO E FONTE ARREDONDADA (INTER)
st.set_page_config(page_title="LAUNCHBI - Full Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #050810; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 20px;
    }
    h1, h2, h3 { font-style: italic; text-transform: uppercase; color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DE LEADS (HORA E REGIÃO) ---
@st.cache_data
def load_leads():
    np.random.seed(42)
    rows = 300
    paises = ['Brazil', 'Portugal', 'USA', 'Japan', 'Angola', 'Spain']
    df = pd.DataFrame({
        'Data': [datetime.now() - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(rows)],
        'Pais': np.random.choice(paises, rows),
        'Pesquisa': np.random.choice([True, False], rows, p=[0.45, 0.55])
    })
    df['Hora'] = df['Data'].dt.hour
    return df

df_leads = load_leads()

# 2. MENU LATERAL
with st.sidebar:
    st.title("LAUNCHBI")
    token = st.text_input("Meta Access Token", type="password")
    ad_id = st.text_input("Ad Account ID")

# 3. DASHBOARD
st.title("INTELLIGENCE HUB")

# --- LINHA 1: META ADS (TRÁFEGO) ---
st.subheader("📈 TRÁFEGO PAGO (META)")
c1, c2, c3, c4, c5 = st.columns(5)
# Simulação caso o token não seja inserido
c1.metric("GASTO", "R$ 4.250,00")
c2.metric("IMPRESSÕES", "150.400")
c3.metric("CTR", "1.85%")
c4.metric("CLIQUES", "2.780")
c5.metric("CPM", "R$ 28,25")

# --- LINHA 2: LEADS E PESQUISA ---
st.subheader("👥 PERFORMANCE DE LEADS")
l1, l2, l3, l4 = st.columns(4)
respondentes = df_leads['Pesquisa'].sum()
taxa = (respondentes/len(df_leads))*100

l1.metric("TOTAL DE LEADS", len(df_leads))
l2.metric("RESPONDERAM", respondentes, f"taxa: {taxa:.1f}%", delta_color="normal")
l3.metric("TAXA RESPOSTA", f"{taxa:.1f}%")
l4.metric("CUSTO/LEAD", "R$ 14,16")

# --- LINHA 3: GRÁFICOS (HORA E REGIÃO) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⏰ PICO DE ENTRADA (24H)")
    hourly = df_leads.groupby('Hora').size().reset_index(name='Volume')
    fig_h = px.area(hourly, x='Hora', y='Volume', template='plotly_dark')
    fig_h.update_traces(line_color='#3b82f6')
    st.plotly_chart(fig_h, use_container_width=True)

with col_right:
    st.subheader("🌎 DISTRIBUIÇÃO GLOBAL")
    mapa = df_leads.groupby('Pais').size().reset_index(name='Leads')
    fig_m = px.choropleth(mapa, locations='Pais', locationmode='country names', 
                          color='Leads', color_continuous_scale='Blues', template='plotly_dark')
    st.plotly_chart(fig_m, use_container_width=True)