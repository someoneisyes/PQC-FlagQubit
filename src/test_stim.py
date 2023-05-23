import stim

circuit = stim.Circuit("""
H 0
CNOT 0 1
M 0 1
""")

print(circuit.compile_sampler().sample(10))