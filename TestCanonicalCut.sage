import os

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
    q = floor(n / b)
    r = n - q * b
    r_crit = ceil( b / 2 )
    if r <= r_crit:
        b1 = floor( (b + r) / 2 )
        bqp1 = ceil( (b+r) / 2 )
        eseq = [b1] + (q-1) * [b] + [bqp1]
        return SpanFromSeq(eseq)
    else:
        b1 = r - ceil( b / 2 )
        bqp2 = ceil( b / 2 )
        eseq = [b1] + q * [b] + [bqp2]
        return SpanFromSeq(eseq)



def get_objective_value(G, pair_cut):
    n = G.order()
    AdjMat = G.adjacency_matrix()
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
    for b in range(1,n):
        pair_cut = GetCanonicalCut(n, b)
#        print("pair_cut=", pair_cut)
        obj_val = get_objective_value(G, pair_cut)
        if obj_val > max_val:
            max_val = obj_val
    return max_val

def GenerateExample(n, k):
    G = Graph()
    G.add_vertices(range(n))
    n_edge = 0
    for i in range(n):
        for j in range(n):
            if i != j and abs(i - j) <= k:
                G.add_edge(i, j)
                n_edge += 1
    print("Adj(G)=")
#    print(G.adjacency_matrix())
    the_cut = G.max_cut()
    can_cut = get_canonical_best(G)
    if the_cut == can_cut:
        return [n_edge, the_cut, can_cut]
    else:
        edge_cut = G.max_cut(False, vertices=True)
        pair_cut = edge_cut[2]
        obj_val = get_objective_value(G, pair_cut)
        return [n_edge, the_cut, can_cut, pair_cut]


#DoDebug = True
DoDebug = False
if DoDebug:
   the_gen = GenerateExample(16,8)

#SearchCounterExample = True
SearchCounterExample = False
if SearchCounterExample:
    for n in range(2,20):
        for k in range(1,n+1):
            print("------------- n =", n, " k=", k, " ---------------")
            the_info = GenerateExample(n,k)
            if the_info[1] != the_info[2]:
                print("n=", n, " k=", k)
                print("the_info=", the_info)
                sys.exit(1)
            print("n=", n, " k=", k, " the_info=", the_info)

GenerateData = True
#GenerateData = False
if GenerateData:
    for n in range(2,30):
        for k in range(n+1):
            print("------------- n =", n, " k=", k, " ---------------")
            FileSave="DATA_MaxCut/SAGE_Result_" + str(n) + "_" + str(k)
            if not os.path.exists(FileSave):
                print("Creating data")
                the_info = GenerateExample(n,k)
                f = open(FileSave, "w")
                f.write("return rec(n:=" + str(n) + ", k:=" + str(k) + ", the_info:=" + str(the_info) + ");")
                f.close()
            else:
                print("File already existing")
