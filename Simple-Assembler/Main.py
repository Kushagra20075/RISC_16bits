def addLabel(label, memAddress, lineNum):
    if isDuplicateLabel(label):
        print(lineNum, "Label has been defined more than once")
        exit()
    elif isDuplicateVar(label):
        print(lineNum, "Variable cannot be used as a Label")
        exit()
    elif label in reservedKeywords:
        print(lineNum, label, " is a Reserved keyword; Cannot be used as Label")
        exit()
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
        print(lineNum, "Symbol has been defined more than once")
        exit()
    elif isDuplicateLabel(variable):
        print(lineNum, "Label cannot be used as a variable")
        exit()
    elif variable in reservedKeywords:
        print(lineNum, "Reserved keyword; Cannot be declared as Variable")
        exit()
    elif variable.isdigit():
        print(lineNum, "Variable cannot be a numeric value or start with a digit")
        exit()
    else:
        c=0 # check for alphanum and _
        for i in variable:
            if i.isalnum() or i=="_":
                c=0
            else:
                c=1
                print(lineNum,"Illegal variable name")
                exit()
        varTable[variable] = varAddress

def checkImmediate(immediate):
    if immediate[0] == "$":
        value = immediate[1:]
        if value.isdigit() and 0 <= int(value) < 256:
            return 
            #changed
    print("Invalid Immediate")
    exit()

def checkInstruction(instructionline, type, lineNum):
    instruction= instructionline.split()
    #added for checking immediate and flags
    if type == "A":
        if len(instruction)<4 or len(instruction)>4:
            print(lineNum,"Illegal syntax for Type A instruction")
            exit()
        if (instruction[1] not in reg) or (instruction[2] not in reg) or (instruction[3] not in reg):
            print(lineNum,"Typo for Type A instruction")
            exit()
        if instruction[1]=="FLAGS" or instruction[2]=="FLAGS" or instruction[3]=="FLAGS":
            print(lineNum,"Illegal use of flags")
            exit()
    if type == "B":
        if len(instruction)<3 or len(instruction)>3:
            print(lineNum,"Illegal syntax for Type b instruction")
            exit()
        if (instruction[1] not in reg) or (instruction[2][0] != "$"):
            print(lineNum,"Typo for Type B instruction")
            exit()
        checkImmediate(instruction[2])
        if instruction[1]=="FLAGS":
            print(lineNum,"Illegal use of flags")
            exit()
    if type == "C":
        if len(instruction)<3 or len(instruction)>3:
            print(lineNum,"Illegal syntax for Type C instruction")
            exit()
        if (instruction[1] not in reg) or (instruction[2] not in reg):
            print(lineNum,"Typo for Type C instruction")
            exit()
        if instruction[0]=="mov":
            if instruction[1]=="FLAGS":
                print(lineNum,"Illegal use of flags")
                exit()
        else:
            if instruction[1]=="FLAGS" or instruction[2]=="FLAGS":
                print(lineNum,"Illegal use of flags")
                exit()        
    if type == "D":
        if len(instruction)<3 or len(instruction)>3:
            print(lineNum,"Illegal syntax for Type D instruction")
            exit()
        #change
        if (instruction[1] not in reg) or (instruction[2] not in varTable) :
            print(lineNum,"Typo for Type D instruction")
            exit()
        if instruction[1]=="FLAGS":
            print(lineNum,"Illegal use of flags")
            exit()
    if type == "E":
        if len(instruction)<2 or len(instruction)>2:
            print(lineNum,"Illegal syntax for Type E instruction")
            exit()
        #change
        if instruction[1] not in labelTable:
            print(lineNum,"Typo for Type E instruction")
            exit()
        if instruction[1]=="FLAGS":
            print(lineNum,"Illegal use of flags")
            exit()
    #added for hlt
    if type == "F":
        if len(instruction)>1 :
            print(lineNum,"Illegal syntax for halt instruction")
            exit()
#here x arguement was added as it is to check multiple labels in a single line
#it is used only in line 141
def extractOpcodeVarLabel(lineNum, line ,x):
    OP = line.split(" ")
    op = OP[0]
    global address
    global vAddress
    #check instruction functions added
    if op == "add":
        address += 1
        #added line below
        addOpcode('add', '00000', "A")
    elif op == "sub":
        address += 1
        #added line below
        addOpcode('sub', '00001', "A")
    elif op == "mov" and len(OP) == 3 and OP[2][0] == "$":
        address += 1
        #added line below
        addOpcode('mov', '00010', "B")
    elif op == "mov" and len(OP) == 3 and OP[2][0] != "$":
        address += 1
        #added line below
        addOpcode('mov', '00011', "C")
    elif op == "ld":
        address += 1
        #added line below
        addOpcode('ld', '00100', "D")
    elif op == "st":
        address += 1
        #added line below
        addOpcode('st', '00101', "D")
    elif op == "mul":
        address += 1
        #added line below
        addOpcode('mul', '00110', "A")
    elif op == "div":
        address += 1
        #added line below
        addOpcode('div', '00111', "C")
    elif op == "rs":
        address += 1
        #added line below
        addOpcode('rs', '01000', "B")
    elif op == "ls":
        address += 1
        #added line below
        addOpcode('ls', '01001', "B")
    elif op == "xor":
        address += 1
        #added line below
        addOpcode('xor', '01010', "A")
    elif op == "or":
        address += 1
        #added line below
        addOpcode('or', '01011', "A")
    elif op == "and":
        address += 1
        addOpcode('and', '01100', "A")
    elif op == "not":
        address += 1
        addOpcode('not', '01101', "C")
    elif op == "cmp":
        address += 1
        #added line below
        addOpcode('cmp', '01110', "C")
    elif op == "jmp":
        address += 1
        #added line below
        addOpcode('jmp', '01111', "E")
    elif op == "jlt":
        address += 1
        #added line below
        addOpcode('jlt', '10000', "E")
    elif op == "jgt":
        address += 1
        #added line below
        addOpcode('jgt', '10001', "E")
    elif op == "je":
        address += 1
        #added line below
        addOpcode('je', '10010', "E")
    elif op == "hlt":
        address += 1
        #added line below
        addOpcode('hlt', '10011', "F")
    else:
        if op == "var":
            variable = OP[1]
            vAddress += 1
            addVar(variable, vAddress, lineNum)
            #changed 
        elif op[-1] == ":":
            #this part was added to check for multiple labels in a single line
            if(x==1):
                print(lineNum,"multiple labels in single line")
                exit()
            label = op[:-1]
            #address + =1 was removed as we will call the function again
            #the function add label has now address +1 
            # orginal lines
            # address + =1
            #addLabel(label, address, lineNum)
            addLabel(label, address, lineNum)
        else :
            print(lineNum,"Illegal instruction")
            exit()

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
    #check misuse of flags
    if register == "FLAGS":
        print(lineNum,"Flags Register Misuse")
        exit()
    if register in reg :
        return reg[register]
    print(lineNum,"Invalid Register")
    exit()

reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
reservedKeywords = ["add", "sub", "mul", "div", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt","ld", "st", "rs", "ls", "mov", "var"]
labelTable = {}
varTable = {}
opcodeTable = {}
vAddress = 0
address = -1

def bitscode(n):
    x = bin(n).replace("0b", "")
    while len(x)<8:
        x = "0" + x
    return x

def getcode(instruction,type):
    OP = instruction.split(" ")
    op = OP[0]
    if(type=="A"):
        opcode = opcodeTable[op][0]
        reg1 =reg[OP[1]]
        reg2 = reg[OP[2]]
        reg3 = reg[OP[3]]
        code = opcode + "00" + reg1 + reg2 + reg3
        return code
    if(type=="B"):
        if(op=="mov"):
            opcode = opcodeTable["movB"][0]
        else:
            opcode = opcodeTable[op][0]
        reg1 = reg[OP[1]]
        val = OP[2][1:]
        #function to take its binary in 8 bits
        imm = bitscode(int(val))
        code = opcode + reg1 + imm
        return code
    if(type=="C"): 
        if(op=="mov"):
            opcode = opcodeTable["movC"][0]
        else:
            opcode = opcodeTable[op][0]
        reg1 = reg[OP[1]]
        reg2 = reg[OP[2]]
        code = opcode + "00000" +  reg1 + reg2
        return code
    if (type == "D"):
        opcode = opcodeTable[op][0]
        reg1 = reg[OP[1]]
        mem = varTable[OP[2]]
        strmem = bitscode(int(mem))
        code = opcode + reg1 + strmem
        return code
    if (type == "E"):
        opcode = opcodeTable[op][0]
        mem = labelTable[OP[1]]
        strmem = bitscode(int(mem))
        code = opcode + "000" + strmem
        return code
    if(type=="F"):
        opcode = opcodeTable[op][0]
        code = opcode + "00000000000"
        return code
def gettype(instruction):
    OP = instruction.split(" ")
    op = OP[0]
    if op == "add":
        return "A"
    elif op == "sub":
        return "A"
    elif op == "mov" and len(OP) == 3 and OP[2][0] == "$":
        return "B"
    elif op == "mov" and len(OP) == 3 and OP[2][0] != "$":
        return "C"
    elif op == "ld":
        return "D"
    elif op == "st":
        return "D"
    elif op == "mul":
        return "A"
    elif op == "div":
        return "C"
    elif op == "rs":
        return "B"
    elif op == "ls":
        return "B"
    elif op == "xor":
        return "A"
    elif op == "or":
        return "A"
    elif op == "and":
        return "A"
    elif op == "not":
        return "C"
    elif op == "cmp":
        return "C"
    elif op == "jmp":
        return "E"
    elif op == "jlt":
        return "E"
    elif op == "jgt":
        return "E"
    elif op == "je":
        return "E"
    elif op == "hlt":
        return "F"


#after Nishaant's
def main():
    a=[]
    l=""
    x=0
    cc=[]
    #clean code to be store in cc
    #pass one function not made separately
    while True:
        s=""
        try:
            s=input()
            #change this
            if(s!="" and s!="0"):
                a.append(s)
            if(s=="0"):
                break
        except EOFError:
            break
    i=0
    while i<len(a):
        x=0
        l=a[i].split()
        if i==len(a)-1:
            if len(l)!=1:
                print(i+1,"Last instruction should be just hlt")
                exit()
            else:
                if l[0]!="hlt":
                    print(i+1,"Last should be halt")
                    exit()
        if l[0]=="hlt":
            if i<len(a)-1:
                print(i+1,"hlt not being used as the last instruction")
                exit()
        if ":" in l[0]:
            if ":" in l[1]:
                x=1
        else:
            x=0
        extractOpcodeVarLabel(i+1,a[i],x)
        if ":" in l[0]:
            lab,ll= checkLabel(a[i])
            extractOpcodeVarLabel(i+1,ll,x)
            cc.append([ll,i+1])
        elif "var" in l[0]:
            if len(cc)!=0:
                print(i+1,"Variable declared somewhere other than the beginning")
                exit()
        else:
            cc.append([a[i],i+1])
            #append full instruction if not a label or a variable
        i+=1
# pass one part of the cases I could think of done
#     print(cc)
    output=[]
    for var in varTable.keys():
        varTable[var] = varTable[var] + address
    for x in range (0,len(cc)):
        instruction = cc[x][0]
        linenum = cc[x][1]
        type = gettype(instruction)
        checkInstruction(instruction,type,linenum)
        code = getcode(instruction,type)
        output.append(code)
    for i in output:
        print(i)
if __name__=="__main__" :
    main()
