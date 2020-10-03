#!/usr/bin/env python
# coding: utf-8

print("Ch 8: Aer out of the box, a perfect quantum computer")
print("----------------------------------------------------")

# Import Qiskit
from qiskit import QuantumCircuit
from qiskit import Aer, IBMQ, execute

# Import visualization tools
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from  IPython.core.display import display


# Load account
print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

# Enter number of SWAP gates to include with your circuit with (default 20)
user_input = input("Enter number of SWAP gates to use: ")
try:
   n = int(user_input)
except ValueError:
   n=10
n_gates=n

# Construct quantum circuit
circ = QuantumCircuit(2, 2)
circ.x(0)
while n >0:
    circ.swap(0,1)
    circ.barrier()
    n=n-1
circ.measure([0,1], [0,1])
print("Circuit with",n_gates,"SWAP gates.\n")
display(circ.draw())

# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
result = execute(circ, simulator, shots=simulator.configuration().max_shots).result()
counts = result.get_counts(circ)
display(plot_histogram(counts, title='Simulated counts for '+str(n_gates)+' SWAP gates.'))
print("Simulated SWAP counts:",counts)
input("Press enter to run on an IBM Q backend...\n")

# Import the least busy backend
from qiskit.providers.ibmq import least_busy
backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
print("Least busy backend:",backend)

# Execute and get counts
job = execute(circ, backend, shots=backend.configuration().max_shots)
job_monitor(job)
nisq_result=job.result()
nisq_counts=nisq_result.get_counts(circ)
print("NISQ SWAP counts:",nisq_counts)
display(plot_histogram(nisq_counts, title='Counts for '+str(n_gates)+' SWAP gates on '+str(backend)))
input("Press enter to transpile the circuit...\n")


# Comparing the circuit with the transpiled circuit
from qiskit.compiler import transpile
trans_swap = transpile(circ, backend)
print(trans_swap)
print("Basis gates:",backend.configuration().basis_gates)
print("SWAP circuit depth:",circ.depth(),"gates")
print("Transpiled SWAP circuit depth:",trans_swap.depth(),"gates")




