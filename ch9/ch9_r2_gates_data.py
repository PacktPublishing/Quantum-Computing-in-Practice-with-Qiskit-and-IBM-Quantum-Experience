# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print("Ch 9: Qubit properties")
print("----------------------")

# Import Qiskit and load account
print("Loading Qiskit...")
from qiskit import IBMQ

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

#global available_backends

def select_backend():
    # Get all available and operational backends.
    print("Getting available backends...")
    available_backends = provider.backends(filters=lambda b: not b.configuration().simulator)
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

def qubit_details(backend):
    for n in range(len(backend.properties().qubits)):
        print("\nQubit",n)
        print("-------")
        print("Readout error:",round(backend.properties().readout_error(n)*100,2),"%")
        print("T1:", int(backend.properties().t1(n)*1000000),"\u03BCs")
        print("T2:",int(backend.properties().t2(n)*1000000),"\u03BCs")
        for m in range(len(backend.configuration().basis_gates)):
            gate = backend.configuration().basis_gates[m]
            if gate!="cx":
                print("\n",gate)
                print("Gate length:",round(backend.properties().gate_length(gate,[n])*1000000,2),"\u03BCs")
                print("Gate error:", round(backend.properties().gate_error(gate,[n])*100,2),"%")
    if len(backend.properties().qubits)>1:  
        print("\nCX gates")  
        print("---------")  
        for k in range(len(backend.configuration().coupling_map)):
            qubits=backend.configuration().coupling_map[k]
            print("\n", gate,qubits)
            print("Gate length:",round(backend.properties().gate_length(gate,qubits)*1000000,2),"\u03BCs")
            print("Gate error:", round(backend.properties().gate_error(gate,qubits)*100,2),"%")
    print("\n")
        
def main(): 
    backend=""
    while backend!="exit":
        backend=select_backend()
        if backend!="exit":
            qubit_details(backend)

    #print(backend.properties().qubits)

    #print(backend.configuration())

if __name__ == '__main__':
    main()