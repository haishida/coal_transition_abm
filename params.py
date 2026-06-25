from dataclasses import dataclass


@dataclass
class Params:
    #### Model Parameters ####
    width: int = 21
    height: int = 21
    init_Human: float = 0.5   # Initial human number (probability)
    mutant_rate: float = 0.05   # Mutant rate
    timing_put_mine: int = 30
    uncultivable_range: int = 0   # Uncultivable field from mine
    desert_rate: float = 0.0   # Tendency of deserty area
    coal_ratio: float = 1.0   # Only for coal_favor, max value
    cultivable_rate: float = 1.0   # Cultivable rate of forests; default = 1.0

    #############
    ### Human ###
    #############
    metabo: float = 1.0
    bmr: float = 0.75   # BMR for human metabolism
    eta_Human: float = 1.0   # Thermal efficiency of human work
    fuel_needs_pc: float = 1.0   # Fuel needs of a human being; default = 1.0

    neighbor_radius: int = 10   # Search area/distance for fuels
    target_area: int = 2   # Search area for target cell to place offspring

    #############
    ### Fuels ###
    #############

    #### Mine / Coal ####
    exist_mine: bool = True
    mine_position: tuple = (10, 10)
    init_stock_Coal: float = 100000000000000000   # Initial stock

    ex_cost_Coal: float = 0.01   # Default = 0.01; range: 0.01, 0.02, ..., 0.10

    # Coal extraction cost function: f = a_0 + a_1 * x^a_2
    a_0: float = None   # Constant term
    a_1: float = 0.0   # Coefficient
    a_2: float = 1.0   # Exponent
    tr_cost_Coal: float = 0.005   # Transportation cost; default = 0.005

    #### Forest / Fuelwood ####
    potential_Wood: float = 1.0   # Default = 1.0
    lead_time_restration: int = 2   # Lead time of forest restoration from waste land
    ex_cost_Wood: float = 0.01   # Extraction energy cost per unit mass; default = 0.01
    tr_cost_Wood_ratio: float = 2.0   # Wood/Coal ratio of transportation cost per unit mass and distance
    tr_cost_Wood: float = None   # Transportation energy cost per unit mass and distance

    #### Decrease rate of transportation cost: coal and fuelwood ####
    interval: int = 10   # Period during which transportation cost decreases by dec_rate
    dec_rate: float = 0.0
    both: bool = True   # True: fuelwood and coal; False: coal only

    ############
    ### Food ###
    ############

    #### Farm / Food ####
    # Food does not require transportation cost.
    lead_time_ignored_farm_into_waste: int = 1
    potential_Food: float = 1.0
    ex_cost_Food: float = 0.02   # Default = 0.02

    def __post_init__(self):
        if self.tr_cost_Wood is None:
            self.tr_cost_Wood = self.tr_cost_Wood_ratio * self.tr_cost_Coal

        self.a_0 = self.ex_cost_Coal