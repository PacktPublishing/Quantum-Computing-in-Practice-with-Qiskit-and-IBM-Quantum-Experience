#!/usr/bin/env python
# coding: utf-8

print("Ch 7: Understanding your circuits with the unitary simulator")
print("------------------------------------------------------=-----")

# Import the required Qiskit classes
from qiskit import(QuantumCircuit, execute, Aer)

# Import some math that we might need
from math import pow

import numpy as np
np.set_printoptions(precision=3)

# Create some circuits
def circuits():
    circuits=[]
    # Circuit 1 - one qubit in superposition
    circuit1 = QuantumCircuit(1,1)
    circuit1.h(0)
    # Circuit 2 - two qubits in superposition
    circuit2 = QuantumCircuit(2,2)
    circuit2.h([0,1])
    # Circuit 3 - two entangled qubits
    circuit3 = QuantumCircuit(2,2)
    circuit3.h([0])
    circuit3.cx(0,1)
    # Bundle the circuits in a list and return the list
    circuits=[circuit1,circuit2,circuit3]
    return(circuits)

# Get unitary matrix from unitary simulator 
def show_unitary(circuit):
    global unit
    backend = Aer.get_backend('unitary_simulator') 
    unit=execute(circuit, backend).result().get_unitary(circuit)
    print("Unitary matrix for the circuit:\n-------------------------------\n",unit)

# Calculate and display the unitary matrix 
def calc_unitary(circuit,unitary):
    # Set number of shots
    shots=1000
    # Calculate possible number of outcomes, 2^n qubits
    binary=int(pow(2,circuit.width()/2))    
    # Set the binary key for correct binary conversion
    bin_key='0'+str(int(circuit.width()/2))+'b'        
    # Create a qubit vector based on all qubits in the ground state |0> and a results list for all possible outcomes.
    vector=[1]
    outcomes=[format(0, bin_key)+":"]
    for q in range (1,binary):
        vector.append(0)
        outcomes.append(format(q, bin_key)+":")
    qubits=np.array(vector)    
    # Calculate the dot product of the unitary matrix and the qubits set by the qubits parameter.
    a_thru_d=np.dot(unitary,qubits)    
    # Print the probabilities (counts) of the calculated outcome.
    calc_counts={}
    for out in range (0,len(a_thru_d)):
        calc_counts[outcomes[out]]=(int(pow(abs(a_thru_d[out]),2)*shots))
    print("\nCalculated counts:\n------------------\n",calc_counts)    
    # Automate creation of measurement gates from number of qubits 
    # Run the circuit on the backend
    if circuit.width()==2:
        circuit.measure([0],[0])
    else: 
        circuit.measure([0,1],[0,1])
    backend_count = Aer.get_backend('qasm_simulator') 
    counts=execute(circuit, backend_count,shots=shots).result().get_counts(circuit)    
    # Print the counts of the measured outcome.
    print("\nExecuted counts:\n----------------\n",counts,"\n")

# Main loop
def main():
    user_input=1
    print("\nEnter the number for the circuit to explore:\n--------------------------------------------")
    while user_input!=0:
        print("\n0. Exit \n1. One qubit superposition\n2. Two qubit superposition\n3. Two qubit entanglement\n4. Import QASM from IBM Quantum Experience")
        user_input=int(input())
        if user_input!=0:
            if user_input==4:
                # From Qasm to Qiskit
                print("Paste a QASM string after stripping off any measurement gates:")
                qc = QuantumCircuit.from_qasm_str(input())
                print("\nImported circuit:\n-----------------")
            else:    
                circ=circuits()
                qc=circ[user_input-1]
                print("\nSelected circuit:\n-----------------")
            print(qc)
            show_unitary(qc)
            calc_unitary(qc,unit)
        else:
            print("Exiting")


if __name__ == '__main__':
    main()