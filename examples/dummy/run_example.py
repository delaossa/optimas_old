from optimas.core import VaryingParameter, Objective
from optimas.generators import AxSingleFidelityGenerator
from optimas.evaluators import TemplateEvaluator
from optimas.explorations import Exploration


def analyze_simulation(simulation_directory, output_params):
    """Function that analyzes the simulation output and fills in the
    dictionary of output parameters."""
    # Read back result from file
    with open('result.txt') as f:
        result = float(f.read())
    # Fill in output parameters.
    output_params['f'] = result
    return output_params


# Create varying parameters and objectives.
var_1 = VaryingParameter('x0', 0., 15.)
var_2 = VaryingParameter('x1', 0., 15.)
obj = Objective('f', minimize=True)


# Create generator.
gen = AxSingleFidelityGenerator(
    varying_parameters=[var_1, var_2],
    objectives=[obj],
    n_init=4
)


# Create evaluator.
ev = TemplateEvaluator(
    sim_template='template_simulation_script.py',
    analysis_func=analyze_simulation
)


# Create exploration.
exp = Exploration(
    generator=gen,
    evaluator=ev,
    max_evals=10,
    sim_workers=4,
    run_async=True
)


# To safely perform exploration, run it in the block below (this is needed
# for some flavours of multiprocessing, namely spawn and forkserver)
if __name__ == '__main__':
    exp.run()
