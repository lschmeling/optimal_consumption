# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from oemof import solph
from oemof.solph import Source, Sink, Bus, Flow, Model, EnergySystem

# Data
PV_GENERATION = [0, 0, 0, 0, 0, 0.027480659, 0.294524282, 1.331494976, 1.706408406,
                 0.064760407, 3.800581979, 6.237957612, 5.083272487, 3.797069942,
                 0.658074974, 1.81976262, 0.343014305, 0.041634414, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0.091170394, 0.096628428, 1.468532199, 1.157308321,
                 1.919360332, 5.037426632, 4.908060113, 2.819814453, 5.701970869,
                 3.65146691, 1.684222347, 0.462257651, 0.080636749, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0.053167691, 0.282335054, 0.88806353, 3.353525588,
                 4.23977131, 4.050275376, 1.64465707, 0.014475718, 4.811141123,
                 2.799112532, 1.870968326, 0.334504689, 0.075924716, 0, 0, 0, 0, 0, 0]

GRID_PRICES = [0.0300, 0.0334, 0.0370, 0.0371, 0.0404, 0.0375, 0.0356, 0.0321, 0.0346, 0.0345,
               0.0386, 0.0422, 0.0446, 0.0397, 0.0384, 0.0401, 0.0401, 0.0425, 0.0390, 0.0369,
               0.0330, 0.0332, 0.0313, 0.0266, 0.0272, 0.0224, 0.0229, 0.0274, 0.0243, 0.0280,
               0.0236, 0.0212, 0.0253, 0.0224, 0.0267, 0.0247, 0.0271, 0.0304, 0.0345, 0.0330,
               0.0334, 0.0309, 0.0271, 0.0243, 0.0247, 0.0251, 0.0204, 0.0239, 0.0218, 0.0220,
               0.0262, 0.0222, 0.0244, 0.0214, 0.0254, 0.0267, 0.0298, 0.0320, 0.0286, 0.0313,
               0.0294, 0.0329, 0.0359, 0.0324, 0.0320, 0.0271, 0.0295, 0.0307, 0.0309, 0.0338,
               0.0297, 0.0296]


def calc_energysystem(demand):
    """
    Simulate a household with PV and battery storage based on a demand profile.

    :param demand: List of hourly electricity consumption values
    :return: Solved oemof energysystem
    """
    # Set up model
    datetimeindex = pd.date_range("1/1/2016", periods=len(PV_GENERATION), freq="H")
    energysystem = EnergySystem(timeindex=datetimeindex)
    b_el = Bus(label="b_el")
    energysystem.add(b_el)

    # Electricity Grid
    m_el_in = Source(label="m_el_in", outputs={b_el: solph.Flow(nominal_value=5,
                                                                variable_costs=GRID_PRICES)})
    m_el_out = Sink(label="m_el_out", inputs={b_el: solph.Flow(nominal_value=5,
                                                                variable_costs=0.06)})
    energysystem.add(m_el_in, m_el_out)

    # PV Source
    t_pv = Source(label="t_pv", outputs={b_el: Flow(fix=PV_GENERATION,
                                                    nominal_value=1)})
    energysystem.add(t_pv)

    # Battery
    s_el = solph.components.GenericStorage(nominal_storage_capacity=10,
                                           label="s_el",
                                           inputs={b_el: solph.Flow(nominal_value=5)},
                                           outputs={b_el: solph.Flow(nominal_value=5)},
                                           loss_rate=7E-5,
                                           inflow_conversion_factor=0.95,
                                           outflow_conversion_factor=0.95)

    energysystem.add(s_el)

    # Sink for demand
    d_el = Sink(label="d_el", inputs={b_el: Flow(nominal_value=1,
                                                 fix=demand)})
    energysystem.add(d_el)

    # Solve energy system
    om = Model(energysystem=energysystem)
    om.solve(solver='cbc')

    # Process results
    energysystem.results["main"] = solph.processing.results(om)
    energysystem.results["meta"] = solph.processing.meta_results(om)

    return energysystem


def calc_cost(demand):
    """
    Calculate the cost of the solved energy system
    :param demand: List of hourly electricity consumption values
    :return: Cost of the energy system
    """
    energysystem = calc_energysystem(demand)
    objective = energysystem.results["meta"]['objective']
    return objective


if __name__ == '__main__':
    energysystem = calc_energysystem(np.ones(len(PV_GENERATION)))

    results = energysystem.results["main"]

    storage = solph.views.node(results, "s_el")
    electricity = solph.views.node(results, "b_el")

    _, ax = plt.subplots()
    storage["sequences"].plot(ax=ax, kind="line", drawstyle="steps-post")
    plt.legend()

    _, ax = plt.subplots()
    electricity["sequences"].plot(ax=ax, kind="line", drawstyle="steps-post")
    plt.legend()

    plt.show()
