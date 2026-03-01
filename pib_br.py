# %% Importa biblioteca
from bcb import sgs
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np

# %% Importar dados do PIB
pib_hist = sgs.get("22109", "2017-01-01", dt.datetime.today())
pib_hist_var = pib_hist.pct_change().dropna() * 100
pib_hist_var_12m = pib_hist_var.rolling(window=4).apply(lambda x: (np.prod(1 + x / 100) -1) * 100, raw = True).dropna()
pib_hist_var = pib_hist_var.loc[pib_hist_var.index.intersection(pib_hist_var_12m.index)]
# %% Importar PIB e sub itens do PIB em 2025
agro = sgs.get("22105", "2025-01-01", dt.datetime.today())
agro = agro.pct_change().dropna() * 100
industry = sgs.get("22106", "2025-01-01", dt.datetime.today())
industry = industry.pct_change().dropna() * 100
services = sgs.get("22107", "2025-01-01", dt.datetime.today())
services = services.pct_change().dropna() * 100
private_consumption = sgs.get("22110", "2025-01-01", dt.datetime.today())
private_consumption = private_consumption.pct_change().dropna() * 100
government_consumption = sgs.get("22111", "2025-01-01", dt.datetime.today())
government_consumption = government_consumption.pct_change().dropna() * 100
investments = sgs.get("22113", "2025-01-01", dt.datetime.today())
investments = investments.pct_change().dropna() * 100
exports = sgs.get("22114", "2025-01-01", dt.datetime.today())
exports = exports.pct_change().dropna() * 100
imports = sgs.get("22115", "2025-01-01", dt.datetime.today())
imports = imports.pct_change().dropna() * 100
pib = sgs.get("22109", "2025-01-01", dt.datetime.today())
pib = pib.pct_change().dropna() * 100

pib_df = pd.concat([
    agro.rename(columns={"22105": "Agro"}),
    industry.rename(columns={"22106": "Indústria"}),
    services.rename(columns={"22107": "Serviços"}),
    private_consumption.rename(columns={"22110": "Cons. Privado"}),
    government_consumption.rename(columns={"22111": "Cons. Governo"}),
    investments.rename(columns={"22113": "Investimentos"}),
    exports.rename(columns={"22114": "Exportação"}),
    imports.rename(columns={"22115": "Importação"}),
    pib.rename(columns={"22109": "PIB"}),
], axis=1)

pib_df = pib_df.T
pib_df.columns = ["Variação"]
pib_df.index.name = "Setor"
print(pib_df)

# %% Plotar Gráfico
plt.figure(figsize = (16,8))
plt.plot(pib_hist_var_12m, label = "PIB 4 Trimestres", color = "orange")
plt.bar(x = pib_hist_var.index, height= pib_hist_var.iloc[:, 0], width= 85, color= "orange", label = "Variação Trimestral")
plt.annotate("fonte: Banco Central Br / IBGE", xy = (0, -0.1), xycoords = "axes fraction", fontsize = 10, color = "gray", ha = "left", va = "bottom")
plt.annotate("Fabricio Orlandin, CFP®", xy=(1, -0.1), xycoords= "axes fraction", fontsize=10, color="gray", ha="right", va="bottom")
plt.annotate(f"{pib_hist_var.iloc[-1,0]:.1f}%", xy = (pib_hist_var.index[-1], pib_hist_var.iloc[-1,0] + 0.2), color = "black", fontsize = 8, ha = "center", va = "center")
plt.annotate(f"{pib_hist_var.iloc[-2,0]:.1f}%", xy = (pib_hist_var.index[-2], pib_hist_var.iloc[-2,0] + 0.25), color = "black", fontsize = 8, ha = "center", va = "center")
plt.annotate(f"{pib_hist_var_12m.iloc[-1,0]:.1f}%", xy = (pib_hist_var_12m.index[-1], pib_hist_var_12m.iloc[-1,0] + 0.25), color = "black", fontsize = 8, ha = "left", va = "center")
plt.ylabel("Variação do PIB")
plt.xlabel("Trimestres")
plt.legend()
plt.show()

# %%
plt.figure(figsize=(12,6))
plt.bar(x = pib_df.index, height= pib_df["Variação"], width= 0.5, color = "steelblue", label = "Variação por setor")
plt.annotate("fonte: Banco Central Br / IBGE", xy = (0, -0.1), xycoords = "axes fraction", fontsize = 10, color = "gray", ha = "left", va = "bottom")
plt.annotate("Fabricio Orlandin, CFP®", xy=(1, -0.1), xycoords= "axes fraction", fontsize=10, color="gray", ha="right", va="bottom")
for i, (setor, valor) in enumerate(pib_df["Variação"].items()):
    plt.annotate(f"{valor:.1f}%", 
                 xy=(i, valor), 
                 xytext=(0, 5), 
                 textcoords="offset points", 
                 ha="center", va="bottom", 
                 fontsize=8, color="black")
plt.ylabel("Variação do PIB")
plt.show()

# %%
