OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
cz q[1],q[0];
h q[1];
z q[0];
measure q[0] -> c[0];
measure q[1] -> c[1];
