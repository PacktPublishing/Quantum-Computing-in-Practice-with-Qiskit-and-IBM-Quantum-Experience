#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""


print("Ch 7: IBM Q simulators and how they are used")
print("--------------------------------------------")

# Import Qiskit and load account
from qiskit import Aer, IBMQ

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()


# Load backends
backends=Aer.backends()
print("\nAer backends:\n\n",backends)


# Collect Aer simulators
simulators=[]
for sim in range(0,len(backends)):
    backend = Aer.get_backend(str(backends[sim]))
    simulators.append(backend.configuration())

# Add IBM Q simulator
ibmq_simulator=provider.backends(simulator=True)
simulators.append(provider.get_backend(str(ibmq_simulator[0])).configuration())

# Display the raw simulator configuration details
print("\nSimulator configuration details:")
for sim in range(0,len(simulators)):
    print("\n")
    print(simulators[sim].backend_name)
    print(simulators[sim].to_dict())
    
# Fish out criteria to compare
print("\n")
print("{0:25} {1:<10} {2:<10} {3:<10}".format("Name","#Qubits","Max shots.","Description"))
print("{0:25} {1:<10} {2:<10} {3:<10}".format("----","-------","--------","------------"))

description=[]
for sim in range(0,len(simulators)):
    if simulators[sim].local==True:
        description.append(simulators[sim].description)
    elif simulators[sim].local==False:
        description.append("Non-local IBM Q simulator")
    print("{0:25} {1:<10} {2:<10} {3:<10}".format(simulators[sim].backend_name,
                                                  simulators[sim].n_qubits,
                                                  simulators[sim].max_shots,
                                                  description[sim]))
