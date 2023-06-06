using Jabalizer

circuit = [
    ("CNOT",["2","1"]),
    ("CNOT",["2","3"]),
    ("CNOT",["2","1"]),
    ("CNOT",["3","1"]),
    ("CNOT",["3","4"])
    ]

icm_circuit = Jabalizer.compile(circuit, 4, [""])

println(icm_circuit)

Jabalizer.save_circuit_to_cirq_json(icm_circuit[1], "./src/circuit")

