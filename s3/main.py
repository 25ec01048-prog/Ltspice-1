import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


vgs = ["vgs=300m", "vgs=600m","vgs=900m", "vgs=1.5"]
vsat = 1.5-0.33
x_label = 'Vd'
y_label = 'Id(M1)'

for i in vgs:
    
    df = pd.read_csv(i+'.txt', delimiter="\t")
    print(df.columns)
    y = plt.plot(df[x_label], df[y_label], label="V_$g$="+i.split("=")[-1]+" (V)")
    
df_v = pd.read_csv('vgs=1.5.txt',sep="\t")

x_ind = np.where(df_v[x_label] > vsat)[0][0] # index of the last zero crossing
gd = np.gradient( df_v[y_label][x_ind:],df_v[x_label][x_ind:]).mean() # numerical derivative
ro = (1/gd)/1000
print(gd, ro)
#f'$g_d = {round(gd, 2)} S r_{{o}} = {round(ro, 2)} k\\Omega\\mu m $',
plt.text(0.5, 0.0003, f'$g_d = {round(gd*1000, 2)}mS/\\mu m $\n $r_{{o}} = {round(ro, 2)} k\\Omega\\mu m$ ', fontsize=10, color='black', ha='center')
plt.xlabel(f'$V_{{DS}}$ V')
plt.ylabel(f'$I_{{D}}$ A')
plt.legend()
plt.title(f'Output Characteristics of MOSFET')
plt.grid(True, linestyle='--', alpha=0.6) 
plt.legend() 
plt.savefig('s3.png', dpi=600) 
