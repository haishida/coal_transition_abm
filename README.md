# Coal Transition ABM

This repository contains Python code for an agent-based model used in the paper:

**"Conditions for Coal Dependence in Preindustrial Societies: An Agent-Based Analysis of the Fuelwood-to-Coal Transition"**

The model examines the conditions under which a transition from fuelwood to coal can emerge in preindustrial biomass societies.

## Repository structure

```text
coal_transition_abm/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── params.py
├── agents.py
├── model.py
├── stats.py
└── run_baseline.py
```

## Files

* `params.py`: model parameters
* `agents.py`: Human and Field agent classes
* `model.py`: main Mesa model
* `stats.py`: functions for collecting simulation statistics
* `run_baseline.py`: script for running the baseline simulation
* `requirements.txt`: required Python packages
* `LICENSE`: software license

## Requirements

This code requires Python 3 and the following Python packages:

* mesa
* numpy
* pandas
* matplotlib
* tqdm

Install the required packages with:

```bash
pip install -r requirements.txt
```

## How to run

Run the baseline simulation with:

```bash
python run_baseline.py
```

For a short test run:

```bash
python run_baseline.py --steps 10
```

The script generates a CSV file containing simulation results. 

## License

This code is released under the MIT License.

## Author

Hazuki Ishida
Faculty of Economics, Doshisha University

## Simulation Data

Aggregated simulation results supporting Figures 3–7 of the manuscript are available in the [`data/`](data/) directory.
The directory contains CSV and Excel files documenting the effects of fuel demand, forest convertibility, and coal extraction costs on simulated coal use and population dynamics.
For details of the datasets, parameter definitions, and aggregation procedures, see [`data/README.md`](data/README.md).
The complete raw simulation outputs are not included in this repository.
