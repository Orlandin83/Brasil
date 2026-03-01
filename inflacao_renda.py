#%% Bibliotecas
import ipeadatapy as ipea
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from bcb import sgs
#%% IPCA
ipca = sgs.get(433, "2020-01-01", dt.datetime.today())
ipca = ipca.rename(columns={"433": "IPCA"})
#%% Dataframe do IPEA com as inflações por faixa de renda
renda = {"DIMAC_INF1": "renda muito baixa", #cria uma lista com os códigos por renda
         "DIMAC_INF2": "renda baixa",
         "DIMAC_INF3": "renda média-baixa",
         "DIMAC_INF4": "renda média",
         "DIMAC_INF5": "renda média-alta",
         "DIMAC_INF6": "renda alta"
}
series = [ipca] # Cria uma lista para receber as séries
for code, label in renda.items(): # percorre o dicionáro para usar todos os códigos
    df=ipea.timeseries(series=code) # um dataframe para cada código
    df = df.iloc[:,-1] # usa apenas a última coluna
    df = df.rename(label) # renomeia a coluna para os nomes usados no dicionário
    series.append(df) # adiciona os df à lista de séries
# %%
ipca_renda = pd.concat(series,axis=1) # unifica todas as séries da lista em um dataframe
# %%
ipca12m = ipca_renda.rolling(window=12).apply(lambda x:(np.prod(1 + x/100)-1)* 100).dropna()
# %%
plt.figure(figsize=(24,16))
for col in ipca12m.columns:
    if col=="IPCA":
        plt.plot(ipca12m[col], label=f"{col}: {ipca12m[col].iloc[-1]:.2f}%",
                 linestyle="-", color="black")
    else:
        line=plt.plot(ipca12m[col], label=f"{col}: {ipca12m[col].iloc[-1]:.2f}%",
                      linestyle="--")[0]        
plt.legend()
plt.title("IPCA12m por faixa de renda", loc="left")
plt.annotate("fonte: IBGE (Biblioteca BC) / IPEA DATA", xy=(0.07,0.02), xycoords="figure fraction", va="bottom", ha="left", fontsize=12, color="black")
plt.annotate("elaboração: Fabricio Orlandin, CFP®", xy=(0.8,0.02), xycoords="figure fraction", va="bottom", ha="right", fontsize=12, color="black")
plt.show()
# %%
