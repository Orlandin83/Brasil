#%% Importar bibliotecas 
from bcb import sgs
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np
#%% Construir dataframe selic
selic0 = sgs.get(432, "2012-03-01", "2016-03-04")
selic1 = sgs.get(432, "2016-03-05", dt.datetime.today())
selic = pd.concat([selic0, selic1], axis=0)
#%% Construir dataframe IPCA
IPCA_mensal = sgs.get(433, "2012-03-01", dt.datetime.today())
#%% Construir dataframe IPCA 12 meses
IPCA12m = sgs.get(13522, "2012-03-01", dt.datetime.today())
#%% Construir dataframe desemprego
desemprego = sgs.get (24369, "2012-03-01", dt.datetime.today())
#%% Construir dataframe do núcleo do ipca de 12 meses
nucleo_ipca = sgs.get(28751, "2010-01-01", dt.datetime.today())
nucleo_ipca = nucleo_ipca.rolling(window=12).apply(lambda x:(np.prod((x / 100)+1)-1) * 100, raw = True).dropna()
nucleo_ipca = nucleo_ipca[nucleo_ipca.index >= desemprego.index[0]]
print(nucleo_ipca)
# %% Plotar gráfico
plt.figure(figsize=(18,9))
plt.bar(x = desemprego.index, height= desemprego.iloc[:,0], width= 50, color = "lightgray", label = "Taxa de Desemprego")
plt.bar(x = IPCA_mensal.index, height= IPCA_mensal.iloc[:,0], width= 20, color = "blue", label = "IPCA Mensal")
plt.plot(IPCA12m, color = "blue", label = "IPCA 12 meses")
plt.plot(selic, label = "Taxa Selic", color = "black")
plt.plot(nucleo_ipca, color = "darkblue", label = "Núcleo IPCA (ex alimentos e energia) 12 meses")
plt.axhline(y = 4.5, linestyle = "--", color = "darkgray")
plt.axhline(y = 3, linestyle = "--", color = "black")
plt.axhline(y = 1.5, linestyle = "--", color = "darkgray")
plt.annotate("fonte: Banco Central do Brasil e IBGE", xy=(0, -0.05), xycoords="axes fraction", color = "black", fontsize = 10, va = "top", ha = "left")
plt.annotate("Fabricio Orlandin, CFP®", xy=(1, -0.05), xycoords="axes fraction", color = "black", fontsize = 10, va = "top", ha = "right")
plt.text(x = desemprego.index[-1], y = 4.3, s = "Teto: 4,5%", color = "darkgray", fontsize = 6, va = "top", ha = "center")
plt.text(x = desemprego.index[-1], y = 2.8, s = "Meta IPCA: 3%", color = "black", fontsize = 6, va = "top", ha = "center")
plt.text(x = desemprego.index[-1], y = 1.7, s = "Piso: 1,5%", color = "darkgray", fontsize = 6, va = "bottom", ha = "center")
plt.legend(loc="upper left")
plt.annotate(f"{IPCA_mensal.iloc[-1,0]:.2f}%", xy=(IPCA_mensal.index[-1], IPCA_mensal.iloc[-1,0]), color = "blue", fontsize = 6, va = "bottom", ha = "left")
plt.annotate(f"{IPCA_mensal.iloc[-2,0]:.2f}%", xy=(IPCA_mensal.index[-2], IPCA_mensal.iloc[-2,0] + 0.2), color = "blue", fontsize = 6, va = "top", ha = "center")
plt.annotate(f"{IPCA_mensal.iloc[-13,0]:.2f}%", xy=(IPCA_mensal.index[-13], -0.1), color = "blue", fontsize = 6, va = "top", ha = "center")
plt.annotate(f"{IPCA12m.iloc[-1,0]:.2f}%", xy = (IPCA12m.index[-1], IPCA12m.iloc[-1,0]), color = "blue", fontsize = 6, va = "top", ha = "left")
plt.annotate(f"{desemprego.iloc[-1,0]:.2f}%", xy = (desemprego.index[-1], desemprego.iloc[-1,0]), color = "gray", fontsize = 6, va = "bottom", ha = "left")
plt.annotate(f"{selic.iloc[-1,0]:.2f}%", xy = (selic.index[-1], selic.iloc[-1,0]), color = "black", fontsize = 6, va = "bottom", ha = "left")
plt.annotate(f"{nucleo_ipca.iloc[-1,0]:.2f}%", xy = (nucleo_ipca.index[-1], nucleo_ipca.iloc[-1,0]), color = "darkblue", fontsize = 6, va = "top", ha = "left")
plt.title("Juros, Inflação, Desemprego", loc= "left")
plt.show()

# %%
