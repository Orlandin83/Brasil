#%% Bibliotecas
from bcb import sgs
import seaborn as sns
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
#%% Período
start="2020-01-01"
end=dt.datetime.today()
#Dataframe IPCA
ipca12m = sgs.get(13522, start, end)
ipca12m = ipca12m.rename(columns={"13522": "IPCA 12m"})
#%% Dataframe Médias Núcleos 12m
nucleo = [11427,16121,27838,27839,11426,4466,16122,28751,28750]
ipca_nucleo = sgs.get(nucleo, "2019-02-01", end)
ipca_nucleo["Média"] = ipca_nucleo.mean(axis=1).round(2)
ipca_nucleo_12m = ipca_nucleo.rolling(window=12).apply(lambda x:(np.prod(1+x/100)-1)*100).dropna()
print(ipca_nucleo_12m)
# %% Cesta IPCA
cesta = [1635,1636,1637,1638,1639,1641,1642,1643,1640]
ipca_cesta = sgs.get(cesta, start, end)
ipca_cesta = ipca_cesta.rename(columns={"1635": "Alimentação e Bebidas",
                                        "1636": "Habitação",
                                        "1637": "Artigos de Residência",
                                        "1638": "Vestuário",
                                        "1639": "Transportes",
                                        "1641": "Saúdes e Cuidados Pessoais",
                                        "1642": "Despesas Pessoais",
                                        "1643": "Educação",
                                        "1640": "Comunicação"})
ipca_cesta = ipca_cesta.iloc[-1]
print(ipca_cesta)
# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,7), sharex=False, gridspec_kw={"height_ratios": [3,1]})
ax1.plot(ipca12m, label = "IPCA 12m", color = "black")
ax1.plot(ipca_nucleo_12m["Média"], label = "Média Núcleos IPCA", color = "black", linestyle = "--")
ax1.annotate(f"{ipca12m.iloc[-1,0]}%",
             xy=(ipca12m.index[-1], ipca12m.iloc[-1,0]-0.2),
             va="top", ha="left", fontsize=8, color="darkgrey")
ax1.annotate(f"{ipca_nucleo_12m["Média"].iloc[-1]:.2f}%",
             xy=(ipca_nucleo_12m.index[-1], ipca_nucleo_12m.iloc[-1,0]+0.3),
             va="bottom", ha="left", fontsize=8, color="darkgrey")
ax1.set_ylabel("IPCA 12m (%)")
ax1.legend()
categories = ipca_cesta.index
values = ipca_cesta.values
x_pos = np.arange(len(categories))
bars = ax2.bar(x_pos, values, color="lightblue", alpha=0.3)
ax2.bar_label(bars, label_type="center", fmt="%.2f%%", fontsize=9, color="blue")
ax2.set_ylabel("IPCA por grupo (%)")
ax2.axhline(0, linestyle="--", color="blue", linewidth=0.4)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(categories, rotation=45, ha="right")
plt.tight_layout()
plt.annotate("fonte: IBGE / BCB", xy=(0.08,0.02), xycoords="figure fraction", va="bottom", ha="left", fontsize=10, color="black")
plt.annotate("elaboração: Fabricio Orlandin, CFP®", xy=(0.8,0.02), xycoords="figure fraction", va="bottom", ha="right", fontsize=10, color="black")
plt.show()

# %%
