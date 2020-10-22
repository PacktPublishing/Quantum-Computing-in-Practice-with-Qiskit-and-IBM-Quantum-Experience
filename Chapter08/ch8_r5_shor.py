#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 12:20:21 2020

@author: hassi
"""

print('\nChapter 8: Shor Code')
print('---------------------')

from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

# Supporting methods
from math import pi
from random import random
from IPython.core.display import display

# Set the Aer simulator backend
backend = Aer.get_backend('qasm_simulator')

# Function that returns the state vector (Psi) for the qc
def get_psi(qc):
    global psi
    backend = Aer.get_backend('statevector_simulator') 
    result = execute(qc, backend).result()
    psi = result.get_statevector(qc)
    return(psi) 

# Function that adds an error to the first qubit
def add_error(error, circuit,ry_error, rz_error):
    circuit.barrier([x for x in range(circuit.num_qubits)])
    if error=="1": #Bit flip error
        circuit.x(0)
    elif error=="2": #Bit flip plus phase flip error
        circuit.x(0)
        circuit.z(0)
    else: #Theta plus phi shift and Random    
        circuit.ry(ry_error,0)
        circuit.rz(rz_error,0)
    circuit.barrier([x for x in range(circuit.num_qubits)])
    return(circuit)

def not_corrected(error, ry_error, rz_error):
    # Non-corrected code
    qco = QuantumCircuit(1,1)
    print("\nOriginal qubit, in state |0>")
    display(plot_bloch_multivector(get_psi(qco)))
    display(plot_state_qsphere(get_psi(qco)))
    # Add error
    add_error(error,qco, ry_error, rz_error)
    
   
    print("\nQubit with error...")
    display(plot_bloch_multivector(get_psi(qco)))
    display(plot_state_qsphere(get_psi(qco)))
    
    qco.measure(0,0)
    display(qco.draw('mpl'))
    
    job = execute(qco, backend, shots=1000)        
    counts = job.result().get_counts()
    
    print("\nResult of qubit error:")
    print("-----------------------")
    print(counts)

def shor_corrected(error, ry_error, rz_error):    
    # A combination of a three qubit phase flip code, and 3 bit flip codes
    
    qc = QuantumCircuit(9,1)
    
    print("\nOriginal LSB qubit, in state |...0>")
    display(plot_state_qsphere(get_psi(qc)))
    
    # Start of phase flip code
    qc.cx(0,3)
    qc.cx(0,6)
    
    qc.h(0)
    qc.h(3)
    qc.h(6)
    
    qc.barrier([x for x in range(qc.num_qubits)])
    
    # Start of bit flip codes
    qc.cx(0,1)
    qc.cx(3,4)
    qc.cx(6,7)
    
    qc.cx(0,2)
    qc.cx(3,5)
    qc.cx(6,8)
            
    # Error code
    add_error(error,qc, ry_error, rz_error)
    
    print("Qubit with error... LSB can be in |...0> and in |...1>, with various phase.")
    display(plot_state_qsphere(get_psi(qc)))
    display(qc.draw('mpl'))
    
    # End of bit flip codes

    qc.cx(0,1)
    qc.cx(3,4)
    qc.cx(6,7)
    
    qc.cx(0,2)
    qc.cx(3,5)
    qc.cx(6,8)
    
    qc.ccx(1,2,0)
    qc.ccx(4,5,3)
    qc.ccx(8,7,6)
    
    # End of phase flip code
    
    qc.h(0)
    qc.h(3)
    qc.h(6)
    
    qc.cx(0,3)
    qc.cx(0,6)
    qc.ccx(6,3,0)
    
    qc.barrier([x for x in range(qc.num_qubits)])

    qc.measure(0,0)
    
    print("Error corrected qubit... LSB in |...0> with phase 0.")
    display(plot_state_qsphere(get_psi(qc)))
    display(qc.draw('mpl'))
    
    job = execute(qc, backend, shots=1000)        
    counts = job.result().get_counts()
    
    print("\nResult of qubit error after Shor code correction:")
    print("--------------------------------------------------")
    print(counts)
    

def main():
    error="1"
    ry_error=0
    rz_error=0
    while error!="0":
        error=input("Select an error:\n1. Bit flip\n2. Bit flip plus phase flip\n3. Theta plus phi shift\n4. Random\n")
        if error=="3":
            ry_error=float(input("Enter theta:\n"))
            rz_error=float(input("Enter phi:\n"))
        if error=="4":
            ry_error=pi*random()
            rz_error=2*pi*random()
        not_corrected(error, ry_error, rz_error)
        input("Press enter for error correction...")
        shor_corrected(error, ry_error, rz_error)
       
if __name__ == '__main__':
    main()