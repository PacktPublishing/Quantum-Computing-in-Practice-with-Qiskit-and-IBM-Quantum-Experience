#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:27:14 2019

@author: hnorlen
"""

# Import Qiskit
from qiskit import QuantumCircuit
from qiskit import Aer, IBMQ, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

IBMQ.load_account()
provider = IBMQ.get_provider()

# List Aer backends
Aer.backends()

# Construct quantum circuit
n=10
circ = QuantumCircuit(2, 2)
circ.x(0)
while n >0:
    circ.swap(0,1)
    circ.barrier()
    n=n-1
circ.measure([0,1], [0,1])
print(circ)
# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
sim_result = execute(circ, simulator, shots=10000).result()
sim_counts = sim_result.get_counts(circ)
print("Sim SWAP counts:",sim_counts)
plot_histogram(sim_counts, title='Sim SWAP counts')

# Import the least busy backend
from qiskit.providers.ibmq import least_busy
backend = least_busy(provider.backends(operational=True, simulator=False))
# Execute and get counts
job = execute(circ, backend, shots=backend.configuration().max_shots)
job_monitor(job)
nisq_result=job.result()
nisq_counts=nisq_result.get_counts(circ)
print("NISQ SWAP counts:",nisq_counts)
plot_histogram(nisq_counts, title='IBM Q SWAP counts')

# Comparing the circuit with the transpled circuit
from qiskit.compiler import transpile
trans_swap = transpile(circ, backend)
print(trans_swap)
print("Basis gates:",backend.configuration().basis_gates)
print("SWAP circuit depth:",circ.depth(),"gates")
print("Transpiled SWAP circuit depth:",trans_swap.depth(),"gates")

