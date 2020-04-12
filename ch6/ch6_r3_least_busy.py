#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

IBMQ.load_account()
provider = IBMQ.get_provider()

backend = least_busy(provider.backends(simulator=False))
filtered_backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))


print("Least busy backend:", backend.name())
print("Least busy 5-qubit backend:", filtered_backend.name())

from qiskit.tools.monitor import backend_overview
backend_overview()
