
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Gate-source voltages
vgs = ["vgs=300m", "vgs=600m", "vgs=900m", "vgs=1.5"]

x_label = "Vd"
y_label = "Id(M1)"

# Saturation-region boundary
vsat = 1.5 - 0.33  # 1.17 V

# Figure
fig, ax = plt.subplots(figsize=(10, 7))

for ind, spice_name in enumerate(vgs):

    # ---------- SPICE data ----------
    df_spice = pd.read_csv(spice_name + ".txt", sep="\t")
    df_spice = df_spice.sort_values(by=x_label)

    vds_spice = df_spice[x_label].to_numpy()
    id_spice = df_spice[y_label].to_numpy()

    # Output conductance
    gd_spice = np.gradient(id_spice, vds_spice)

    # Plot SPICE data
    ax.plot(
        vds_spice,
        gd_spice,
        linestyle="-",
        label=f"$V_{{GS}}$ = {spice_name.split('=')[-1]} V"
    )

    # ---------- Output resistance at highest VGS ----------
    if ind == len(vgs) - 1:

        sat_spice = vds_spice >= vsat

        if np.any(sat_spice):

            gd_spice_sat = np.mean(gd_spice[sat_spice])

            ro_spice = (
                1 / gd_spice_sat
                if gd_spice_sat != 0 else np.inf
            )

            # Assumes current is normalized per μm of device width
            ro_spice_kohm_um = ro_spice / 1000

            print("\nOutput resistance at VGS = 1.5 V")
            print(f"Saturation region: VDS >= {vsat:.2f} V")
            print(
                f"SPICE: ro = {ro_spice_kohm_um:.4f} kΩ·μm"
            )
            print(
                f"SPICE: gd = {gd_spice_sat * 1e6:.4f} μS/μm"
            )

            # Display resistance values on plot
            ro_text = (
                r"$V_{GS}=1.5\,\mathrm{V}$" "\n"
                f"$V_{{DS}}\\geq {vsat:.2f}\\,\\mathrm{{V}}$"
                "\n\n"
                f"SPICE: $r_o$ = {ro_spice_kohm_um:.2f} "
                r"$\mathrm{k}\Omega\cdot\mu\mathrm{m}$" "\n"
                f"SPICE: $g_d$ = {gd_spice_sat * 1e6:.2f} "
                r"$\frac{\mu\mathrm{S}}{\mu\mathrm{m}}$"
            )

            ax.text(
                0.04, 0.96,
                ro_text,
                transform=ax.transAxes,
                fontsize=10,
                va="top",
                ha="left",
                bbox=dict(
                    boxstyle="round,pad=0.5",
                    facecolor="white",
                    edgecolor="gray",
                    alpha=0.9
                )
            )

# ---------- Plot formatting ----------
ax.set_xlabel(r"$V_{DS}$ (V)", fontsize=12)
ax.set_ylabel(
    r"$g_d = \frac{dI_D}{dV_{DS}}$ (S)",
    fontsize=12
)
ax.set_title("Output Conductance vs Drain-to-Source Voltage")

ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(fontsize=9)

fig.tight_layout()

# Save figure
fig.savefig("gd_vs_vds.png", dpi=600, bbox_inches="tight")
plt.show()
