"""
Compare the performance of algorithms for fair course allocation.

Programmer: Erel Segal-Halevi
Since: 2023-07
"""

######### COMMON VARIABLES AND ROUTINES ##########

from typing import *

import numpy as np

from fairpyx import divide, AgentBundleValueMatrix, Instance
from fairpyx.algorithms import maximin_aware
import fairpyx.algorithms as crs
max_value = 1000
normalized_sum_of_values = 1000
TIME_LIMIT = 30
other_algorithms = [
    crs.utilitarian_matching,
    crs.iterated_maximum_matching_unadjusted,
    crs.iterated_maximum_matching_adjusted,
    # crs.serial_dictatorship,                  # Very bad performance
    crs.round_robin,
    crs.bidirectional_round_robin,
    crs.almost_egalitarian_without_donation,
    crs.almost_egalitarian_with_donation
]
algorithms_to_check_on_three = [
    maximin_aware.divide_and_choose_for_three,
    maximin_aware.alloc_by_matching
] + other_algorithms

algorithms_to_check_on_any = [maximin_aware.alloc_by_matching]  + other_algorithms


def evaluate_algorithm_on_instance(algorithm, instance):
    allocation = divide(algorithm, instance)
    matrix = AgentBundleValueMatrix(instance, allocation)
    # deficit is based on agent capacity, which isn't defined in our case
    capacity_error = instance.num_of_items - np.ceil(instance.num_of_items / instance.num_of_agents)
    matrix.use_normalized_values()
    return {
        "utilitarian_value": matrix.utilitarian_value(),
        "egalitarian_value": matrix.egalitarian_value(),
        "egalitarian_utilitarian_ratio": matrix.egalitarian_value()/matrix.utilitarian_value(),
        "max_envy": matrix.max_envy(),
        "mean_envy": matrix.mean_envy(),
        "max_deficit": matrix.max_deficit() - capacity_error,
        "mean_deficit": matrix.mean_deficit() - capacity_error,
    }


######### EXPERIMENT WITH UNIFORMLY-RANDOM DATA ##########

def item_allocation_with_random_instance_uniform(
        num_of_agents: int, num_of_items: int,
        value_noise_ratio: float,
        algorithm: Callable,
        random_seed: int, ):
    agent_capacity_bounds = [num_of_items, num_of_items]
    item_capacity_bounds = [1, 1]
    np.random.seed(random_seed)
    instance = Instance.random_uniform(
        num_of_agents=num_of_agents, num_of_items=num_of_items,
        normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=agent_capacity_bounds,
        item_capacity_bounds=item_capacity_bounds,
        item_base_value_bounds=[1, max_value],
        item_subjective_ratio_bounds=[1 - value_noise_ratio, 1 + value_noise_ratio]
    )
    return evaluate_algorithm_on_instance(algorithm, instance)


def run_experiment_on_three():
    # Run on uniformly-random data:
    experiment = experiments_csv.Experiment("results/", "mma_comparison.csv",
                                            backup_folder="results/backup/")
    # experiment.clear_previous_results()
    input_ranges = {
        "num_of_agents": [3],  # due to divide and choose restrictions
        "num_of_items": [250, 500, 750, 1000, 1500, 2000],
        "value_noise_ratio": [0, 0.2, 0.5, 0.8, 1],
        "algorithm": algorithms_to_check_on_three,
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(item_allocation_with_random_instance_uniform, input_ranges, time_limit=TIME_LIMIT)


def run_experiment_on_any():
    # Run on uniformly-random data:
    experiment = experiments_csv.Experiment("results/", "mma_comparison.csv",
                                            backup_folder="results/backup/")
    # experiment.clear_previous_results()
    input_ranges = {
        "num_of_agents": [3, 25, 50, 100],
        "num_of_items": [250, 500, 750, 1000, 1500, 2000],
        "value_noise_ratio": [0, 0.2, 0.5, 0.8, 1],
        "algorithm": algorithms_to_check_on_any,
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(item_allocation_with_random_instance_uniform, input_ranges, time_limit=TIME_LIMIT)


######### MAIN PROGRAM ##########

if __name__ == "__main__":
    import experiments_csv, logging

    experiments_csv.logger.setLevel(logging.INFO)

    # run_experiment_on_any()
    # run_experiment_on_three()
