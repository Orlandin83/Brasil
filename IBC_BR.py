#%%
import datetime as dt
from bcb import sgs
import pandas as pd
import matplotlib.pyplot as plt

#%%
ibc_br = sgs.get(24364, "2025-01-01", dt.date.today())
ibc_br = ibc_br / ibc_br.iloc[0,0]
agriculture = sgs.get(29602, "2025-01-01", dt.date.today())
agriculture = agriculture / agriculture.iloc[0,0]
industry = sgs.get(29604, "2025-01-01", dt.date.today())
industry = industry / industry.iloc[0,0]
services = sgs.get(29606, "2025-01-01", dt.date.today())
services = services / services.iloc[0,0]
nonfarm = sgs.get(29608, "2025-01-01", dt.date.today())
nonfarm = nonfarm / nonfarm.iloc[0,0]
taxes = sgs.get(29610, "2025-01-01", dt.date.today())
taxes = taxes / taxes.iloc[0,0] 
# %%
plt.figure(figsize= (12, 5))
plt.plot(ibc_br, label= "IBC-BR", color= "green")
plt.plot(agriculture, label= "Agricultura", color= "lightgray")
plt.plot(industry, label= "Indústria", color= "black")
plt.plot(services, label= "Serviços", color= "red")
plt.plot(nonfarm, label= "Não Agropecuário", color= "orange")
plt.plot(taxes, label= "Impostos", color= "blue")
plt.axhline(y= 1, linestyle = "--", color= "black")
plt.legend()
plt.ylabel("Acumulado")
plt.text(x= 0.85, y= -0.20, s= "Fabricio Orlandin, CFP®", color= "black", transform= plt.gca().transAxes)
plt.text(x= 0, y= -0.10, s= "fonte: Banco Central do Brasil", color= "black", transform= plt.gca().transAxes)
plt.title("Atividade (IBC-BR)", loc= "left")
plt.show()



# %%
