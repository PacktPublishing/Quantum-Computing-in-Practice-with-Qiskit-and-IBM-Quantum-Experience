#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ, QuantumCircuit, execute
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

from IPython.core.display import display

print("Ch 6: Comparing backends")
print("------------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

# Cceate a Bell circuit 
qc = QuantumCircuit(2,2)

qc.h(0)
qc.cx(0,1)
qc.measure([0,1],[0,1])

print("\nQuantum circuit:")
print(qc)

# Get all available and operational backends.
backends = provider.backends(filters=lambda b: b.configuration().n_qubits > 1 and b.status().operational)

print("\nAvailable backends:", backends)

# Run the program on all backends and create a counts dictionary with the results from the executions.
counts = {}
for n in range(0, len(backends)):
    print('Run on:', backends[n])
    job = execute(qc, backends[n], shots=1000)
    job_monitor(job)
    result = job.result()
    counts[backends[n].name()] = result.get_counts(qc)

#Display the data that we want to plot.
print("\nRaw results:", counts)

#Optionally define the histogram colors. 
colors = ['green','darkgreen','red','darkred', 'orange','yellow','blue','darkblue','purple']

#Plot the counts dictionary values in a histogram, using the counts dictionary keys as legend.
display(plot_histogram(list(counts.values()), title = "Bell results on all available backends", legend=list(counts), color = colors[0:len(backends)], bar_labels = True))

