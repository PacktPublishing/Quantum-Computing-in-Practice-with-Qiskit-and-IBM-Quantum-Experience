#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy


IBMQ.load_account()
provider = IBMQ.get_provider()


# Get all available and operational backends.
available_backends = provider.backends(operational=True)

# Fish out criteria to compare
print("{0:20} {1:<10} {2:<10} {3:<10}".format("Name","#Qubits","Max exp.","Pending jobs"))
print("{0:20} {1:<10} {2:<10} {3:<10}".format("----","-------","--------","------------"))

for n in range(0, len(available_backends)):
    backend = provider.get_backend(str(available_backends[n]))
    print("{0:20} {1:<10} {2:<10} {3:<10}".format(backend.name(),backend.configuration().n_qubits,backend.configuration().max_experiments,backend.status().pending_jobs))

# Select the least busy backend with 5 qubits

backend = least_busy(provider.backends(n_qubits=5,operational=True, simulator=False))

# Print out qubit properties for the backend.

print()
print("Qubit data for backend:",backend.status().backend_name)

for q in range (0, backend.configuration().n_qubits):
    print("Qubit",q,":")
    for n in range (0, len(backend.properties().qubits[0])):
        print(backend.properties().qubits[q][n].name,"=",backend.properties().qubits[q][n].value,backend.properties().qubits[q][n].unit)


