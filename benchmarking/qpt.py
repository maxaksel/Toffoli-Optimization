# General Imports
from math import pi
from copy import deepcopy
import numpy as np
import time
from collections import defaultdict

# Qiskit-related Imports
import qiskit
from qiskit.providers.backend import IBMQBackend
import qiskit.quantum_info as qi
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister, Aer, transpile, execute
from qiskit.providers.aer import noise
from qiskit.compiler import assemble
from qiskit.circuit import Gate
from qiskit.result import Result
from qiskit import IBMQ
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit.ignis.verification.tomography import state_tomography_circuits, StateTomographyFitter
from qiskit.ignis.verification.tomography import process_tomography_circuits, ProcessTomographyFitter
from qiskit.ignis.verification.tomography import gateset_tomography_circuits, GatesetTomographyFitter
import qiskit.ignis.mitigation.measurement as mc
from qiskit.ignis.mitigation.measurement import tensored_meas_cal, TensoredMeasFitter
from qiskit.quantum_info import Choi, Kraus, DensityMatrix
from qiskit.extensions import HGate, XGate
from qiskit import pulse
from qiskit.pulse.library import Gaussian
from qiskit.visualization import plot_state_city
from qiskit.result import Result

#Error bar-related Imports
import statistics
from error_bar import Montecarlo


def generate_qpt_circuits(circuit: QuantumCircuit, backend: IBMQBackend) -> List[QuantumCircuit]:
    """
    Generate process tomography circuits.

    :param circuit: quantum circuit to characterize
    :param backend: IBM Q backend to target
    :return: a list of labelbed QPT circuits
    """
    qpt_circuits = process_tomography_circuits(circuits, [0, 1, 3])

    for circuit in qpt_circuits:
        circuit.add_calibration('ccx', [0, 1, 3], canonical_toffoli_schedule)  # add optimized CCX schedule to each qpt circuit

    t_qpt_circuits = [transpile(circuit, backend=backend) for circuit in qpt_circuits]

    return t_qpt_circuits


def run_qpt_job(qpt_circuits: List[QuantumCircuit], provider: Provider, backend: IBMQBackend, shots: int, job_name: str) -> str:
    IBMQ.load_account()  # attempt to load IBMQ account
    job_manager = IBMQJobManager()  # instantiate a job manager
    qpt_job = job_manager.run(qpt_circuits, backend=backend, name=job_name, shots=shots)

    return qpt_job.job_set_id()


def compute_fidelity(qpt_circuits: List[QuantumCircuit], qpt_result: Result, target_unitary: qi.Operator, mc_trials: int) -> Tuple[float, float]
    fidelity_list = []

    #simulating multinomial distribution based on the mitigated distribution from mitigated_c_ccx_job_result
    for _ in range(mc_trials):
        qpt_result_random = Montecarlo(qpt_result)
        qpt_tomo_random = ProcessTomographyFitter(qpt_result_random, qpt_circuits)
        # Tomographic reconstruction of the canonical CCX operation
        choi_fit_lstsq = qpt_tomo_random.fit(method='lstsq')

        avg_fidelity_mc = qi.average_gate_fidelity(choi_fit_lstsq, target=target_unitary)
        fidelity_list.append(fidelity_mc)

    avg_fidelity = sum(fidelity_list) / len(fidelity_list)
    error_bar = statistics.pstdev(fidelity_list) * 1.96  # 95% confidence interval

    return avg_fidelity, error_bar



def compute_fidelity_job_id(qpt_circuits: List[QuantumCircuit], provider: Provider, qpt_result_job_id: str, target_unitary: qi.Operator, mc_trials: int) -> Tuple[float, float]:
    """
    Compute average gate fidelity from the job id of a QPT run on quantum hardware.

    :param qpt_circuits: a list of the original QPT circuits sent to quantum computer
    :param provider: the provider used to send said QPT circuits
    :param qpt_result_job_id: a string with the QPT job id
    :param target_unitary: a Qiskit qi.Operator object with the unitary matrix of the desired operation
    :param mc_trials: the number of Monte Carlo trials to run for error bar purposes
    """
    qpt_job = job_manager.retrieve_job_set(job_set_id=qpt_result_job_id, provider=provider)
    qpt_result = qpt_job.results().combine_results()

    return compute_fidelity(qpt_circuits, qpt_result, target_unitary, mc_trials)

