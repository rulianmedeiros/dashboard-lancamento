import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. SETUP E ESTILO "DARK NEON"
st.set_page_config(page_title="LAUNCHBI - Intelligence Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
    
    /* Reset de fonte para Quicksand (Arredondada) */
    html, body, [class*="css"], .stMetric, h1, h2, h3 { 
        font-family: 'Quicksand', sans-serif !important; 
    }

    /* Fundo azul-profundo idêntico ao print */
    .main { 
        background-color: #050810; 
        color: #ffffff; 
    }

    /* Cards Estilo Intelligence com Borda Glow */
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.1);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* Sidebar Escura e Profissional */
    section[data-testid="stSidebar"] {
        background-color: #0a0e1a !important;
        border-right: 1px solid #1e293b;
    }

    /* Títulos em Itálico Estilo LaunchBI */
    h1, h2, h3 { 
        font-style: italic; 
        text-transform: uppercase; 
        color: #3b82f6; 
        letter-spacing: -1px;
        font-weight: 700;
    }
    
    /* Customização da Tabela */
    .stDataFrame {
        border: 1px solid #1e293b;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MENU LATERAL (SIDEBAR)
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.button("📊 DASHBOARD", use_container_width=True)
    st.button("🎯 PESQUISA LEADS", use_container_width=True, type="primary")
    st.button("📈 TRÁFEGO PAGO", use_container_width=True)
    st.markdown("---")
    projeto = st.selectbox("PROJETO ATUAL", ["Projeto Rulian", "Alimentação Pro"])

# 3. ÁREA PRINCIPAL
st.markdown(f"<p style='color: #3b82f6; font-weight: bold;'>PROJETO: {projeto}</p>", unsafe_allow_html=True)
st.title("INTELLIGENCE HUB")

# --- MÉTRIAS PRINCIPAIS (ESTILO SaaS) ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("INVESTIMENTO (7D)", "R$ 4.184,56", "Meta Ads")
m2.metric("TAXA DE RESPOSTA", "42%", "85 Respondentes")
m3.metric("LEADS QUALIFICADOS", "142", "Aprovados IA")
m4.metric("CPL MÉDIO", "R$ 4,12", "Saudável")

st.markdown("---")

# --- GRÁFICOS RESTAURADOS (HORA E REGIÃO) ---
col_map, col_time = st.columns([1.5, 1])

# Dados para os gráficos
df_dummy = pd.DataFrame({
    'Hora': list(range(24)),
    'Volume': [10,12,8,5,3,4,15,30,45,60,80,95,110,105,90,85,120,150,140,110,90,70,40,20],
    'Pais': ['Brazil', 'Portugal', 'USA', 'Japan', 'Angola', 'Spain'],
    'Leads': [150, 45, 30, 25, 20, 15]
})

with col_map:
    st.subheader("🌐 ALCANCE GLOBAL")
    fig_map = px.choropleth(df_dummy, locations='Pais', locationmode='country names', color='Leads',
                            color_continuous_scale=['#0d1221', '#3b82f6'], template='plotly_dark')
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

with col_time:
    st.subheader("⏰ PICO DE ENTRADA (24H)")
    fig_time = px.area(df_dummy, x='Hora', y='Volume', template='plotly_dark')
    fig_time.update_traces(line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)')
    fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_time, use_container_width=True)

# TABELA ESTILO HUB
st.subheader("⚡ LEADS DA CAMPANHA")
st.dataframe(df_dummy[['Pais', 'Leads']].head(5), use_container_width=True)