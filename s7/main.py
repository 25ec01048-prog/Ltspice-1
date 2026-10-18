import matplotlib.pyplot as plt
import pandas as pd
import numpy  as np

df = pd.read_csv("circuit.txt", delimiter="\t")

plt.plot(df["V2"], df["V(vout)"])

plt.xlabel("$V_{in}$")
plt.ylabel("$V_{out}$")
plt.title("CMOS Inverter $V_{out}$ vs $V_{in}$")
plt.grid(True, linestyle='--', alpha=0.6) 
plt.tight_layout()
plt.savefig("cmosinverter.png", dpi=600)