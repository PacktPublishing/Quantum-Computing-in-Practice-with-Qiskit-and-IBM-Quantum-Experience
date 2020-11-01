#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

# Import core IPython display method
from IPython.core.display import display

# The core Grover functions

def create_oracle(oracle_type,size):
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
    global qr, cr
    qr = QuantumRegister(size)
    cr = ClassicalRegister(size)
    oracleCircuit=QuantumCircuit(qr,cr)
    oracle_type_rev=oracle_type[::-1]
    oracleCircuit.h(qr[size-1])
    if size==2: 
        oracleCircuit.cx(qr[size-2],qr[size-1]);
    if size==3:
        oracleCircuit.ccx(qr[size-3],qr[size-2],qr[size-1])
    if size==4:
        oracleCircuit.mcx([qr[size-4],qr[size-3],qr[size-2]],qr[size-1])
    if size>=5:
        oracleCircuit.mcx([qr[size-5],qr[size-4],qr[size-3],qr[size-2]],qr[size-1])
    oracleCircuit.h(qr[size-1])
    for n in range(size-1,-1,-1):
        if oracle_type_rev[n] =="0":
            oracleCircuit.x(qr[n])
    return(oracleCircuit)

def create_amplifier(size):
    from qiskit import QuantumCircuit
    # Let's create the amplifier circuit for two qubits.
    amplifierCircuit=QuantumCircuit(qr,cr)
    amplifierCircuit.barrier(qr)
    amplifierCircuit.h(qr)
    amplifierCircuit.x(qr)
    amplifierCircuit.h(qr[size-1])
    if size==2: 
        amplifierCircuit.cx(qr[size-2],qr[size-1]);
    if size==3:
        amplifierCircuit.ccx(qr[size-3],qr[size-2],qr[size-1])
    if size==4:
        amplifierCircuit.mcx([qr[size-4],qr[size-3],qr[size-2]],qr[size-1])
    if size>=5:
        amplifierCircuit.mcx([qr[size-5],qr[size-4],qr[size-3],qr[size-2]],qr[size-1])
    amplifierCircuit.h(qr[size-1])
    amplifierCircuit.barrier(qr)
    amplifierCircuit.x(qr)
    amplifierCircuit.h(qr)
    return(amplifierCircuit)
    
def create_grover(oracleCircuit,amplifierCircuit,showstep):
    from qiskit import QuantumCircuit
    from math import sqrt, pow, pi
    groverCircuit = QuantumCircuit(qr,cr)
    # Initiate the Grover with Hadamards
    if showstep: display_circuit(groverCircuit,True,False)
    groverCircuit.h(qr)
    groverCircuit.barrier(qr)
    if showstep: display_circuit(groverCircuit,True,False)
    # Add the oracle and the inversion
    for n in range(int(pi/4*(sqrt(pow(2,oracleCircuit.num_qubits))))):
        groverCircuit+=oracleCircuit
        if showstep: display_circuit(groverCircuit,True,False)
        groverCircuit+=amplifierCircuit
        if showstep: display_circuit(groverCircuit,True,False)
    # Add measurements
    groverCircuit.measure(qr,cr)
    return(groverCircuit)

# The visualizarion functions
def print_psi(psi):
    if len(psi)==2:
        print("Statevector:\n", round(psi[0].real,3),"|0\u27E9 ", round(psi[1].real,3),"|1\u27E9 ")
    elif len(psi)==4:
        print("Statevector:\n", round(psi[0].real,3),"|00\u27E9 ", round(psi[1].real,3),"|01\u27E9 ", round(psi[2].real,3),"|10\u27E9 ", round(psi[3].real,3),"|11\u27E9 ")
    elif len(psi)==8:
        print("Statevector:\n", round(psi[0].real,3),"|000\u27E9 ", round(psi[1].real,3),"|001\u27E9 ", round(psi[2].real,3),"|010\u27E9 ", round(psi[3].real,3),"|011\u27E9 ", round(psi[4].real,3),"|100\u27E9 ", round(psi[5].real,3),"|101\u27E9 ", round(psi[6].real,3),"|110\u27E9 ", round(psi[7].real,3),"|111\u27E9 ")
    else:
        print("Statevector:\n", psi)

def get_psi(circuit, vis): 
    from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere
    from qiskit import Aer, execute
    global psi
    backend = Aer.get_backend('statevector_simulator') 
    psi = execute(circuit, backend).result().get_statevector(circuit)
    if vis=="Q":
        display(plot_state_qsphere(psi))
    elif vis=="M":
        print(psi)
    elif vis=="B":
        display(plot_bloch_multivector(psi))
    vis=""
    print_psi(psi)
    return(psi)
    
def print_unitary(circuit):
    from qiskit import BasicAer, execute
    import numpy
    numpy.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    
    backend = BasicAer.get_backend('unitary_simulator') 
    unit=execute(circuit, backend).result().get_unitary(circuit)
    print("Unitary matrix:\n")
    print(unit.real)
    
def display_circuit(circuit,psi,unitary):
    disp=True
    if disp:
        display(circuit.draw(output="mpl"))
        if psi:
            get_psi(circuit,"Q")
        if unitary:
            print_unitary(circuit)
            
# The execute functions
            
def get_backend(back):
    from qiskit import Aer, IBMQ
    from qiskit.providers.ibmq import least_busy
    if back=="IBMQ":
        global ibmqbackend 
        print("Loading IBMQ account...")
        IBMQ.load_account()
        print("Getting least busy backend...")
        provider = IBMQ.get_provider()
        ibmqbackend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))   
        backend = ibmqbackend 
    else:
        backend = Aer.get_backend('qasm_simulator')
    return(backend)                       

def run_grover(oracle_type,groverCircuit,backend):
    from qiskit import execute
    from qiskit.tools.visualization import plot_histogram
    from qiskit.tools.monitor import job_monitor
    print("Sending job to: "+str(backend.name()))
    shots = 8192
    job = execute(groverCircuit, backend, shots=shots)
    job_monitor(job)
    results = job.result()
    answer = results.get_counts()
    print("Grover search outcome for |"+str(oracle_type)+"\u27E9 oracle")
    title = "Grover on "+str(backend.name())
    display(plot_histogram(answer, title=title))
    return(results,backend)

def mitigated_results(backend,circuit,results,results_sim):
    from qiskit import Aer, execute
    from qiskit import QuantumRegister
    # Import the required classes
    from qiskit.providers.aer.noise import NoiseModel
    from qiskit.ignis.mitigation.measurement import (complete_meas_cal,CompleteMeasFitter)
    from qiskit.tools.visualization import plot_histogram
    import numpy
    numpy.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    
    # Get noise model for backend
    noise_model = NoiseModel.from_backend(backend)
    
    # Create the measurement fitter
    qr = QuantumRegister(circuit.num_qubits)
    meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal')
    job = execute(meas_calibs, backend=Aer.get_backend('qasm_simulator'), shots=8192, noise_model=noise_model)
    cal_results = job.result()
    meas_fitter = CompleteMeasFitter(cal_results, state_labels, circlabel='mcal')
    print(meas_fitter.cal_matrix)

    # Get the filter object
    meas_filter = meas_fitter.filter
    
    # Results with mitigation
    mitigated_results = meas_filter.apply(results)
    mitigated_counts = mitigated_results.get_counts(0)
    
    title = "Mitigated Grover on "+str(ibmqbackend.name())
    display(plot_histogram([results_sim.get_counts(),results.get_counts(), mitigated_counts], title=title, legend=['sim','noisy', 'mitigated']))
    return(mitigated_counts)

def transpile_circuit(circuit,backend):
    from qiskit.compiler import transpile
    trans_circ = transpile(circuit, backend)
    display(trans_circ.draw(output="mpl"))
    print("Circuit data\n\nDepth: ",trans_circ.depth(),"\nWidth: ",trans_circ.width(),"\nSize: ",trans_circ.size())


