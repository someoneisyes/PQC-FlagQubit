using Jabalizer

circuit = Jabalizer.load_circuit_from_cirq_json("random_circuit")

icm_circuit = Jabalizer.compile(circuit, 4, ["H","T"])

println(icm_circuit)

Jabalizer.save_circuit_to_cirq_json(icm_circuit[1], "./src/circuit")

