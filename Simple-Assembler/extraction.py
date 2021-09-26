def addLabel(label, memAddress, lineNum):
    if isDuplicateLabel(label):
        raise Exception(lineNum, "Label has been defined more than once")
    elif isDuplicateVar(label):
        raise Exception(lineNum, "Variable cannot be used as a Label")
    elif label in reservedKeywords:
        raise Exception(lineNum, label, " is a Reserved keyword; Cannot be used as Label")
    else:
        labelTable[label] = memAddress

def addOpcode(opcode, opcodeBin, instructionClass):
    if list(opcodeTable.keys()).count(opcode) == 0:
        if opcode == "mov" and instructionClass == "B":
            opcodeTable[opcode+"B"] = [opcodeBin, instructionClass]
            return
        if opcode == "mov" and instructionClass == "C":
            opcodeTable[opcode+"C"] = [opcodeBin, instructionClass]
            return
        opcodeTable[opcode] = [opcodeBin, instructionClass]

def addVar(variable, varAddress, lineNum):
    if isDuplicateVar(variable):
        raise Exception(lineNum, "Symbol has been defined more than once")
    elif isDuplicateLabel(variable):
        raise Exception(lineNum, "Label cannot be used as a variable")
    elif variable in reservedKeywords:
        raise Exception(lineNum, "Reserved keyword; Cannot be declared as Variable")
    elif variable.isdigit():
        raise Exception(lineNum, "Variable cannot be a numeric value or start with a digit")
    else:
        varTable[variable] = varAddress

def checkImmediate(immediate):
    if immediate[0] == "$":
        value = int(immediate[1:])
        if value.isdigit() and 0 <= value < 256:
            return value
    raise Exception("Invalid Immediate")

def checkInstruction(instruction, type, lineNum):
    if type == "A":
        if len(instruction)<4 or len(instruction)>4:
            raise Exception(lineNum,"Illegal syntax for Type A instruction")
        if instruction[1] or instruction[2] or instruction[3] not in reg:
            raise Exception(lineNum,"Typo for Type A instruction")
    if type == "B":
        if len(instruction)<3 or len(instruction)>3:
            raise Exception(lineNum,"Illegal syntax for Type b instruction")
        if (instruction[1] not in reg) or (instruction[2][0] != "$"):
            raise Exception(lineNum,"Typo for Type B instruction")
    if type == "C":
        if len(instruction)<3 or len(instruction)>3:
            raise Exception(lineNum,"Illegal syntax for Type C instruction")
        if instruction[1] or instruction[2] not in reg:
            raise Exception(lineNum,"Typo for Type C instruction")
    if type == "D":
        if len(instruction)<3 or len(instruction)>3:
            raise Exception(lineNum,"Illegal syntax for Type D instruction")
        if (instruction[1] not in reg) or (instruction[2] not in (varTable and labelTable)):
            raise Exception(lineNum,"Typo for Type D instruction")
    if type == "E":
        if len(instruction)<2 or len(instruction)>2:
            raise Exception(lineNum,"Illegal syntax for Type E instruction")
        if instruction[1] not in (varTable and labelTable):
            raise Exception(lineNum,"Typo for Type E instruction")

def extractOpcodeVarLabel(lineNum, line):
    OP = line.split(" ")
    op = OP[0]
    global address
    global vAddress

    if op == "add":
        address += 1
        addOpcode('add', '00000', "A")
    elif op == "sub":
        address += 1
        addOpcode('sub', '00001', "A")
    elif op == "mov" and len(OP) == 3 and OP[2][0] == "$":
        address += 1
        addOpcode('mov', '00010', "B")
    elif op == "mov" and len(OP) == 3 and OP[2][0] != "$":
        address += 1
        addOpcode('mov', '00011', "C")
    elif op == "ld":
        address += 1
        addOpcode('ld', '00100', "D")
    elif op == "st":
        address += 1
        addOpcode('st', '00101', "D")
    elif op == "mul":
        address += 1
        addOpcode('mul', '00110', "A")
    elif op == "div":
        address += 1
        addOpcode('div', '00111', "C")
    elif op == "rs":
        address += 1
        addOpcode('rs', '01000', "B")
    elif op == "ls":
        address += 1
        addOpcode('ls', '01001', "B")
    elif op == "xor":
        address += 1
        addOpcode('xor', '01010', "A")
    elif op == "or":
        address += 1
        addOpcode('or', '01011', "A")
    elif op == "and":
        address += 1
        addOpcode('and', '01100', "A")
    elif op == "not":
        address += 1
        addOpcode('not', '01101', "C")
    elif op == "cmp":
        address += 1
        addOpcode('and', '01110', "C")
    elif op == "jmp":
        address += 1
        addOpcode('jmp', '01111', "E")
    elif op == "jlt":
        address += 1
        addOpcode('jlt', '10000', "E")
    elif op == "jgt":
        address += 1
        addOpcode('jgt', '10001', "E")
    elif op == "je":
        address += 1
        addOpcode('je', '10010', "E")
    elif op == "hlt":
        address += 1
        addOpcode('hlt', '10011', "F")
    else:
        if op == "var":
            variable = OP[1]
            vAddress += 1
            addVar(variable, vAddress, lineNum)
        if op[-1] == ":":
            label = op[:-1]
            address += 1
            addLabel(label, address, lineNum)
        else :
            raise Exception(lineNum,"Illegal instruction")

def checkLabel(line):
    label = ''
    i = line.find(':')
    if i != -1:
        label = line[:i].strip()
        line = line[i + 1:].strip()
    return label, line

def isDuplicateVar(variable):
    if list(varTable.keys()).count(variable) > 0:
        return True
    return False

def isDuplicateLabel(label):
    if list(labelTable.keys()).count(label) > 0:
        return True
    return False

def checkReg(register,lineNum):
    if register in reg :
        return reg[register]
    raise Exception(lineNum,"Invalid Register")

reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
reservedKeywords = ["add", "sub", "mul", "div", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt","ld", "st", "rs", "ls", "mov", "var"]
labelTable = {}
varTable = {}
opcodeTable = {}
vAddress = 0
address = -1