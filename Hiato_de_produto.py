#%%
from bcb import sgs
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter
import datetime as dt
#%%
PIB_df = sgs.get(4382, start='1996-01-01', end= dt.date.today())
PIB_df.columns = ['PIB']
# %%
pib_ciclo, pib_tendencia = hpfilter(PIB_df['PIB'], lamb=129600)
hiato = pib_ciclo / pib_tendencia * 100
PIB_df['Hiato'] = hiato
print(PIB_df)
# %%
plt.figure(figsize=(18,12))
plt.plot(PIB_df['Hiato'], label= 'Hiato do Produto', color='blue')
plt.axhline(y= 0, linestyle= '--', color='grey')
plt.grid(True)
plt.text(x= 1, y= -0.1, s= 'Fabricio Orlandin, CFP®', fontsize = 15, ha= 'right', transform= plt.gca().transAxes)
plt.text(x= 0, y= -0.1, s= 'fonte: Banco Central do Brasil', fontsize= 15, ha= 'left', transform= plt.gca().transAxes)
plt.title('Hiato do Produto', fontsize = 15)
plt.legend(fontsize= 15)
plt.show()

# %%
