#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020
Updated March 2023

@author: hassi
"""


from qiskit import QuantumCircuit, execute, Aer

from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

# Import image and file processing tools
from PIL import Image
import os

print("Ch 6: Animating the U gate")
print("-------------------------")

# This program requires an /images directory at the same location as the script.
dirName = 'images'
print("Checking if /images directory exists...")
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory" , dirName ,  "created ")
else:    
    print("Directory" , dirName ,  "exists")


def get_psi(circuit):
    global psi
    backend = Aer.get_backend('statevector_simulator') 
    result = execute(circuit, backend).result()
    psi = result.get_statevector(circuit)
    return(psi) 

def create_images(theta=0.0,phi=0.0,lam=0.0):
    # Set the loop parameters
    steps=20.0
    theta_steps=theta/steps
    phi_steps=phi/steps
    lam_steps=lam/steps
    n, theta,phi,lam=0,0.0,0.0,0.0
    # Create image and animation tools
    global q_images, b_images, q_filename, b_filename
    b_images=[]
    q_images=[]
    b_filename="animated_qubit"
    q_filename="animated_qsphere"

    # The image creation loop
    while n < steps+1:
        qc=QuantumCircuit(1)
        qc.u(theta,phi,lam,0)
        title="U: \u03B8 = "+str(round(theta,2))+" \u03D5 = "+str(round(phi,2))+" \u03BB = "+str(round(lam,2))

        # Get the statevector of the qubit 
        # Create Bloch sphere images
        plot_bloch_multivector(get_psi(qc),title).savefig('images/bloch'+str(n)+'.png')
        imb = Image.open('images/bloch'+str(n)+'.png')
        b_images.append(imb)
        # Create Q sphere images
        plot_state_qsphere(psi).savefig('images/qsphere'+str(n)+'.png')
        imq = Image.open('images/qsphere'+str(n)+'.png')
        q_images.append(imq)
        # Rev our loop
        n+=1
        theta+=theta_steps
        phi+=phi_steps
        lam+=lam_steps

# Create and save the animated GIFs
def save_gif(gate):
    duration=100
    b_images[0].save('U_'+b_filename+'.gif',
               save_all=True,
               append_images=b_images[1:],
               duration=duration,
               loop=0)
    q_images[0].save('U_'+q_filename+'.gif',
               save_all=True,
               append_images=q_images[1:],
               duration=duration,
               loop=0)
    print("Bloch sphere animation saved as: \n"+os.getcwd()+"/"+gate+"_"+b_filename+".gif"+"\nQsphere animation saved as: \n"+os.getcwd()+"/"+gate+"_"+q_filename+".gif")

# Main loop
def main(): 
    global gate
    gate=""
    theta=0.0
    phi=0.0
    lam=0.0
    while gate !="exit": 
        print("Enter U-gate rotation angles:")
        theta=float(input("Enter \u03B8:\n"))
        phi=float(input("Enter \u03D5:\n"))
        lam=float(input("Enter \u03BB:\n"))
        print("Building animation...")
        create_images(theta,phi,lam)
        save_gif(gate)

            
if __name__ == '__main__':
    main()