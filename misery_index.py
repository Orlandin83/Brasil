#%%
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from bcb import sgs
import eurostat
#%% Brasil
ipca12m = sgs.get("13522", "2012-03-01", dt.datetime.today())
desemprego = sgs.get("24369", "2012-03-01", dt.datetime.today())
desemprego = desemprego.rolling(window=12).apply(lambda x:(np.mean(x)), raw= True).dropna()
ipca12m = ipca12m.loc[ipca12m.index <= desemprego.index[-1]]
ipca12m = ipca12m.loc[ipca12m.index >= desemprego.index[0]]
misery_index_BR = pd.DataFrame(ipca12m.iloc[:,0] + desemprego.iloc[:,0].dropna())
# %% EUA
cpi = pdr.DataReader("CPIAUCSL", "fred", "2012-03-01", dt.datetime.today())
cpi = cpi.pct_change().dropna()
cpi12m = cpi.rolling(window=12).apply(lambda x:(np.prod(1 + x)-1)*100, raw=True).dropna()
unemployment = pdr.DataReader("UNRATE", "fred", "2012-03-01", dt.datetime.today())
unemployment = unemployment.rolling(window=12).apply(lambda x:(np.mean(x)), raw= True).dropna()
unemployment = unemployment.loc[unemployment.index >= cpi12m.index[0]]
misery_index_US = pd.DataFrame(unemployment.iloc[:,0] + cpi12m.iloc[:,0])
#%%
plt.figure(figsize=(18,6))
plt.plot(misery_index_BR, label= "Misery Index BR", color = "blue")
plt.plot(misery_index_US, label= "Misery Index US", color = "red")
plt.annotate("Fabricio Orlandin, CFP®", xy = (1, -0.1), xycoords = "axes fraction", color = "black", fontsize = 10, ha= "right", va= "center")
plt.annotate("fonte: IBGE e Banco Central do Brasil / Federal Reserve", xy = (0, -0.1), xycoords = "axes fraction", color = "black", fontsize = 10, ha= "left", va= "center")
plt.annotate(f"{misery_index_BR.iloc[-1,0]:.2f}%", xy=(misery_index_BR.index[-1], misery_index_BR.iloc[-1,0] + 0.2), color = "blue", fontsize = 8, ha = "left", va = "bottom")
plt.annotate(f"{misery_index_US.iloc[-1,0]:.2f}%", xy=(misery_index_US.index[-1], misery_index_US.iloc[-1,0] + 0.1), color = "red", fontsize = 8, ha = "left", va = "bottom")
plt.axvline(x = pd.to_datetime("2020-03-01"), color= "black", linestyle= "--")
plt.axhline(y= np.mean(misery_index_BR.iloc[:,0]), color= "blue", linestyle= "--")
plt.axhline(y= np.mean(misery_index_US.iloc[:,0]), color= "red", linestyle= "--")
plt.annotate("Pandemia Covid-19", xy=(pd.to_datetime("2020-03-01"), 13), color= "black", fontsize=8, rotation= 90, va= "top", ha= "right")
plt.legend()
plt.title("Misery Index", loc= "left")
plt.show()

# %%
