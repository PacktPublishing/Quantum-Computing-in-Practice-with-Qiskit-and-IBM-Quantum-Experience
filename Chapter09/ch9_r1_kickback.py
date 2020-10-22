#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 2020

@author: hassi
"""

# Importing Qiskit
from qiskit import QuantumCircuit
# Import display circuit from our Grover collection
from ch9_grover_functions import display_circuit

def main():
    # First, let's see a phase shift
    print("Ch 9: Phase kickback")
    print("--------------------")

    print("\nLet's start with initalizing a single qubit to |0>...")
    qc1 = QuantumCircuit(1)
    display_circuit(qc1,True,False)

    input("Press Enter to set the qubit in superposition...")
    qc1.h(0)
    display_circuit(qc1,True,False)

    input("Press Enter to add a phase shift...")
    qc1.z(0)
    display_circuit(qc1,True,False)

    input("Press Enter to create a two qubit circuit...")
    qc = QuantumCircuit(2)
    display_circuit(qc,True,False)

    input("Press Enter to set qubits in superposition...")
    qc.h([0,1])
    display_circuit(qc,True,False)

    input("Press Enter to phase shift second qubit using Z gate...")
    qc.z(1)
    display_circuit(qc,True,False)

    input("Press Enter to phase shift first qubit using Z gate...")
    qc.z(0)
    display_circuit(qc,True,False)

    input("Press Enter to create a new circuit...")
    qc = QuantumCircuit(2)
    display_circuit(qc,True,False)

    input("Press Enter to set qubits in superposition...")
    qc.h([0,1])
    qc.barrier([0,1])
    display_circuit(qc,True,False)

    input("Press Enter to phase shift second qubit using Z gate...")
    qc.z(1)
    display_circuit(qc,True,False)

    input("Press Enter to add a CX...")
    qc.cx(0,1)
    display_circuit(qc,True,False)

if __name__ == '__main__':
    main()
