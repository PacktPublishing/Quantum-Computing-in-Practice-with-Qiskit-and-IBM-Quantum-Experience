#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram, plot_error_map

from IPython.core.display import display

print("Ch 6: Compare qubits")
print("--------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

backend = least_busy(provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 1 and b.status().operational))
print("Selected backend:",backend.status().backend_name)

# Pull out the gates information.
gates=backend.properties().gates

gate_type = "cx"
cx_best_worst = [[[0,0],1],[[0,0],0]]
for n in range (0, len(gates)):
    if gates[n].gate == gate_type:
        if gate_type == "cx":
            print(gates[n].name, ":", gates[n].parameters[0].name,"=", gates[n].parameters[0].value)
            if cx_best_worst[0][1]>gates[n].parameters[0].value:
                cx_best_worst[0][1]=gates[n].parameters[0].value
                cx_best_worst[0][0]=gates[n].qubits
            if cx_best_worst[1][1]<gates[n].parameters[0].value:
                cx_best_worst[1][1]=gates[n].parameters[0].value
                cx_best_worst[1][0]=gates[n].qubits
        else:
            print(gates[n].gate, gates[n].parameters[0].name,gates[n].parameters[0].value)

print("Best CX gate:", cx_best_worst[0][0], ",", round(cx_best_worst[0][1]*100,3),"%")
print("Worst CX gate:", cx_best_worst[1][0], ",", round(cx_best_worst[1][1]*100,3),"%")

# Display the error map for the selected backend
display(plot_error_map(backend))

# Create two circuits sized after the selected backend
q1 = QuantumRegister(backend.configuration().n_qubits)
c1 = ClassicalRegister(backend.configuration().n_qubits)
qc_best = QuantumCircuit(q1, c1)
qc_worst = QuantumCircuit(q1, c1)

#Best circuit
qc_best.h(q1[cx_best_worst[0][0][0]])
qc_best.cx(q1[cx_best_worst[0][0][0]], q1[cx_best_worst[0][0][1]])
qc_best.measure(q1[cx_best_worst[0][0][0]], c1[0])
qc_best.measure(q1[cx_best_worst[0][0][1]], c1[1])
print("Best CX:")
print(qc_best)

#Worst circuit
qc_worst.h(q1[cx_best_worst[1][0][0]])
qc_worst.cx(q1[cx_best_worst[1][0][0]], q1[cx_best_worst[1][0][1]])
qc_worst.measure(q1[cx_best_worst[1][0][0]], c1[0])
qc_worst.measure(q1[cx_best_worst[1][0][1]], c1[1])

print("Worst CX:")
print(qc_worst)

# Run the best and worst circuits on the backend
job_best = execute(qc_best, backend, shots=1000)
job_monitor(job_best)
job_worst = execute(qc_worst, backend, shots=1000)
job_monitor(job_worst)

# Create and run a benchmark circuit on a local simulator
q = QuantumRegister(backend.configuration().n_qubits)
c = ClassicalRegister(backend.configuration().n_qubits)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)

# Print the job results
best_result = job_best.result()
counts_best  = best_result.get_counts(qc_best)
print("Best qubit pair:")
print(counts_best)

worst_result = job_worst.result()
counts_worst  = worst_result.get_counts(qc_worst)
print("Worst qubit pair:")
print(counts_worst)

sim_result = job_sim.result()
counts_sim  = sim_result.get_counts(qc)
print("Simulated baseline:")
print(counts_sim)

# Display the job results for comparison
display(plot_histogram([counts_worst, counts_best, counts_sim],
  title = "Best and worst qubit pair for: " + backend.name(),
  legend     = ["Worst qubit pair","Best qubit pair","Simulated baseline"],             
  sort       = 'desc',
  figsize    = (15,12),
  color      = ['red','green', 'blue'],
  bar_labels = True))





