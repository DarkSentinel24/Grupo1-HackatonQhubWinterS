from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def qubit_actual(ket, compuerta):
    qc_h = QuantumCircuit(1,1)
    qc_h.h(0)
    H = Operator(qc_h)

    qc_x = QuantumCircuit(1,1)
    qc_x.x(0)
    X = Operator(qc_x)

    qc_y = QuantumCircuit(1,1)
    qc_y.y(0)
    Y = Operator(qc_y)

    qc_z = QuantumCircuit(1,1)
    qc_z.z(0)
    Z = Operator(qc_z)

    qc_s = QuantumCircuit(1,1)
    qc_s.s(0)
    S = Operator(qc_s)

    qc_t = QuantumCircuit(1,1)
    qc_t.t(0)
    T = Operator(qc_t)
    
    if compuerta == 'H':
        ket = ket.evolve(H)
    elif compuerta == 'X':
        ket = ket.evolve(X)
    elif compuerta == 'Y':
        ket = ket.evolve(Y)
    elif compuerta == 'Z':
        ket = ket.evolve(Z)
    elif compuerta == 'S':
            ket = ket.evolve(S)
    elif compuerta == 'T':
            ket = ket.evolve(T)

    return ket

def colapsar_qubit(ket):
    outcome, collapsed_psi = ket.measure()
    return [outcome, collapsed_psi]