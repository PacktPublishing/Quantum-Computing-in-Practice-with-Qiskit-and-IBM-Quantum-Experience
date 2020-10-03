#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

print("Ch 6: Least busy backend")
print("------------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

# Finding the least busy backend
backend = least_busy(provider.backends(operational=True, simulator=False))
print("Least busy backend:", backend.name())

filtered_backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
print("\nLeast busy 5-qubit backend:", filtered_backend.name())

from qiskit.tools.monitor import backend_overview
print("\nAll backends overview:\n")
backend_overview()
