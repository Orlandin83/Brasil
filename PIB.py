#%% Importando bibliotecas
from bcb import sgs
from datetime import datetime
import matplotlib.pyplot as plt
#%%
pib = sgs.get(4385, start="2012-01-01", end=datetime.today())
unemployment = sgs.get(24380, start="2012-01-01", end=datetime.today())
# %%
fig, ax1 = plt.subplots(figsize=(12, 5))
# Gráfico do PIB no eixo primário
ax1.plot(pib, label="PIB", color="blue")
ax1.set_xlabel("Meses")
ax1.set_ylabel("Milhões U$", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.grid(True)
# Criando eixo secundário para taxa de desemprego
ax2 = ax1.twinx()
ax2.plot(unemployment, label="Desemprego", color="red")
ax2.set_ylabel("População Desempregada", color="red")
ax2.tick_params(axis="y", labelcolor="red")
# Adicionando título e legendas
fig.suptitle("PIB e Taxa de Desemprego")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.text(x=0.85, y=-0.10, s="Fabricio Orlandin, CFP®", color="grey", transform=plt.gca().transAxes)
plt.text(x=0, y=-0.10, s="Fonte: Banco Central do Brasil", color="grey", transform=plt.gca().transAxes)
plt.legend()
plt.show()
# %%
