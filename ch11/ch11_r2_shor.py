#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 20:25:05 2020

@author: hassi
"""

# https://qiskit.org/documentation/stubs/qiskit.aqua.algorithms.Shor.html#qiskit.aqua.algorithms.Shor


from qiskit import Aer, IBMQ
from qiskit.aqua.algorithms import Shor

def display_shor(N):
    print("Building Shor circuit...")
    shor_circuit = Shor(N=N, a=2).construct_circuit()
    print(shor_circuit)
    print("Circuit data\n\nDepth: ",shor_circuit.depth(),"\nWidth: ",shor_circuit.width(),"\nSize: ",shor_circuit.size())

def run_shor(N):
    if N<=20: #Arbitrarily set upper limit for local simulator    
        print("Getting local simulator backend...")
        backend = Aer.get_backend('qasm_simulator')
    else:
        print("Loading account...")
        IBMQ.load_account()
        provider = IBMQ.get_provider()
        print("Getting IBM Q simulator backend...")
        backend = provider.get_backend('ibmq_qasm_simulator')
    print("Running Shor's algorithm for",str(N),"on", backend,"...")
    results=Shor(N=N, a=2).run(backend)
    print("\nResults:")
    if results['factors']==[]:
        print("No prime factors: ",str(N),"=",str(N))
    elif isinstance(results['factors'][0],int):
        print("Prime factors: ",str(N),"=",results['factors'][0],"^ 2")
    else:
        print("Prime factors: ",str(N),"=",results['factors'][0][0],"*",results['factors'][0][1])

def main():
    number=1
    while number!=0:
        print("\nCh 11: Shor's algorithm with Aqua")
        print("---------------------------------")    
        number=int(input("\nEnter an odd number >1:\n"))
        if number>0:
            type=input("Enter R to run the Shor algorithm, D to display the circuit.\n")
            if type.upper()=="D":
                display_shor(number)
            elif type.upper()=="R":
                run_shor(number)
            elif type.upper() in ["RD","DR"]:
                run_shor(number)
                display_shor(number)

if __name__ == '__main__':
    main()