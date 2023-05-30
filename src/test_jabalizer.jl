using Jabalizer

circuit = [("H",["1"]),("CNOT",["1","2"]),("CNOT",["1","3"]),("H",["1"]),("X",["2"])]

icm_circuit = Jabalizer.compile(circuit, 4, ["H","X"])

println(icm_circuit)

Jabalizer.save_circuit_to_cirq_json(icm_circuit[1], "./src/circuit")

