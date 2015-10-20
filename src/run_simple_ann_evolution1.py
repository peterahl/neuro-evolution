from ne_simulator.sim_objects.ann_simple_agent import \
    ANNSimpleAgent  # @UnusedImport
import json
from ne_simulator.evolution import SIMULATOR_CLASS, EVOLUTION_CLASS,\
    SIMULATIONS_COUNT, SCENARIOS, SIMULATOR_CONFIGURATION, Evolution


_SIMULATION_COUNTS = 6


def main():
    # Create and add module to be used by the run function.
    with open('configurations/random_agent.json') as jfile:
        scenario = json.load(jfile)

    scenario["parameters"] = {
        (24, 13): (
            [],
            {'score_monitor_class':
			    'ne_simulator.experiments.simple_ann_evolution1.monitor.Monitor'})}
    scenario["steps_limiter_steps"] = 100
    configuration =  {
        EVOLUTION_CLASS: "ne_simulator.experiments.simple_ann_evolution1.evolution.Evolution",
        SIMULATIONS_COUNT: _SIMULATION_COUNTS,
        SCENARIOS: [{
            SIMULATOR_CLASS: (
                    "ne_simulator.sim_mixins.steps_limiter.StepsLimiter",
                    "ne_simulator.simulator.Simulator"),
            SIMULATOR_CONFIGURATION: scenario}],
    }
    Evolution.get_instance(configuration).run()

if __name__ == '__main__':
    main()
