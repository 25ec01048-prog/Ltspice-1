import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parameters = ['VTH0', 'TOXE', 'L(drawn)','XL','LINT','W(drawn)','WINT', 'NDEP','NSD', 'XJ', 'NGATE', 'U0', 'VSAT', 'RDSW']
for i, param  in enumerate(parameters):
    i = i+1
    df = pd.read_csv('idvg_'+str(i)+'.txt', delimiter="\t")
    print("-----Threshold Voltage-----")
    x_label = "vg"
    y_labels = ["Id(high)", "Id(low)", "Id(normal)"]
    fig , ax = plt.subplots(1, 3, figsize=(15,6))
    v_t = np.array([])
    for y_label in y_labels:
        df_v = df.sort_values(by=(x_label))
        y = ax[0].plot(df_v[x_label], df_v[y_label], label=y_label)
        
        ax[0].axvline(x=df_v[x_label][0], color=y[0].get_color(), linestyle=':', label=f'$I_{{Doff}}$ = {df[y_label][0]:.2e} A')
        ax[0].axvline(x=df_v.iloc[-1][x_label], color=y[0].get_color(), linestyle=':', label=f'$I_{{Don}}$ = {df_v.iloc[-11][y_label]:.2e} A')
        
        gm = np.gradient( df_v[y_label],df_v[x_label],) # numerical derivative
            
        highslope_gm = np.where(gm > 0.9 * gm.max())[0] # index of the last zero crossing
            
        coef = np.polyfit(df_v[x_label][highslope_gm], df_v[y_label][highslope_gm], 1)
            
        v_t_t = -coef[1]/coef[0] # threshold voltage from linear extrapolation
        #ax[0].axvline(x=v_t_t, color=y[0].get_color(), linestyle=':', label=f'Intercept ({v_t_t:.2f} V)')
        print("Threshold voltage:",round(v_t_t,2),y_label)
        v_t = np.append(v_t, v_t_t)
        polynomial = np.poly1d(coef)

            # 3. Define an extended X-range for extrapolation (e.g., up to x=10)
        x_extended = np.linspace(0, 1.2, 100)
        y_extrapolated = polynomial(x_extended)

            # 4. Plot the results
            # plt.scatter(x, y, color='blue', label='Original Data')
        ax[0].plot(x_extended, y_extrapolated, linestyle='--', label=f'X-Intercept ({v_t_t:.2f} V)', color=y[0].get_color())

    # print(v_t)
    ax[0].set_ylim(-0.0001)
    # print(round(v_t.mean(), 2) ,' V is the average threshold voltage')
    # ax[0].text(0.4, 0.0003, f'$V_{{TH}} = {round(v_t.mean(), 2)} V$', fontsize=10, color='black', ha='center'
    ax[0].set_xlabel(f'$V_{{GS}}$ V')
    ax[0].set_ylabel(f'$I_{{D}}$ A')
    ax[0].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V')
    ax[0].grid(True, linestyle='--', alpha=0.6)
    ax[0].legend()
    print("-----Subthreshold -----")
    ## subthrehold loagrathmic graph
    ax2 = ax[1].twinx()  # Create a secondary y-axis for the logarithmic plot
    v_t = np.array([])
    for y_label in y_labels:
        df_v = df.sort_values(by=(x_label))
        y_log = df_v[y_label].apply(lambda x: np.log10(x) if x > 0 else np.nan) # Apply log10 to Y values, handling non-positive values
        y = ax[1].plot(df_v[x_label], df_v[y_label], label=y_label+" (V)")
        gm = np.gradient(y_log,df_v[x_label]) # numerical derivative
            
            # highslope_gm = (df_v[x_label] >= 0.2) & (df_v[x_label] <= 0.5) 
        highslope_gm = np.where(gm > 0.9 * gm.max())[0]# index 
            
        coef = np.polyfit(df_v[x_label][highslope_gm],y_log[highslope_gm], 1)
        print(coef)
        v_t_t = 1/coef[0] *1000 # subthreshold voltage from linear extrapolation
        polynomial = np.poly1d(coef)
        x=df_v[x_label][(highslope_gm[0])-5:(highslope_gm[-1])+10]
        y2 = 10**polynomial(x)
        ax[1].plot(x, y2, linestyle='--', label=f'SS = {round(v_t_t,2)} mV/decade', color=y[0].get_color())
        print("subthreshold voltage:",round(v_t_t,2)," mV/decade at ",y_label )
        v_t = np.append(v_t, v_t_t)
        polynomial = np.poly1d(coef)

    ax[1].set_yscale('log')  # Set the y-axis to logarithmic scale

    # print(round(v_t.mean(), 2) ,' mV/decade is the average subthreshold voltage')
    #ax[1].text(1.5, 0.0005, f' Avg Subthreshold Voltage: ${round(v_t.mean(), 2)} mV/decade$', fontsize=10, color='black', ha='center')
    ax[1].set_xlabel(f'$V_{{GS}}$ V')
    ax[1].set_ylabel(f'$I_{{D}}$ A')
    ax[1].set_title(f'$I_{{D}}$ A - $V_{{GS}}$ V Characteristics (LOG SCALE)')
    ax[1].grid(True, linestyle='--', alpha=0.6)
    ax[1].legend()

    df = pd.read_csv('idvd_'+str(i)+'.txt', delimiter="\t")
    x_label = "vd"
    for y_label in y_labels:
        y = ax[2].plot(df[x_label], df[y_label], label=y_label)
        
    # df_v = pd.read_csv('vgs=1.5.txt',sep="\t")

    # x_ind = np.where(df_v[x_label] > vsat)[0][0] # index of the last zero crossing
    # gd = np.gradient( df_v[y_label][x_ind:],df_v[x_label][x_ind:]).mean() # numerical derivative
    # ro = (1/gd)/1000
    # print(gd, ro)
    #f'$g_d = {round(gd, 2)} S r_{{o}} = {round(ro, 2)} k\\Omega\\mu m $',
    #ax[3].text(0.5, 0.0003, f'$g_d = {round(gd*1000, 2)}mS/\\mu m $\n $r_{{o}} = {round(ro, 2)} k\\Omega\\mu m$ ', fontsize=10, color='black', ha='center')
    ax[2].set_xlabel(f'$V_{{DS}}$ V')
    ax[2].set_ylabel(f'$I_{{D}}$ A')
    ax[2].set_title(f'$I_d-V_{{ds}}$ Output Characteristics of MOSFET')
    ax[2].grid(True, linestyle='--', alpha=0.6) 
    ax[2].legend()
    fig.suptitle("Parameter - "+ param)
    plt.tight_layout()
    plt.savefig(param+'.png', dpi=600)
