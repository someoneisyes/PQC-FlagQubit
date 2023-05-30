import stim
import cirq
import stimcirq

f = open("./src/circuit")

json_string = f.read()

new_circuit = cirq.read_json(json_text=json_string)
ops = [cirq.measure(q) for q in new_circuit.all_qubits()]

new_circuit.append(ops)

sampler = stimcirq.StimSampler()
result = sampler.run(new_circuit, repetitions=30)

print(new_circuit)
print(result)
