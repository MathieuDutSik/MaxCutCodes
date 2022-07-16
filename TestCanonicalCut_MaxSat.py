import os
import numpy as np
import networkx as nx
import math


def SpanFromSeq(eseq):
    Sset = []
    Scon = []
    pos = 0
    shift = 0
#    print("eseq=", eseq)
    for esiz in eseq:
        for idx in range(esiz):
            evert = shift + idx
            if pos == 0:
                Sset.append(evert)
            else:
                Scon.append(evert)
        shift += esiz
        pos = 1 - pos
    return [Sset, Scon]

def GetCanonicalCut(n, b):
#    print("GetCanonicalCut n=" + str(n) + " b=" + str(b))
    q = math.floor(n / b)
    r = n - q * b
#    print("    r=", r)
    r_crit = math.ceil( b / 2 )
#    print("    r_crit=", r_crit)
    if r <= r_crit:
        b1 = math.floor( (b + r) / 2 )
        bqp1 = math.ceil( (b+r) / 2 )
        eseq = [b1] + (q-1) * [b] + [bqp1]
#        print("    1 : eseq=" + str(eseq))
        return SpanFromSeq(eseq)
    else:
        b1 = r - math.floor( b / 2 )
        bqp2 = math.floor( b / 2 )
        eseq = [b1] + q * [b] + [bqp2]
#        print("    2 : eseq=" + str(eseq))
        return SpanFromSeq(eseq)



def get_adjacency_matrix(G):
    n = G.order()
    AdjMat = np.zeros(shape=(n,n), dtype=np.int64)
    for eV in G.edges():
        aV = eV[0]
        bV = eV[1]
        AdjMat[aV,bV] = 1
        AdjMat[bV,aV] = 1
    return AdjMat




def get_objective_value(G, pair_cut):
    n = G.order()
    AdjMat = get_adjacency_matrix(G)
    vSet = [2] * n
    for idx in pair_cut[0]:
        vSet[idx] = 0
    for idx in pair_cut[1]:
        vSet[idx] = 1
#    print("vSet=", vSet)
    obj_val = 0
    for i in range(n):
        for j in range(n):
            if i < j and AdjMat[i,j] == 1 and vSet[i] != vSet[j]:
                obj_val += 1
    return obj_val

def get_canonical_best(G):
    n = G.order()
    max_val = 0
    b_best = 0
    for b in range(1,n):
        pair_cut = GetCanonicalCut(n, b)
#        print("pair_cut=", pair_cut)
        obj_val = get_objective_value(G, pair_cut)
        if obj_val > max_val:
            max_val = obj_val
            b_best = b
    return [b_best, max_val]


def RemoveFileIfExist(efile):
    if os.path.exists(efile):
        os.remove(efile)


def Compute_MaxCut_MaxSat(G):
    n_node = len(G.nodes)
    n_edge = len(G.edges)
    n_cond = 2 * n_edge
    #
    # If it matches then we have to early terminate
    # because otherwise all the 2^n cases have to be considered
    #
    n_node_two = n_node // 2
    best_possible_cut = n_node_two * (n_node - n_node_two)
    [b_best, max_val] = get_canonical_best(G)
    if max_val == best_possible_cut:
        pair_cut = GetCanonicalCut(n_node, b_best)
        the_vector = [0] * n_node
        for ex in pair_cut[0]:
            the_vector[ex] = 1
        return the_vector
    #
    FileInput = "/tmp/evalmaxsat_input"
    fI = open(FileInput, "w")
    fI.write("p wcnf " + str(n_node) + " " + str(n_cond) + " 15\n")
    for i, j in G.edges:
        iP = i + 1
        jP = j + 1
        fI.write("1 " + str(iP) + " " + str(jP) + " 0\n")
        fI.write("1 " + str(-iP) + " " + str(-jP) + " 0\n")
    fI.close()
    #
    FileOut = "/tmp/evalmaxsat_out"
    eProg = "EvalMaxSAT_bin"
    eCommand = eProg + " " + FileInput + " > " + FileOut
    os.system(eCommand)
    #
    x_sol = [10] * n_node
    fO = open(FileOut, "r")
    l_lines = fO.readlines()
    fO.close()
    e_linecrit = l_lines[2]
    LStr = e_linecrit.split(" ")
    for i in range(1,len(LStr)):
        eVal = int(LStr[i])
        if eVal < 0:
            pos = -eVal - 1
            x_sol[pos] = 0
        if eVal > 0:
            pos = eVal - 1
            x_sol[pos] = 1
    return x_sol


def GetGraph(n,k):
    G = nx.Graph()
    for i in range(n):
        for j in range(n):
            if i != j and abs(i - j) <= k:
                G.add_edge(i, j)
    return G


def get_pair_cut(the_vector):
    n = len(the_vector)
    eSet = []
    fSet = []
    for i in range(n):
        if the_vector[i] == 1:
            eSet.append(i)
        else:
            fSet.append(i)
    return [eSet, fSet]


def GenerateExample_Best(n, k):
    G = GetGraph(n,k)
    the_vector = Compute_MaxCut_MaxSat(G)
    pair_cut = get_pair_cut(the_vector)
    best_cut = get_objective_value(G, pair_cut)
    return [best_cut, the_vector]



def GenerateExample_Can(n, k):
    print("GenerateExample_Can n=" + str(n) + " k=" + str(k))
    G = GetGraph(n,k)
    return get_canonical_best(G)



def CreateFile_Best(n,k):
    FileSave = "DATA_MaxCut/MAXSAT_BestResult_" + str(n) + "_" + str(k)
    print("FileSave=", FileSave)
    if not os.path.exists(FileSave):
        [best_cut, the_vector] = GenerateExample_Best(n, k)
        f = open(FileSave, "w")
        f.write("return rec(n:=" + str(n) + ", k:=" + str(k) + ", best_cut:=" + str(best_cut) + ", best_part:=" + str(the_vector) + ");")
        f.close()
    else:
        print("CreateFile_Best: File already existing at n=" + str(n) + " k=" + str(k))

def CreateFile_Can(n,k):
    FileSave = "DATA_MaxCut/CanResult_" + str(n) + "_" + str(k)
    if not os.path.exists(FileSave):
        print("Creating canonical data for n=" + str(n) + " k=" + str(k))
        [b_best, can_cut] = GenerateExample_Can(n, k)
        f = open(FileSave, "w")
        f.write("return rec(n:=" + str(n) + ", k:=" + str(k) + ", can_cut:=" + str(can_cut) + ", b_best:=" + str(b_best) + ");")
        f.close()
    else:
        print("CreateFile_Can: File already existing at n=" + str(n) + " k=" + str(k))



DebugCanonical = False
if DebugCanonical:
    # For n = 19 k = 6
    # The counter example is b=5
    # q = 3  r = 4
    GenerateExample_Can(19, 6)



GenerateCanonicalInfo = False
#GenerateCanonicalInfo = True
if GenerateCanonicalInfo:
    for n in range(2,400):
        for k in range(1,n+1):
            CreateFile_Can(n,k)

#GenerateBestInfo = False
GenerateBestInfo = True
if GenerateBestInfo:
    for n in range(2,400):
        for k in range(1,n+1):
            CreateFile_Best(n,k)


