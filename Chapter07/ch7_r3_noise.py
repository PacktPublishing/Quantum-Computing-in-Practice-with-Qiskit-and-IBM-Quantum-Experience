#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

print("Ch 7: Adding the noise profile of an IBM Q machine to your local simulator")
print("--------------------------------------------------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ, QuantumCircuit, execute
from qiskit.providers.aer.noise import NoiseModel
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

import numpy as np
np.set_printoptions(precision=3)
from  IPython.core.display import display

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

global backend, noise_model

def select_backend():
    # Get all available and operational backends.
    available_backends = provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 1 and b.status().operational)
    
    # Fish out criteria to compare
    print("{0:20} {1:<10} {2:<10}".format("Name","#Qubits","Pending jobs"))
    print("{0:20} {1:<10} {2:<10}".format("----","-------","------------"))
         
    for n in range(0, len(available_backends)):
        backend = provider.get_backend(str(available_backends[n]))
        print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits),backend.status().pending_jobs)

    select_backend=input("Select a backend ('exit' to end): ")
    
    if select_backend!="exit":
        backend = provider.get_backend(select_backend)
    else:
        backend=select_backend
    return(backend)

def build_noise_model(backend):

    # Construct the noise model from backend
    noise_model = NoiseModel.from_backend(backend)
    print(noise_model)
    return(noise_model)
    
def execute_circuit(backend, noise_model):
    # Basis gates for the noise model
    basis_gates = noise_model.basis_gates
    
    # Coupling map
    coupling_map = backend.configuration().coupling_map
    
    print("Coupling map: ",coupling_map)
    
    # Construct the GHZ-state quantum circuit
    circ = QuantumCircuit(3, 3)
    circ.h(0)
    circ.cx(0, 1)
    circ.cx(0, 2)
    circ.measure([0,1,2], [0,1,2])
    print(circ)

    
    # Execute on QASM simulator and get counts
    counts = execute(circ, Aer.get_backend('qasm_simulator')).result().get_counts(circ)
    display(plot_histogram(counts, title='Ideal counts for 3-qubit GHZ state on local qasm_simulator'))
    
    # Execute noisy simulation on QASM simulator and get counts
    counts_noise = execute(circ, Aer.get_backend('qasm_simulator'), noise_model=noise_model, coupling_map=coupling_map, basis_gates=basis_gates).result().get_counts(circ)
    display(plot_histogram(counts_noise, title="Counts for 3-qubit GHZ state with noise model on local qasm simulator"))

    # Execute noisy simulation on the ibmq_qasm_simulator and get counts
    counts_noise_ibmq = execute(circ, provider.get_backend('ibmq_qasm_simulator'), noise_model=noise_model, coupling_map=coupling_map, basis_gates=basis_gates).result().get_counts(circ)
    display(plot_histogram(counts_noise_ibmq, title="Counts for 3-qubit GHZ state with noise model on IBMQ qasm simulator"))
    
    # Execute job on IBM Q backend and get counts
    job = execute(circ, backend)
    job_monitor(job)
    counts_ibmq=job.result().get_counts()
    
    title="Counts for 3-qubit GHZ state on IBMQ backend " + backend.name()
    display(plot_histogram(counts_ibmq, title=title))

    # Display the results for all runs
    display(plot_histogram([counts, counts_noise, counts_noise_ibmq, counts_ibmq], bar_labels=True, legend=["Baseline","Noise on simulator", "Noise on IBMQ simulator", "IBM Q backend"], title="Comparison"))

while True:
    # Select backend
    back=select_backend()
    if back=="exit":
        break
    # Build noise model and then run the circuit
    noise=build_noise_model(back)
    execute_circuit(back, noise)
