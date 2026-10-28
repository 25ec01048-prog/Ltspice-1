import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from PyLTSpice import RawRead



raw_data = RawRead('idvg.raw')

# Get time axis and specific trace data (e.g., V(out))
v = raw_data.get_trace('V(v_g)')
i = raw_data.get_trace('Id(M1)')
# Export to CSV or text file using numpy
export_data = np.column_stack((v, i))
np.savetxt('idvg.txt', export_data, delimiter='\t', header='vg\tId(M1)', comments='')

df_spice = pd.read_csv('idvg.txt', delimiter="\t")
print(df_spice.head())


print("-----Threshold Voltage-----")

# fig , ax = plt.subplots(1, 2, figsize=(11,6))
v_t = np.array([])

# *** Spice ****
x_label = "vg"
y_label = "Id(M1)"
df_v = df_spice.sort_values(by=(x_label))
y = plt.plot(df_v[x_label], df_v[y_label], label="SPICE")
gm = np.gradient( df_v[y_label],df_v[x_label],) # numerical derivative
highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing    
coef = np.polyfit(df_v[x_label][highslope_gm], df_v[y_label][highslope_gm], 1)
v_t_t_s = -coef[1]/coef[0] # threshold voltage from linear extrapolation
polynomial = np.poly1d(coef)
x_extended = np.linspace(v_t_t_s, 1.5, 100)
y_extrapolated = polynomial(x_extended)
plt.plot(x_extended, y_extrapolated, linestyle='--', label=f'$V_{{th}}$ = ({v_t_t_s:.2f} V)', color=y[0].get_color())
print(v_t_t_s)
# **** TCAD ***
df = pd.read_csv('q5.csv')
v = "V_D=0.4"
df_v = df.sort_values(by=(v+" X"))
np.savetxt('idvg_tcad.txt', df_v[[v+ " X",v+" Y"]], delimiter='\t', header="vg\tId(M1)", comments='')

y = plt.plot(df_v[v+" X"], df_v[v+" Y"], label="TCAD")
gm = np.gradient( df_v[v+" Y"],df_v[v+" X"],) # numerical derivative
    
highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
    
coef = np.polyfit(df_v[v+ " X"][highslope_gm], df_v[v+" Y"][highslope_gm], 1)
v_t_t = -coef[1]/coef[0] 
polynomial = np.poly1d(coef)
x_extended = np.linspace(v_t_t, 1.5, 100)
y_extrapolated = polynomial(x_extended)
plt.plot(x_extended, y_extrapolated, linestyle='--', label=f'$V_{{th}}$ = ({v_t_t:.2f} V)', color=y[0].get_color())

print(v_t_t)

# plt.semilogy()
plt.xlabel(f'$V_{{GS}}$ V')
plt.ylabel(f'$I_{{D}}$ A')
plt.title(f'$I_{{D}}$ A - $V_{{GS}}$ V')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()





print("-----Subthreshold -----")
df_v = df_spice.sort_values(by=(x_label))
df_v = df_v[df_v[x_label]< v_t_t_s]

y_log = df_v[y_label].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values

gm = np.gradient(df_v[x_label],y_log) # numerical derivative
    
print(gm.min()*1000)

plt.tight_layout()
plt.savefig('s6_idvg.png', dpi=600)
