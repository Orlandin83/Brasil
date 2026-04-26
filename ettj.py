#%% Bibliotecas
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%% CONFIG
url = "https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp"
max = 2520

#%% DATABASE + EXTRAÇÃO DOS PARÂMETROS
data_teste = pd.Timestamp.today().normalize()
while True:
    data_formatada = data_teste.strftime("%d/%m/%Y")
    
    payload = {
        'Idioma': 'PT',
        'Dt_Ref': data_formatada,
        'saida': 'csv'
    }
    response = requests.post(url, data=payload)
    linhas_csv = response.text.splitlines()
    
    linhas_pre = [linha for linha in linhas_csv if linha.startswith("PREFIXADOS")]
    linhas_ipca = [linha for linha in linhas_csv if linha.startswith("IPCA")]
    
    # Verifica se encontrou as duas curvas para o dia
    if len(linhas_pre) > 0 and len(linhas_ipca) > 0:
        linha_alvo_pre = linhas_pre[0]
        linha_alvo_ipca = linhas_ipca[0]
        break
    else:
        data_teste = data_teste - pd.tseries.offsets.BDay(1)
# Parâmetros PREFIXADOS
colunas_pre = linha_alvo_pre.split(';')
b1_pre = float(colunas_pre[1].replace(',', '.'))
b2_pre = float(colunas_pre[2].replace(',', '.'))
b3_pre = float(colunas_pre[3].replace(',', '.'))
b4_pre = float(colunas_pre[4].replace(',', '.'))
l1_pre = float(colunas_pre[5].replace(',', '.'))
l2_pre = float(colunas_pre[6].replace(',', '.'))
# Parâmetros IPCA
colunas_ipca = linha_alvo_ipca.split(';')
b1_ipca = float(colunas_ipca[1].replace(',', '.'))
b2_ipca = float(colunas_ipca[2].replace(',', '.'))
b3_ipca = float(colunas_ipca[3].replace(',', '.'))
b4_ipca = float(colunas_ipca[4].replace(',', '.'))
l1_ipca = float(colunas_ipca[5].replace(',', '.'))
l2_ipca = float(colunas_ipca[6].replace(',', '.'))

#%% CÁLCULO DA CURVA DE SVENSSON (LINEAR)
vertices_uteis = np.arange(1, max + 1)
t = vertices_uteis / 252
# Cálculo PREFIXADOS
termo1_pre = (1 - np.exp(-l1_pre * t)) / (l1_pre * t)
termo2_pre = termo1_pre - np.exp(-l1_pre * t)
termo3_pre = ((1 - np.exp(-l2_pre * t)) / (l2_pre * t)) - np.exp(-l2_pre * t)
taxas_pre = b1_pre + b2_pre * termo1_pre + b3_pre * termo2_pre + b4_pre * termo3_pre
# Cálculo IPCA
termo1_ipca = (1 - np.exp(-l1_ipca * t)) / (l1_ipca * t)
termo2_ipca = termo1_ipca - np.exp(-l1_ipca * t)
termo3_ipca = ((1 - np.exp(-l2_ipca * t)) / (l2_ipca * t)) - np.exp(-l2_ipca * t)
taxas_ipca = b1_ipca + b2_ipca * termo1_ipca + b3_ipca * termo2_ipca + b4_ipca * termo3_ipca

#%% CONSOLIDA DATAFRAME
df = pd.DataFrame({
    'Vertice': vertices_uteis, 
    'Taxa_Pre': taxas_pre,
    'Taxa_IPCA': taxas_ipca
})
df = df.set_index("Vertice")
df["Taxa_Pre"] = df["Taxa_Pre"] * 100
df["Taxa_IPCA"] = df["Taxa_IPCA"] * 100
df["Inflação Implícita"] = ((1 + df['Taxa_Pre'] / 100) / (1 + df['Taxa_IPCA'] / 100) - 1) * 100
print(df)

#%% PLOTAGEM DO GRÁFICO
plt.figure(figsize=(16,6))
plt.plot(df['Taxa_Pre'], label="ETTJ Prefixada", color="blue")
plt.plot(df['Taxa_IPCA'], label="ETTJ IPCA", color="lightblue")
plt.plot(df['Inflação Implícita'], label="Inflação Implícita", color="red")
plt.axhline(y=3, linestyle="--", color="black")
plt.legend()
plt.show()
# %%
