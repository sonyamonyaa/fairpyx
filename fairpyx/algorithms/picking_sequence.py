"""
Allocate course seats using a picking sequence.

Three interesting special cases of a picking-sequence are: round-robin, balanced round-robin, and serial dictatorship.

Programmer: Erel Segal-Halevi
Since: 2023-06
"""

from itertools import cycle
from fairpyx import Instance, AllocationBuilder

import logging
logger = logging.getLogger(__name__)


def picking_sequence(alloc: AllocationBuilder, agent_order:list):
    """
    Allocate the given items to the given agents using the given picking sequence.
    :param alloc: an allocation builder, which tracks the allocation and the remaining capacity for items and agents.
    :param agent_order: a list of indices of agents, representing the picking sequence. The agents will pick items in this order.

    >>> from fairpyx.adaptors import divide
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": {"c1": 10, "c2": 8, "c3": 6}, "Bob": {"c1": 10, "c2": 8, "c3": 6}, "Chana": {"c1": 6, "c2": 8, "c3": 10}, "Dana": {"c1": 6, "c2": 8, "c3": 10}}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> divide(picking_sequence, instance=instance, agent_order=["Alice","Bob", "Chana", "Dana","Dana","Chana","Bob", "Alice"])
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    logger.info("\nPicking-sequence with items %s , agents %s, and agent-order %s", alloc.remaining_item_capacities, alloc.remaining_agent_capacities, agent_order)
    for agent in cycle(agent_order):
        if alloc.isdone():
            logger.info("No more items to allocate")
            break
        if not agent in alloc.remaining_agent_capacities:
            logger.info("No more agents with capacities")
            continue
        potential_items_for_agent = set(alloc.remaining_items_for_agent(agent))
        if len(potential_items_for_agent)==0:
            logger.info("Agent %s cannot pick any more items: remaining=%s, bundle=%s", agent, alloc.remaining_item_capacities, alloc.bundles[agent])
            alloc.remove_agent_from_loop(agent)
            continue
        best_item_for_agent = max(potential_items_for_agent, key=lambda item: alloc.effective_value(agent,item))
        # logger.info("\nAgent %s picks item %s", agent, best_item_for_agent)
        alloc.give(agent, best_item_for_agent, logger)


def serial_dictatorship(alloc: AllocationBuilder, agent_order:list=None):
    """
    Allocate the given items to the given agents using the serial_dictatorship protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.

    >>> from fairpyx.adaptors import divide
    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> divide(serial_dictatorship, instance=instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c3']}
    """
    if agent_order is None: agent_order = alloc.remaining_agents()
    agent_order = sum([alloc.remaining_agent_capacities[agent] * [agent] for agent in agent_order], [])
    picking_sequence(alloc, agent_order)


def round_robin(alloc: AllocationBuilder, agent_order:list=None):
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.

    >>> from fairpyx.adaptors import divide
    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> divide(round_robin, instance=instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c3']}

    # Agent conflicts:
    >>> instance  = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations, agent_conflicts={"Alice": ['c1', 'c2']})
    >>> divide(round_robin, instance=instance)
    {'Alice': ['c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c1', 'c2', 'c3']}

    # Item conflicts:
    >>> instance  = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations, item_conflicts={"c1": ['c2'], "c2": ['c1']})
    >>> divide(round_robin, instance=instance)
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    if agent_order is None: agent_order = list(alloc.remaining_agents())
    picking_sequence(alloc, agent_order)

def bidirectional_round_robin(alloc: AllocationBuilder, agent_order:list=None):
    """
    Allocate the given items to the given agents using the bidirectional-round-robin protocol (ABCCBA), in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> from fairpyx.adaptors import divide
    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> divide(bidirectional_round_robin, instance=instance)
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    if agent_order is None: agent_order = alloc.remaining_agents()
    picking_sequence(alloc, list(agent_order) + list(reversed(agent_order)))




round_robin.logger = picking_sequence.logger = serial_dictatorship.logger = logger


### MAIN

if __name__ == "__main__":
    # import doctest
    # print("\n",doctest.testmod(), "\n")

    # sys.exit()

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    from fairpyx.adaptors import divide
    agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    valuations = {"Alice": {"c1": 10, "c2": 8, "c3": 6}, "Bob": {"c1": 10, "c2": 8, "c3": 6}, "Chana": {"c1": 6, "c2": 8, "c3": 10}, "Dana": {"c1": 6, "c2": 8, "c3": 10}}
    instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    divide(picking_sequence, instance=instance, agent_order=["Alice","Bob", "Chana", "Dana","Dana","Chana","Bob", "Alice"])

    # from fairpyx.adaptors import divide_random_instance

    # print("\n\nRound robin:")
    # divide_random_instance(algorithm=round_robin, 
    #                        num_of_agents=30, num_of_items=10, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
    #                        item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
    #                        random_seed=1)
    # print("\n\nBidirectional round robin:")
    # divide_random_instance(algorithm=bidirectional_round_robin, 
    #                        num_of_agents=30, num_of_items=10, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
    #                        item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
    #                        random_seed=1)
