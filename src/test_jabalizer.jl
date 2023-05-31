using Jabalizer

circuit = [
    ("H",["3"]),
    ("CNOT",["2","3"]),
    ("T^-1",["3"]),
    ("CNOT",["1","3"]),
    ("T",["3"]),
    ("CNOT",["2","3"]),
    ("T^-1",["3"]),
    ("CNOT",["1","3"]),
    ("T",["2"]),
    ("T",["3"]),
    ("CNOT",["1","2"]),
    ("H",["3"]),
    ("T",["1"]),
    ("T^-1",["2"]),
    ("CNOT",["1","2"]),
    ]

icm_circuit = Jabalizer.compile(circuit, 4, ["H","T","T^-1"])

println(icm_circuit)

Jabalizer.save_circuit_to_cirq_json(icm_circuit[1], "./src/circuit")

