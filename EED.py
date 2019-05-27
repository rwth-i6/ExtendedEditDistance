# -*- coding:utf-8 -*-
import ctypes
import os

import util


#Python wrpaper for the C++ EED implementation
def eed(hyp, ref):
    _eed = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + '/libEED.so')
    #print(os.path.dirname(os.path.abspath(__file__)))
    _eed.wrapper.restype = ctypes.c_float
    hyp.insert(0, " ")
    hyp.append(" ")
    ref.insert(0, " ")
    ref.append(" ")
    hyp_c = (ctypes.c_ulonglong * len(hyp))()
    hyp_c[:] = [bytes_to_int(x.encode('utf-8')) for x in hyp]
    ref_c = (ctypes.c_ulonglong * len(ref))()
    ref_c[:] = [bytes_to_int(x.encode('utf-8')) for x in ref]
    alpha = 2.0
    deletion = 0.2
    insertion = 1.0
    substitution = 1.0
    rho = 0.3
    norm = len(ref_c)
    result = _eed.wrapper(hyp_c, ref_c, len(hyp_c), len(ref_c), 
                          ctypes.c_float(alpha), ctypes.c_float(deletion), 
                          ctypes.c_float(insertion), ctypes.c_float(substitution), ctypes.c_float(rho), 
                          norm) 
    return min(1.0, result)


def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


#Distance measure used for substitutions/identity operation
def distance(refWord, hypWord):
    if refWord == hypWord:
        return 0
    else:
        return 1
   

#Python Implementation of EED, ~30x slower than the C++ one
def eed_python(hyp, ref):
    hyp.insert(0, " ")
    hyp.append(" ")
    ref.insert(0, " ")
    ref.append(" ")
    alpha = 2.0
    deletion = 0.2
    #substitutions are implemented via the distance function
    insertion = 1.0
    rho = 0.3
    lj =[0]*(len(hyp)+1)
    row = [1]*(len(hyp)+1) #row[i] stores cost of cheapest path from (0,0) to (i,l) in CDER aligment grid.
    row[0] = 0 #CDER initialisation 0,0 = 0 rest 1
    nextRow = [float('inf')]*(len(hyp)+1)
    for w in range(1, len(ref)+1):
        for i in range(0, len(hyp)+1):
            if i > 0 :
              nextRow[i] = min(nextRow[i-1] + deletion, row[i-1]+distance(ref[w-1],hyp[i-1]), row[i]+ insertion)
            else :
              nextRow[i] = row[i]+ 1.0        
        minInd = nextRow.index(min(nextRow))
        lj[minInd] += 1
        #Long Jumps
        if ref[w-1] == " ":
          longJump = alpha + nextRow[minInd]
          nextRow = [x if x < longJump else longJump for x in nextRow]
        row = nextRow 
        nextRow = [float('inf')] *(len(hyp)+1)
        coverage = rho*sum([x if x > 1 else 0 for x in lj])
    return min(1, (row[-1]+ coverage)/(float(len(ref)) + coverage))


#Provides System scoring with full preprocessing in the case where EED is used as an import  
def score(hypIn, refIn):
    import codecs
    hyp = [util.preprocess(x) for x in open(hypIn, 'r', 'utf-8').readlines()]
    ref = [util.preprocess(x) for x in open(refIn, 'r', 'utf-8').readlines()]
    scores = []
    for (h,r) in zip(hyp,ref):
        h, r = list(h), list(r)
        score = eed(h,r)
        scores.append(score)    
    return sum(scores)/len(scores)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Extended Edit Distance Metric for Machine Translation')
    parser.add_argument('-ref', '--reference', help='Reference file', required=True)
    parser.add_argument('-hyp', '--hypothesis', help='Input(test) file', required=True)
    parser.add_argument('-v', '--verbose', help='Show scores of each sentence.',
                        action='store_true', default=False)
    return parser.parse_args()    


def main():
    import sys
    import codecs
    args = parse_args()
    hlines = [util.preprocess(x, "en") for x in codecs.open(args.hypothesis, 'r', 'utf-8').readlines()]
    rlines = [util.preprocess(x, "en") for x in codecs.open(args.reference, 'r', 'utf-8').readlines()]
    if len(hlines) != len(rlines):
        print("Error: input file has {0} lines, but reference has {1} lines.".format(len(hlines), len(rlines)))
        sys.exit(1)
    scores = []
    for lineno, (hline, rline) in enumerate(zip(hlines, rlines), start=1):
        rline, hline = list(rline), list(hline)
        score = eed(hline, rline)
        scores.append(score)
        if args.verbose:
            print("Sentence {0}: {1:.4f}".format(lineno, score))
    
    average = sum(scores) / len(scores)
    
    print("System Score={0:.4f}".format(average))
    sys.exit(0) 

if __name__ == '__main__':
    main()
