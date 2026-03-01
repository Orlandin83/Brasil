#%% Bibliotecas
import ipeadatapy as ipea
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from bcb import sgs
#%% Dataframe com imoveis
fipezap = ipea.timeseries("FIPE12_VENBR12")
fipezap = pd.DataFrame(fipezap)
fipezap = fipezap.rename(columns={"VALUE (-)": "FIPEZAP"})
fipezap = pd.to_numeric(fipezap["FIPEZAP"])
print(fipezap)
#%% Dataframe com IPCA
ipca = sgs.get(433, "2008-01-01", dt.datetime.today())
ipca = ipca.rename(columns={"433": "IPCA"})
print(ipca)
# %% Unificando e ampliando o Dataframe
dataframe = pd.concat([fipezap, ipca], axis=1) #unifica
dataframe["Fator IPCA"] = (1 + dataframe["IPCA"]/100).cumprod()
dataframe["Fator IPCA Norm"] = dataframe["Fator IPCA"] / dataframe["Fator IPCA"].iloc[0]
dataframe["FIPEZAP Defl"] = dataframe["FIPEZAP"] / (dataframe["Fator IPCA Norm"])
dataframe["FIPEZAP Defl Acum"] = ((dataframe["FIPEZAP Defl"] / dataframe["FIPEZAP Defl"].iloc[0] - 1) * 100).round(2)
dataframe["Ganho Real"] = (dataframe["FIPEZAP Defl"].pct_change() * 100)
dataframe["CAGR (%) a.a."] = ((dataframe["FIPEZAP Defl"]/dataframe["FIPEZAP Defl"].iloc[0])**(12/(np.arange(len(dataframe))+1)) - 1) * 100
print(dataframe)
#%% Definindo Máx e Mínimos
x_max = dataframe["CAGR (%) a.a."].idxmax()
y_max = dataframe["CAGR (%) a.a."].loc[x_max]
# %%
plt.figure(figsize=(16,7))
plt.plot(dataframe["FIPEZAP Defl Acum"], label=f"FIPEZAP: {dataframe["FIPEZAP Defl Acum"].iloc[-1]}%", color="blue")
plt.plot(dataframe["CAGR (%) a.a."], label=f"Resultado: IPCA + {dataframe['CAGR (%) a.a.'].iloc[-1]:.2f}% a.a.", color="gray")
plt.legend(loc="best")
plt.title(f"Índice FIPEZAP Deflacionado desde {pd.to_datetime(dataframe.index[0]).strftime("%m-%Y")}", loc="left")
plt.annotate("fonte: IPEA", xy=(0.08,0.02), xycoords="figure fraction", va="bottom", ha="left", fontsize=10, color="black")
plt.annotate("elaboração: Fabricio Orlandin, CFP®", xy=(0.8,0.02), xycoords="figure fraction", va="bottom", ha="right", fontsize=10, color="black")
plt.grid(axis="y")
plt.ylabel("Valorização Real (%)")
plt.annotate(f"Máx:({x_max.strftime("%m-%Y")})\n\n"
             f"IPCA + {y_max:.2f}% a.a.",
            xy=(x_max, y_max + 0.5),
            va="bottom", ha="center", fontsize=8, color="gray")
plt.annotate(f"Acumulado: IPCA + {dataframe['CAGR (%) a.a.'].iloc[-1]:.2f}% a.a.",
            xy=(dataframe.index[-1], dataframe["CAGR (%) a.a."].iloc[-1] + 0.3),
            va="bottom", ha="right", fontsize=8, color="gray")
plt.show()
# %%
