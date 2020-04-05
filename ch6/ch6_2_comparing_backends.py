#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

IBMQ.load_account()
provider = IBMQ.get_provider()

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)
qc.h(q[0])
qc.cx(q[0],q[1])
qc.measure(q, c)
print(qc)

# Get all available and operational backends.
backends = provider.backends(filters=lambda b: b.configuration().n_qubits > 1 and b.status().operational)

print("Available backends:", backends)

# Run the program on all backends and create a counts dictionary with the results from the executions.
counts = {}
for n in range(0, len(backends)):
    print('Run on:', backends[n])
    job = execute(qc, backends[n], shots=1000)
    job_monitor(job)
    result = job.result()
    counts[backends[n].name()] = result.get_counts(qc)

#Display the data that we want to plot.
print("Raw results:", counts)

#Optionally define the histogram colors. 
colors = ['green','red','darkred', 'orange','yellow','blue','darkblue','purple']

#Plot the counts dictionary values in a histogram, using the counts dictionary keys as legend.
plot_histogram(list(counts.values()), title = "Bell results on all available backends", legend=list(counts), color = colors[0:len(backends)], bar_labels = True)

