import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('q6.csv')
vgs = ["vg=0.3", "vg=0.6","vgs=0.9", "vgs=1.5"]
vsat = 1.5-0.33


for i in vgs:
    df_v = df.sort_values(by=(i+" X"))
    y = plt.plot(df_v[i+" X"], df_v[i+" Y"], label=i+" (V)")
    
df_v = df.sort_values(by=(vgs[-1]+" X"))
x_ind = np.where(df_v[vgs[-1]+" X"] > vsat)[0][0] # index of the last zero crossing
gd = np.gradient( df_v[vgs[-1]+" Y"][x_ind:],df_v[vgs[-1]+" X"][x_ind:]).mean() # numerical derivative
ro = (1/gd)/1000
print(gd, ro)
#f'$g_d = {round(gd, 2)} S r_{{o}} = {round(ro, 2)} k\\Omega\\mu m $',
plt.text(0.5, 0.0005, f'$g_d = {round(gd*1000, 2)}mS/\\mu m $\n $r_{{o}} = {round(ro, 2)} k\\Omega\\mu m$ ', fontsize=10, color='black', ha='center')
plt.xlabel(f'$V_{{DS}}$ V')
plt.ylabel(f'$I_{{D}}$ A')
plt.legend()
plt.title(f'Output Characteristics of MOSFET')
plt.grid(True, linestyle='--', alpha=0.6) 
plt.legend() 
plt.savefig('q6.png', dpi=600) 
plt.show()