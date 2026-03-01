#%%
from bcb import sgs
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
#%%
tx_desemprgo = sgs.get(24369, "2010-01-01", datetime.today())
print(tx_desemprgo)
# %%
plt.figure(figsize=(16,8))
plt.plot(tx_desemprgo, label='Percentual de Desemprego', color='blue')
plt.legend()
plt.grid(True)
plt.ylabel('% de Desemprego')
plt.xlabel('Tempo')
plt.annotate(f'  {tx_desemprgo.iloc[-1,0]}%',
             xy=(tx_desemprgo.index[-1], tx_desemprgo.iloc[-1]),
             xytext=(tx_desemprgo.index[-1], tx_desemprgo.iloc[-1] + 0.0),
             fontsize=10, color='blue', ha='left')
plt.text(tx_desemprgo.index[-1], plt.ylim()[0] - 1, "Fabricio Orlandin, CFP®", fontsize=15, ha='right', color='grey')
plt.text(tx_desemprgo.index[0], plt.ylim()[0] - 1, "fonte: Banco Central do Brasil", fontsize=15, ha='left', color='grey')
plt.show()
# %%
