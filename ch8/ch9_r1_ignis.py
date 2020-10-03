# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print("Ch 9: Ignis 1")
print("--------------------------------------------------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ, QuantumRegister, execute

#from qiskit.providers.aer import noise
from qiskit import QuantumCircuit
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from IPython.core.display import display

import numpy as np
np.set_printoptions(precision=3)

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

def mitigated_results(backend,circuit,results):
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
    print(meas_fitter.cal_matrix)
    meas_fitter.plot_calibration()
    # Get the filter object
    meas_filter = meas_fitter.filter
    
    # Results with mitigation
    mitigated_results = meas_filter.apply(results)
    mitigated_counts = mitigated_results.get_counts(0)

    return(mitigated_counts)


qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0,1)
qc.cx(0,2) 
#qc.h(3)
#qc.cx(3,4) 
qc.measure_all()
display(qc.draw('mpl'))

job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=8192)
job_monitor(job)
results = job.result()
sim_counts = results.get_counts()
print(sim_counts)


backend=select_backend()
job = execute(qc, backend=backend, shots=8192)
job_monitor(job)
results = job.result()
noisy_counts = results.get_counts()
print(noisy_counts)

mitigated_counts=mitigated_results(backend,qc,results)


print(mitigated_counts)


display(plot_histogram([sim_counts, noisy_counts, mitigated_counts], legend=['sim','noisy', 'mitigated']))
