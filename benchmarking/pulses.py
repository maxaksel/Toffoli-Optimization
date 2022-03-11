from math import pi

#Qiskit-related imports
from qiskit.providers.backend import IBMBackend

# Superstaq-related imports
import cirq
from cirq_superstaq import Service, AceCRPlusMinus, AceCRMinusPlus
import cirq_superstaq
from cirq.contrib.svg import SVGCircuit

class PulseGates:
    def __init__(backend: IBMQBackend, ss_host, ss_api):
        self.backend = backend
        self.service = Service(remote_host=ss_host, api_key=ss_api) # Superstaq API key

    def get_canonical_linear_toffoli(self, qubits: List[int]) -> Schedule:
        q0 = qubits[0]
        q1 = qubits[1]
        q2 = qubits[2]

        with pulse.build(backend, name='canonical_linear_toffoli') as canonical_toffoli_schedule:
            pulse.u3(pi/2, 0, pi, q2)  # Hadamard

            # T gates on qubits 0, 1, 2
            pulse.u3(0, 0, pi/4, q0)
            pulse.u3(0, 0, pi/4, q1)
            pulse.u3(0, 0, pi/4, q2)

            pulse.cx(q0, q1)
            pulse.cx(q1, q2)
            pulse.cx(q0, q1)

            pulse.u3(0, 0, pi/4, q2)

            pulse.cx(q1, q2)
            pulse.cx(q0, q1)

            pulse.u3(0, 0, -pi/4, q1)
            pulse.u3(0, 0, -pi/4, q2)

            pulse.cx(q1, q2)
            pulse.cx(q0, q1)

            pulse.u3(0, 0, -pi/4, q2)

            pulse.cx(q1, q2)

            pulse.u3(pi/2, 0, pi, q2)  # Hadamard

        return canonical_toffoli_schedule

    def get_optimized_linear_toffoli(self, qubits: List[int], target: str):
        q0 = cirq.LineQubit(qubits[0])
        q1 = cirq.LineQubit(qubits[1])
        q2 = cirq.LineQubit(qubits[2])

        opt_toffoli = cirq.Circuit(
            # Specify pulse here
            cirq.Moment(cirq.rz(3*pi/4)(q0), cirq.rz(pi/4)(q1), cirq.rz(-pi/2)(q2)),
            cirq.Moment(cirq_superstaq.AceCR("-+", cirq.rx(np.pi/2))(q0, q1), cirq.rx(pi/2)(q2)),
            cirq.Moment(cirq.rz(-pi/2)(q0), cirq.rz(pi/2)(q1), cirq.rz(pi/4)(q2)),
            cirq.Moment(cirq_superstaq.AceCR("-+", cirq.rx(-np.pi/2))(q1, q2)),
            cirq.Moment(cirq_superstaq.AceCR("+-", cirq.rx(np.pi/2))(q0, q1)),
            cirq.Moment(cirq.rz(pi/2)(q0), cirq.rz(-pi/2)(q1), cirq.rz(pi/4)(q2)),
            cirq.Moment(cirq_superstaq.AceCR("+-", cirq.rx(np.pi/2))(q1, q2)),
            cirq.Moment(cirq_superstaq.AceCR("-+", cirq.rx(np.pi/2))(q0, q1)),
            cirq.Moment(cirq.rz(-pi/2)(q0), cirq.rz(pi/4)(q1), cirq.rz(-pi/4)(q2)),
            cirq.Moment(cirq_superstaq.AceCR("-+", cirq.rx(np.pi/2))(q1, q2)),
            cirq.Moment(cirq_superstaq.AceCR("+-", cirq.rx(np.pi/2))(q0, q1)),
            cirq.Moment(cirq.rz(-pi/2)(q1), cirq.rz(-pi/4)(q2)),
            cirq.Moment(AceCRPlusMinus(q1, q2)),
            cirq.Moment(cirq.rz(pi/2)(q2)),
            cirq.Moment(cirq.rx(pi/2)(q2)),
            cirq.Moment(cirq.rz(pi)(q2))
        )

        opt_schedule = self.service.ibmq_compile(opt_toffoli, target=target)

        return opt_schedule
