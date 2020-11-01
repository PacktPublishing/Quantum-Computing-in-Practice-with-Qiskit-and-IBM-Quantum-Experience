#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

#!/usr/bin/env python
# coding: utf-8

print("Loading Qiskit...")
from qiskit import QuantumCircuit, IBMQ
from qiskit.compiler import transpile
from qiskit.providers.ibmq import least_busy

from IPython.core.display import display

# Load account and find an available 5-qubit backend
print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

print("Getting backend...")
backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))

# Uncomment to set the backend to a simulator
#backend = provider.get_backend('ibmq_qasm_simulator')

print("Ch 6: Transpiling circuits")
print("--------------------------")

# Print the basis gates and coupling map for the selected backend
print("Basis gates for:", backend)
print(backend.configuration().basis_gates)
print("Coupling map for:", backend)
print(backend.configuration().coupling_map)

def build_circuit(choice):
    # Create the circuit 
    qc = QuantumCircuit(5,5)
    
    if choice=="1":
        # Simple X
        qc.x(0)
    elif choice=="2":
        # Add H
        qc.x(0)
        qc.h(0)
    elif choice=="3":
        # H + Barrier
        qc.x(0)
        qc.barrier(0)
        qc.h(0)
    elif choice=="4":
        # Controlled Y (CY)
        qc.cy(0,1)
    elif choice=="5":    
        # Non-conforming CX
        qc.cx(0,4)
    else:
        # Multi qubit circuit
        qc.h(0)
        qc.h(3)
        qc.cx(0,4)
        qc.cswap(3,1,2)

    # Show measurement targets
    #qc.barrier([0,1,2,3,4])
    #qc.measure([0,1,2,3,4],[0,1,2,3,4])

    return(qc)



def main(): 
    choice="1"
    while choice !="0": 
        choice=input("Pick a circuit: \n1. Simple X\n2. Add H\n3. H + Barrier\n4. Controlled-Y\n5. Non-conforming CX\n6. Multi-gate\n")
        qc=build_circuit(choice) 
        # Create the transpiled circuit
        trans_qc = transpile(qc, backend)
        
        # Print the original and transpiled circuits
        print("Circuit:")
        display(qc.draw())
        print("Transpiled circuit:")
        display(trans_qc.draw())
        
        # Print the original and transpiled circuit depths
        print("Circuit depth:")
        print("---------------")
        print("Circuit:", qc.depth())
        print("Transpiled circuit:", trans_qc.depth())
        
        # Print the original and transpiled circuit sizes
        print("\nCircuit size:")
        print("---------------")
        print("Circuit:", qc.size())
        print("Transpiled circuit:", trans_qc.size())

if __name__ == '__main__':
    main()