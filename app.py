import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
# Importando a biblioteca do Meta (Certifique-se que está no seu docker-compose)
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="LAUNCHBI - Intelligence Hub", layout="wide", page_icon="🚀")

# 2. UI/UX: FONTE REDONDA E ESTILO DARK PRO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .main { background-color: #050810; color: #ffffff; }
    
    /* Cards Estilo Intelligence */
    div[data-testid="stMetric"] {
        background-color: #0d1221;
        border: 1px solid #1e293b;
        border-radius: 16px; /* Fonte e bordas mais redondas */
        padding: 25px;
    }
    
    h1, h2, h3 { font-style: italic; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE INTEGRAÇÃO META ADS ---
def get_meta_ads_data(access_token, ad_account_id):
    try:
        FacebookAdsApi.init(access_token=access_token)
        account = AdAccount(f'act_{ad_account_id}')
        
        fields = [
            'spend', 'impressions', 'clicks', 'ctr', 'cpm', 
            'conversions', 'cost_per_conversion'
        ]
        params = {'date_preset': 'last_7d'}
        
        insights = account.get_insights(fields=fields, params=params)
        
        if insights:
            return dict(insights[0])
        return None
    except Exception as e:
        return f"Erro na API: {str(e)}"

# 3. SIDEBAR: CONFIGURAÇÕES POR PROJETO
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6;'>LAUNCHBI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Gerenciamento de Projetos e IDs
    projeto_ativo = st.selectbox("PROJETO ATUAL", ["Projeto Rulian", "Confeitaria Pro", "Hambúrguer Gourmet"])
    
    st.markdown("### 🔑 META ADS CONFIG")
    # Campos para você preencher
    token = st.text_input("Access Token", type="password", help="Insira o Token do seu App no Meta")
    ad_id = st.text_input("Ad Account ID", help="Apenas os números da conta de anúncio")
    
    st.markdown("---")
    st.info(f"Configurado para: {projeto_ativo}")

# 4. LÓGICA DE DADOS (REAL OU FICTÍCIO)
if token and ad_id:
    # Tenta puxar dados reais se o token for inserido
    meta_data = get_meta_ads_data(token, ad_id)
else:
    # Dados de exemplo (Fictícios) para o visual não ficar vazio
    meta_data = {
        'spend': '4250.00', 'impressions': '150000', 'ctr': '1.85', 
        'clicks': '2775', 'cpm': '28.33', 'conversions': '45'
    }

# 5. DASHBOARD PRINCIPAL
st.title("INTELLIGENCE HUB")
st.markdown(f"#### ANÁLISE DE TRÁFEGO: {projeto_ativo}")

# LINHA 1: MÉTRICAS DO META ADS
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("INVESTIMENTO", f"R$ {float(meta_data.get('spend', 0)):,.2f}")
with col2:
    st.metric("IMPRESSÕES", f"{int(meta_data.get('impressions', 0)):,}")
with col3:
    st.metric("CTR MÉDIO", f"{meta_data.get('ctr', 0)}%")
with col4:
    st.metric("CLIQUES NO LINK", f"{meta_data.get('clicks', 0)}")

# LINHA 2: CONVERSÕES E CUSTOS
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CPM", f"R$ {float(meta_data.get('cpm', 0)):,.2f}")
with c2:
    st.metric("CONVERSÕES", meta_data.get('conversions', '0'))
with c3:
    # Cálculo simples de custo por conversão
    invest = float(meta_data.get('spend', 0))
    conv = float(meta_data.get('conversions', 1)) # evita divisão por zero
    st.metric("CUSTO POR CONV.", f"R$ {invest/conv:.2f}")

st.markdown("---")

# LINHA 3: GRÁFICO DE PICO (Utilizando sua lógica de leads 24h)
st.subheader("⏰ JANELA DE PICO (CONVERSÕES POR HORA)")
# Simulando dados de hora para visualização
chart_data = pd.DataFrame({
    'Hora': list(range(24)),
    'Volume': np.random.randint(10, 100, 24)
})
fig_time = px.area(chart_data, x='Hora', y='Volume', template='plotly_dark', color_discrete_sequence=['#3b82f6'])
fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_time, use_container_width=True)