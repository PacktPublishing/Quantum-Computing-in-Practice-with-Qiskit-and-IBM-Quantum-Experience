#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:21:15 2020

@author: hassi
"""

print("Ch 8: Qubit properties")
print("----------------------")

from qiskit import IBMQ

print("Getting providers...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

def select_backend():
    # Get all available and operational backends.
    print("Getting backends...")
    available_backends = provider.backends(filters=lambda b: not b.configuration().simulator and b.configuration().n_qubits > 0 and b.status().operational)
    # Fish out criteria to compare
    print("{0:20} {1:<10}".format("Name","#Qubits"))
    print("{0:20} {1:<10}".format("----","-------"))        
    for n in range(0, len(available_backends)):
        backend = provider.get_backend(str(available_backends[n]))
        print("{0:20} {1:<10}".format(backend.name(),backend.configuration().n_qubits))
    select_backend=input("Select a backend ('exit' to end): ")
    if select_backend!="exit":
        backend = provider.get_backend(select_backend)
    else:
        backend=select_backend
    return(backend)

def display_information(backend):
    basis_gates=backend.configuration().basis_gates
    n_qubits=backend.configuration().n_qubits
    if n_qubits>1:
        coupling_map=backend.configuration().coupling_map
    else:
        coupling_map=[]
    micro=10**6

    for qubit in range(n_qubits):
        print("\nQubit:",qubit)
        print("T1:",int(backend.properties().t1(qubit)*micro),"\u03BCs")
        print("T2:",int(backend.properties().t2(qubit)*micro),"\u03BCs")
        print("Readout error:",round(backend.properties().readout_error(qubit)*100,2),"%")
        for bg in basis_gates:
            if bg!="cx":
                if backend.properties().gate_length(bg,[qubit])!=0:
                    print(bg,round(backend.properties().gate_length(bg,[0])*micro,2),"\u03BCs", "Err:",round(backend.properties().gate_error(bg,[qubit])*100,2),"%") 
                else:    
                    print(bg,round(backend.properties().gate_length(bg,[0])*micro,2),"\u03BCs", "Err:",round(backend.properties().gate_error(bg,[qubit])*100,2),"%")
        if n_qubits>0:
            for cm in coupling_map:
                if qubit in cm:
                    print("cx",cm,round(backend.properties().gate_length("cx",cm)*micro,2),"\u03BCs", "Err:",round(backend.properties().gate_error("cx",cm)*100,2),"%")
    
# Main 
def main():
    backend=select_backend()
    display_information(backend)

if __name__ == '__main__':
    main()