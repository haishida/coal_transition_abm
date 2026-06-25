"""Main Mesa model for the coal-transition ABM."""

import math
import random

import mesa
import pandas as pd
from mesa.discrete_space import OrthogonalMooreGrid

from agents import Field, Human
from params import Params
from stats import (
    stat_annual_coal_production,
    stat_average_coal_ratio,
    stat_average_cost_coal,
    stat_average_cost_wood,
    stat_average_mileage_coal,
    stat_average_mileage_wood,
    stat_coal_extraction_cost,
    stat_coal_favor_share,
    stat_coal_share,
    stat_cumulative_production,
    stat_population,
)


params = Params()


class FossilModel(mesa.Model):
    def __init__(
        self,
        width=params.width,
        height=params.height,
        desert_rate=params.desert_rate,
        coal_ratio=params.coal_ratio,
        cultivable_rate=params.cultivable_rate,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.step_counter = 0
        self.mine_position = [params.mine_position]

        self.desert_rate = desert_rate
        self.coal_ratio = coal_ratio
        self.cultivable_rate = cultivable_rate

        # Records of fuel transactions
        self.coal_deal = []
        self.wood_deal = []

        # Create grid
        self.grid = OrthogonalMooreGrid(
            [self.height, self.width],
            torus=False,
            capacity=math.inf,
            random=self.random,
        )

        # Put field agents
        for cell in self.grid.all_cells.cells:
            f = Field(self, cell)
            if random.random() < self.cultivable_rate:
                f.cultivable = True

        # Put desert cells
        self.put_desert(desert_rate)

        # Forest pattern
        self.forest_pattern_01(params.uncultivable_range)

        # Put human agents
        for c in self.grid.all_cells.cells:
            if random.random() < params.init_Human:
                cr = random.uniform(0.01, self.coal_ratio)
                h = Human(self, coal_ratio=cr)
                h.cell = c
                h.cultivate()

        # Set DataCollector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Population": stat_population,
                "Annual_coal_production": stat_annual_coal_production,
                "Coal_share": stat_coal_share,
                "Coal_favor_share": stat_coal_favor_share,
                "Average_coal_ratio": stat_average_coal_ratio,
                "Average_coal_cost": stat_average_cost_coal,
                "Average_wood_cost": stat_average_cost_wood,
                "Average_coal_mileage": stat_average_mileage_coal,
                "Average_wood_mileage": stat_average_mileage_wood,
                "Cumulative_coal_production": stat_cumulative_production,
                "Coal_extraction_cost": stat_coal_extraction_cost,
            }
        )
        self.datacollector.collect(self)

        # Set up DataFrame
        self.df = pd.DataFrame(
            {
                "Step": [self.step_counter],
                "Population": [stat_population(self)],
                "Annual_coal_production": [stat_annual_coal_production(self)],
                "Coal_share": [stat_coal_share(self)],
                "Coal_favor_share": [stat_coal_favor_share(self)],
                "Average_coal_ratio": [stat_average_coal_ratio(self)],
                "Average_coal_cost": [stat_average_cost_coal(self)],
                "Average_wood_cost": [stat_average_cost_wood(self)],
                "Average_coal_mileage": [stat_average_mileage_coal(self)],
                "Average_wood_mileage": [stat_average_mileage_wood(self)],
                "Cumulative_coal_production": [stat_cumulative_production(self)],
                "Coal_extraction_cost": [stat_coal_extraction_cost(self)],
            }
        )

    #### Put desert cells ####
    def put_desert(self, rate):
        for c in self.grid.all_cells.cells:
            for a in c.agents:
                if isinstance(a, Field):
                    if random.random() < rate:
                        a.type = "Desert"
                        a.cultivable = False
                    break

    def forest_pattern_01(self, r):
        """
        Forest cells within distance r from the mine cannot be converted into farmland.
        """
        if r > 0:
            x = self.mine_position[0][0]
            y = self.mine_position[0][1]
            cell = self.grid[(x, y)]
            neighbor_cells = cell.get_neighborhood(r, include_center=True)

            for c in list(neighbor_cells):
                for a in c.agents:
                    if isinstance(a, Field):
                        a.type = "Forest"
                        a.cultivable = False

    def put_mine(self):
        if params.exist_mine and self.step_counter == params.timing_put_mine:
            x = self.mine_position[0][0]
            y = self.mine_position[0][1]
            cell = self.grid[(x, y)]

            for a in cell.agents:
                if isinstance(a, Field):
                    a.type = "Mine"
                    break

    def put_mine_with_agents(self):
        if params.exist_mine and self.step_counter == params.timing_put_mine:
            x = self.mine_position[0][0]
            y = self.mine_position[0][1]
            cell = self.grid[(x, y)]

            for a in cell.agents:
                if isinstance(a, Field):
                    a.type = "Mine"

                    moore_cells = cell.get_neighborhood(1, include_center=False)

                    for c in moore_cells:
                        for a in c.agents:
                            if isinstance(a, Human):
                                a.remove()
                            elif isinstance(a, Field):
                                a.type = "Forest"
                                a.cultivable = True

                    for c in moore_cells:
                        h = Human(self, c)
                        h.cultivate()
                        h.doll = True
                        h.coal_favor = True

    def update_df(self):
        new_df = pd.DataFrame(
            {
                "Step": [self.step_counter],
                "Population": [stat_population(self)],
                "Annual_coal_production": [stat_annual_coal_production(self)],
                "Coal_share": [stat_coal_share(self)],
                "Coal_favor_share": [stat_coal_favor_share(self)],
                "Average_coal_ratio": [stat_average_coal_ratio(self)],
                "Average_coal_cost": [stat_average_cost_coal(self)],
                "Average_wood_cost": [stat_average_cost_wood(self)],
                "Average_coal_mileage": [stat_average_mileage_coal(self)],
                "Average_wood_mileage": [stat_average_mileage_wood(self)],
                "Cumulative_coal_production": [stat_cumulative_production(self)],
                "Coal_extraction_cost": [stat_coal_extraction_cost(self)],
            }
        )

        self.df = pd.concat([self.df, new_df], axis=0, ignore_index=True)

    def step(self):
        self.coal_deal = []
        self.wood_deal = []

        # Put mine
        self.put_mine_with_agents()

        if self.step_counter > params.timing_put_mine:
            self.agents_by_type[Field].do("step_00")

        self.agents_by_type[Field].shuffle_do("step_01")

        self.agents_by_type[Human].shuffle_do("step_01")
        self.agents_by_type[Human].shuffle_do("step_02")
        self.agents_by_type[Human].shuffle_do("step_03")
        self.agents_by_type[Human].shuffle_do("step_04")

        self.agents_by_type[Field].do("step_02")
        self.agents_by_type[Field].do("step_03")

        # Data
        self.datacollector.collect(self)

        # Update DataFrame
        self.update_df()

        # Update step counter
        self.step_counter += 1
