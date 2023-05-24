import stim
import cirq
import stimcirq

circuit = stim.Circuit("""
H 0
CNOT 0 1
M 0 1
""")

print(circuit.compile_sampler().sample(10))

f = open("./src/circuit")

json_string = f.read()

new_circuit = cirq.read_json(json_text=json_string)

print(new_circuit)
