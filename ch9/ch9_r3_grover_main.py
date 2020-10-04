#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 2020

@author: hassi
"""
# Import the required functions
from ch9_grover_functions import create_oracle, create_amplifier, create_grover, display_circuit, get_backend, run_grover, mitigated_results, transpile_circuit

# Main loop
def main():
    oracle_type=""
    ibmqbackend=""
    while oracle_type!=0:
        sample_oracle="1"
        print("\nCh 9: The Grover search algorithm ")
        print("----------------------------------")  
        size=int(input("Enter the number of qubits (2-5):\n"))
        if size>5: size=5
        for n in range(size-1):
            sample_oracle+="0"
        oracle_type=input("Input your "+str(size)+"-bit oracle. E.g: "+sample_oracle+":\n")
        oracle=create_oracle(oracle_type,size)
        print("Oracle circuit for |"+str(oracle_type)+"\u27E9")
        display_circuit(oracle,False, True)
        input("Press enter to create the amplifier circuit...")
        amplifier=create_amplifier(size)
        display_circuit(amplifier,False,True)
        input("Press enter to create the Grover circuit...")
        grover=create_grover(oracle,amplifier,True)
        display_circuit(grover,False,False)
        input("Press enter to run the Grover circuit...")
        sim_res=run_grover(oracle_type,grover,get_backend(""))
        answer=input("Enter 'Y' to run the Grover circuit on an IBMQ backend...")
        if answer in ["Y","y"]:
            ibmqbackend=get_backend("IBMQ")
            q_res=run_grover(oracle_type,grover,ibmqbackend)
            if size<4:
                input("Press enter to see the final, mitigated results")
                mitigated_results(ibmqbackend,grover,q_res[0],sim_res[0])
        input("Press enter to see the final, transpiled circuit")
        if not ibmqbackend:
            ibmqbackend=get_backend("IBMQ")
        transpile_circuit(grover, ibmqbackend)

if __name__ == '__main__':
    main()
