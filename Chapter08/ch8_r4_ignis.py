#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

print("Ch 8: Correct for the expected")
print("------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ, QuantumRegister, execute

from qiskit import QuantumCircuit
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from IPython.core.display import display

print("Getting providers...")
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
    select_backend=input("Select a backend ('exit' to end): ")
    if select_backend!="exit":
        backend = provider.get_backend(select_backend)
    else:
        backend=select_backend
    return(backend)

def create_circuit():
     #Create the circuit
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0,1)
    circuit.cx(0,2) 

    circuit.measure_all()
    print("Our circuit:")
    display(circuit.draw('mpl'))
    return(circuit)

def simulator_results(circuit):
    # Run the circuit on the local simulator
    job = execute(circuit, backend=Aer.get_backend('qasm_simulator'), shots=8192)
    job_monitor(job)
    results = job.result()
    sim_counts = results.get_counts()
    print("Simulator results:\n",sim_counts)
    return(sim_counts)

def noisy_results(circuit,backend):
    # Select backend and run the circuit
    
    job = execute(circuit, backend=backend, shots=8192)
    job_monitor(job)
    results = job.result()
    noisy_counts = results.get_counts()
    print(backend,"results:\n",noisy_counts)
    return(noisy_counts,results)

def mitigated_results(circuit,backend,results):
    # Import the required methods
    from qiskit.providers.aer.noise import NoiseModel
    from qiskit.ignis.mitigation.measurement import (complete_meas_cal,CompleteMeasFitter)
    
    # Get noise model for backend
    noise_model = NoiseModel.from_backend(backend)
    
    # Create the measurement fitter
    qr = QuantumRegister(circuit.num_qubits)
    meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')
    job = execute(meas_calibs, backend=Aer.get_backend('qasm_simulator'), shots=8192, noise_model=noise_model)
    cal_results = job.result()
    meas_fitter = CompleteMeasFitter(cal_results, state_labels, circlabel='mcal')
    #print(meas_fitter.cal_matrix)
    
    # Plot the calibration matrix
    print("Calibration matrix")
    meas_fitter.plot_calibration()
    
    # Get the filter object
    meas_filter = meas_fitter.filter
    
    # Results with mitigation
    mitigated_results = meas_filter.apply(results)
    mitigated_counts = mitigated_results.get_counts(0)
    print("Mitigated",backend,"results:\n",mitigated_counts)
    return(mitigated_counts)

def main():
    backend=select_backend()
    circ=create_circuit()
    sim_counts=simulator_results(circ)
    noisy_counts,results=noisy_results(circ,backend)
    # Analyze and error correct the measurements 
    mitigated_counts=mitigated_results(circ,backend,results)
        
    # Show all results as a comparison
    print("Final results:")
    display(plot_histogram([sim_counts, noisy_counts, mitigated_counts], legend=['sim','noisy', 'mitigated']))
       
if __name__ == '__main__':
    main()