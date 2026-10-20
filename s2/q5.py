import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('q5.csv')
print("-----Threshold Voltage-----")
vds = ["V_D=0.05"]
fig , ax = plt.subplots(1, 2, figsize=(11,6))
v_t = np.array([])
for i,v in enumerate(vds):
    df_v = df.sort_values(by=(v+" X"))
    y = ax[0].plot(df_v[v+" X"], df_v[v+" Y"], label="TCAD")
    gm = np.gradient( df_v[v+" Y"],df_v[v+" X"],) # numerical derivative
    
    highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
    
    coef = np.polyfit(df_v[v+ " X"][highslope_gm], df_v[v+" Y"][highslope_gm], 1)
    
    v_t_t = -coef[1]/coef[0] 
    polynomial = np.poly1d(coef)

    x_extended = np.linspace(0, 1.5, 100)
    y_extrapolated = polynomial(x_extended)
    ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f"$V_{{th}}$ = {round(v_t_t,2)} V", color=y[0].get_color())

dfs = [['$V_d$ = 0.05','v_d=50mv.txt']]

x_label = "vg"
y_label = "Id(M1)"
for i in dfs:
    df2 = pd.read_csv(i[1], delimiter="\t")
    df_v = df2.sort_values(by=(x_label))
    y = ax[0].plot(df_v[x_label], df_v[y_label], label="SPICE")
    gm = np.gradient( df_v[y_label],df_v[x_label],) # numerical derivative
        
    highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
        
    coef = np.polyfit(df_v[x_label][highslope_gm], df_v[y_label][highslope_gm], 1)
        
    v_t_t = -coef[1]/coef[0] # threshold voltage from linear extrapolation
    # ax[0].axvline(x=v_t_t, color=y[0].get_color(), linestyle=':', label=f'Intercept ({v_t_t:.2f} V)')
    
    
    print("Threshold voltage:",round(v_t_t,2)," V at vds=", i[0]," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

        # 3. Define an extended X-range for extrapolation (e.g., up to x=10)
    x_extended = np.linspace(0, 1, 100)
    y_extrapolated = polynomial(x_extended)

        # 4. Plot the results
        # plt.scatter(x, y, color='blue', label='Original Data')
    ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f"$V_{{th}}$ = {round(v_t_t,2)} V", color=y[0].get_color())
ax[0].set_ylim(-0.00005)
ax[0].set_xlabel(f'$V_{{GS}}$ V')
ax[0].set_ylabel(f'$I_{{D}}$ A')
ax[0].set_title(f'$I_{{D}}$ (A) - $V_{{GS}}$ (V) , $V_D$ = 0.05 (V)')
ax[0].grid(True, linestyle='--', alpha=0.6)
ax[0].legend()
print("-----Subthreshold -----")
## subthrehold loagrathmic graph
ax2 = ax[1].twinx()  # Create a secondary y-axis for the logarithmic plot
v_t = np.array([])
for i,v in enumerate(vds):
    df_v = df.sort_values(by=(v+" X"))
    y_log = df_v[v+" Y"].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
    y = ax[1].plot(df_v[v+" X"], df_v[v+" Y"], label="TCAD")
    gm = np.gradient(y_log,df_v[v+" X"]) # numerical derivative
    
    # highslope_gm = (df_v[v+ " X"] >= 0.2) & (df_v[v+ " X"] <= 0.5) 
    highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
    
    coef = np.polyfit(df_v[v+ " X"][highslope_gm],y_log[highslope_gm], 1)
    print(coef)
    v_t_t = 1/coef[0] *1000 # SS from linear extrapolation
    polynomial = np.poly1d(coef)
    x=df_v[v+ " X"][(highslope_gm[0])-5:(highslope_gm[-1])+10]
    y2 = 10**polynomial(x)
    ax[1].plot(x, y2, linestyle='--', label=f'SS = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
    print("SS:",round(v_t_t,2)," mV/decade at vds=", v," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)
    

for i in dfs:
    df = pd.read_csv(i[1], delimiter="\t")
    df_v = df.sort_values(by=(x_label))
    y_log = df_v[y_label].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
    y = ax[1].plot(df_v[x_label], df_v[y_label], label="SPICE")
    gm = np.gradient(y_log,df_v[x_label]) # numerical derivative
        
        # highslope_gm = (df_v[x_label] >= 0.2) & (df_v[x_label] <= 0.5) 
    highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
        
    coef = np.polyfit(df_v[x_label][highslope_gm],y_log[highslope_gm], 1)
    print(coef)
    v_t_t = 1/coef[0] *1000 # SS from linear extrapolation
    polynomial = np.poly1d(coef)
    x=df_v[x_label][(highslope_gm[0])-15:(highslope_gm[-1])+20]
    y2 = 10**polynomial(x)
    ax[1].plot(x, y2, linestyle='--', label=f'SS = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
    print("SS:",round(v_t_t,2)," mV/decade at vds=", i[0]," V")
    v_t = np.append(v_t, v_t_t)
    polynomial = np.poly1d(coef)

ax[1].set_yscale('log')  # Set the y-axis to logarithmic scale

ax[1].set_xlabel(f'$V_{{GS}}$ V')
ax[1].set_ylabel(f'$I_{{D}}$ A')
ax[1].set_title(f'$I_{{D}}$ (A) - $V_{{GS}}$ (V) , $V_D$ = 0.05 (V) (LOG SCALE)')
ax[1].grid(True, linestyle='--', alpha=0.6)
ax[1].legend()
plt.tight_layout()
plt.savefig('s2.png', dpi=600)
