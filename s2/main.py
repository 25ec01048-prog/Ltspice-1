import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dfs = [['$V_d$ = 0.05','v_d=50mv.txt'], ['$V_d$ = 1.1','v_d=11v.txt']]
# df = pd.read_csv('idvg.txt', delimiter="\t")
print("-----Threshold Voltage-----")
x_label = "vg"
y_label = "Id(M1)"
fig , ax = plt.subplots(1, 2, figsize=(11,6))
v_t = np.array([])
ax2 = ax[0].twinx() 
for i in dfs:
    df = pd.read_csv(i[1], delimiter="\t")
    df_v = df.sort_values(by=(x_label))
    y = ax[0].plot(df_v[x_label], df_v[y_label], label=i[0]+" (V)")
    gm = np.gradient( df_v[y_label],df_v[x_label],) # numerical derivative
    
    ax2.plot(df_v[x_label],gm, linestyle=":", color = y[0].get_color())
    highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
        
    coef = np.polyfit(df_v[x_label][highslope_gm], df_v[y_label][highslope_gm], 1)
    
    v_t_t = -coef[1]/coef[0] # threshold voltage from linear extrapolation
    ax[0].axvline(x=df_v[x_label][0], color=y[0].get_color(), linestyle=':', label=f'$I_{{Doff}}$ = {df[y_label][0]:.2e} A')
    ax[0].axvline(x=df_v.iloc[-1][x_label], color=y[0].get_color(), linestyle=':', label=f'$I_{{Don}}$ = {df_v.iloc[-1][y_label]:.2e} A')
    
    
    print("Threshold voltage:",round(v_t_t,2)," V at vds=", i[0]," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

        # 3. Define an extended X-range for extrapolation (e.g., up to x=10)
    x_extended = np.linspace(0.2, 0.8, 100)
    y_extrapolated = polynomial(x_extended)

        # 4. Plot the results
        # plt.scatter(x, y, color='blue', label='Original Data')
    ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f'$V_{{th}}$ = {v_t_t:.2f} (V)', color=y[0].get_color())

# print(v_t)
# print(round(v_t.mean(), 2) ,' V is the average threshold voltage')
# ax[0].text(0.4, 0.0003, f'$V_{{TH}} = {round(v_t.mean(), 2)} V$', fontsize=10, color='black', ha='center')
ax[0].set_ylim(-0.0001)
ax[0].set_xlabel(f'$V_{{GS}}$ V')
ax[0].set_ylabel(f'$I_{{D}}$ A')
ax[0].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V')
ax[0].grid(True, linestyle='--', alpha=0.6)
ax[0].legend()
print("-----Subthreshold -----")
## subthrehold loagrathmic graph
ax2 = ax[1].twinx()  # Create a secondary y-axis for the logarithmic plot
v_t = np.array([])
for i in dfs:
    df = pd.read_csv(i[1], delimiter="\t")
    df_v = df.sort_values(by=(x_label))
    y_log = df_v[y_label].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
    y = ax[1].plot(df_v[x_label], df_v[y_label], label=i[0]+" (V)")
    gm = np.gradient(y_log,df_v[x_label]) # numerical derivative
        
        # highslope_gm = (df_v[x_label] >= 0.2) & (df_v[x_label] <= 0.5) 
    highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
        
    coef = np.polyfit(df_v[x_label][highslope_gm],y_log[highslope_gm], 1)
    print(coef)
    v_t_t = 1/coef[0] *1000 # subthreshold voltage from linear extrapolation
    polynomial = np.poly1d(coef)
    x=df_v[x_label][(highslope_gm[0])-15:(highslope_gm[-1])+20]
    y2 = 10**polynomial(x)
    ax[1].plot(x, y2, linestyle='--', label=f'Subthreshold Voltage = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
    print("subthreshold voltage:",round(v_t_t,2)," mV/decade at vds=", i[0]," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

ax[1].set_yscale('log')  # Set the y-axis to logarithmic scale

# print(round(v_t.mean(), 2) ,' mV/decade is the average subthreshold voltage')
# ax[1].text(1.5, 0.0003, f' Avg Subthreshold Voltage: ${round(v_t.mean(), 2)} mV/decade$', fontsize=10, color='black', ha='center')
ax[1].set_xlabel(f'$V_{{GS}}$ V')
ax[1].set_ylabel(f'$I_{{D}}$ A')
ax[1].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V Characteristics (LOG SCALE)')
ax[1].grid(True, linestyle='--', alpha=0.6)
ax[1].legend()
plt.tight_layout()
plt.savefig('s2.png', dpi=600)
