using Jabalizer

circuit = [("H",["1"]),("CNOT",["1","2"])]

icm_circuit = Jabalizer.compile(circuit, 3, [""])

println(icm_circuit)

Jabalizer.save_circuit_to_cirq_json(icm_circuit[1], "./src/circuit")

