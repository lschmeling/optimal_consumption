# Optimal Consumption

The task set here is intended to find suitable candidates for a Master's thesis at DLR VE. 
The topic of the thesis is on the temporal optimisation of the energy demand of private households 
under the use of complex energy systems.

## Problem Definition

The aim of this task is to optimise the energy consumption of a household in such a way that the minimum energy costs
are achieved. The household owns a photovoltaic system and battery storage. The optimisation is to be automated with an
optimisation algorithm which minimises the energy costs. These results can then be used to advise and incentivise 
residents with regard to their energy consumption.

## Content of this repository

This repository contains the model of a fictional household's energy system, which can be found in `oemof.model.py`. 
The model is based on python and the modelling framework [oemof.solph](https://github.com/oemof/oemof-solph).
Two functions are available, both of which take a time series of the energy consumption as a list of 72 hourly values
as input. The function `calc_cost()` returns the actual costs of the energy system in this period and can be used for
optimisation. The second function `calc_energysystem()` returns the solved oemof energy system and can be used for
example to visualise the results. A possible visualisation can also be seen there.

## Task

The task is to connect any optimiser to this problem, which optimises the energy consumption on the basis of the costs
incurred. It is not a question of a sensible reduction in consumption, but only of a temporal shift. The energy demand
is fixed and equals 100 kWh in the period under consideration. The optimisation should be fully automated, i.e. it 
should not require any user input, and should be applicable to other time series and changed energy systems without 
any adjustments. The implementation of the energy system may be adapted if necessary, as long as the basic functionality
of the modelled energy system remains.

## Submission of the results

As a result, the completed script as well as a 4-page PowerPoint with the following contents are to be handed in:
- Page 1: Description of the problem and the energy system
- Page 2: Presentation of the optimisation approach used
- Page 3: Problems in the implementation and their solution
- Page 4: Result of the optimisation

These can either be submitted as a pull request to this repository or sent to [Lucas Schmeling](lucas.schmeling@dlr.de).
The finished script is graded according to its quality (minimum cost) and its performance (minimum computing time).
However, unfinished submissions will also be considered as long as they can show that the problem has been dealt with
in depth and that sensible approaches can be shown.