import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
st.set_page_config(page_title="LAUNCHBI | Command Center", layout="wide")

# 2. CSS CUSTOMIZADO (VISUAL COMMAND CENTER)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .main { background-color: #11141d; color: #e2e8f0; }
    
    section[data-testid="stSidebar"] {
        background-color: #1a1f2c !important;
        border-right: 1px solid #2d3748;
    }
    
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1e2533, #161b26);
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
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

# --- FUNÇÃO PARA BUSCAR DADOS DO N8N ---
def fetch_n8n_data(projeto_id, campaign):
    # ATENÇÃO: Substitua 'sua-url-aqui' pela Production URL do nó Webhook no seu n8n
    url = "https://n8n.rulianmedeiros.com/webhook/busca-leads" 
    params = {"id": projeto_id, "campaign": campaign}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        # Silencia o erro para manter a interface limpa se o n8n estiver offline
        return pd.DataFrame()

# --- DADOS ESTÁTICOS (DASHBOARD) ---
def get_vendas_data():
    return pd.DataFrame({
        'Dia': ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB'],
        'Valor': [45, 90, 35, 38, 65, 95, 160]
    })

df_vendas = get_vendas_data()

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6; font-size: 24px;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px;'>---</p>", unsafe_allow_html=True)
    
    if 'menu_ativo' not in st.session_state:
        st.session_state.menu_ativo = "Dashboard"

    if st.button("📊 DASHBOARD"):
        st.session_state.menu_ativo = "Dashboard"
    if st.button("🎯 PESQUISA LEADS"):
        st.session_state.menu_ativo = "Pesquisa Leads"
    if st.button("📈 TRÁFEGO PAGO"):
        st.session_state.menu_ativo = "Tráfego Pago"

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    # IDs configurados conforme a estrutura do seu Postgres
    projeto_opcoes = {"PROJETO RULIAN": 15, "CONFEITARIA PRO": 16}
    projeto_selecionado = st.selectbox("PROJETO ATUAL", list(projeto_opcoes.keys()))
    projeto_id = projeto_opcoes[projeto_selecionado]
    
    campanha = st.text_input("CAMPANHA (UTM)", value="lc14")
    st.button("➡️ SAIR")

# 4. ÁREA PRINCIPAL DINÂMICA
if st.session_state.menu_ativo == "Dashboard":
    st.title("Command Center.")
    st.markdown("Análise de performance e mix de inteligência comercial.")

    tabs = st.tabs(["HOJE", "7 DIAS", "30 DIAS", "MÊS ATUAL", "ANTERIOR", "TOTAL"])

    with tabs[1]:
        st.markdown("### 4. PERIODOS REALIZADOS")
        c1, c2, c3 = st.columns(3)
        c1.metric("FATURAMENTO BRUTO", "R$ 360,19", "Fluxo de Entrada")
        c2.metric("SALDO LÍQUIDO", "R$ 330,67", "Caixa Real")
        c3.metric("VOLUME OPERAÇÃO", "R$ 29,52", "3 Transações")

        st.markdown("---")
        col_vendas, col_pagamento = st.columns(2)
        with col_vendas:
            st.markdown("#### ATIVIDADE DE VENDAS (Diário)")
            fig_vendas = px.bar(df_vendas, x='Dia', y='Valor', template='plotly_dark', color_discrete_sequence=['#3b82f6'])
            fig_vendas.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0), height=300)
            st.plotly_chart(fig_vendas, use_container_width=True)
            
        with col_pagamento:
            st.markdown("#### MIX DE PAGAMENTO")
            fig_donut = px.pie(values=[70, 30], names=['CRÉDITO', 'PIX'], hole=0.6, color_discrete_sequence=['#3b82f6', '#6366f1'], template='plotly_dark')
            fig_donut.update_layout(margin=dict(l=0, r=0, t=20, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig_donut, use_container_width=True)

elif st.session_state.menu_ativo == "Pesquisa Leads":
    st.title("Intelligence Leads.")
    st.markdown(f"Monitoramento qualitativo para a campanha **{campanha}**.")
    
    # Busca dados reais do seu fluxo n8n conectado ao Postgres
    df_leads_real = fetch_n8n_data(projeto_id, campanha)
    
    if not df_leads_real.empty:
        # KPIs REAIS EXTRAÍDOS DO BANCO
        l1, l2, l3, l4 = st.columns(4)
        l1.metric("LEADS TOTAIS", len(df_leads_real), "Base Postgres")
        
        # Cálculo dinâmico de idade média
        if 'idade' in df_leads_real.columns:
            idade_media = int(df_leads_real['idade'].astype(int).mean())
            l2.metric("IDADE MÉDIA", f"{idade_media} anos")
        else:
            l2.metric("IDADE MÉDIA", "N/A")
            
        l3.metric("ORIGEM PREDOMINANTE", df_leads_real['utm_source'].mode()[0] if 'utm_source' in df_leads_real.columns else "N/A")
        
        if 'dispositivo' in df_leads_real.columns:
            l4.metric("DEVICE (MOBILE)", f"{len(df_leads_real[df_leads_real['dispositivo']=='Celular'])} leads")
        else:
            l4.metric("DEVICE (MOBILE)", "N/A")

        st.markdown("---")

        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### 🌎 Leads por Estado")
            if 'estado' in df_leads_real.columns:
                fig_estado = px.bar(df_leads_real.groupby('estado').size().reset_index(name='Qtd'), 
                                    x='estado', y='Qtd', template='plotly_dark', color_discrete_sequence=['#3b82f6'])
                fig_estado.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_estado, use_container_width=True)

        with g2:
            st.markdown("#### ⏰ Horário de Cadastro")
            if 'hora_cadastro' in df_leads_real.columns:
                fig_hora = px.area(df_leads_real.groupby('hora_cadastro').size().reset_index(name='Qtd'), 
                                   x='hora_cadastro', y='Qtd', template='plotly_dark')
                fig_hora.update_traces(line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)')
                fig_hora.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_hora, use_container_width=True)

        st.dataframe(df_leads_real, use_container_width=True)
    else:
        st.warning("Aguardando dados ou Webhook offline. Verifique a URL de produção no código.")

elif st.session_state.menu_ativo == "Tráfego Pago":
    st.title("Performance Tráfego.")
    st.markdown("Integração direta com Meta Ads.")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("GASTO TOTAL", "R$ 4.184,56", "Últimos 7 dias")
    t2.metric("CTR MÉDIO", "1.70%", "+0.2%")
    t3.metric("CPM", "R$ 28,45", "Saudável")
    t4.metric("CLIQUES NO LINK", "2.350", "Meta Ads")