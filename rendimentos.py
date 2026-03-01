#%% Bibliotecas
import sidrapy
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from bcb import sgs
import numpy as np
# %% Dataframe de IPCA em janelas de 12 meses
ipca12m = sgs.get(433, "2012-04-01", dt.datetime.today())
ipca48m = ipca12m.rolling(window=48).apply(lambda x:((1+x/100).prod()-1)*100).dropna().round(2)
print(ipca48m)
# %% Dataframe de variação do rendimento médio das famílias
rend_bruto = sidrapy.get_table("6390",
                         period="201203-202512",
                         territorial_level="1",
                         ibge_territorial_code="1",
                         variable="5933"
                         )
#%% Limpando Dataframe
rend_clean = rend_bruto[["D2C", "V"]] # Mantém apenas as colunas de data e renda
rend_clean = rend_clean.rename(columns={"D2C": "Data", "V": "Renda"}) #Renomeia colunas
rend_clean = rend_clean.iloc[1:] # inicia o dataframe da segunda linha eliminando subtítulos
rend_clean = rend_clean.set_index("Data") #Transforma a coluna de trimestres em index
rend_clean = pd.DataFrame(rend_clean).astype(int) # Transforma em número 
rend_clean.index = pd.to_datetime(rend_clean.index.astype(str), format="%Y%m")
rend48m = rend_clean.pct_change().dropna()
rend48m = rend48m.rolling(window=48).apply(lambda x:((1 + x).prod()-1)*100).dropna().round(2)
print(rend48m)
# %% Início dos Mandatos
mandatos = {"Temer":"2016-09-01", "Bolsonaro": "2019-01-01", "Lula": "2023-01-01"}
# %%
plt.figure(figsize=(14,8))
plt.plot(ipca48m, label="Inflação 48m", color="red", linestyle="--")
plt.plot(rend48m, label="Variação do rendimento médio 48m", color="blue", linestyle="--")
plt.legend()
plt.title("Valorização da Renda Média(48m) x Inflação(48m)", loc="left")
plt.annotate(f"{ipca48m.iloc[-1,0]}%",
             xy=(ipca48m.index[-1], ipca48m.iloc[-1,0]),
             va="top", ha="left", fontsize=8, color="red")
plt.annotate(f"{rend48m.iloc[-1,0]}%",
             xy=(rend48m.index[-1], rend48m.iloc[-1,0]),
             va="bottom", ha="left", fontsize=8, color="blue")
plt.annotate("fonte: IBGE", xy=(0.07,0.02), xycoords="figure fraction", va="bottom", ha="left", fontsize=8, color="black")
plt.annotate("elaboração: Fabricio Orlandin, CFP®", xy=(0.8,0.02), xycoords="figure fraction", va="bottom", ha="right", fontsize=8, color="black")
for nome, data in mandatos.items():
    plt.axvline(pd.to_datetime(data), color="black", linestyle="--")
plt.annotate("Dilma", xy=(0.09, 0.12), xycoords="figure fraction", fontsize=10, color="black")
plt.annotate("Temer", xy=(0.21, 0.12), xycoords="figure fraction", fontsize=10, color="black")
plt.annotate("Bolsonaro", xy=(0.42, 0.12), xycoords="figure fraction", fontsize=10, color="black")
plt.annotate("Lula", xy=(0.7, 0.12), xycoords="figure fraction", fontsize=10, color="black")
plt.show()
# %%
