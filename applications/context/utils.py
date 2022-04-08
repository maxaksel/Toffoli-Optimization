"""
Module containing utilities for context-aware Toffoli gate discovery.
"""


def generate_circuit_structures(num_mq_ins: int, num_layers: int):
    """
    Generate a list of lists, each representing a series of multi-qubit
    instructions that makeup the structure of a parameterizable quantum
    circuit (remember these instructions are multiplied "backwards" in unitary)
    :param num_mq_ins: number of multi-qubit instructions
    :param num_layers: number of circuit layers to generate
    :return: a list of lists each with length num_layers
    """
    if num_layers == 0:
        return [[]]  # recursive base case
    structures = []
    for permutation in generate_circuit_structures(num_mq_ins, num_layers - 1):
        for ins in range(num_mq_ins):
            structures.append([ins] + permutation)
    return structures
