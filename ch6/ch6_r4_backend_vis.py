#!/usr/bin/env python
# coding: utf-8#

# Import the required Qiskit classes
from qiskit import IBMQ, QuantumCircuit, transpile
from qiskit.providers.ibmq import least_busy

# Import the backend visualization methods
from qiskit.visualization import plot_gate_map, plot_error_map, plot_circuit_layout

from IPython.core.display import display

print("Ch 6: Backend visualization")
print("---------------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

# Get all available and operational backends.
print("Getting the available backends...")
available_backends = provider.backends(filters=lambda b: b.configuration().n_qubits > 1 and b.status().operational)

# Fish out criteria to compare
print("{0:20} {1:<10}".format("Name","#Qubits"))
print("{0:20} {1:<10}".format("----","-------"))

for n in range(0, len(available_backends)):
    backend = provider.get_backend(str(available_backends[n]))
    print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits))

# Select a backend or go for the least busy backend with more than 1 qubits
backend_input = input("Enter the name of a backend, or X for the least busy:")
if backend_input not in ["X","x"]:
    backend = provider.get_backend(backend_input)
else:
    backend = least_busy(provider.backends(filters=lambda b: b.configuration().n_qubits > 1 and b.status().operational))
# Display the gate and error map for the backend.
print("\nQubit data for backend:",backend.status().backend_name)

display(plot_gate_map(backend, plot_directed=True))
display(plot_error_map(backend))

# Create and transpile a 2 qubit Bell circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)

display(qc.draw('mpl'))
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
display(qc_transpiled.draw('mpl'))

# Display the circuit layout for the backend.
display(plot_circuit_layout(qc_transpiled, backend, view='physical'))

