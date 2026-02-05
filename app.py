import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Lançamento Global BI", layout="wide", page_icon="🌐")

# 2. ESTILO GLASSMORPHISM (VISUAL ESTILO VIDRO)
st.markdown("""
    <style>
    /* Fundo Escuro Moderno */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Efeito Vidro nos Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Menu Lateral Customizado */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MENU LATERAL (SIDEBAR)
with st.sidebar:
    st.title("🚀 Lançamento BI")
    st.markdown("---")
    menu = st.radio(
        "Navegação",
        ["📊 Dashboard Principal", "📈 Análise Detalhada", "⚙️ Configurações"],
        index=0
    )
    st.markdown("---")
    st.info("Status: VPS Online 🟢")

# 4. SIMULAÇÃO DE DADOS GLOBAIS E TEMPORAIS
@st.cache_data
def generate_global_data():
    np.random.seed(42)
    rows = 200
    countries = ['Brazil', 'Portugal', 'United States', 'Angola', 'Spain', 'Japan', 'Italy']
    
    data = pd.DataFrame({
        'Data_Hora': [datetime.now() - timedelta(minutes=np.random.randint(0, 1440)) for _ in range(rows)],
        'Pais': np.random.choice(countries, rows),
        'Qualificacao': np.random.choice(['Alta', 'Média', 'Baixa'], rows),
        'Valor_Lead': np.random.uniform(2, 12, rows)
    })
    data['Hora'] = data['Data_Hora'].dt.hour
    return data

df = generate_global_data()

# 5. CONTEÚDO PRINCIPAL: DASHBOARD
if menu == "📊 Dashboard Principal":
    st.header("📍 Monitoramento em Tempo Real")
    
    # MÉTRICAS PRINCIPAIS (Cards Estilo Vidro)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Leads Totais (24h)", len(df), "+18%")
    c2.metric("Países Ativos", df['Pais'].nunique(), "Global")
    c3.metric("CPL Médio", f"R$ {df['Valor_Lead'].mean():.2f}", "-5%")
    c4.metric("Conversão Estimada", "4.2%", "+0.5%")

    st.markdown("---")

    # GRÁFICOS DE ANÁLISE
    col_map, col_time = st.columns([1.2, 1])

    with col_map:
        st.subheader("🌎 Origem dos Leads (Mundo)")
        # Gráfico de Mapa Coroplético (Mundo Inteiro)
        fig_map = px.choropleth(
            df.groupby('Pais').size().reset_index(name='Quantidade'),
            locations='Pais',
            locationmode='country names',
            color='Quantidade',
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_map, use_container_width=True)

    with col_time:
        st.subheader("⏰ Horário de Pico (Entrada)")
        # Gráfico de Área por Hora (24h)
        hourly_data = df.groupby('Hora').size().reset_index(name='Leads')
        fig_time = px.area(
            hourly_data, x='Hora', y='Leads',
            labels={'Hora': 'Hora do Dia', 'Leads': 'Volume de Leads'},
            template='plotly_dark',
            color_discrete_sequence=['#3b82f6']
        )
        fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_time, use_container_width=True)

    # TABELA FINAL
    st.subheader("📋 Últimas Atividades")
    st.dataframe(df.sort_values('Data_Hora', ascending=False).head(10), use_container_width=True)

else:
    st.warning("Esta seção está sendo preparada com base nos seus dados reais.")