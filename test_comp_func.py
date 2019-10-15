from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute
IBMQ.load_account()
#from qiskit.aqua.circuits.gates import mct
q = QuantumRegister(11)
c = ClassicalRegister(4)
qc = QuantumCircuit(q,c)
ite=1
from qiskit.aqua.circuits.gates import mct
def compare(a,b,c,d,e,f):
    qc.cx(q[a],q[e])
    qc.cx(q[c],q[e])
    qc.cx(q[b],q[f])
    qc.cx(q[d],q[f])
def compare_inverse(a,b,c,d,e,f):
    qc.cx(q[d],q[f])
    qc.cx(q[b],q[f])
    qc.cx(q[c],q[e])
    qc.cx(q[a],q[e])
def hadder(a,b,c):
    #XOR
    qc.cx(q[b], q[c])
    qc.cx(q[a], q[c])
    #AND
    qc.ccx(q[a], q[b], q[c])
def ihadder(a,b,c):
    qc.ccx(q[a], q[b], q[c])
    qc.cx(q[a], q[c])
    qc.cx(q[b], q[c])

#diffusion operations
def diffusion(a,b,c,d,e):
    qc.h(q[a])
    qc.h(q[b])
    qc.h(q[c])
    qc.h(q[d])
    qc.x(q[a])
    qc.x(q[b])
    qc.x(q[c])
    qc.x(q[d])
    qc.h(q[d])  
    qc.mct([q[a],q[b],q[c]], q[d],[q[e]], mode='basic')
    qc.h(q[d])  
    qc.x(q[a])
    qc.x(q[b])
    qc.x(q[c])
    qc.x(q[d])
    qc.h(q[a])
    qc.h(q[b])
    qc.h(q[c])
    qc.h(q[d])

#initialization
qc.x(q[7])
qc.h(q[7])
for i in range(ite):
    qc.h(q[0:4])
    qc.barrier()
    compare(0,1,2,3,4,5)
    hadder(4,5,8)
    qc.barrier()
    qc.cx(q[8],q[7])
    qc.barrier()
    ihadder(4,5,8)
    qc.barrier()
    compare_inverse(0,1,2,3,4,5)
    qc.barrier()
    diffusion(0,1,2,3,4)
    qc.barrier()
qc.measure(q[0:4], c[0:4])



backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=10000)
result = job.result()
count =result.get_counts()
print(count)
#qc.draw(output='mpl')


