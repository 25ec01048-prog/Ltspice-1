
import matplotlib.pyplot as plt
import pandas as pd

# Gate-source voltages
vgs_spice = ["vgs=300m", "vgs=600m", "vgs=900m", "vgs=1.5"]
vgs_tcad = ["vg=0.3", "vg=0.6", "vgs=0.9", "vgs=1.5"]

# Load TCAD data
df_tcad = pd.read_csv("q6.csv")

# Column names
vds_col = "Vd"
id_col = "Id(M1)"

# Plot
fig, ax = plt.subplots(figsize=(9, 6))

for spice_name, tcad_name in zip(vgs_spice, vgs_tcad):

    # SPICE data (solid line)
    df_spice = pd.read_csv(spice_name + ".txt", sep="\t")
    df_spice = df_spice.sort_values(by=vds_col)

    line, = ax.plot(
        df_spice[vds_col],
        df_spice[id_col],
        linestyle="-",
        label=f"$V_{{GS}}$ = {spice_name.split('=')[-1]} V (SPICE)"
    )

    # TCAD data (dashed line)
    vds_tcad_col = f"{tcad_name} X"
    id_tcad_col = f"{tcad_name} Y"

    df_tcad_sorted = df_tcad.sort_values(by=vds_tcad_col)
    df_tcad_sorted = df_tcad_sorted[df_tcad_sorted[vds_tcad_col] < 2]

    ax.plot(
        df_tcad_sorted[vds_tcad_col],
        df_tcad_sorted[id_tcad_col],
        linestyle="--",
        color=line.get_color(),
        label=f"$V_{{GS}}$ = {spice_name.split('=')[-1]} V (TCAD)"
    )

# Formatting
ax.set_xlabel(r"$V_{DS}$ (V)")
ax.set_ylabel(r"$I_D$ (A)")
ax.set_title("Output Characteristics of MOSFET")

ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(fontsize=9, ncol=2)

fig.tight_layout()
fig.savefig("s3.png", dpi=600, bbox_inches="tight")
