#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

# https://qiskit.org/documentation/stubs/qiskit.aqua.algorithms.Shor.html#qiskit.aqua.algorithms.Shor


from qiskit import Aer, IBMQ
from qiskit.aqua.algorithms import Shor
import time

def display_shor(N):
    print("Building Shor circuit...")
    shor_circuit = Shor(N=N).construct_circuit()
    print(shor_circuit)
    print("Circuit data\n\nDepth: ",shor_circuit.depth(),"\nWidth: ",shor_circuit.width(),"\nSize: ",shor_circuit.size())

def run_shor(N):
    if N<=64: #Arbitrarily set upper limit for local simulator    
        print("Getting local simulator backend...")
        backend = Aer.get_backend('qasm_simulator')
    else:
        print("Getting provider...")
        if not IBMQ.active_account():
            IBMQ.load_account()
        provider = IBMQ.get_provider()
        print("Getting IBM Q simulator backend...")
        backend = provider.get_backend('ibmq_qasm_simulator')
    print("Running Shor's algorithm for",str(N),"on", backend,"...")
    results=Shor(N=N).run(backend)
    print("\nResults:")
    if results['factors']==[]:
        print("No prime factors: ",str(N),"=",str(N))
    elif isinstance(results['factors'][0],int):
        print("Prime factors: ",str(N),"=",results['factors'][0],"^ 2")
    else:
        print("Prime factors: ",str(N),"=",results['factors'][0][0],"*",results['factors'][0][1])

def main():
    number=1
    print("\nCh 11: Shor's algorithm with Aqua")     
    print("---------------------------------")   
    while number!=0:
        number=int(input("\nEnter an odd number N >1 (0 to exit):\n"))
        if number>1 and number % 2>0:
            type=input("Enter R to run the Shor algorithm, D to display the circuit.\n")
            start_time=time.time()
            if type.upper()=="D":
                display_shor(number)
            elif type.upper()=="R":
                run_shor(number)
            elif type.upper() in ["RD","DR"]:
                display_shor(number)
                run_shor(number)
            end_time=time.time()
            print("Elapsed time: ","%.2f" % (end_time-start_time), "s")
        else:
            print("The number must be odd and larger than 1.")

if __name__ == '__main__':
    main()