# LTspice MOSFET Characterisation and CMOS Inverter

**Course:** EC2L104 --- Introduction to EDA Tools\
**Project:** LTspice Exercise Report\
**Technology:** 65 nm PTM MOSFET model card

## Overview

This project uses LTspice to study MOSFET characteristics, investigate
how model parameters affect device performance, compare SPICE results
with TCAD characteristics, and analyse a CMOS inverter. The report is
organised into seven exercises (S1--S7).

## Exercises

### S1 --- Reading the Model Card

-   Extracts model-card parameters such as `XL`, `LINT`, `WINT`, and
    `TOXE`.
-   Calculates effective channel length, effective width, and oxide
    capacitance.
-   Compares drain current for drawn channel lengths of 65 nm and 70 nm.
-   The reported operating-point current decreases from 1.15 mA to 1.05
    mA as channel length increases.

### S2 --- Transfer Characteristics

-   Simulates drain current (`ID`) against gate-source voltage (`VGS`)
    at different drain-source voltages.
-   Extracts threshold voltage, ON current, OFF current, and
    subthreshold swing.
-   Reported values include `VTH ≈ 0.37 V`, `ION ≈ 1.15 mA/µm`, and
    `IOFF ≈ 66.9 nA/µm`.

### S3 --- Output Characteristics

-   Plots `ID–VD` curves for multiple gate-source voltages.
-   Estimates output conductance (`gds`) in the saturation region and
    calculates output resistance (`ro = 1/gds`).
-   Reported at `VGS = 1.5 V`: `gds ≈ 312.16 µS/µm` and
    `ro ≈ 3.20 kΩ·µm`.

### S4 --- Physics Check

-   Examines the effects of setting `UA` and `UB` to zero and increasing
    `VSAT`.
-   Relates these changes to vertical-field mobility degradation and
    high-field velocity saturation.
-   Highlights velocity saturation as a major limitation on ON current
    in a short-channel device.

### S5 --- Parametric Variation

-   Varies 14 model parameters around their nominal values.
-   Tracks changes in threshold voltage (`VTH`), subthreshold swing
    (`SS`), ON current (`ION`), and OFF current (`IOFF`).
-   Parameters studied: `VTH0`, `TOXE`, drawn `L`, `XL`, `LINT`, drawn
    `W`, `WINT`, `NDEP`, `NSD`, `XJ`, `NGATE`, `U0`, `VSAT`, and `RDSW`.
-   The report finds that threshold voltage is particularly affected by
    `VTH0`, `TOXE`, effective channel length, `NDEP`, and `NGATE`; ON
    current is strongly affected by effective channel length, mobility,
    velocity saturation, series resistance, and gate doping.

### S6 --- Approximate Match to TCAD

-   Compares LTspice curves with TCAD transfer and output
    characteristics.
-   Tunes parameters including `VTH0`, `VOFF`, `NFACTOR`, `U0`, `VSAT`,
    `PCLM`, and `ETA0`.
-   The objective is to align the threshold/subthreshold region,
    saturation current, and output-curve slope.

### S7 --- CMOS Inverter

-   Simulates a CMOS inverter using 65 nm nMOS and pMOS devices.
-   Uses a 1.1 V supply, with nMOS width of 1 µm and pMOS width of 2 µm.
-   Analyses the voltage-transfer characteristic and switching
    behaviour.
-   Reported results: `VOH = 1.10 V`, `VOL = 0 V`, switching threshold
    `VM ≈ 0.55 V`, and maximum gain magnitude of approximately 8.

## Repository Contents

The report expects circuit and plot images in the project root or in the
following directories:

-   `figs/`
-   `s1/`, `s2/`, `s3/`, `s4/`, `s5/`, `s6/`, `s7/`

Examples of referenced figures include `s1-circuit.png`, `s2.png`,
`s3.png`, `s4.png`, `s5-circuit1.png`, `s6_idvg.png`, `s6_idvd.png`,
`s7-circuit.png`, and `s7.png`. The report's LaTeX figure helper
displays a placeholder when an expected image is missing.

## Tools and Technologies

-   **LTspice** --- circuit simulation and operating-point/DC analyses
-   **65 nm PTM model card** --- MOSFET device modelling
-   **LaTeX** --- report preparation
-   **Python (NumPy/Matplotlib)** --- used for plotting or numerical
    analysis referenced in the report
-   **TCAD** --- reference characteristics for the approximate model
    comparison



## Main Takeaways

-   Increasing channel length reduces drain current in the reported
    operating-point comparison.
-   Transfer curves provide estimates of threshold voltage, ON/OFF
    current, and subthreshold swing.
-   Output conductance is non-zero, so the MOSFET has finite output
    resistance in saturation.
-   Short-channel effects, oxide thickness, mobility, velocity
    saturation, and parasitic resistance influence device performance.
-   Model-parameter tuning can bring SPICE characteristics closer to
    TCAD results.
-   The CMOS inverter provides rail-to-rail output levels and switches
    near half the 1.1 V supply.

## Author

**Tuladhar Reddy Madireddi**\
**Roll No.:** 25EC01048
