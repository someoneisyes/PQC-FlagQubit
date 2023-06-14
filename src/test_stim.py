import stim
import cirq
import stimcirq
import random

f = open("./src/circuit")

json_string = f.read()

f.close()

num_qubit = 4
anc_num = 0

new_circuit = cirq.read_json(json_text=json_string)

for i in range(num_qubit, len(new_circuit.all_qubits())):
    new_circuit = new_circuit.transform_qubits(qubit_map = {cirq.NamedQubit("anc_{}".format(anc_num)): cirq.NamedQubit("{}".format(i))})
    anc_num += 1

def run_all(new_circuit):

    def boolToBin(bool):
        if bool:
            return 1
        else:
            return 0
        
    #print(new_circuit)

    def addflags(circuit,numqubits,x_errors,y_errors,random_errors,numerrors):

        #list of operators and the control and target qubit
        list = []
        for moment in circuit:
            for i in moment:
                list.append(str(i))


        #finding if there is many controls on 1 qubit
        
        control = []
        
        target = []
        
        for i in range(numqubits):
            listo = []
            for r in range(len(list)):
                if list[r][5] == str(i):
                    listo.append(list[r])

            control.append(listo)

        #finding if there is many targets on 1 qubit
            
        for i in range(numqubits):
            listo = []
            for r in range(len(list)):
                if list[r][8] == str(i):
                    listo.append(list[r])

            target.append(listo)

        #Create new circuit but in stim
        c = stim.Circuit()

        #adding the first end of the flags: 
        if x_errors:
            for r in range(len(control)):
                if len(control[r]) >= 1:
                    if len(target[r]) >= 1:
                        c.append_operation("CNOT",[r,(numqubits+r)])
                elif len(control[r]) >= 2:
                    c.append_operation("CNOT",[r,(numqubits+r)])
        if y_errors:
            for r in range(len(target)):
                if len(target[r]) >= 1:
                    if len(control[r]) > 1:
                        c.append_operation("X", (numqubits*2+r))
                        c.append_operation("H", (numqubits*2+r))
                        c.append_operation("CNOT",[(numqubits*2+r),r ])
                if len(target[r]) >= 2:
                    c.append_operation("X", (numqubits*2+r))
                    c.append_operation("H", (numqubits*2+r))
                    c.append_operation("CNOT",[(numqubits*2+r),r ])

        #adding error
        if random_errors:
            for i in range(numerrors):
                rand = random.randrange(numqubits)
                pos = random.randrange(len(list))
                list.insert(pos,"X({e})".format(e = rand))
            
            
            
            

        #adding the original circuit 
        for d in range(len(list)):
            if list[d][0] == 'C':
                c.append_operation("CNOT",[int(list[d][5]),int(list[d][8])])
            elif list[d][0] == 'X':
                c.append_operation("X_ERROR",int(list[d][2]),1)


        #adding the other end of the flags
        if x_errors:
            for r in range(len(control)):
                if len(control[r]) >= 1:
                    if len(target[r]) >= 1:
                        c.append_operation("CNOT",[r,(numqubits+r)])
                elif len(control[r]) >= 2:
                    c.append_operation("CNOT",[r,(numqubits+r)])
        if y_errors:
            for r in range(len(target)):
                if len(target[r]) >= 1:
                    if len(control[r]) >= 1:
                        c.append_operation("CNOT",[(numqubits*2+r),r])
                        c.append_operation("H", (numqubits*2+r))

                if len(target[r]) >= 2:
                        c.append_operation("CNOT",[(numqubits*2+r),r])
                        c.append_operation("H", (numqubits*2+r))

        #adding measurement gate 

        for i in  range(numqubits*2):
            c.append_operation("MR",i)

        

        return c

    b = addflags(new_circuit,len(new_circuit.all_qubits()),True,False,True,1) 

    v = stimcirq.stim_circuit_to_cirq_circuit(b)

    result = b.compile_sampler().sample(1)

    result_bin = []

    for l in result:
        result_bin.append(list(map(boolToBin,l)))

    #print(v)

    num_qubits = len(new_circuit.all_qubits())
    num_total = len(v.all_qubits())

    num_ancs = num_total - num_qubits


    def flag_raised(res):
        for i in res:
            test = i[-num_ancs:]
            if 1 in test:
                return 1

        return 0

    return flag_raised(result_bin)

final_res = 0

for i in range(1000):
    final_res = final_res + run_all(new_circuit=new_circuit)

print("times that flags are raised : {}".format(final_res))

print("probability of flags being raised: {}".format(final_res*1.0/1000.0))