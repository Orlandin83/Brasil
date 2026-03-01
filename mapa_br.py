#%% importações
from bcb import sgs
import pandas as pd
import numpy as np
import datetime as dt
from statsmodels.tsa.filters.hp_filter import hpfilter
import matplotlib.pyplot as plt
import sidrapy as sdr
#%% dataframes SELIC × IPCA
selic0 = sgs.get(432, "2010-01-01", "2016-12-31")
selic1 = sgs.get(432, "2017-01-01", dt.datetime.today())
selic = pd.concat([selic0, selic1])
selic = selic.rename(columns={"432":"Selic"})
ipca0 = sgs.get (433, "2010-01-01", "2016-12-31")
ipca1 = sgs.get (433, "2017-01-01", dt.datetime.today())
ipca = pd.concat([ipca0, ipca1])
ipca = ipca.rename(columns={"433":"IPCA mensal"})
ipca12m = sgs.get(13522, "2010-01-01", dt.datetime.today())
ipca12m = ipca12m.rename(columns={"13522":"IPCA 12m"})
# %% Dataframe Núcleos do IPCA
nucleos = [11427, 16121, 27838, 27839, 11426, 4466, 16122, 28751, 28750]
media_nucleos0 = sgs.get(nucleos, "2009-02-01", "2015-12-31")
media_nucleos1 = sgs.get(nucleos, "2016-01-01", dt.datetime.today())
media_nucleos = pd.concat([media_nucleos0, media_nucleos1])
media_nucleos["Média"] = media_nucleos.mean(axis=1)
media_nucleos = media_nucleos["Média"]
media_nucleos12m = media_nucleos.rolling(window=12).apply(lambda x:
                                                          (np.prod(1+x/100)-1)*100, raw=True).dropna()
media_nucleos12m = pd.DataFrame(media_nucleos12m).astype(float).round(2)
# %% Dataframe Desemprego
desemprego = sgs.get(24369,"2009-02-01", dt.datetime.today())
desemprego = desemprego.rename(columns={"24380": "Desemprego (%) "})
media_desemprego_12m = desemprego.rolling(window=12).mean().dropna()
media_desemprego_12m = pd.DataFrame(media_desemprego_12m)
desemprego = desemprego.reindex(media_desemprego_12m.index)
media_desemprego_12m = media_desemprego_12m.astype(float).round(2)
#%% Dataframe PIB QoQ
pib_qoq = sdr.get_table(
    table_code="5932",          # tabela 5932 - PIB Trimestral
    territorial_level="1",      # N1 = Brasil
    ibge_territorial_code="1",  # código 1 = Brasil
    variable="6564",            # taxa trimestre contra trimestre imediatamente anterior (%)
    period="201001 - 202503",     # toda a faixa de trimestres listada em /P/
    classifications={"11255": "90707"},    # código da classificação "Setores e subsetores"         # categoria 90707 = PIB a preços de mercado
)
# Limpando o Dataframe e Padronizando o Index
pib_qoq = pib_qoq[["D2N", "V"]] #elimina colunas desnecessárias
pib_qoq.columns = ("Data", "Variação") #atribui os nomes Data e Variação p/ colunas 
pib_qoq = pib_qoq.iloc[1:] # inicia a partir da segunda linha eliminando o cabeçalho
pib_qoq = pib_qoq.set_index("Data") #transforma a coluna data em index
pib_qoq = pd.DataFrame(pib_qoq).astype(float) #transforma os dados em float 
idx = pib_qoq.index.to_series() # cria uma série a partir do index
ano = idx.str.extract(r"(\d{4})", expand=False) # extrai o ano do texto do index
tri = idx.str.extract(r"(\d+)\D+trimestre", expand=False) # extrai o trimestre  do texto do index
period_str = ano + "Q"+ tri # monta o padrão YYYYT
pib_qoq.index = pd.PeriodIndex(period_str, freq="Q") # transforma o padrão em data trimestral
pib_qoq.index = pib_qoq.index.to_timestamp(how="start") # atribui a data inicial do trimestre
# %% Dataframe PIB YoY
pib_yoy = sdr.get_table(
    table_code="5932",
    territorial_level="1",
    ibge_territorial_code="1",
    variable="6561",
    period="201001-202503",
    classifications={"11255": "90707"},   
)
pib_yoy = pib_yoy[["D2N", "V"]]
pib_yoy.columns = ("Data", "Variação")
pib_yoy = pib_yoy.iloc[1:]
pib_yoy = pib_yoy.set_index("Data")
pib_yoy = pd.DataFrame(pib_yoy).astype(float)
idx = pib_yoy.index.to_series()
ano = idx.str.extract(r"(\d{4})", expand=False)
tri = idx.str.extract(r"(\d+)\D+trimestre", expand=False)
period_str = ano + "Q"+ tri
pib_yoy.index = pd.PeriodIndex(period_str, freq="Q")
pib_yoy.index = pib_yoy.index.to_timestamp(how="start")
# %% Hiato de Produto
pib_df = sdr.get_table(
    table_code="1621",
    territorial_level="1",
    ibge_territorial_code="1",
    variable="584",
    period="201001-202503",
    classifications={"11255": "90707"},
)
pib_df = pib_df[["D2N", "V"]]
pib_df.columns = ("Data", "PIB")
pib_df = pib_df.iloc[1:]
pib_df = pib_df.set_index("Data")
idx = pib_df.index.to_series()
ano = idx.str.extract(r"(\d{4})", expand = False)
tri = idx.str.extract(r"(\d+)\D+trimestre", expand = False)
period_str = ano + "Q" + tri
pib_df.index = pd.PeriodIndex(period_str, freq="Q")
pib_df.index = pib_df.index.to_timestamp(how="start")
pib_ciclo, pib_tendencia = hpfilter(pib_df['PIB'], lamb=1600)
pib_df["Ciclo"] = pib_ciclo
pib_df["Tendencia"] = pib_tendencia
pib_df["Hiato"] = pib_df["Ciclo"] / pib_df["Tendencia"] * 100
pib_df = pd.DataFrame(pib_df)
#%% Dataframe IBC-BR
ibcbr = sgs.get(24364, "2020-01-01", dt.datetime.today())
industria = sgs.get(29604, "2020-01-01", dt.datetime.today())
agropecuaria = sgs.get(29602, "2020-01-01", dt.datetime.today())
servicos = sgs.get(29606, "2020-01-01", dt.datetime.today())
ibcbr_norm        = (ibcbr / ibcbr.iloc[0] - 1) * 100
industria_norm    = (industria / industria.iloc[0] - 1) * 100
agropecuaria_norm = (agropecuaria / agropecuaria.iloc[0] - 1) * 100
servicos_norm     = (servicos / servicos.iloc[0] - 1) * 100
ibcbr_var = ibcbr.pct_change() * 100
ibcbr_var = ibcbr_var.astype(float).round(1).dropna()
#%% Gráfico 1 IPCA e Selic
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(16,10))
axes[0,0].plot(selic, color="black", label="Selic")
axes[0,0].plot(ipca12m, color="blue", label="IPCA 12m")
axes[0,0].plot(media_nucleos12m, color="darkblue", label="Média Núcleos IPCA 12m", linestyle = "--")
axes[0,0].bar(ipca.index, height=ipca.iloc[:,0], width=25, label = "IPCA mensal", color="blue")
axes[0,0].annotate(f"{selic.iloc[-1,0]}%",
                   xy=(selic.index[-1], selic.iloc[-1,0] - 1),
                   ha="left",va="bottom", color="black", fontsize=8)
axes[0,0].annotate(f"{ipca12m.iloc[-1,0]}%",
                   xy=(ipca12m.index[-1], ipca12m.iloc[-1,0] - 0.8),
                   ha="right", va="bottom", color="blue", fontsize=8)
axes[0,0].annotate(f"{media_nucleos12m.iloc[-1,0]}%",
                   xy=(media_nucleos12m.index[-1], media_nucleos12m.iloc[-1,0] + 0.5),
                   ha="left", va="bottom", color="darkblue", fontsize=8)
axes[0,0].annotate(f"{ipca.iloc[-1,0]}%",
                   xy=(ipca.index[-1], ipca.iloc[-1,0] + 0.5),
                   ha="left", va="bottom", color="blue", fontsize=6)
axes[0,0].annotate(f"{ipca.iloc[-2,0]}%",
                   xy=(ipca.index[-2], ipca.iloc[-1,0] - 1),
                   ha="right", va="bottom", color="blue", fontsize=6)
axes[0,0].annotate(f"{ipca.iloc[-13,0]}%",
                   xy=(ipca.index[-13], ipca.iloc[-1,0] - 1),
                   ha="right", va="bottom", color="blue", fontsize=6)
axes[0,0].axhline(y= 3, linestyle="--", color = "black")
axes[0,0].axhline(y= 4.5, linestyle="--", color = "gray")
axes[0,0].axhline(y= 1.5, linestyle="--", color = "gray")
axes[0,0].annotate("3,0%", xy=(ipca12m.index[0], 3),
                   ha="right", va="bottom", fontsize = 6, color = "black")
axes [0,0].annotate("4,5%", xy=(ipca12m.index[0], 4.5),
                   ha="right", va="top", fontsize=6, color="gray")
axes[0,0].annotate("1,5%", xy=(ipca12m.index[0], 1.5),
                   ha="right", va="bottom", fontsize=6, color="gray")
axes[0,0].legend(fontsize=6)
axes[0,0].set_title("Juros x Inflação", fontsize=8, loc="left")
# Gráfico 2 - Desemprego
axes[0,1].bar(desemprego.index, height=desemprego.iloc[:,0], width=25,
               color="gray", label="Taxa de Desemprego")
axes[0,1].plot(media_desemprego_12m, color = "blue", label="Média Desemprego 12m", linestyle="--")
axes[0,1].annotate(f"{desemprego.iloc[-1,0]}%",
                    xy=(desemprego.index[-1], desemprego.iloc[-1,0]),
                    ha="left", va="bottom", color="gray", fontsize=6)
axes[0,1].annotate(f"{media_desemprego_12m.iloc[-1, 0]}%",
                    xy=(media_desemprego_12m.index[-1], media_desemprego_12m.iloc[-1,0]),
                    ha="left", va="bottom", color="blue", fontsize=6)
axes[0,1].legend (fontsize=6)
axes[0,1].set_title("Taxa de Desemprego", fontsize = 8, loc="left")
# Gráfico 3 - PIB
colors = np.where(pib_qoq.iloc[:,0] < 0, "red", "blue")
axes[1,0].bar(x=pib_qoq.index, height = pib_qoq.iloc[:,0], width = 60,
              color=colors, label="PIB Trimestral QoQ")
axes[1,0].plot(pib_df["Hiato"], color = "black", linestyle = "--", label= "Hiato de Produto")
axes[1,0].annotate(f"{pib_df['Hiato'].iloc[-1]:.2f}",
                   xy = (pib_df.index[-1], pib_df["Hiato"].iloc[-1] - 0.5),
                   va = "top", ha = "center", color = "black", fontsize = 6)
axes[1,0].annotate(f"PIB QoQ: {pib_qoq.iloc[-1,0]:.2f}%",
                   xy=(0.8, 0.8), xycoords = "axes fraction",
                   ha="left", va="bottom", color="blue", fontsize=6)
axes[1,0].annotate(f"PIB YoY: {pib_yoy.iloc[-1,0]:.2f}%",
                   xy=(0.8, 0.75), xycoords = "axes fraction",
                   ha="left", va="bottom", color="blue", fontsize=6)
axes[1,0].legend(fontsize = 6)
axes[1,0].set_title("PIB Trimestral", loc="left", fontsize = 8)
# Gráfico 4 -
colors = np.where(ibcbr_var.iloc[:,0] < 0, "darkgray", "black")
colors_bar = np.where(ibcbr_var.iloc[-1,0] < 0, "red", "blue").item()
axes[1,1].bar(x=ibcbr_var.index, height=ibcbr_var.iloc[:,-1],width=15, color=colors, label="IBC-BR mensal")
axes[1,1].plot(ibcbr_norm, color="black", label="Índice IBC-BR", linestyle="-")
axes[1,1].plot(industria_norm, color="darkblue", label="Indústria", linestyle="--")
axes[1,1].plot(agropecuaria_norm, color="green", label="Agropecuária", linestyle="--")
axes[1,1].plot(servicos_norm, color="purple", label="Serviços", linestyle="--")
axes[1,1].annotate(f"{ibcbr_norm.iloc[-1,0]:.2f}%",
                   xy=(ibcbr_norm.index[-1], ibcbr_norm.iloc[-1,0] - 0.5),
                   ha="left", va="bottom", color="black", fontsize=5)
axes[1,1].annotate(f"{industria_norm.iloc[-1,0]:.2f}%",
                   xy=(industria_norm.index[-1], industria_norm.iloc[-1,0] - 0.5),
                   ha="left", va="bottom", color="darkblue", fontsize=5)
axes[1,1].annotate(f"{agropecuaria_norm.iloc[-1,0]:.2f}%",
                   xy=(agropecuaria_norm.index[-1], agropecuaria_norm.iloc[-1,0] - 0.6),
                   ha="left", va="bottom", color="green", fontsize=5)
axes[1,1].annotate(f"{servicos_norm.iloc[-1,0]:.2f}%",
                   xy=(servicos_norm.index[-1], servicos_norm.iloc[-1,0] + 0.05),
                   ha="left", va="bottom", color="purple", fontsize=5)
axes[1,1].annotate(f"{ibcbr_var.iloc[-1,0]:.2f}%",
                   xy=(ibcbr_var.index[-1], ibcbr_var.iloc[-1,0] - 0.35),
                   ha="left", va="bottom", color=colors_bar, fontsize=5)
axes[1,1].legend(fontsize=6)
axes[1,1].tick_params(axis="x", labelsize=6)  # ajuste o número
axes[1,1].set_title("IBC-BR e Setores", fontsize=8, loc="left")
# Ajustes finais do gráfico
plt.tight_layout(pad=2.0)
fig.suptitle("Indicadores Econômicos - BR", fontsize=12, loc="right")
plt.annotate("Fonte: IBGE / Banco Central do Brasil (BCB)", xy=(0.06,0.0),
             va="bottom", ha="left", xycoords="figure fraction",
             color="black", fontsize=10)
plt.annotate("Elaborado por: Fabricio Orlandin, CFP®", xy=(0.84,0.0),
             va="bottom", ha="right", xycoords="figure fraction",
             color="black", fontsize=10)
plt.show()
# %%
