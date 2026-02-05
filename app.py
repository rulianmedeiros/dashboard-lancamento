import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
st.set_page_config(page_title="LAUNCHBI | Command Center", layout="wide")

# 2. CSS CUSTOMIZADO (VISUAL COMMAND CENTER)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .main { background-color: #11141d; color: #e2e8f0; }
    
    /* Sidebar Estilo Minimalista */
    section[data-testid="stSidebar"] {
        background-color: #1a1f2c !important;
        border-right: 1px solid #2d3748;
    }
    
    /* Cards com Degradê e Bordas Suaves */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1e2533, #161b26);
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Botões de Período (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1a1f2c;
        padding: 10px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: #2d3748;
        border-radius: 8px;
        color: #94a3b8;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    h1, h2 { font-weight: 600; letter-spacing: -0.5px; color: #ffffff; }
    p { color: #94a3b8; }
    
    /* Ajuste para botões do menu lateral */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: transparent;
        color: #94a3b8;
        border: 1px solid transparent;
        padding: 10px 15px;
    }
    .stButton > button:hover {
        color: #3b82f6;
        border: 1px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS ---
def get_data():
    df_vendas = pd.DataFrame({
        'Dia': ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB'],
        'Valor': [45, 90, 35, 38, 65, 95, 160]
    })
    return df_vendas

df_vendas = get_data()

# 3. SIDEBAR (MENU REORGANIZADO)
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6; font-size: 24px;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px;'>---</p>", unsafe_allow_html=True)
    
    # Navegação por estado
    if 'menu_ativo' not in st.session_state:
        st.session_state.menu_ativo = "Dashboard"

    if st.button("📊 DASHBOARD"):
        st.session_state.menu_ativo = "Dashboard"
    if st.button("🎯 PESQUISA LEADS"):
        st.session_state.menu_ativo = "Pesquisa Leads"
    if st.button("📈 TRÁFEGO PAGO"):
        st.session_state.menu_ativo = "Tráfego Pago"

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    projeto = st.selectbox("PROJETO ATUAL", ["PROJETO RULIAN", "CONFEITARIA PRO"])
    st.button("➡️ SAIR")

# 4. ÁREA PRINCIPAL DINÂMICA
if st.session_state.menu_ativo == "Dashboard":
    st.title("Command Center.")
    st.markdown("Análise de performance e mix de inteligência comercial.")

    tabs = st.tabs(["HOJE", "7 DIAS", "30 DIAS", "MÊS ATUAL", "ANTERIOR", "TOTAL"])

    with tabs[1]: # 7 Dias
        st.markdown("### 4. PERIODOS REALIZADOS")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("FATURAMENTO BRUTO", "R$ 360,19", "Fluxo de Entrada")
        with c2:
            st.metric("SALDO LÍQUIDO", "R$ 330,67", "Caixa Real")
        with c3:
            st.metric("VOLUME OPERAÇÃO", "R$ 29,52", "3 Transações")

        st.markdown("---")
        
        col_vendas, col_pagamento = st.columns(2)
        with col_vendas:
            st.markdown("#### ATIVIDADE DE VENDAS (Diário)")
            fig_vendas = px.bar(df_vendas, x='Dia', y='Valor', 
                                template='plotly_dark', color_discrete_sequence=['#3b82f6'])
            fig_vendas.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                     margin=dict(l=0, r=0, t=20, b=0), height=300)
            st.plotly_chart(fig_vendas, use_container_width=True)
            
        with col_pagamento:
            st.markdown("#### MIX DE PAGAMENTO")
            fig_donut = px.pie(values=[70, 30], names=['CRÉDITO', 'PIX'], hole=0.6,
                               color_discrete_sequence=['#3b82f6', '#6366f1'], template='plotly_dark')
            fig_donut.update_layout(margin=dict(l=0, r=0, t=20, b=0), showlegend=False, 
                                    paper_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig_donut, use_container_width=True)

elif st.session_state.menu_ativo == "Pesquisa Leads":
    st.title("Pesquisa de Leads")
    st.markdown("Monitoramento de qualificação e funil de entrada.")
    # Aqui você pode manter os gráficos de Hora e Região que já funcionavam
    st.info("Área de análise de leads ativa.")

elif st.session_state.menu_ativo == "Tráfego Pago":
    st.title("Tráfego Pago")
    st.markdown("Integração direta com Meta Ads e Google Ads.")
    # Aqui entra a parte de investimento, CTR e CPM
    st.info("Área de análise de tráfego ativa.")