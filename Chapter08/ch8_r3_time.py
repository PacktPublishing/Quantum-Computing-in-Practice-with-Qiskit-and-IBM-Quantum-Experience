#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

print("Ch 8: How many gates do I have time for")
print("---------------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ, QuantumCircuit, execute
from qiskit.providers.aer.noise import NoiseModel
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from IPython.core.display import display

print("Getting providers...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()


def select_backend():
    # Get all available and operational backends.
    print("Getting backends...")
    available_backends = provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 0 and b.status().operational)
    # Fish out criteria to compare
    print("{0:20} {1:<10} {2:<10}".format("Name","#Qubits","Pending jobs"))
    print("{0:20} {1:<10} {2:<10}".format("----","-------","------------"))
    for n in range(0, len(available_backends)):
        backend = provider.get_backend(str(available_backends[n]))
        print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits),backend.status().pending_jobs)
    select_backend=input("Select a backend:\n")
    backend = provider.get_backend(select_backend)
    return(backend)

def display_information(backend,n_id,ttype):
    micro=10**6
    qubit=0
    T1=int(backend.properties().t1(qubit)*micro)
    T2=int(backend.properties().t2(qubit)*micro)
    id_len=backend.properties().gate_length("id",[0])*micro
    if ttype=="T1":
        T=T1
    else:
        T=T2
    print("\nBackend data:")
    print("\nBackend online since:",backend.configuration().online_date.strftime('%Y-%m-%d'))
    print("Qubit:",qubit)
    print("T1:",T1,"\u03BCs")
    print("T2:",T2,"\u03BCs")
    print("Readout error:",round(backend.properties().readout_error(qubit)*100,2),"%")
    print("Qubit",qubit,"Id length:",round(id_len,3),"\u03BCs") 
    print(ttype,"-id =", round(T-n_id*id_len,2),"\u03BCs",int((100*n_id*id_len)/T),"%")
    return(T)
        
def build_circuit(ttype,n_id):
    qc = QuantumCircuit(1,1)
    qc.x(0)
    if ttype in ["T2","t2"]:
        qc.h(0)
    for n in range(int(n_id)):
        qc.id(0)
        qc.barrier(0)
    if ttype in ["T2","t2"]:
        qc.h(0)
    qc.measure(0,0)
    return(qc)

def build_noise_model(backend):
    print("Building noise model...")
    # Construct the noise model from backend
    noise_model = NoiseModel.from_backend(backend)
    return(noise_model)
    
def execute_circuit(backend, circuit,noise_model, n_id):
    # Basis gates for the noise model
    basis_gates = noise_model.basis_gates
    # Coupling map
    coupling_map = backend.configuration().coupling_map 
    # Execute noisy simulation on QASM simulator and get counts
    noisy_counts = execute(circuit, Aer.get_backend('qasm_simulator'), noise_model=noise_model, coupling_map=coupling_map, basis_gates=basis_gates).result().get_counts(circuit)
    return(noisy_counts)

# Main 
def main():
    # Set the time type
    ttype="T1"
    # Select the backend to simulate or run on
    backend=select_backend()
    back_sim=input("Enter Q to run on the selected backend, S to run on the simulated backend:\n")
    if back_sim in ["Q","q"]:
        sim=False
    else:
        sim=True
        noise_model=build_noise_model(backend)
    n_id=int(input("Number of id gates:\n"))
    t=display_information(backend,n_id,ttype)
    qc=build_circuit(ttype,n_id)  
    # Print sample circuit
    print("\nSample 5-Id gate",ttype,"circuit:")
    display(build_circuit(ttype,5).draw('mpl'))

    # Run the circuit on a simulator
    job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=8192)
    results = job.result()
    sim_counts = results.get_counts()
    print("\nRunning:")
    print("Results for simulator:",sim_counts)
    # Run the circuit
    entry={'sim':sim_counts}
    legend=['sim']
    length=n_id
    while length!=0:
        qc=build_circuit(ttype,length)
        if sim:
            noisy_counts=execute_circuit(backend,qc,noise_model,length)
        else:
            job = execute(qc, backend=backend, shots=8192)
            job_monitor(job)
            results = job.result()
            noisy_counts = results.get_counts()
        print("Results for",length,"Id gates:",noisy_counts)
        entry.update({str(length):noisy_counts})
        legend.append(str(length))
        length=int(length/4)
    # Store  the results in an array
    results_array=[]
    for i in legend:
        results_array.append(entry[i])
    # Display the final results
    title="ID-circuits on "+str(backend)+" with "+ttype+"= "+str(t)+" \u03BCs"
    if sim:
        title+=" (Simulated)"
    title+=" \nOnline since: "+str(backend.configuration().online_date.strftime('%Y-%m-%d'))
    display(plot_histogram(results_array, legend=legend, title=title))

if __name__ == '__main__':
    main()
