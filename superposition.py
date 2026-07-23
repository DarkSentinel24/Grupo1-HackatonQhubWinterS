from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Operator, Statevector

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

    if compuerta == 'H':
        ket = ket.evolve(H)
    elif compuerta == 'X':
        ket = ket.evolve(X)
    elif compuerta == 'Y':
        ket = ket.evolve(Y)
    else:
        ket = ket.evolve(Z)

    return ket

def colapsar_qubit(ket):
    outcome, collapsed_psi = ket.measure()
    return [outcome, collapsed_psi]