import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_spice = pd.read_csv('idvg.txt', delimiter="\t")


print("-----Threshold Voltage-----")

fig , ax = plt.subplots(1, 2, figsize=(11,6))
v_t = np.array([])

# *** Spice ****
x_label = "vg"
y_label = "Id(M1)"
df_v = df_spice.sort_values(by=(x_label))
y = ax[0].plot(df_v[x_label], df_v[y_label], label="SPICE")
gm = np.gradient( df_v[y_label],df_v[x_label],) # numerical derivative
highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing    
coef = np.polyfit(df_v[x_label][highslope_gm], df_v[y_label][highslope_gm], 1)
v_t_t = -coef[1]/coef[0] # threshold voltage from linear extrapolation
polynomial = np.poly1d(coef)
x_extended = np.linspace(0, 3, 100)
y_extrapolated = polynomial(x_extended)
ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f'$V_{{th}}$ = ({v_t_t:.2f} V)', color=y[0].get_color())

# **** TCAD ***
df = pd.read_csv('q5.csv')
v = "V_D=0.4"
df_v = df.sort_values(by=(v+" X"))
y = ax[0].plot(df_v[v+" X"], df_v[v+" Y"], label="TCAD")
gm = np.gradient( df_v[v+" Y"],df_v[v+" X"],) # numerical derivative
    
highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
    
coef = np.polyfit(df_v[v+ " X"][highslope_gm], df_v[v+" Y"][highslope_gm], 1)
v_t_t = -coef[1]/coef[0] 
polynomial = np.poly1d(coef)
x_extended = np.linspace(0, 1.5, 100)
y_extrapolated = polynomial(x_extended)
ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f'$V_{{th}}$ = ({v_t_t:.2f} V)', color=y[0].get_color())




ax[0].set_xlabel(f'$V_{{GS}}$ V')
ax[0].set_ylabel(f'$I_{{D}}$ A')
ax[0].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V')
ax[0].grid(True, linestyle='--', alpha=0.6)
ax[0].legend()





print("-----Subthreshold -----")
## subthrehold loagrathmic graph
ax2 = ax[1].twinx()  # Create a secondary y-axis for the logarithmic plot

df_v = df_spice.sort_values(by=(x_label))
y_log = df_v[y_label].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
y = ax[1].plot(df_v[x_label], df_v[y_label], label="SPICE")
gm = np.gradient(y_log,df_v[x_label]) # numerical derivative
    
   
highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
    
coef = np.polyfit(df_v[x_label][highslope_gm],y_log[highslope_gm], 1)
print(coef)
v_t_t = 1/coef[0] *1000 # subthreshold voltage from linear extrapolation
polynomial = np.poly1d(coef)
x=df_v[x_label][(highslope_gm[0])-5:(highslope_gm[-1])+10]
y2 = 10**polynomial(x)
ax[1].plot(x, y2, linestyle='--', label=f'SS = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
polynomial = np.poly1d(coef)




ax[1].set_yscale('log')  # Set the y-axis to logarithmic scale

ax[1].set_xlabel(f'$V_{{GS}}$ V')
ax[1].set_ylabel(f'$I_{{D}}$ A')
ax[1].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V Characteristics (LOG SCALE)')
ax[1].grid(True, linestyle='--', alpha=0.6)
ax[1].legend()
plt.tight_layout()
plt.savefig('s5.png', dpi=600)
