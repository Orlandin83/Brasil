#%%
from bcb import sgs
import matplotlib.pyplot as plt
import datetime as dt
endividamento = sgs.get(29038, start= '2008-01-01', end= dt.date.today())
# %%
plt.figure(figsize=(16,12))
plt.plot(endividamento, color='grey', label= 'Endividamento das Famílias')
plt.grid(True)
plt.ylabel("Percentual de Endividamento")
plt.xlabel("Período")
plt.text(x=0, y=-0.1, s='fonte: Banco Central do Brasil', color='grey', transform= plt.gca().transAxes)
plt.text(x=0.8, y=-0.1, s='Fabricio Orlandin, CFP®', color='grey', transform= plt.gca().transAxes)
plt.title("Endividamento das Famílias")
plt.show()
# %%
juros = sgs.get(29033, start= '2008-01-01', end= dt.date.today())
display(juros)
# %%
plt.figure(figsize=(16,12))
plt.plot(juros, color='grey', label= 'Pagamento de Juros')
plt.grid(True)
plt.ylabel("Percentual")
plt.xlabel("Período")
plt.text(x=0, y=-0.1, s='fonte: Banco Central do Brasil', color='grey', transform= plt.gca().transAxes)
plt.text(x=0.8, y=-0.1, s='Fabricio Orlandin, CFP®', color='grey', transform= plt.gca().transAxes)
plt.title("Juros de Dívida no Orçamento das Famílias")
plt.show()
# %%
