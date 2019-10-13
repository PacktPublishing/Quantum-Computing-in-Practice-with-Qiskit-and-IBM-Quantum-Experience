#!/usr/bin/env python
# coding: utf-8

# "Describing a quantum state by its density matrix is a fully general alternative formalism to describing a quantum state by its state vector (its "ket") or by a statistical ensemble of kets. However, in practice, it is often most convenient to use density matrices for calculations involving mixed states, and to use kets for calculations involving only pure states."
# 
# "Also, if a quantum system has two or more subsystems that are entangled, then each subsystem must be treated as a mixed state even if the complete system is in a pure state.[1] The density matrix is also a crucial tool in quantum decoherence theory."
# 
# https://people.eecs.berkeley.edu/~vazirani/f04quantum/notes/mixed.pdf

# In[1]:
print("Ch 8: Running “diagnostics” with the state vector simulator")
print("-----------------------------------------------------------")



# Import the required Qiskit classes
from qiskit import(
    QuantumCircuit,
    execute,
    Aer,
    IBMQ)

# Import Blochsphere visualization
from qiskit.visualization import *

# Import some math that we will need
from math import pi

# Set numbers display options
import numpy as np
np.set_printoptions(precision=3)


# In[4]:


# Create a function that requests and display the state vector
# Use this function as a diagnositc tool when constructing your circuits
backend = Aer.get_backend('statevector_simulator') 

def s_vec(circuit):
    print(circuit.n_qubits, "qubit quantum circuit:\n------------------------")
    print(circuit)
    psi=execute(circuit, backend).result().get_statevector(circuit)
    print("State vector for the",circuit.n_qubits,"qubit circuit:\n\n",psi)
    print("\nState vector as Bloch sphere.\n")
    display(plot_bloch_multivector(psi))
    print("\nState vector as Q sphere.")
    display(plot_state_qsphere(psi,figsize=(5,5)))
    input("Press enter to continue...\n")

# # One qubit states

# In[5]:


# One qubit states
qc = QuantumCircuit(1,1)
s_vec(qc)
qc.h(0)
s_vec(qc)
qc.rz(pi/2,0)
s_vec(qc)

# # Two qubit states

# In[7]:


# Two qubit states
qc = QuantumCircuit(2,2)
s_vec(qc)
qc.h([0])
s_vec(qc)
qc.swap(0,1)
s_vec(qc)

# # Entangled states

# In[8]:


# Entangled qubit states
qc = QuantumCircuit(2,2)
s_vec(qc)
qc.h(0)
s_vec(qc)
qc.cx(0,1)
s_vec(qc)
qc.rz(pi/4,0)
s_vec(qc)


# Notice how the Bloch sphere visualization doesn't lend itself very well to displaying entangled qubits, as they cannot be thought of as individual entities. And there is no good way of displaying multiple qubits on one Bloch sphere. A better option here is the density matrix, displayed as a state city.

# In[9]:


# Measuring entangled qubits
qc.measure([0,1],[0,1])
print("Running the",qc.n_qubits,"qubit circuit on the qasm_simulator:\n")
print(qc)
backend_count = Aer.get_backend('qasm_simulator') 
counts=execute(qc, backend_count,shots=10000).result().get_counts(qc)
print("Result:\n", counts)


