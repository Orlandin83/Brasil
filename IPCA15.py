#%%
from bcb import sgs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt

#%%
ipca15 = sgs.get(7478,start='2010-01-01', end= dt.date.today())
ipca = sgs.get(433,start='2010-01-01',end= dt.date.today())
ipca_12m = ipca.rolling(window=12).apply(lambda x: (np.prod((x/100)+1)-1)*100,raw=True).dropna()
ipca15_12m = ipca15.rolling(window=12).apply(lambda x: (np.prod((x/100)+1)-1)*100,raw=True).dropna()
print(ipca15_12m)
print(ipca_12m)

#%%
plt.figure(figsize=(16,8))
plt.plot(ipca15_12m, label='IPCA-15 12M (%)', color='red')
plt.plot(ipca_12m, label='IPCA 12M (%)', color='gray')
plt.legend()
plt.title('IPCA x IPCA-15')
plt.xlabel('Data')
plt.ylabel('(%)')
plt.text(ipca15_12m.index[-1], plt.ylim()[0] - 1, "Fabricio Orlandin, CFP®", fontsize=15, ha='right', color='black')
plt.text(ipca15_12m.index[0], plt.ylim()[0] - 1, "fonte: Banco Central do Brasil", fontsize=15, ha='left', color='black')

plt.annotate(f'IPCA 12m:{ipca_12m.iloc[-1,0]:.2f}%',
             xy=(ipca_12m.index[-1], ipca_12m.iloc[-1]),
             xytext=(ipca_12m.index[-1], ipca_12m.iloc[-1] + 0.5),
             fontsize=10, color='black', ha='left')

plt.annotate(f'IPCA-15_12m: {ipca15_12m.iloc[-1,0]:.2f}%',
             xy=(ipca15_12m.index[-1], ipca15_12m.iloc[-1]),  
             xytext=(ipca15_12m.index[-1], ipca15_12m.iloc[-1] + 0.2),  
             fontsize=10, color='red', ha='left')
plt.axhline(y=1.5, color='gray', linestyle='--', linewidth=1, label='1,5%')  # Linha em 1,5%
plt.axhline(y=3.0, color='blue', linestyle='--', linewidth=1, label='3,0%')  # Linha em 3%
plt.axhline(y=4.5, color='gray', linestyle='--', linewidth=1, label='4,5%')  # Linha em 4,5%

plt.text(ipca15_12m.index[-1], 1.5, '1,5%', verticalalignment='bottom', color='gray', fontsize=10)
plt.text(ipca15_12m.index[-1], 3.0, '3,0%', verticalalignment='bottom', color='blue', fontsize=10)
plt.text(ipca15_12m.index[-1], 4.5, '4,5%', verticalalignment='bottom', color='gray', fontsize=10)
plt.show()
