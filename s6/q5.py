import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('q5.csv')
print("-----Threshold Voltage-----")
vds = ["V_D=0.4"]
fig , ax = plt.subplots(1, 2, figsize=(11,6))
v_t = np.array([])
for i,v in enumerate(vds):
    df_v = df.sort_values(by=(v+" X"))
    y = ax[0].plot(df_v[v+" X"], df_v[v+" Y"], label=v+" (V)")
    gm = np.gradient( df_v[v+" Y"],df_v[v+" X"],) # numerical derivative
    
    highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
    
    coef = np.polyfit(df_v[v+ " X"][highslope_gm], df_v[v+" Y"][highslope_gm], 1)
    
    v_t_t = -coef[1]/coef[0] # threshold voltage from linear extrapolation
    ax[0].axvline(x=v_t_t, color=y[0].get_color(), linestyle=':', label=f'Intercept ({v_t_t:.2f} V)')
    print("Threshold voltage:",round(v_t_t,2)," V at vds=", v," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

    # 3. Define an extended X-range for extrapolation (e.g., up to x=10)
    x_extended = np.linspace(0, 3, 100)
    y_extrapolated = polynomial(x_extended)

    # 4. Plot the results
    # plt.scatter(x, y, color='blue', label='Original Data')
    ax[0].plot(x_extended, y_extrapolated, linestyle='--', label='Extrapolated Line', color=y[0].get_color())

# print(v_t)
print(round(v_t.mean(), 2) ,' V is the average threshold voltage')
ax[0].text(0.4, 0.0003, f'$V_{{TH}} = {round(v_t.mean(), 2)} V$', fontsize=10, color='black', ha='center')
ax[0].set_xlabel(f'$V_{{GS}}$ V')
ax[0].set_ylabel(f'$I_{{D}}$ A')
ax[0].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V')
ax[0].grid(True, linestyle='--', alpha=0.6)
ax[0].legend()
print("-----Subthreshold -----")
## subthrehold loagrathmic graph
ax2 = ax[1].twinx()  # Create a secondary y-axis for the logarithmic plot
v_t = np.array([])
for i,v in enumerate(vds):
    df_v = df.sort_values(by=(v+" X"))
    y_log = df_v[v+" Y"].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
    y = ax[1].plot(df_v[v+" X"], df_v[v+" Y"], label=v+" (V)")
    gm = np.gradient(y_log,df_v[v+" X"]) # numerical derivative
    
    # highslope_gm = (df_v[v+ " X"] >= 0.2) & (df_v[v+ " X"] <= 0.5) 
    highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
    
    coef = np.polyfit(df_v[v+ " X"][highslope_gm],y_log[highslope_gm], 1)
    print(coef)
    v_t_t = 1/coef[0] *1000 # subthreshold voltage from linear extrapolation
    polynomial = np.poly1d(coef)
    x=df_v[v+ " X"][(highslope_gm[0])-5:(highslope_gm[-1])+10]
    y2 = 10**polynomial(x)
    ax[1].plot(x, y2, linestyle='--', label=f'Subthreshold Voltage = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
    print("subthreshold voltage:",round(v_t_t,2)," mV/decade at vds=", v," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

ax[1].set_yscale('log')  # Set the y-axis to logarithmic scale

print(round(v_t.mean(), 2) ,' mV/decade is the average subthreshold voltage')
ax[1].text(1.5, 0.0005, f' Avg Subthreshold Voltage: ${round(v_t.mean(), 2)} mV/decade$', fontsize=10, color='black', ha='center')
ax[1].set_xlabel(f'$V_{{GS}}$ V')
ax[1].set_ylabel(f'$I_{{D}}$ A')
ax[1].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V Characteristics (LOG SCALE)')
ax[1].grid(True, linestyle='--', alpha=0.6)
ax[1].legend()
plt.tight_layout()
plt.savefig('q5_ltspice.png', dpi=600)
