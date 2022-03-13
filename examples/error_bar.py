import numpy as np
from copy import deepcopy

from qiskit.result import Result


def Montecarlo(job_result):
    """Generating random data using multinomial distribution, reference:https://arxiv.org/abs/2108.02626"""
    job_result_dict = job_result.to_dict()
    job_result_random_dict = deepcopy(job_result_dict)
    for i in range(len(job_result_random_dict['results'])):
        counts_dict = job_result_random_dict['results'][i]['data']['counts']
        total_count = sum(counts_dict.values())
        orign_probs = [i/total_count for i in counts_dict.values()]
        new_probs = np.random.multinomial(total_count, orign_probs)
        index = 0
        for key in counts_dict.keys():
            counts_dict[key] = new_probs[index]
            index += 1
    return Result.from_dict(job_result_random_dict)