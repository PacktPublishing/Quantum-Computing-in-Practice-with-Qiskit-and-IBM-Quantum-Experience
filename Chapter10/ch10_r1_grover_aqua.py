#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

from qiskit import Aer, IBMQ

# Do the necessary import for our program
#from qiskit.utils.algorithms import Grover
from qiskit.algorithms import Grover, AmplificationProblem
#from qiskit.aqua.components.oracles import LogicalExpressionOracle, TruthTableOracle, AmplificationProblem
from qiskit.aqua.components.oracles import TruthTableOracle 
from qiskit.circuit.library import PhaseOracle

# Import basic plot tools
from qiskit.tools.visualization import plot_histogram

from IPython.core.display import display

global oracle_method, oracle_type


def log_length(oracle_input,oracle_method):
    from math import sqrt, pow, pi, log
    if oracle_method=="log":
        filtered = [c.lower() for c in oracle_input if c.isalpha()]
        result = len(filtered)
        num_iterations=int(pi/4*(sqrt(pow(2,result))))
    else:
        num_iterations = int(pi/4*(sqrt(pow(2,log(len(oracle_input),2)))))
    print("Iterations: ", num_iterations)
    return num_iterations

def create_oracle(oracle_method):
    oracle_text={"log":"~A & ~B & C","bit":"00001000"}
    # set the input
    global num_iterations    
    print("Enter the oracle input string, such as:"+oracle_text[oracle_method]+"\nor enter 'def' for a default string.")
    oracle_input=input('\nOracle input:\n ')
    if oracle_input=="def":
        oracle_type=oracle_text[oracle_method]
    else:
        oracle_type = oracle_input
    num_iterations=log_length(oracle_type, oracle_method)
    return(oracle_type)

def create_grover(oracle_type, oracle_method):
    # Build the circuit
    if oracle_method=="log":
        #algorithm = Grover(LogicalExpressionOracle(oracle_type),num_iterations=num_iterations)
        algorithm = Grover(PhaseOracle(oracle_type))
        #problem = AmplificationProblem(num_iterations=num_iterations)
        oracle_circuit = Grover(PhaseOracle(oracle_type)).construct_circuit()
    else:
        #algorithm = Grover(TruthTableOracle(oracle_type),num_iterations=num_iterations)
        algorithm = Grover(TruthTableOracle(oracle_type))
        #problem = AmplificationProblem(num_iterations=num_iterations)
        oracle_circuit = Grover(TruthTableOracle(oracle_type)).construct_circuit()

    display(oracle_circuit.draw(output="mpl"))
    display(algorithm)
    return(algorithm)
    #return(algorithm, problem)

def run_grover(algorithm,oracle_type,oracle_method):
    # Run the algorithm on a simulator, printing the most frequently occurring result

    backend = Aer.get_backend('qasm_simulator')
    result = algorithm.run(backend)
    print("Oracle method:",oracle_method)
    print("Oracle for:", oracle_type)
    print("Aer Result:",result['top_measurement'])
    display(plot_histogram(result['measurement']))
    
    # Run the algorithm on an IBM Q backend, printing the most frequently occurring result
    print("Getting provider...")
    if not IBMQ.active_account():
        IBMQ.load_account()
    provider = IBMQ.get_provider()
    from qiskit.providers.ibmq import least_busy
    
    filtered_backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
        
    result = algorithm.run(filtered_backend)

    print("Oracle method:",oracle_method)
    print("Oracle for:", oracle_type)
    print("IBMQ "+filtered_backend.name()+" Result:",result['top_measurement'])
    display(plot_histogram(result['measurement']))

    print(result)

# Main loop
def main():
    oracle_method="log"
    while oracle_method!=0:
        print("Ch 11: Grover search with Aqua")
        print("------------------------------")    
        # set the oracle method: "Log" for logical expression or "Bit" for bit string. 
        oracle_method = input("Select oracle method (log or bit):\n")
        type=create_oracle(oracle_method)
        algorithm=create_grover(type, oracle_method)
        run_grover(algorithm,type, oracle_method)
    
if __name__ == '__main__':
    main()