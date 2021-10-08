import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib import *
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.font_manager import FontProperties
from matplotlib import gridspec
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def bull_call_spread(MEP,LST,HST,Premium_Paid,Premium_Received):
#------------------------------------
    Net_debt = Premium_Paid - Premium_Received
#------------------------------------
    LSIV = np.where(MEP > LST, MEP - LST, 0)

# PREMIUM PAID
    PP = [-Premium_Paid]*len(MEP)
    PP1 = [Premium_Paid]*len(MEP)

# LOWER STRIKE - PAY OFF
    LSPO = LSIV-PP1 

# Higher STRIKE - Intrinsic Value
    HSIV = np.where(MEP > HST, MEP-HST, 0)
    PR = [Premium_Received ]*len(MEP)

# HS - Pay off
    HSPO = PR-HSIV 

# STRATEGY PAY OFF
    SGPO = LSPO + HSPO

# Break Even
    BE = LST+Net_debt
# Maximum Profit
    Max_Profit = HST-LST-Net_debt 
    
    d = dict(A=MEP, B=LSIV, C=PP, D=LSPO, E=HSIV, F=PR, G=HSPO, H = SGPO)
    df = pd.DataFrame(dict([ (pd.Series(k)) for k in d.items() ]))
    df.columns = ["Market Expiry","LS-IV", "PP", "LS Payoff", "HS-IV", "PR","HS Payoff", "Strategy Pay off"] 
    
    print("Break even (Rs) =", BE)
    print("\nMaximum Profit (Rs) =",Max_Profit )
    print("\nMaximum Loss (Rs) =", Net_debt)
    print("\n============================================================================")
    print("Strategy Report:")
    print("============================================================================")
    print("Market Expectation : Moderately Bullish")
    print("\n1) Strategy makes loss if price goes below ", LST,"Rs, Loss is restricted to", Net_debt,"Rs")
    print("\n2) Break Even (No profit or Loss) when price goes ", BE,"Rs")
    print("\n3) Makes money if price goes above ", BE,"Rs and maximum profit is", Max_Profit,"Rs" )
    print("============================================================================")

    fig, ax = plt.subplots(figsize=(7, 3),dpi=400)
    plt.title('Bull Call Spread Pay Off', fontsize=12)
    plt.xticks(fontsize=10)
    ax.plot(df["Market Expiry"], df["Strategy Pay off"], linestyle='-', color='tab:green', alpha=0.7, linewidth=1.5)
    plt.axhline(0, color='k', linestyle='-',linewidth = 0.5)
    plt.axvline(LST+Net_debt, color='tab:red', linestyle='-',linewidth = 1)
    plt.grid(b=None, which='major', axis='both')
    ax.set_xlabel("Matket Expiry Price (Rs)")
    ax.set_ylabel("Profit/Loss (Rs)")
    xloc = MultipleLocator(50)
    yloc = MultipleLocator(20)
    ax.xaxis.set_minor_locator(xloc)
    ax.yaxis.set_minor_locator(yloc)
    return df
