# -*- coding: utf-8 -*-

"""
This module is the driver module for PyQuOpt
"""
import sys
import numpy as np
from mpi4py import MPI
sys.path.append('../..')

# User-defined libraries
from pyquopt import *
from utils import generate_circuit_structures


mq_dict = {
    0: ThreeGates.CX01,
    1: ThreeGates.CX02,
    2: ThreeGates.CX12
}


if __name__ == '__main__':
    """
    Program entry
    """

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Set optimization hyperparameters
    num_qubits = 3
    num_mq_instructions = 6  # want to explore circuits with six multi-qubit gates
    num_params = 3 * num_qubits * (num_mq_instructions + 1)  # formula explained in MICRO paper
    alpha = 0  # penalty for non-standard angles
    gamma = 0  # penalty for large angles
    non_fixed_params = np.ones(num_params)  # leave all parameters unfixed
    fixed_params_vals = np.zeros(num_params)  # unfixed parameters should have a "fixed" value of 0
    for i in range(9):
        non_fixed_params[i] = 0
        non_fixed_params[-i] = 0  # first and last layers should contain no U3 gates

    # Generate circuit substructures and determine which ones this rank will explore
    circuit_structures = generate_circuit_structures(num_mq_ins=len(mq_dict), num_layers=num_mq_instructions)
    start = 16 * rank
    stop = 16 * (rank + 1)

    for i in range(start, stop):
        structure = circuit_structures[i]

        # Create unitary builder to check validity of implementation
        ub = UnitaryBuilder(num_qubits=num_qubits, mq_instructions=structure, mq_dict=mq_dict)

        # Run optimization routing 20 times for this structure
        optimizer = Optimizer(num_qubits=num_qubits, mq_instructions=structure, mq_dict=mq_dict,
                              target=ThreeGates.TOFFOLI,
                              alpha=alpha, gamma=gamma, non_fixed_params=non_fixed_params,
                              fixed_params_vals=fixed_params_vals)

        opt_params, opt_val = optimizer.find_parameters_least_squares(20)
        implementation_matrix = ub.build_unitary(opt_params)
        unitary_distance = get_unitary_infidelity(ThreeGates.TOFFOLI, implementation_matrix, 8)

        if unitary_distance < 0.01:
            data_file = open(f"/home/mbowman/Toffoli-Optimization/applications/context/out/out_full_{''.join(structure)}.txt"
                             , "w")
            data_file.write("PyQuOpt Results\n==========\n")
            data_file.write(f"Rank {rank} Computation\n======\n")
            data_file.write(f"Parameters: {list(opt_params)}")
            data_file.write("\n")
            data_file.write(f"Unitary distance: {unitary_distance}")
            data_file.write("\n")
            data_file.close()
