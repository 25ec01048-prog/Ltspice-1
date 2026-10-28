
import matplotlib.pyplot as plt
import pandas as pd

# Gate-source voltages
vgs_spice = ["vgs=300m", "vgs=600m", "vgs=900m", "vgs=1.5"]

# Column names
vds_col = "Vd"
id_col = "Id(M1)"

# Plot
fig, ax = plt.subplots(figsize=(9, 6))

for spice_name in vgs_spice:

    # Load SPICE data
    df_spice = pd.read_csv(spice_name + ".txt", sep="\t")
    df_spice = df_spice.sort_values(by=vds_col)

    ax.plot(
        df_spice[vds_col],
        df_spice[id_col],
        linestyle="-",
        label=f"$V_{{GS}}$ = {spice_name.split('=')[-1]} V"
    )

# Formatting
ax.set_xlabel(r"$V_{DS}$ (V)")
ax.set_ylabel(r"$I_D$ (A)")
ax.set_title("Output Characteristics of MOSFET")

ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(fontsize=9)

fig.tight_layout()
fig.savefig("s3.png", dpi=600, bbox_inches="tight")
plt.show()
