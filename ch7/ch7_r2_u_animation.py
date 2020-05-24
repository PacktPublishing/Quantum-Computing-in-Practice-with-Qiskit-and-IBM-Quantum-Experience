## !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:41:46 2020

@author: hassi
"""


from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

from PIL import Image
import os

print("Animating the U gates")
print("---------------------")

def get_psi(circuit):
    global psi
    backend = Aer.get_backend('statevector_simulator') 
    result = execute(circuit, backend).result()
    psi = result.get_statevector(circuit)
    return(psi) 

def create_images(gate,theta=0.0,phi=0.0,lam=0.0):
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
        if gate=="u3":
            qc.u3(theta,phi,lam,0)
            title="U3: \u03B8 = "+str(round(theta,2))+" \u03D5 = "+str(round(phi,2))+" \u03BB = "+str(round(lam,2))
        elif gate=="u2":
            qc.u2(phi,lam,0)
            title="U2: \u03D5 = "+str(round(phi,2))+" \u03BB = "+str(round(lam,2))
        else:
            qc.h(0)
            qc.u1(phi,0)
            title="U1: \u03D5 = "+str(round(phi,2))

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
    b_images[0].save(gate+'_'+b_filename+'.gif',
               save_all=True,
               append_images=b_images[1:],
               duration=duration,
               loop=0)
    q_images[0].save(gate+'_'+q_filename+'.gif',
               save_all=True,
               append_images=q_images[1:],
               duration=duration,
               loop=0)
    print("Bloch sphere animation saved as: \n"+os.getcwd()+"/"+gate+"_"+b_filename+".gif"+"\nQsphere animation saved as: \n"+os.getcwd()+"/"+gate+"_"+q_filename+".gif")

# Main loop
gate=""
while gate !="exit": 
    gate=input("Enter u3, u2, or u3:\n")
    if gate =="u3":
        theta=float(input("Enter \u03B8:\n"))
    if gate in ["u3","u2","u1"]:
        phi=float(input("Enter \u03D5:\n"))
    if gate in ["u3","u2"]:
        lam=float(input("Enter \u03BB:\n"))
    if gate in ["u3","u2","u1"]:
        print("Building animation...")
        create_images(gate,theta,phi,lam)
        save_gif(gate)
    else:
        print("Not a valid gate, try again...")