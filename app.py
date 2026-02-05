import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. SETUP DE ALTA PERFORMANCE
st.set_page_config(page_title="LAUNCHBI | Intelligence Hub", layout="wide")

# CSS para forçar o visual SaaS (Fundo #050810 e bordas Glow)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Quicksand', sans-serif !important; }
    .main { background-color: #050810; color: #ffffff; }
    
    /* Menu Lateral Dark */
    section[data-testid="stSidebar"] {
        background-color: #0a0e1a !important;
        border-right: 1px solid #1e293b;
    }

    /* Cards com Glow Azul Elétrico */
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.08);
    }
    
    /* Botões do Menu Lateral estilo SaaS */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: transparent;
        border: 1px solid #1e293b;
        color: #94a3b8;
        text-align: left;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stButton>button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }

    h1, h2, h3 { font-style: italic; text-transform: uppercase; color: #3b82f6; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE DADOS CORRIGIDO (EVITA O VALUEERROR) ---
def get_safe_data():
    np.random.seed(42)
    # Criamos listas com exatamente o mesmo tamanho (24 itens para 24 horas)
    horas = list(range(24))
    leads_por_hora = np.random.randint(20, 150, 24).tolist()
    
    df_time = pd.DataFrame({'Hora': horas, 'Volume': leads_por_hora})
    
    # Lista separada para o mapa (6 países)
    paises = ['Brazil', 'Portugal', 'United States', 'Angola', 'Japan', 'Spain']
    leads_mapa = [180, 65, 42, 38, 25, 12]
    df_map = pd.DataFrame({'Pais': paises, 'Leads': leads_mapa})
    
    return df_time, df_map

df_time, df_map = get_safe_data()

# 2. SIDEBAR PROFISSIONAL
with st.sidebar:
    st.markdown("<h1 style='font-size: 26px; margin-bottom: 30px;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.button("📊 DASHBOARD")
    st.button("🎯 PESQUISA LEADS")
    st.button("📈 TRÁFEGO PAGO")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 12px;'>PROJETO ATUAL</p>", unsafe_allow_html=True)
    projeto = st.selectbox("", ["PROJETO RULIAN", "CONFEITARIA PRO"], label_visibility="collapsed")
    
    st.markdown("---")
    st.subheader("🔑 META ADS")
    token = st.text_input("Token", type="password")
    ad_id = st.text_input("Account ID")

# 3. ÁREA PRINCIPAL
st.markdown(f"<p style='color: #3b82f6; font-size: 14px; font-weight: 700;'>PROJETO: {projeto} | CAMPANHA: LC14</p>", unsafe_allow_html=True)
st.title("INTELLIGENCE HUB")

# KPI'S COM DESIGN MODERNO
m1, m2, m3, m4 = st.columns(4)
m1.metric("INVESTIMENTO (7D)", "R$ 4.184,56", "Meta Ads")
m2.metric("TAXA DE RESPOSTA", "42%", "85 Respondentes")
m3.metric("LEADS QUALIFICADOS", "142", "Aprovados IA")
m4.metric("CPL MÉDIO", "R$ 4,12", "Saudável")

st.markdown("<br>", unsafe_allow_html=True)

# GRÁFICOS LADO A LADO
g1, g2 = st.columns([1.5, 1])

with g1:
    st.subheader("🌐 ALCANCE GLOBAL")
    fig_map = px.choropleth(df_map, locations='Pais', locationmode='country names', color='Leads',
                            color_continuous_scale=['#0d1221', '#3b82f6'], template='plotly_dark')
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

with g2:
    st.subheader("⏰ PICO DE ENTRADA (24H)")
    fig_time = px.area(df_time, x='Hora', y='Volume', template='plotly_dark')
    fig_time.update_traces(line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.1)')
    fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_time, use_container_width=True)