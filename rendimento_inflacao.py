#%% Bibliotecas
import sidrapy
from bcb import sgs 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
#%% Inflação
ipca_m = sgs.get(433, "2000-01-01", dt.datetime.today())
# %% Renda Média
renda = sidrapy.get_table("6390", territorial_level=1, ibge_territorial_code=1, variable="5929", period="201203-202602")
renda = renda[["D2C", "V"]]
renda = renda.iloc[1:]
renda["D2C"] = pd.to_datetime(renda["D2C"] + "01")
renda = renda.set_index("D2C")
#%% Unir dataframes
renda_ipca = pd.concat([ipca_m, renda], axis = 1).dropna()
renda_ipca["V"] = renda_ipca["V"].astype(int)
#%% Mandatos
dilma = "2012-03-01" #início da pnad contínua
temer = "2016-09-01"
bolsonaro = "2019-01-01"
lula = "2023-01-01"
#%% Dilma
df_dilma = renda_ipca.loc[(renda_ipca.index >= dilma) & (renda_ipca.index < temer)]
df_dilma["433"] = df_dilma["433"].shift(1).fillna(0)
df_dilma["IPCA Acum"] = ((1 + (df_dilma["433"] / 100 )).cumprod() - 1) * 100
df_dilma["Valorização Renda Média"] = (df_dilma["V"] / df_dilma["V"].iloc[0] - 1) * 100
df_dilma = df_dilma.reset_index(drop=True)
# %% Temer
df_temer = renda_ipca.loc[(renda_ipca.index >= temer) & (renda_ipca.index < bolsonaro)]
df_temer["433"] = df_temer["433"].shift(1).fillna(0)
df_temer["IPCA Acum"] = ((1 + (df_temer["433"] / 100 )).cumprod() - 1) * 100
df_temer["Valorização Renda Média"] = (df_temer["V"] / df_temer["V"].iloc[0] - 1) * 100
df_temer = df_temer.reset_index(drop=True)
# %% Bolsonaro
df_bolsonaro = renda_ipca.loc[(renda_ipca.index >= bolsonaro) & (renda_ipca.index < lula)]
df_bolsonaro["433"] = df_bolsonaro["433"].shift(1).fillna(0)
df_bolsonaro["IPCA Acum"] = ((1 + (df_bolsonaro["433"] / 100 )).cumprod() - 1) * 100
df_bolsonaro["Valorização Renda Média"] = (df_bolsonaro["V"] / df_bolsonaro["V"].iloc[0] - 1) * 100
df_bolsonaro = df_bolsonaro.reset_index(drop=True)
# %% Lula
df_lula = renda_ipca.loc[(renda_ipca.index >= lula)]
df_lula["433"] = df_lula["433"].shift(1).fillna(0)
df_lula["IPCA Acum"] = ((1 + (df_lula["433"] / 100 )).cumprod() - 1) * 100
df_lula["Valorização Renda Média"] = (df_lula["V"] / df_lula["V"].iloc[0] - 1) * 100
df_lula = df_lula.reset_index(drop=True)
# %% Gráficos
fig, axs = plt.subplots(4, 1, figsize=(16,8))
gov_dfs = [df_dilma, df_temer, df_bolsonaro, df_lula]
gov_names = ["Dilma", "Temer", "Bolsonaro", "Lula"]
for df, nome, ax in zip(gov_dfs, gov_names, axs):
    ax.plot(df["IPCA Acum"], label = "Inflação Acumulada", linestyle = "--", color="red")
    ax.plot(df["Valorização Renda Média"], label = "Valorização Renda Média", color="black")
    ax.set_title(f"Governo {nome}", loc="left")
    ax.legend(loc = "upper left")
    ax.annotate(
    f"{df["IPCA Acum"].iloc[-1]:.2f}%",
                xy=(df.index[-1], df["IPCA Acum"].iloc[-1]),
                va="top", ha="left", fontsize=6, color="red"
)
    ax.annotate(
    f"{df["Valorização Renda Média"].iloc[-1]:.2f}%",
                xy=(df.index[-1], df["Valorização Renda Média"].iloc[-1]),
                va="top", ha="left", fontsize=6, color="black"
)
    ax.annotate(
    f"Ganho real em {len(df)} meses: {((1 + df['Valorização Renda Média'].iloc[-1] / 100) / (1 + df['IPCA Acum'].iloc[-1] / 100) - 1) * 100:.2f}%",
    xy=(df.index[-1], 0),
    va="bottom", ha="right", fontsize=9, color="black",
    fontweight="bold"
)
plt.annotate(
    "* Governo Dilma desde a criação da PNAD Contínua em março de 2012",
    xy = (0.05, 0.03), xycoords="figure fraction",
    fontsize=8, color="gray"
)
plt.annotate(
    "fonte: PNAD Contínua - IBGE",
    xy = (0.05, 0.002), xycoords="figure fraction",
    fontsize=8, color="gray"
)
plt.annotate(
    "elaborado por: Fabricio Orlandin, CFP®",
    xy = (0.78, 0.002), xycoords="figure fraction",
    fontsize=8, color="gray"
)
plt.tight_layout()
plt.show()
# %%
