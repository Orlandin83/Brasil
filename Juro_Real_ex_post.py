#%%
from bcb import sgs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
#%% Extrai bases da Selic 
selic1 = sgs.get(432, start= '2010-01-01', end= '2015-12-31')
selic2 = sgs.get(432, start = '2016-01-01', end= '2021-12-31')
selic3 = sgs.get(432, start= '2022-01-01', end= dt.date.today())
selic_df = pd.concat([selic1, selic2, selic3]) # Unifica as bases da Selic em um único dataframe
#%%
selic_df["TaxaDia"] = (1 + selic_df["432"] / 100) ** (1 / 252) - 1  # Converte a taxa Selic anual para taxa diária
selic_df["Selic12m"] = selic_df["TaxaDia"].rolling(window=252).apply(lambda x: (np.prod(1 + x) - 1) * 100, raw=True)  # Calcula a Selic acumulada em 12 meses
display(selic_df)
# %% Extrai as bases do IPCA e aplica a fórmula de IPCA 12 meses - rolling
ipca12m_df = sgs.get(433, start= '2010-01-01', end= dt.date.today())
ipca12m_df = ipca12m_df.rolling(window=12).apply(lambda x: (np.prod((x/100)+1)-1)*100,raw=True).dropna()
display(ipca12m_df)
# %% 
juro_real_df = selic_df[["Selic12m"]].copy()
juro_real_df.columns = ["Selic12m"]
juro_real_df["IPCA12m"] = ipca12m_df["433"]
juro_real_df["IPCA12m"].fillna(method='ffill', inplace=True)
juro_real_df["IPCA12m"].fillna(ipca12m_df.iloc[-1,0], inplace=True)
juro_real_df["Juro_Real"] = juro_real_df["Selic12m"] - juro_real_df["IPCA12m"]
display(juro_real_df)
juro_real_df.to_excel("Juro_Real.xlsx", index=True, sheet_name='Juro_Real')
# %%
plt.figure(figsize=(16,8))
plt.plot(juro_real_df['Selic12m'], label='Selic12m', color='black')
plt.plot(juro_real_df['IPCA12m'], label='IPCA12m', color='grey')
plt.plot(juro_real_df['Juro_Real'], label= 'Juro_Real', color='red')
plt.axhline(0, linestyle='--', color='grey')
plt.text(x=0, y=-0.1, s='fonte: Banco Central do Brasil', color='grey', transform= plt.gca().transAxes)
plt.text(x=1, y=-0.1, s='Fabricio Orlandin, CFP®', ha='right', color='grey', transform= plt.gca().transAxes)
plt.legend()
plt.grid()
plt.annotate(f'IPCA 12m:{float(juro_real_df["IPCA12m"].iloc[-1]):.2f}%',
             xy=(juro_real_df["IPCA12m"].index[-1], float(juro_real_df["IPCA12m"].iloc[-1])),
             xytext=(juro_real_df["IPCA12m"].index[-1], float(juro_real_df["IPCA12m"].iloc[-1]) + 0.5),
             fontsize=10, color='grey', ha='left')
plt.annotate(f'SELIC: {float(juro_real_df["Selic12m"].iloc[-1]):.2f}%',
             xy=(juro_real_df["Selic12m"].index[-1], float(juro_real_df["Selic12m"].iloc[-1])),  
             xytext=(juro_real_df["Selic12m"].index[-1], float(juro_real_df["Selic12m"].iloc[-1]) - 0.7),  
             fontsize=10, color='black', ha='left')
plt.annotate(f'Juro Real: {float(juro_real_df['Juro_Real'].iloc[-1]):.2f}%',
             xy=(juro_real_df['Juro_Real'].index[-1], float(juro_real_df['Juro_Real'].iloc[-1])),  
             xytext=(juro_real_df['Juro_Real'].index[-1], float(juro_real_df['Juro_Real'].iloc[-1]) - 0.7),
             fontsize=10, color='red', ha='left')
plt.show()

# %%
