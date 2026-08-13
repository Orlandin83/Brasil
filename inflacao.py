#%% BIBLIOTECAS
import pandas as pd
import numpy as np
import sidrapy as sd
import matplotlib.pyplot as plt
from bcb import sgs
import datetime as dt

#%% IPCA MENSAL
start = "2020-01-01"
end = dt.datetime.today()
ipca_m = sgs.get(433, start, end)
ipca_m = ipca_m[-13:]
#%% CESTA IPCA
cesta = [1635, 1636, 1637, 1638, 1639, 1641, 1642, 1643, 1640, 433]
ipca_cesta = sgs.get(cesta, start, end)
ipca_cesta = ipca_cesta.rename(columns={"1635": "Alimentação e Bebidas",
                                        "1636": "Habitação",
                                        "1637": "Artigos de Residência",
                                        "1638": "Vestuário",
                                        "1639": "Transportes",
                                        "1641": "Saúde e Cuidados Pessoais",
                                        "1642": "Despesas Pessoais",
                                        "1643": "Educação",
                                        "1640": "Comunicação",
                                        "433": "IPCA"}
                                        )
ipca_cesta = ipca_cesta.iloc[-1].sort_values()

#%% IPCA 12 meses e núcleos 12 meses
ipca_12m = sgs.get(13522, start, end)
ipca_12m = ipca_12m.rename(columns={"13522": "IPCA 12m"})
nucleos = [11427, 16121, 27838, 27839, 11426, 4466, 16122, 28751, 28750]
ipca_nucleo = sgs.get(nucleos, start, end)
ipca_nucleo["Média"] = ipca_nucleo.mean(axis=1)
ipca_nucleo = ipca_nucleo["Média"]
ipca_nucleo_12m = ipca_nucleo.rolling(window=12).apply(lambda x:(np.prod(1 + x /100) - 1)* 100)
ipca_12m = pd.concat([ipca_12m, ipca_nucleo_12m], axis = 1).dropna()

#%% GRÁFICO
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(16,12))
fig.suptitle(f"Inflação - {ipca_m.index[-1].strftime('%m/%Y')}", fontsize=16, fontweight="bold", color="darkblue")
bar_ax1 = ax1.bar(
    x=ipca_m.index,
    height=ipca_m["433"],
    width=15,
    color= "lightblue",
)
destaque = [-1, -2, -13]
for b in destaque:
    bar_ax1[b].set_color("darkblue")
    bar_ax1[b].set_alpha(0.7)
for a in destaque:
    ax1.annotate(f"{ipca_m["433"].iloc[a]}%",
                 xy = (ipca_m.index[a], ipca_m["433"].iloc[a]),
                 va="bottom",
                 ha="center",
                 fontsize=10,
                 color="darkblue",
                 bbox=dict(fc="white",
                           ec="darkblue",linewidth=0.3,
                           alpha=0.8,
                           boxstyle="round,pad=0.2")
)
ax1.tick_params(axis= "x", rotation=45)
ax1.set_title("IPCA mensal",
              loc="left",
              fontweight="bold",
              fontsize= 14,
              color="darkblue")
ax1.axhline(y=0, color="black", linestyle="--")

bar_ax2 = ax2.bar(
    x=ipca_cesta.index,
    height=ipca_cesta,
    width=0.5,
    color="lightblue",
)
nome = list(ipca_cesta.index).index("IPCA")
bar_ax2[nome].set_color("darkblue")
bar_ax2[nome].set_alpha(0.7)
ax2.bar_label(
    bar_ax2,
    label_type="edge",
    fmt="%.2f%%",
    fontsize=10,
    color="darkblue",
    bbox=dict(fc="white",
              ec="darkblue",linewidth=0.3,
              alpha=0.8,
              boxstyle="round,pad=0.2"
))
ax2.tick_params(axis="x", rotation=45)
ax2.set_title("Cesta IPCA",
              loc="left",
              fontweight="bold",
              fontsize=14,
              color="darkblue")

ax3.plot(ipca_12m["IPCA 12m"],
         label="IPCA 12m",
         alpha=0.5,
         color="darkblue",
         linestyle="-"
         )
ax3.plot(ipca_12m["Média"],
         label="Média dos Núcleos",
         alpha=0.8,
         color="lightblue",
         linestyle="--"
         )
ax3.annotate(
    f"{ipca_12m["IPCA 12m"].iloc[-1]:.2f}%",
    xy=(ipca_12m.index[-1], ipca_12m["IPCA 12m"].iloc[-1] + 0.7),
    va="center",
    ha="left",
    fontsize=10,
    color="white",
    bbox=dict(
        fc="darkblue",
        ec="white",
        linewidth=0.3,
        alpha=0.8,
        boxstyle="round,pad=0.2"
        )
)
ax3.annotate(
    f"{ipca_12m["Média"].iloc[-1]:.2f}%",
    xy=(ipca_12m.index[-1], ipca_12m["Média"].iloc[-1] - 0.5),
    va="center",
    ha="left",
    fontsize=10,
    color="darkblue",
    bbox=dict(
        fc="lightblue",
        ec="white",
        linewidth=0.3,
        alpha=0.8,
        boxstyle="round,pad=0.2"
        )
)
ax3.legend()
ax3.set_title("IPCA 12m e Média Núcleos",
              loc="left",
              fontweight="bold",
              fontsize=14,
              color="darkblue")
ax3.axhline(y=4.5, color="gray", linestyle="--")
ax3.axhline(y=3, color="black", linestyle="--")
ax3.axhline(y=1.5, color="gray", linestyle="--")
ax3.annotate("Teto: 4,5%",
             xy=(ipca_12m.index[0], 4.4),
             va="top", ha="left",
             fontsize=6,
             color="gray")
ax3.annotate("Meta: 3%",
             xy=(ipca_12m.index[0], 2.9),
             va="top", ha="left",
             fontsize=6,
             color="black")
ax3.annotate("Piso: 1,5%",
             xy=(ipca_12m.index[0], 1.4),
             va="top", ha="left",
             fontsize=6,
             color="gray")
plt.annotate("fonte: IBGE", xy=(0.08,0.035), xycoords="figure fraction", va="bottom", ha="left", fontsize=10, color="black")
plt.annotate("elaboração: Fabricio Orlandin, CFP®", xy=(0.8,0.035), xycoords="figure fraction", va="bottom", ha="right", fontsize=10, color="black")
plt.tight_layout()
plt.show()
# %%
