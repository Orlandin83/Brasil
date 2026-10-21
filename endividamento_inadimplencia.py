#%% bibliotecas
from bcb import sgs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime as dt

DATA_INICIAL = "2012-01-01"

#%% Rótulos das barras
def rotular_barras(barras_saldo, barras_inadimplencia, percentuais):
    ax = plt.gca()

    for barras, valores, percentual, cor in (
        (barras_saldo, [barra.get_height() for barra in barras_saldo], False, "darkblue"),
        (barras_inadimplencia, percentuais, True, "blue"),
    ):
        # Exibe o saldo e o percentual em todas as barras.
        for barra, valor in zip(barras, valores):
            if pd.isna(valor) or barra.get_height() <= 0:
                continue
            texto = f"{valor:,.2f}".translate(str.maketrans({",": ".", ".": ","}))
            if percentual:
                texto += "%"
            ax.annotate(
                texto,
                (barra.get_x() + barra.get_width() / 2,
                 barra.get_height()),
                xytext=(0, 3 if percentual else -3),
                textcoords="offset points",
                rotation=90, ha="center", va="bottom" if percentual else "top",
                fontsize=6, color=cor,
            )

#%% Inad PF
cred_pf = (sgs.get(22050, start=DATA_INICIAL, end=dt.datetime.today()) / 1000).astype(float).round(2)
cred_pf = cred_pf.rename(columns={"22050": "Saldo_PF"})
cred_pf["%_Inadimplência"] = sgs.get(21084, start=DATA_INICIAL, end=dt.datetime.today())
cred_pf["Inadimplência"] = (cred_pf["Saldo_PF"] / 100 * cred_pf["%_Inadimplência"]).astype(float).round(2)
cred_pf_bim = cred_pf.loc[cred_pf.index.month % 2 == 0]
print(cred_pf_bim)
#%% Inad PJ
cred_pj = (sgs.get(22047, start=DATA_INICIAL, end=dt.datetime.today()) / 1000).astype(float).round(2)
cred_pj = cred_pj.rename(columns={"22047": "Saldo_PJ"})
cred_pj["%_Inadimplência"] = sgs.get(21083, start=DATA_INICIAL, end=dt.datetime.today())
cred_pj["Inadimplência"] = (cred_pj["Saldo_PJ"] / 100 * cred_pj["%_Inadimplência"]).astype(float).round(2)
cred_pj_bim = cred_pj.loc[cred_pj.index.month % 2 == 0]
print(cred_pj_bim)
#%%grafico pf
plt.figure(figsize=(18,8))
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.tick_params(axis="both", labelsize=10)
plt.subplots_adjust(left=0.045, right=0.99, top=0.95, bottom=0.11)
barras_saldo_pf = plt.bar(cred_pf_bim.index, cred_pf_bim["Saldo_PF"], width=45, label = "Saldo PF", color="lightblue", alpha=0.6)
barras_inad_pf = plt.bar(cred_pf_bim.index, cred_pf_bim["Inadimplência"], width=45, label = "Inadimplência PF", color="blue")
rotular_barras(barras_saldo_pf, barras_inad_pf, cred_pf_bim["%_Inadimplência"])
plt.title("Saldo de Crédito e Inadimplência PF (R$ bilhões)", fontsize=12, loc="left")
plt.legend(loc="upper left", fontsize=12)
plt.annotate("Fonte: Banco Central do Brasil (BCB)", xy=(0.125,0.02),
             va="bottom", ha="left", xycoords="figure fraction",
             color="black", fontsize=10)
plt.annotate("Elaborado por: Fabricio Orlandin, CFP®", xy=(0.98,0.02),
             va="bottom", ha="right", xycoords="figure fraction",
             color="black", fontsize=10)
plt.show()
#%%grafico pj
plt.figure(figsize=(18,8))
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.tick_params(axis="both", labelsize=10)
plt.subplots_adjust(left=0.045, right=0.99, top=0.95, bottom=0.11)
barras_saldo_pj = plt.bar(cred_pj_bim.index, cred_pj_bim["Saldo_PJ"], width=45, label = "Saldo PJ", color="lightblue", alpha=0.6)
barras_inad_pj = plt.bar(cred_pj_bim.index, cred_pj_bim["Inadimplência"], width=45, label = "Inadimplência PJ", color="blue")
rotular_barras(barras_saldo_pj, barras_inad_pj, cred_pj_bim["%_Inadimplência"])
plt.title("Saldo de Crédito e Inadimplência PJ (R$ bilhões)", fontsize=12, loc="left")
plt.legend(loc="upper left", fontsize=12)
plt.annotate("Fonte: Banco Central do Brasil (BCB)", xy=(0.125,0.02),
             va="bottom", ha="left", xycoords="figure fraction",
             color="black", fontsize=10)
plt.annotate("Elaborado por: Fabricio Orlandin, CFP®", xy=(0.98,0.02),
             va="bottom", ha="right", xycoords="figure fraction",
             color="black", fontsize=10)
plt.show()
# %%
