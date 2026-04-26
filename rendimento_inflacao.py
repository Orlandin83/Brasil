#%% Bibliotecas
import sidrapy
from bcb import sgs 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
#%% Inflação
ipca_m = sgs.get(433, "2000-01-01", dt.datetime.today())
print(ipca_m)
# %% Renda Média
renda = sidrapy.get_table("6390", territorial_level=1, ibge_territorial_code=1, variable="5929", period="201203-202602")
renda = renda[["D2C", "V"]]
renda = renda.iloc[1:]
renda["D2C"] = pd.to_datetime(renda["D2C"] + "01")
renda = renda.set_index("D2C")
#%% Unir dataframes
renda_ipca = pd.concat([ipca_m, renda], axis = 1).dropna()
print(renda_ipca)
#%% Mandatos
dilma = "2012-03-01" #início da pnad contínua
temer = "2016-09-01"
bolsonaro = "2019-01-01"
lula = "2023-01-01"
#%% Dilma
df_dilma = renda_ipca.loc[(renda_ipca.index >= dilma) & (renda_ipca.index < temer)]
df_dilma = df_dilma.reset_index()
print(df_dilma)
# %%
df_temer = renda_ipca.loc[(renda_ipca.index >= temer) & (renda_ipca.index < bolsonaro)]
print(df_temer)
# %%
df_bolsonaro = renda_ipca.loc[(renda_ipca.index >= bolsonaro) & (renda_ipca.index < lula)]
print(df_bolsonaro)
# %%
df_lula = renda_ipca.loc[(renda_ipca.index >= lula)]
print(df_lula)
# %%
