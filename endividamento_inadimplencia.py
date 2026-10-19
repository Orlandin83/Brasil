#%% bibliotecas
from bcb import sgs
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
#%% Inad PF
cred_pf = (sgs.get(22050, start="2016-01-01", end=dt.datetime.today()) / 1000).astype(float).round(2)
cred_pf = cred_pf.rename(columns={"22050": "Saldo_PF"})
cred_pf["%_Inadimplência"] = sgs.get(21084, start="2016-01-01", end=dt.datetime.today())
cred_pf["Inadimplência"] = (cred_pf["Saldo_PF"] / 100 * cred_pf["%_Inadimplência"]).astype(float).round(2)
cred_pf_bim = cred_pf.loc[cred_pf.index.month % 2 == 0]
print(cred_pf_bim)
#%% Inad PJ
#cred_pj = (sgs.get(22047, start="2020-01-01", end=dt.datetime.today()) / 1000).astype(float).round(2)
#cred_pj = cred_pj.rename(columns={"22047": "Saldo_PJ"})
#cred_pj["%_Inadimplência"] = sgs.get(21083, start="2020-01-01", end=dt.datetime.today())
#3cred_pj["Inadimplência"] = (cred_pj["Saldo_PJ"] / 100 * cred_pj["%_Inadimplência"]).astype(float).round(2)
#print(cred_pj)
#%%grafico pj
plt.figure(figsize=(16,8))
plt.bar(cred_pf_bim.index, cred_pf_bim["Saldo_PF"], width=30, label = "Saldo PF", color="lightblue", alpha=0.6)
plt.bar(cred_pf_bim.index, cred_pf_bim["Inadimplência"], width=30, label = "Inadimplência PF", color="blue")
plt.title("Saldo de Crédito e Inadimplência PF (R$ bilhões)", fontsize=16, loc="left")
plt.legend(loc="upper left", fontsize=12)
plt.annotate("Fonte: Banco Central do Brasil (BCB)", xy=(0.1,0.02),
             va="bottom", ha="left", xycoords="figure fraction",
             color="black", fontsize=10)
plt.annotate("Elaborado por: Fabricio Orlandin, CFP®", xy=(0.8,0.02),
             va="bottom", ha="right", xycoords="figure fraction",
             color="black", fontsize=10)
plt.show()
# %%
