# Data supporting the fuelwood-to-coal transition study

This repository directory contains figure-supporting simulation outputs associated with the manuscript:

**Conditions for Coal Dependence in Preindustrial Societies: An Agent-Based Analysis of the Fuelwood-to-Coal Transition**  
Hazuki Ishida, Doshisha University.

## Contents and correspondence to figures

| Manuscript figure | File | Relevant content |
| --- | --- | --- |
| Figure 3 (baseline coal share and population) | `Figure3_data.csv` | Means and sample standard deviations of 20 simulation runs, for simulation steps -10 through 100 |
| Figure 4 (cultivable-land conditions) | `Baseline_cultivable.xlsx` | `Coal_share` and `Population` sheets, including the `CR*` series |
| Figure 5 (fuel demand and cultivability) | `pcFUEL_Cultivable.xlsx` | `Coal_share` sheet; combinations of per-capita fuel demand and cultivability |
| Figure 6(a)–(c) (coal extraction cost) | `Ext_cost.xlsx` | `Coal_share` and related fuel-demand-specific worksheets |
| Figure 6(d) (fuel demand of 4.0, extraction-cost comparison) | `Figure6d_data.csv` | Coal-share series for extraction-cost parameters 0.01, 0.05, and 0.10; steps -10 through 199 |
| Figure 7 (coal-share contour plots) | `Figure7_data.csv` | Parameter grid and coal-share outcomes, 1,000 distinct parameter combinations |

The original workbook sheet names and series labels have been preserved. Please consult the manuscript and plotting code for parameter definitions, figure legends, and interpolation/plotting settings. Figure-to-data correspondence is based on the current manuscript and notebook inspection; exact numerical reproduction of all plotted lines has not been independently verified for this deposit.

## Column definitions for exported CSV files

### `Figure3_data.csv`
- `Step`: simulation time, shifted to match the horizontal axis used in Figure 3
- `Coal_share_mean`: mean coal share across 20 runs
- `Coal_share_sd`: sample standard deviation of coal share across 20 runs (`ddof=1`)
- `Population_mean`: mean population across 20 runs
- `Population_sd`: sample standard deviation of population across 20 runs (`ddof=1`)

Only the displayed interval (steps -10 to 100) is retained in this file. The untrimmed exported time series is not included.

### `Figure6d_data.csv`
- `Step`: simulation time, from -10 to 199
- `Coal_share_exc_0.01`, `Coal_share_exc_0.05`, `Coal_share_exc_0.10`: mean coal-share trajectories for the corresponding coal extraction-cost settings, with per-capita fuel demand set to 4.0

The last available step is 199, not 200; no artificial final row was added.

### `Figure7_data.csv`
- `Fuel_needs_pc`: per-capita fuel requirement (`pcf`)
- `cultivable_rate`: cultivable-land conversion rate (`cr`)
- `ex_cost_Coal`: coal extraction-cost parameter (`exc`)
- `Coal_share`: aggregated coal share for the parameter combination

This file was derived from the `Summary` worksheet of `Summary.xlsx`. The source contained 1,002 rows for 1,000 distinct parameter combinations. Two duplicate combinations were consolidated by taking the arithmetic mean of their reported `Coal_share` values, matching the plotting notebook's `pivot_table(..., aggfunc="mean")` treatment of duplicates:

| Fuel_needs_pc | cultivable_rate | ex_cost_Coal | Mean Coal_share |
| ---: | ---: | ---: | ---: |
| 2.0 | 0.8 | 0.08 | 0.692443 |
| 5.0 | 0.2 | 0.03 | 0.042288 |

The cause of these source duplicates has not been established. The underlying `Summary.xlsx` has not been modified. Contour interpolation and visual appearance depend on the plotting notebook, not solely on this CSV.

## Time coordinates in Excel workbooks

The plotting notebooks may convert the workbook's stored step to the displayed simulation step by subtracting 30 (`displayed Step = source Step - 30`). The exported CSV files already use their plotted step coordinates. Please inspect the relevant plotting notebook before using workbook step columns directly.

## Software and reproducibility

The model's public source code is available at:

https://github.com/haishida/coal_transition_abm

This package contains **figure-supporting summaries**, not the complete collection of individual simulation-run workbooks. It enables inspection and replotting of the published aggregates, but it is not a substitute for all raw stochastic outputs. Reproducing simulations from scratch requires the model code, run settings, and stochastic execution choices.

## Recommended citation and versioning

When publishing, place this directory under `data/` in the public code repository and create a tagged release. For stronger long-term preservation, archive that release with a repository such as Zenodo and cite the archived version/DOI in the manuscript. Do not claim a DOI until it has been assigned.
