#!/usr/bin/env python
# coding: utf-8#

# Import the required Qiskit classes
from qiskit import(QuantumCircuit, execute, Aer)

# Import Blochsphere visualization
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere
# Import some math that we will need
from  IPython.core.display import display

# Set numbers display options
import numpy as np
np.set_printoptions(precision=3)

# Create a function that requests and display the state vector
# Use this function as a diagnositc tool when constructing your circuits


def measure(circuit):
    measure_circuit=QuantumCircuit(circuit.width())
    measure_circuit+=circuit
    measure_circuit.measure_all()
    #print(measure_circuit)
    backend_count = Aer.get_backend('qasm_simulator') 
    counts=execute(measure_circuit, backend_count,shots=10000).result().get_counts(measure_circuit)    
    # Print the counts of the measured outcome.
    print("\nOutcome:\n",{k: v / total for total in (sum(counts.values())/100,) for k, v in counts.items()},"\n")

def s_vec(circuit):
    backend = Aer.get_backend('statevector_simulator') 
    print(circuit.num_qubits, "qubit quantum circuit:\n------------------------")
    print(circuit)
    psi=execute(circuit, backend).result().get_statevector(circuit)
    print("State vector for the",circuit.num_qubits,"qubit circuit:\n\n",psi)
    print("\nState vector as Bloch sphere:")
    display(plot_bloch_multivector(psi))
    print("\nState vector as Q sphere:")
    display(plot_state_qsphere(psi))
    measure(circuit)
    input("Press enter to continue...\n")
    
# Main loop
def main():
    user_input=1
    while user_input!=0:
        print("Ch 8: Running “diagnostics” with the state vector simulator")
        print("-----------------------------------------------------------")    
        user_input=int(input("\nNumber of qubits:\n"))
        circ_type=input("Superposition 's or entanglement 'e'?\n(To add a phase angle, use 'sp or 'ep'.)\n")
        if user_input>0:
            qc = QuantumCircuit(user_input)
            s_vec(qc)
            qc.h(user_input-1)
            s_vec(qc)
            if user_input>1:
                for n in range(user_input-1):
                    if circ_type in ["e","ep"]:
                        qc.cx(user_input-1,n)
                    else:
                        qc.h(n)
                    s_vec(qc)
                if circ_type in ["sp","ep"]:
                    qc.t(user_input-1)
                    s_vec(qc)

if __name__ == '__main__':
    main()