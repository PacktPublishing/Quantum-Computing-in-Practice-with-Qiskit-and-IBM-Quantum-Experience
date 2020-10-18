#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram,plot_error_map
from qiskit.compiler import transpile


from IPython.core.display import display

print("Ch 9: Comparing qubits on a chip")
print("--------------------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()


def select_backend():
    # Get all available and operational backends.
    available_backends = provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 1 and b.status().operational)
    # Fish out criteria to compare
    print("{0:20} {1:<10} {2:<10}".format("Name","#Qubits","Pending jobs"))
    print("{0:20} {1:<10} {2:<10}".format("----","-------","------------"))        
    for n in range(0, len(available_backends)):
        backend = provider.get_backend(str(available_backends[n]))
        print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits),backend.status().pending_jobs)
    select_backend=input("Select a backend ('LB' for least busy): ")
    if select_backend not in ["LB","lb"]:
        backend = provider.get_backend(str(select_backend))
    else:
        from qiskit.providers.ibmq import least_busy
        backend = least_busy(provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 1 and b.status().operational))
    print("Selected backend:",backend.status().backend_name)
    return(backend)

def get_gate_info(backend):
    # Pull out the gates information.
    gates=backend.properties().gates
    
    #Cycle through the CX gate couplings to find the best and worst 
    cx_best_worst = [[[0,0],1],[[0,0],0]]
    for n in range (0, len(gates)):
        if gates[n].gate ==  "cx":
            print(gates[n].name, ":", gates[n].parameters[0].name,"=", gates[n].parameters[0].value)
            if cx_best_worst[0][1]>gates[n].parameters[0].value:
                cx_best_worst[0][1]=gates[n].parameters[0].value
                cx_best_worst[0][0]=gates[n].qubits
            if cx_best_worst[1][1]<gates[n].parameters[0].value:
                cx_best_worst[1][1]=gates[n].parameters[0].value
                cx_best_worst[1][0]=gates[n].qubits
    print("Best cx gate:", cx_best_worst[0][0], ",", round(cx_best_worst[0][1]*100,3),"%")
    print("Worst cx gate:", cx_best_worst[1][0], ",", round(cx_best_worst[1][1]*100,3),"%")
    display(plot_error_map(backend, show_title=True))
    return(cx_best_worst)

def create_circuits(backend, cx_best_worst):
    print("Building circuits...")
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
    display(qc_best.draw('mpl'))
    trans_qc_best = transpile(qc_best, backend)
    print("Transpiled qc_best circuit:")
    display(trans_qc_best.draw())


    #Worst circuit
    qc_worst.h(q1[cx_best_worst[1][0][0]])
    qc_worst.cx(q1[cx_best_worst[1][0][0]], q1[cx_best_worst[1][0][1]])
    qc_worst.measure(q1[cx_best_worst[1][0][0]], c1[0])
    qc_worst.measure(q1[cx_best_worst[1][0][1]], c1[1])
    
    print("Worst CX:")
    display(qc_worst.draw('mpl'))
    
    return(qc_best,qc_worst)

def compare_cx(backend,qc_best,qc_worst):
    print("Comparing CX pairs...")

    job_best = execute(qc_best, backend, shots=8192)
    job_monitor(job_best)
    job_worst = execute(qc_worst, backend, shots=8192)
    job_monitor(job_worst)
    
    q = QuantumRegister(backend.configuration().n_qubits)
    c = ClassicalRegister(backend.configuration().n_qubits)
    qc = QuantumCircuit(q, c)
    
    qc.h(q[0])
    qc.cx(q[0], q[1])
    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    
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
    
    display(plot_histogram([counts_best, counts_worst, counts_sim],
                           title = "Best and worst qubit pair for: " + backend.name(),
                           legend     = ["Best qubit pair","Worst qubit pair","Simulated baseline"],
                           sort       = 'desc',
                           figsize    = (15,12),
                           color      = ['green', 'red','blue'],
                           bar_labels = True))

def main():
    backend=select_backend()
    cx_best_worst=get_gate_info(backend)
    qc_best, qc_worst=create_circuits(backend, cx_best_worst)
    compare_cx(backend,qc_best,qc_worst)
       
if __name__ == '__main__':
    main()