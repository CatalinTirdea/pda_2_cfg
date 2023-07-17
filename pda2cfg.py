import sys


def transitionCheck(PDA, type, transition):

    for element in PDA[type]:

        if transition == element or transition == "epsilon":
            return True
    return False


def check(PDA):
    valid = True
    nrS = 0
    transitions = 0
    transition = 0
    for state in PDA["states"]:
        if state == 'S':
            nrS += 1
        if nrS > 1:
            return False

    for transitions in range(0, int(len(PDA['transitions'])/6)):

        valid = transitionCheck(PDA, "states", PDA["transitions"][transition])
        if valid == False:
            return valid
        transition += 1

        valid = transitionCheck(PDA, "sigma", PDA["transitions"][transition])

        if valid == False:
            return valid
        transition += 1

        valid = transitionCheck(PDA, "stackalphabet",
                                PDA["transitions"][transition])
        if valid == False:
            return valid
        transition += 2

        valid = transitionCheck(PDA, "stackalphabet",
                                PDA["transitions"][transition])
        if valid == False:
            return valid
        transition += 1

        valid = transitionCheck(PDA, "states", PDA["transitions"][transition])
        if valid == False:
            return valid
        transition += 1

    return valid


def putInDictionary(lines, words, line, PDA, type):
    # put the elements in the dictionary
    while words[0] != "End":
        line += 1
        words = [ele for x in lines[line].split(',') for ele in x.split()]
        if (words[0] != "End"):
            for word in words:
                PDA[type].append(word)


def readFile(file, PDA):
    # read every line
    lines = file.readlines()
    # parse through every line and put in dictionary
    for line in range(0, len(lines) - 1):
        words = [ele for x in lines[line].split(',') for ele in x.split()]

        if len(words) != 0 and (words[0] == "Sigma" or words[0] == "Sigma:"):
            putInDictionary(lines, words, line, PDA, "sigma")

        if len(words) != 0 and (words[0] == "States" or words[0] == "States:"):
            putInDictionary(lines, words, line, PDA, "states")

        if len(words) != 0 and words[0] == "Stack":
            putInDictionary(lines, words, line, PDA, "stackalphabet")

        if len(words) != 0 and (words[0] == "Transitions" or words[0] == "Transitions:"):
            putInDictionary(lines, words, line, PDA, "transitions")


def validate(directory, PDA):

    file = open(directory, "r")

    PDA = {

        "sigma": [],
        "states": [],
        "stackalphabet": [],
        "transitions": []
    }

    readFile(file, PDA)

    return check(PDA), PDA


def createPDA(createdPDA, PDA):
    # put the start and finish state and create key entry for all the transitions
    for state in range(0, len(PDA["states"])):

        if PDA["states"][state] == "S":
            createdPDA["start"] = PDA["states"][state-1]

        if PDA["states"][state] == "F":
            createdPDA["finish"].append(PDA["states"][state-1])

        if PDA["states"][state] != "S" and PDA["states"][state] != "F":
            createdPDA[PDA["states"][state]] = []

    # put the stack alphabet
    createdPDA["stackalphabet"] = PDA["stackalphabet"]

    # put the transitions in the key entry
    current = 0
    for transition in range(0, int(len(PDA["transitions"])/6)):
        for i in range(1, 6):

            createdPDA[PDA["transitions"][current]].append(
                PDA["transitions"][current+i])
        current += 6

    return createdPDA


def printTable(table):
    for i in table:
        print('\t'.join(map(str, i)))


def convertPDA(createdPDA, PDA):
    # we follow these rules
    # 1. ∀p ∈ Q put rule App → ε
    # 2. ∀p, q, r ∈ Q put rule Apq → AprArq
    # 3. ∀p, r, s, q ∈ Q put rule Apq → aArsb if
    #   • (r, u) ∈ δ(p, a, ε) and
    #   • (q, ε) ∈ δ(s, b, u).

    cfgMatrix = []
    nrStates = 0
    for state in PDA['states']:
        if state != "S" and state != "F":
            nrStates += 1
    cfgMatrix = [["" for _ in range(nrStates)] for _ in range(nrStates)]

    # we make step 1 every App with p in Q gets epsilon

    for i in range(nrStates):
        cfgMatrix[i][i] = "epsilon"

    # we do step 2

    for p in range(nrStates):
        for q in range(nrStates):
            for r in range(nrStates):
                if cfgMatrix[p][q] != "":
                    cfgMatrix[p][q] += f" | A{p+1}{r+1},A{r+1}{q+1}"
                else:
                    cfgMatrix[p][q] = f"  A{p+1}{r+1},A{r+1}{q+1}"

    # we do step 3

    nrStates = 0
    for state in PDA['states']:
        if state != "S" and state != "F":
            nrStates += 1

    for state in range(len(PDA["states"])-nrStates+1):
        if PDA['states'][state] == "S" or PDA['states'][state] == "F":
            PDA['states'].pop(state)

    for p in range(nrStates):
        for q in range(nrStates):
            for r in range(nrStates):
                for s in range(nrStates):
                    a = ""
                    b = ""
                    u = ""
                    pars = 0
                    ok = 0
                    ok2 = 0
                    for parser in range(0, int((len(createdPDA[PDA['states'][p]])/5))):

                        if createdPDA[PDA["states"][p]][pars+1] == "epsilon":
                            if createdPDA[PDA["states"][p]][pars+4] == PDA["states"][r]:
                                u = createdPDA[PDA["states"][p]][pars+3]
                                ok = 1
                                a = createdPDA[PDA['states'][p]][pars]
                                break

                        pars += 5
                    pars2 = 0
                    if ok == 1:
                        for parser in range(0, int((len(createdPDA[PDA['states'][s]])/5))):

                            if createdPDA[PDA["states"][s]][pars2+4] == PDA["states"][q]:
                                if createdPDA[PDA["states"][s]][pars2+3] == "epsilon":
                                    if createdPDA[PDA["states"][s]][pars2+1] == u:
                                        b = createdPDA[PDA['states'][s]][pars2]

                                        ok2 = 1
                                        break
                            pars2 += 5
                    if ok2 == 1:
                        cfgMatrix[p][q] += f" | {a},A{r+1}{s+1},{b} "

    return cfgMatrix


def putInFile(cfgMatrix, cfg, createdPDA):

    startStates = []

    for fin in createdPDA["finish"]:
        startStates.append(createdPDA["start"][1] + fin[1])

    for start in startStates:
        cfg.write(f"S -> A{start}")
        cfg.write("\n")

    row = len(cfgMatrix[0])

    for i in range(row):
        for j in range(row):
            cfg.write(f"A{i+1}{j+1} -> {cfgMatrix[i][j]}")
            cfg.write("\n")


def main():
    if len(sys.argv) != 3:
        print("Invalid number of arguments!")
        return
    PDA = {

        "sigma": [],
        "states": [],
        "stackalphabet": [],
        "transitions": []
    }
    valid = False
    valid, PDA = validate(sys.argv[1], PDA)
    if valid == False:
        print("Invalid file!")
        return

    createdPDA = {
        "start": "",
        "finish": [],
        "stackalphabet": []
    }

    createdPDA = createPDA(createdPDA, PDA)
    cfg = open(sys.argv[2], "w")
    cfgMatrix = []
    cfgMatrix = convertPDA(createdPDA, PDA)
    putInFile(cfgMatrix, cfg, createdPDA)


main()
