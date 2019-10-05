#!/usr/bin/env python
# coding: utf-8

print("Ch 8: Adding the noise profile of an IBM Q machine to your local simulator")
print("--------------------------------------------------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ, execute

from qiskit.providers.aer import noise
from qiskit import QuantumCircuit
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

import numpy as np
np.set_printoptions(precision=3)

IBMQ.load_account()
provider = IBMQ.get_provider()

# Get all available and operational backends.
available_backends = provider.backends(operational=True, simulator=False)

# Fish out criteria to compare
print("{0:20} {1:<10} {2:<10}".format("Name","#Qubits","Pending jobs"))
print("{0:20} {1:<10} {2:<10}".format("----","-------","------------"))

for n in range(0, len(available_backends)):
    backend = provider.get_backend(str(available_backends[n]))
    print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits),backend.status().pending_jobs)

select_backend=input("Select a backend: ")

backend = provider.get_backend(select_backend)

properties = backend.properties()
coupling_map = backend.configuration().coupling_map
print(coupling_map)

gates=backend.properties().gates
print(gates)

gate_type = "cx"
gate_times = [('u1', None, 0), ('u2', None, 100), ('u3', None, 200)]
print("The gate errors for the",backend,"backend:\n")
for n in range (0, len(gates)):
    if gates[n].gate == gate_type:
        print(gates[n].name, ":", gates[n].parameters[0].name,"=", f'{(gates[n].parameters[0].value*100):.3f}',"%")
        if (len(gates[n].parameters)) >1:            
            gate_times.append((gates[n].gate,gates[n].qubits,int(gates[n].parameters[1].value)))
if (len(gates[n].parameters)) >1:
    print("\nThe gate times for the",backend,"backend:\n")
else:
    print("\nThe",backend,"backend did not return gate times\n-------------------------------")

print(gate_times)

# Construct quantum circuit
circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure([0,1], [0,1])

# Select simulator backend
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
result = execute(circ, simulator).result()
counts = result.get_counts(circ)
display(plot_histogram(counts, title='Ideal counts for 2-qubit Bell state'))


# Construct the noise model from backend properties and custom gate times

noise_model = noise.device.basic_device_noise_model(properties, gate_times=gate_times)

print(noise_model)

# Get the basis gates for the noise model
basis_gates = noise_model.basis_gates

# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute noisy simulation and get counts
result_noise = execute(circ, simulator, 
                       noise_model=noise_model,
                       coupling_map=coupling_map,
                       basis_gates=basis_gates).result()
counts_noise = result_noise.get_counts(circ)
display(plot_histogram(counts_noise, title="Counts for 2-qubit Bell state with depolarizing noise model"))

# Select the ibmq_qasm_simulator from the IBMQ provider
simulator = provider.get_backend('ibmq_qasm_simulator')

# Execute noisy simulation and get counts
result_noise = execute(circ, simulator, 
                       noise_model=noise_model,
                       coupling_map=coupling_map,
                       basis_gates=basis_gates).result()
counts_noise_ibmq = result_noise.get_counts(circ)
display(plot_histogram(counts_noise_ibmq, title="Counts for 2-qubit Bell state with depolarizing noise model on IBMQ qasm simulator"))


# Execute job on IBM Q backend and get counts
job = execute(circ, backend)
job_monitor(job)

counts_ibmq=job.result().get_counts()

title="2-qubit Bell state on IBMQ backend " + select_backend
display(plot_histogram(counts_ibmq, title=title))

# Display the results for all runs
display(plot_histogram([counts, counts_noise, counts_noise_ibmq, counts_ibmq], bar_labels=True, legend=["Baseline","Noise on simulator", "Noise on IBMQ simulator", "IBM Q backend"], title="Comparison"))

