import stim
import cirq
import stimcirq

f = open("./src/circuit")

json_string = f.read()

f.close()

num_qubit = 4
anc_num = 0

new_circuit = cirq.read_json(json_text=json_string)

print(new_circuit)

for i in range(num_qubit, len(new_circuit.all_qubits())):
    new_circuit = new_circuit.transform_qubits(qubit_map = {cirq.NamedQubit("anc_{}".format(anc_num)): cirq.NamedQubit("{}".format(i))})
    anc_num += 1

#ops = [cirq.measure(q) for q in new_circuit.all_qubits()]
#new_circuit.append(ops)

sampler = stimcirq.StimSampler()
result = sampler.run(new_circuit, repetitions=30)

print(new_circuit)
print(result)
