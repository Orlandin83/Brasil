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
renda_ipca["V"] = renda_ipca["V"].astype(int)
print(renda_ipca)
#%% Mandatos
dilma = "2015-01-01" #início da pnad contínua
temer = "2016-09-01"
bolsonaro = "2019-01-01"
lula = "2023-01-01"
#%% Dilma
df_dilma = renda_ipca.loc[(renda_ipca.index >= dilma) & (renda_ipca.index < temer)]
df_dilma = df_dilma.reset_index()
df_dilma["IPCA Acum"] = (((df_dilma["433"] / 100 ) + 1).cumprod() - 1) * 100
df_dilma["Valorização Renda Média"] = ((df_dilma["V"].pct_change() + 1).cumprod() - 1) * 100 
df_dilma = df_dilma.dropna()
print(df_dilma)
# %%
df_temer = renda_ipca.loc[(renda_ipca.index >= temer) & (renda_ipca.index < bolsonaro)]
df_temer = df_temer.reset_index()
df_temer["IPCA Acum"] = (((df_temer["433"] / 100 ) + 1).cumprod() - 1) * 100
df_temer["Valorização Renda Média"] = ((df_temer["V"].pct_change() + 1).cumprod() - 1) * 100 
df_temer = df_temer.dropna()
print(df_temer)
# %%
df_bolsonaro = renda_ipca.loc[(renda_ipca.index >= bolsonaro) & (renda_ipca.index < lula)]
df_bolsonaro = df_bolsonaro.reset_index()
df_bolsonaro["IPCA Acum"] = (((df_bolsonaro["433"] / 100 ) + 1).cumprod() - 1) * 100
df_bolsonaro["Valorização Renda Média"] = ((df_bolsonaro["V"].pct_change() + 1).cumprod() - 1) * 100 
df_bolsonaro = df_bolsonaro.dropna()
print(df_bolsonaro)
# %%
df_lula = renda_ipca.loc[(renda_ipca.index >= lula)]
df_lula = df_lula.reset_index()
df_lula["IPCA Acum"] = (((df_lula["433"] / 100 ) + 1).cumprod() - 1) * 100
df_lula["Valorização Renda Média"] = ((df_lula["V"].pct_change() + 1).cumprod() - 1) * 100 
df_lula = df_lula.dropna()
print(df_lula)
# %% Gráficos
fig, axs = plt.subplots(4, 1, figsize=(16,8))
gov_dfs = [df_dilma, df_temer, df_bolsonaro, df_lula]
gov_names = ["Dilma", "Temer", "Bolsonaro", "Lula"]
cores = ["blue", "black", "green", "red"]
for df, nome, cor, ax in zip(gov_dfs, gov_names, cores, axs):
    ax.plot(df["IPCA Acum"], label = "Inflação Acumulada", linestyle = "--", color=cor)
    ax.plot(df["Valorização Renda Média"], label = "Valorização Renda Média", color=cor)
    ax.set_title(f"Governo {nome}", loc="left")
    ax.legend(loc = "upper left")
    ax.annotate(f"{df["IPCA Acum"].iloc[-1]:.2f}%",
                xy=(df.index[-1], df["IPCA Acum"].iloc[-1]),
                va="top", ha="left", fontsize=6, color=cor
    )
    ax.annotate(f"{df["Valorização Renda Média"].iloc[-1]:.2f}%",
                xy=(df.index[-1], df["Valorização Renda Média"].iloc[-1]),
                va="top", ha="left", fontsize=6, color=cor
    )
plt.annotate("* Governo Dilma desde a criação da PNAD Contínua em março de 2012",
             xy = (0.05, 0.03), xycoords="figure fraction",
             fontsize=8, color="gray")
plt.annotate("fonte: PNAD Contínua - IBGE",
             xy = (0.05, 0.002), xycoords="figure fraction",
             fontsize=8, color="gray")
plt.annotate("elaborado por: Fabricio Orlandin, CFP®",
             xy = (0.78, 0.002), xycoords="figure fraction",
             fontsize=8, color="gray")
plt.tight_layout()
plt.show()
# %%
