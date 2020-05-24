#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 21:17:25 2020

@author: hassi
"""

#!/usr/bin/env python
# coding: utf-8

from qiskit import QuantumCircuit, IBMQ
from qiskit.compiler import transpile
from qiskit.providers.ibmq import least_busy
from math import pi

# Load account and find an available 5-qubit backend
IBMQ.load_account()
provider = IBMQ.get_provider()
backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))


# Uncomment to set the backend to a simulator
#backend = provider.get_backend('ibmq_qasm_simulator')

print("Ch 7: Transpiling circuits")
print("--------------------------")

# Print the basis gates and coupling map for the selected backend
print("Basis gates for:", backend)
print(backend.configuration().basis_gates)
print("Coupling map for:", backend)
print(backend.configuration().coupling_map)

# Create the circuit and the transpiled circuit
qc = QuantumCircuit(5)
qc.cswap(0,1,2)
trans_qc = transpile(qc, backend)


# Print the original and transpiled circuits
print("Circuit:")
print(qc)
print("Transpiled circuit:")
print(trans_qc)

# Print the original and transpiled circuit depths
print("Circuit depths:")
print("---------------")
print("Circuit:", qc.depth())
print("Transpiled circuit:", trans_qc.depth())

