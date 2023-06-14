import stim
import cirq
import stimcirq
import random

f = open("./src/circuit")

json_string = f.read()

f.close()

num_qubit = 10
anc_num = 0

new_circuit = cirq.read_json(json_text=json_string)

for i in range(num_qubit, len(new_circuit.all_qubits())):
    new_circuit = new_circuit.transform_qubits(qubit_map = {cirq.NamedQubit("anc_{}".format(anc_num)): cirq.NamedQubit("{}".format(i))})
    anc_num += 1

#print(new_circuit)

def run_all(new_circuit):

    def boolToBin(bool):
        if bool:
            return 1
        else:
            return 0

    def addflags(circuit,numqubits,x_errors,y_errors,random_errors,numerrors):

        base_ten = ['0','1','2','3','4','5','6','7','8','9']

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
                if not list[r][6] in base_ten: 
                    if list[r][5] == str(i):
                        listo.append(list[r])
                elif not list[r][7] in base_ten:
                    if list[r][5:7] == str(i):
                        listo.append(list[r])
                elif not list[r][8] in base_ten:
                    if list[r][5:8] == str(i):
                        listo.append(list[r])

            control.append(listo)
        
        #finding if there is many targets on 1 qubit
            
        for i in range(numqubits):
            listo = []
            for r in range(len(list)):
                if not list[r][9] in base_ten: 
                    if list[r][8] == str(i):
                        listo.append(list[r])
                elif not list[r][10] in base_ten:
                    if list[r][8:10] == str(i):
                        listo.append(list[r])
                elif not list[r][11] in base_ten:
                    if list[r][8:11] == str(i):
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
                if not list[d][6] in base_ten:
                    c.append_operation("CNOT",[int(list[d][5]),int(list[d][8:len(list[d])-1])])
                elif list[d][6] in base_ten and not list[d][7] in base_ten:
                    c.append_operation("CNOT",[int(list[d][5:7]),int(list[d][9:len(list[d])-1])])  
                elif list[d][7] in base_ten and not list[d][8] in base_ten:
                    c.append_operation("CNOT",[int(list[d][5:8]),int(list[d][10:len(list[d])-1])])        
                
            elif list[d][0] == 'X':
                c.append_operation("X_ERROR",int(list[d][2:len(list[d])-1]),1)


        #adding the other end of the flags
        if x_errors:
            for r in range(len(control)):
                if len(control[r]) >= 1:
                    if len(target[r]) >= 1:
                        c.append_operation("CNOT",[r,(numqubits+r)])
                elif len(control[r]) >= 1:
                    c.append_operation("CNOT",[r,(numqubits+r)])
        if y_errors:
            for r in range(len(target)):
                if len(target[r]) >= 1:
                    if len(control[r]) >= 1:
                        c.append_operation("CNOT",[(numqubits*2+r),r])
                        c.append_operation("H", (numqubits*2+r))

                if len(target[r]) >= 1:
                        c.append_operation("CNOT",[(numqubits*2+r),r])
                        c.append_operation("H", (numqubits*2+r))

        #adding measurement gate 

        v = stimcirq.stim_circuit_to_cirq_circuit(c)

        for i in  range(numqubits*2):
            c.append_operation("MR",i)

        

        return (c,v)

    b = addflags(new_circuit,len(new_circuit.all_qubits()),True,False,True,20)

    result = b[0].compile_sampler().sample(1)

    result_bin = []

    for l in result:
        result_bin.append(list(map(boolToBin,l)))

    num_qubits = len(new_circuit.all_qubits())
    num_total = len(stimcirq.stim_circuit_to_cirq_circuit(b[0]).all_qubits())

    num_ancs = num_total - num_qubits


    def flag_raised(res):
        for i in res:
            test = i[-num_ancs:]
            if 1 in test:
                return 1

        return 0

    return (flag_raised(result_bin), b[1], result_bin[0])

final_res = 0

iteration = 1000

for i in range(iteration):
    x = run_all(new_circuit=new_circuit)
    final_res = final_res + x[0]
    c = x[1]
    d = x[2]

#print(c)
print("numbers of qubits (excluding flags) : {}".format(len(new_circuit.all_qubits())))
print("numbers of flags : {}".format(len(c.all_qubits())-len(new_circuit.all_qubits())))
print("circuit : {}".format(d[0:len(new_circuit.all_qubits())]))
print("flags : {}".format(d[len(new_circuit.all_qubits()):len(c.all_qubits())]))

print("times that flags are raised : {}".format(final_res))

print("probability of flags being raised: {}".format(final_res*1.0/iteration))