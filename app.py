import os
import subprocess
import sys

# Instalador automático de dependências
def install_dependencies():
    try:
        import streamlit
        import pandas
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
        os.execv(sys.executable, ['python'] + sys.argv)

install_dependencies()

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Lançamento", layout="wide")
st.title("🚀 Dashboard Online")
st.success("O sistema está rodando corretamente na VPS!")

# Dados Simples para Teste
data = pd.DataFrame({'Anúncio': ['AD 01', 'AD 02'], 'Leads': [100, 150]})
st.bar_chart(data.set_index('Anúncio'))