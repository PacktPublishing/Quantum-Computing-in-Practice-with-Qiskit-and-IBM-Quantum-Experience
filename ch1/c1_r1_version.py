#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:59:25 2020

@author: hassi
"""
# Import Qiskit
import qiskit

# Set versions variable to the current Qiskit versions
versions=qiskit.__qiskit_version__

# Print the version number for the Qiskit components

print("Qiskit components and versions:")
print("===============================")
 
for i in versions:
    print (i, versions[i])