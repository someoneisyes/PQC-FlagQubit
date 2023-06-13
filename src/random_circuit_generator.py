import cirq

line_qubits = []

for i in range(4):
    line_qubits.append(cirq.LineQubit(i))

circuit = cirq.testing.random_circuit(line_qubits,6,0.4,{cirq.H : 1, cirq.T: 1, cirq.CNOT: 2})

f = open("random_circuit", "w")

f.write(cirq.to_json(circuit))

f.close