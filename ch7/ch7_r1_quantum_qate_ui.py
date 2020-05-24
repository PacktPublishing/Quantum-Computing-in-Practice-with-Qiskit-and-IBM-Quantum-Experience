#!/usr/bin/env python
"""
User interface software that demonstrates the quantum gates
"""

# Import the required math
import numpy as np
import random #To create random state vector
import cmath #To juggle complex exponentials
from math import  sqrt,pi,sin,cos

# Import the required Qiskit classes
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

# Import Blochsphere visualization
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

# List our gates
rot_gates=["rx","ry","rz"]
unitary_gates=["u1","u2","u3"]
single_gates=["id","x","y","z","t","tdg","s","sdg","h"]+rot_gates
oneq_gates=single_gates+unitary_gates
control_gates=["cx","cy","cz","ch"]
twoq_gates=control_gates+["swap"]
all_gates=oneq_gates+twoq_gates+rot_gates+unitary_gates
# List our start states
start_states=["1","+","-","R","L","r","d"]
valid_start=["0"]+start_states

# Set the global angle parameters
global phi, theta, lam, start_theta, start_phi
phi=0.0
theta=0.0
lam=0.0

# Function that returns the state vector (Psi) for the circuit
def get_psi(circuit):
    global psi
    backend = Aer.get_backend('statevector_simulator') 
    result = execute(circuit, backend).result()
    psi = result.get_statevector(circuit)
    return(psi) 
        
# Function that returns the unitary of the circuit
def get_unitary(circuit):
    simulator = Aer.get_backend('unitary_simulator')
    result = execute(circuit, simulator).result()
    unitary = result.get_unitary(circuit)  
    return(unitary)      

# Function that creates a quantum circuit
def create_circuit(n_qubits,start):
    # Create the quantum circuit
    if start=="1":
        initial_vector = [0,complex(1,0)]
    elif start=="+":
        # Create |+> state
        initial_vector = [1/sqrt(2) * complex(1, 0), 1/sqrt(2) * complex(1, 0)]
    elif start=="-":
        # Create |-> state
        initial_vector = [1/sqrt(2) * complex(1, 0), -1/sqrt(2) * complex(1, 0)]
    elif start=="R":
        # Create |R> state
        initial_vector = [1/sqrt(2) * complex(1, 0), 1*1.j/sqrt(2) * complex(1, 0)]
    elif start=="L":
        # Create |L> state
        initial_vector = [1/sqrt(2) * complex(1, 0), -1*1.j/sqrt(2) * complex(1, 0)]
    elif start=="r":
        # Create random initial vector
        theta=random.random()*pi
        phi=random.random()*2*pi
        a = cos(theta/2)
        b = cmath.exp(phi*1j)*sin(theta/2)
        initial_vector = [a * complex(1, 0), b * complex(1, 0)]
    elif start=="d":
        '''
        # Specify initial vector
        theta=float(input("\u03D5:\n"))
        phi=float(input("\u03B8:\n"))
        '''
        a = cos(start_theta/2)
        b = cmath.exp(start_phi*1j)*sin(start_theta/2)
        initial_vector = [a * complex(1, 0), b * complex(1, 0)]
    else:
        initial_vector = [complex(1,0),0]

    if start!="n":
        print("\nInitial vector for |"+start+">:")
        print(np.around(initial_vector, decimals = 3))
        
    # Create the circuit
    circuit = QuantumCircuit(n_qubits)
    # If the start state is not |0> initialize the qubit
    if start in start_states:
        circuit.initialize(initial_vector,n_qubits-1)

    return(circuit)

# Function that creates the required outputs for the circuit
def qgate_out(circuit,start):
    # Print the circuit
    psi=get_psi(circuit)
    if start!="n":
        print("\nCircuit:")
        print("--------")
        print(circuit)
        print("\nState vector:")
        print("-------------")
        print(np.around(psi, decimals = 3))
        display(plot_bloch_multivector(psi))
        if circuit.num_qubits>1 and gate in control_gates:
            display(plot_state_qsphere(psi))
    return(psi)

# Function that adds a gate to a circuit  
def qgate(gate,start): 
    # If the gates require angles, add those to the QASM code
    qasm_angle_gates={"rx":"rx("+str(theta)+") q[0];", "ry":"ry("+str(theta)+") q[0];", "rz":"rz("+str(phi)+") q[0];", "u1":"u1("+str(phi)+") q[0];", "u2":"u2("+str(phi)+","+str(lam)+") q[0];", "u3":"u3("+str(theta)+","+str(phi)+","+str(lam)+") q[0];"}

    # Create the circuits and then add the gate using QASM import 
    if gate in oneq_gates:
        circuit=create_circuit(1,start)
        qasm_string='OPENQASM 2.0; include "qelib1.inc"; qreg q[1];'
    else: 
        circuit=create_circuit(2,start)
        qasm_string='OPENQASM 2.0; include "qelib1.inc"; qreg q[2];'
    qgate_out(circuit,start)
    
    if gate in oneq_gates:
        if gate in rot_gates+unitary_gates:
            circuit+=QuantumCircuit.from_qasm_str(qasm_string+qasm_angle_gates[gate])
        else:
            circuit+=QuantumCircuit.from_qasm_str(qasm_string+gate+" q[0];")
    else:
        circuit+=QuantumCircuit.from_qasm_str(qasm_string+gate+" q[1],q[0];")
    
    return(circuit)


# Main navigation
print("Visualizing the quantum gates")
print("-----------------------------")
gate=""

while gate !="exit":    
    # Set up the start conditions
    start=input("Start state:\n0. |0\u27E9 \n1. |1\u27E9 \n+. |+\u27E9\n-. |-\u27E9\nR. |R\u27E9\nL. |L\u27E9\nr. Random (a|0\u27E9 + b|1\u27E9)\nd. Define (\u03B8 and \u03D5)\n")
    if start =="d":
        # Specify initial vector
        start_theta=float(input("Enter start \u03B8:\n"))
        start_phi=float(input("Enter start \u03D5:\n"))
    # Select a gate
    print("Enter a gate:\nAvailable gates:\n",all_gates)
    gate=input()
    if gate in ["rx", "ry","u3"]:
        theta=input("Enter rotation (\u03B8):\n")
    if gate in ["u1","u2","u3","rz",]:
        phi=input("Enter rotation (\u03D5):\n")
    if gate in ["u2","u3"]:
        lam=input("Enter rotation (\u03BB):\n")
    if gate in all_gates and start in valid_start:
        # Display the gate unitary for a blank circuit
        blank_qc=qgate(gate,"n")
        print("\nUnitary for the " + gate + " gate:\n")
        print(np.around(get_unitary(blank_qc), decimals = 3))
        # Build the quantum circuit for the gate
        input("Press Enter to see the start setup...")
        qc=qgate(gate, start)
        # Visualize the circuit and the qubit(s)
        input("Press Enter to see the result after the "+gate+" gate...")
        qgate_out(qc,start)
        input("Press Enter to test another gate...")

    else:
        if start not in valid_start:
            print("Not a valid start state.")
        if gate not in all_gates:
            print("Not a valid gate.")
        print("Try again...")


