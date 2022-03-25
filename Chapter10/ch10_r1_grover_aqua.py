#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020, Updated March 2022

@author: hassi
"""

from qiskit import Aer, IBMQ

# Do the necessary import for our program

from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle

# Import basic plot tools
from qiskit.tools.visualization import plot_histogram

from IPython.core.display import display

global oracle_method, oracle_type


def log_length(oracle_input):
    from math import sqrt, pow, pi
    filtered = [c.lower() for c in oracle_input if c.isalpha()]
    result = len(filtered)
    num_iterations=int(pi/4*(sqrt(pow(2,result))))
    return num_iterations

def create_oracle(oracle_method):
    oracle_text={"log":"~A & ~B & C"}
    # set the input
    global num_iterations    
    print("Enter the oracle input string, such as:"+oracle_text[oracle_method]+"\nor enter 'def' for a default string.")
    oracle_input=input('\nOracle input:\n ')
    if oracle_input=="def":
        oracle_type=oracle_text[oracle_method]
    else:
        oracle_type = oracle_input
    num_iterations=log_length(oracle_type)
    print("Iterations: ", num_iterations)
    return(oracle_type)

def run_grover(oracle_type, oracle_method, backend):
    # Create and run the oracle on the selected backen
    oracle = PhaseOracle(oracle_type)
    problem = AmplificationProblem(oracle, is_good_state=oracle.evaluate_bitstring)
    algorithm = Grover(iterations=num_iterations, quantum_instance=QuantumInstance(backend, shots=1024))
    # Display the results
    result = algorithm.amplify(problem)
    display(plot_histogram(result.circuit_results[0]))
    print("Backend:",backend.name()+"\nResult:",result.top_measurement)
    

# Main loop
def main():
    # set the oracle method: "Log" for logical expression  
    oracle_method="log"
    while oracle_method!=0:
        print("Ch 11: Grover search with Aqua")
        print("------------------------------")    
        # Set the oracle type
        oracle_type=create_oracle(oracle_method)

        print("Oracle method:",oracle_method)
        print("Oracle for:", oracle_type)
        # Run on a simulator
        backend = Aer.get_backend('qasm_simulator')
        run_grover(oracle_type, oracle_method, backend)
        # Run the algorithm on an IBM Quantum backend
        print("Getting provider...")
        if not IBMQ.active_account():
            IBMQ.load_account()
        provider = IBMQ.get_provider()
        from qiskit.providers.ibmq import least_busy
        backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
        run_grover(oracle_type, oracle_method, backend)
    
if __name__ == '__main__':
    main()