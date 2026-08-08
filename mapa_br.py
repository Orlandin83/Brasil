#%% importações
from bcb import sgs
import pandas as pd
import numpy as np
import datetime as dt
from statsmodels.tsa.filters.hp_filter import hpfilter
import matplotlib.pyplot as plt
import sidrapy as sdr
#%% IPCA
start = "2023-01-01"
end = dt.datetime.today()
ipca_m = sgs.get(433, start, end)
ipca_12m = sgs.get(13522, start, end)
ipca_12m = ipca_12m.rename(columns={"13522": "IPCA 12m"})
nucleos = [11427, 16121, 27838, 27839, 11426, 4466, 16122, 28751, 28750]
ipca_nucleo = sgs.get(nucleos, start, end)
ipca_nucleo["Média"] = ipca_nucleo.mean(axis=1)
ipca_nucleo = ipca_nucleo["Média"]
ipca_nucleo_12m = ipca_nucleo.rolling(window=12).apply(lambda x:(np.prod(1 + x /100) - 1)* 100)
ipca_12m = pd.concat([ipca_12m, ipca_nucleo_12m], axis = 1).dropna()
ipca_m = ipca_m.loc[ipca_12m.index]
#%% SELIC
selic0 = sgs.get(432, "2010-01-01", "2016-12-31")
selic1 = sgs.get(432, "2017-01-01", dt.datetime.today())
selic = pd.concat([selic0, selic1])
selic = selic.rename(columns={"432":"Selic"})
#%% DESEMPREGO
desemprego = sgs.get(24369,"2009-02-01", dt.datetime.today())
desemprego = desemprego.rename(columns={"24380": "Desemprego (%) "})
media_desemprego_12m = desemprego.rolling(window=12).mean().dropna()
media_desemprego_12m = pd.DataFrame(media_desemprego_12m)
desemprego = desemprego.reindex(media_desemprego_12m.index)
media_desemprego_12m = media_desemprego_12m.astype(float).round(2)
#%% PIB
pib_qoq = sdr.get_table(
    table_code="5932",          # tabela 5932 - PIB Trimestral
    territorial_level="1",      # N1 = Brasil
    ibge_territorial_code="1",  # código 1 = Brasil
    variable="6564",            # taxa trimestre contra trimestre imediatamente anterior (%)
    period="201001 - 202601",     # toda a faixa de trimestres listada em /P/
    classifications={"11255": "90707"},    # código da classificação "Setores e subsetores"         # categoria 90707 = PIB a preços de mercado
)
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
pib_yoy = sdr.get_table(
    table_code="5932",
    territorial_level="1",
    ibge_territorial_code="1",
    variable="6561",
    period="201001-202601",
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
#%% Gráfico 1 Selic
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(16,10))
axes[0,0].plot(selic, color="darkblue", label="Taxa Selic", alpha=0.7)
axes[0,0].annotate(f"{selic.iloc[-1,0]}%",
                   xy=(selic.index[-1], selic.iloc[-1,0] - 1),
                   ha="left",
                   va="bottom",
                   color="white",
                   fontsize=8,
                   bbox=dict(
                       fc="darkblue",
                       ec="none",
                       linewidth=0.3,
                       alpha=0.7,
                       boxstyle="round,pad=0.2"
                    ))
axes[0,0].legend(fontsize=6)
axes[0,0].set_title("Taxa Selic",
                    loc="left",
                    fontweight="bold",
                    fontsize=14,
                    color="darkblue")
# Gráfico 2 - Desemprego
axes[0,1].bar(desemprego.index, height=desemprego.iloc[:,0], width=40,
               color="lightblue", label="Taxa de Desemprego", alpha=0.7)
axes[0,1].plot(media_desemprego_12m, color = "darkblue", label="Média Desemprego 12m", linestyle="--", alpha=0.7)
axes[0,1].annotate(f"{desemprego.iloc[-1,0]}%",
                    xy=(desemprego.index[-1], desemprego.iloc[-1,0]),
                    ha="left", va="bottom",
                    color="darkblue", fontsize=8,
                    bbox=dict(fc="lightblue",
                              ec="lightblue",linewidth=0.3,
                              alpha=0.7,
                              boxstyle="round,pad=0.2")
)
axes[0,1].annotate(f"{media_desemprego_12m.iloc[-1, 0]:.1f}%",
                    xy=(media_desemprego_12m.index[-1], media_desemprego_12m.iloc[-1,0]),
                    ha="left", va="top",
                    color="white", fontsize=8,
                    bbox=dict(fc="darkblue",
                           ec="darkblue",linewidth=0.3,
                           alpha=0.7,
                           boxstyle="round,pad=0.2")
)
axes[0,1].legend (fontsize=6)
axes[0,1].set_title("Taxa de Desemprego",
                    loc="left",
                    fontweight="bold",
                    fontsize=14,
                    color="darkblue")
#Gráfico 3 - Inflação
bar_ax1 = axes[1,0].bar(
    x=ipca_m.index,
    height=ipca_m["433"],
    width=15,
    color= "lightblue",
)
destaque = [-1, -2, -13]
for b in destaque:
    bar_ax1[b].set_color("darkblue")
    bar_ax1[b].set_alpha(0.7)
for a in destaque:
    axes[1,0].annotate(f"{ipca_m["433"].iloc[a]}%",
                 xy = (ipca_m.index[a], ipca_m["433"].iloc[a]),
                 va="bottom",
                 ha="center",
                 fontsize=8,
                 rotation=90,
                 color="darkblue",
                 bbox=dict(fc="white",
                           ec="darkblue",linewidth=0.3,
                           alpha=0.7,
                           boxstyle="round,pad=0.2")
)
axes[1,0].plot(ipca_12m["IPCA 12m"],
         label="IPCA 12m",
         alpha=0.7,
         color="darkblue",
         linestyle="-"
         )
axes[1,0].plot(ipca_12m["Média"],
         label="Média dos Núcleos",
         alpha=0.7,
         color="lightblue",
         linestyle="--"
         )
axes[1,0].annotate(
    f"{ipca_12m["IPCA 12m"].iloc[-1]:.2f}%",
    xy=(ipca_12m.index[-1], ipca_12m["IPCA 12m"].iloc[-1]),
    va="center",
    ha="left",
    fontsize=8,
    color="white",
    bbox=dict(
        fc="darkblue",
        ec="white",
        linewidth=0.3,
        alpha=0.7,
        boxstyle="round,pad=0.2"
        )
)
axes[1,0].annotate(
    f"{ipca_12m["Média"].iloc[-1]:.2f}%",
    xy=(ipca_12m.index[-1], ipca_12m["Média"].iloc[-1]),
    va="center",
    ha="left",
    fontsize=8,
    color="darkblue",
    bbox=dict(
        fc="lightblue",
        ec="white",
        linewidth=0.3,
        alpha=0.7,
        boxstyle="round,pad=0.2"
        )
)
axes[1,0].legend(fontsize=6)
axes[1,0].set_title("IPCA 12m e Média Núcleos",
              loc="left",
              fontweight="bold",
              fontsize=14,
              color="darkblue")
axes[1,0].axhline(y=4.5, color="black", linestyle="--")
axes[1,0].axhline(y=3, color="black", linestyle="--")
axes[1,0].axhline(y=1.5, color="black", linestyle="--")
axes[1,0].annotate("Teto: 4,5%",
             xy=(ipca_12m.index[0], 4.4),
             va="top", ha="left",
             fontsize=6,
             color="black")
axes[1,0].annotate("Meta: 3%",
             xy=(ipca_12m.index[0], 2.9),
             va="top", ha="left",
             fontsize=6,
             color="black")
axes[1,0].annotate("Piso: 1,5%",
             xy=(ipca_12m.index[0], 1.4),
             va="top", ha="left",
             fontsize=6,
             color="black")
axes[1,0].tick_params(axis="x", rotation=45)
# Gráfico 4 - PIB
colors = np.where(pib_qoq.iloc[:,0] < 0, "lightblue", "darkblue")
axes[1,1].bar(x=pib_qoq.index, height = pib_qoq.iloc[:,0], width = 60,
              color=colors, label="PIB Trimestral QoQ", alpha=0.7)
axes[1,1].plot(pib_df["Hiato"], color = "black", linestyle = "--", label= "Hiato de Produto")
axes[1,1].annotate(f"Hiato: {pib_df['Hiato'].iloc[-1]:.2f}",
                   xy = (pib_df.index[-1], pib_df["Hiato"].iloc[-1] - 0.5),
                   va = "top",
                   ha = "center",
                   color = "black",
                   fontsize = 8,
                   bbox=dict(
                       fc="lightblue",
                       ec="none",
                       linewidth=0.3,
                       alpha=0.7,
                       boxstyle="round,pad=0.2"
                   ))
axes[1,1].annotate(f"1T2026 QoQ: {pib_qoq.iloc[-1,0]:.2f}%",
                   xy=(0.05, 0.8),
                   xycoords = "axes fraction",
                   ha="left",
                   va="bottom",
                   color="white",
                   fontsize=8,
                   bbox=dict(
                       fc="darkblue",
                       ec="none",
                       linewidth=0.3,
                       alpha=0.7,
                       boxstyle="round,pad=0.2"
                   ))
axes[1,1].annotate(f"1T2026 YoY: {pib_yoy.iloc[-1,0]:.2f}%",
                   xy=(0.05, 0.75),
                   xycoords = "axes fraction",
                   ha="left",
                   va="bottom",
                   color="white",
                   fontsize=8,
                   bbox=dict(
                       fc="darkblue",
                       ec="none",
                       linewidth=0.3,
                       alpha=0.7,
                       boxstyle="round,pad=0.2"
                   ))
axes[1,1].legend(fontsize=6)
axes[1,1].set_title("PIB Trimestral",
                    loc="left",
                    fontweight="bold",
                    fontsize=14,
                    color="darkblue")
# Ajustes finais do gráfico
plt.tight_layout(pad=2.0)
plt.annotate("Fonte: IBGE / Banco Central do Brasil (BCB)", xy=(0.02,0.0),
             va="bottom", ha="left", xycoords="figure fraction",
             color="black", fontsize=10)
plt.annotate("Elaborado por: Fabricio Orlandin, CFP®", xy=(0.95,0.0),
             va="bottom", ha="right", xycoords="figure fraction",
             color="black", fontsize=10)
plt.show()
# %%
