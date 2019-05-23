# Extended Edit Distance
This repository contains the latest code for the Extended Edit Distance (EED) metric for machine translation. The metric utilises the Levenshtein distance and extends it by adding an additional jump operation.

# Implementation 

The metric is implemented both in C++ and Python. The C++ implementation can be found in *EED.cpp*, where as the Python implementation in *EED.py*. EED.py also provides the entry point for the metric. It calls the compiled C++ variant of the metric *libEED.so*.

# Prerequisites

* Python 3.5 with the packages  `ctypes` and  `codecs`
* C++ 11
 

# Usage Guide
Use:
`python3 EED.py -ref [reference]  -hyp [hypothesis]  [optional: -v]`
* The optional `-v` arguments toggles the verbosity of the output. If present the score for each segment will be shown. 
* It is assumed that each segment is on a separate line.
* The final system/file score is computed by taking the average of all segment scores.

# Customisation Guide
If changes to the metric are desired. The C++ code in EED.cpp has to be altered and recompiled.
Recompilation can be done via:

`g++ EED.cpp -shared -o libEED.so -std=c++11 -fPIC -O3 -flto -funroll-loops -frename-registers`

Further optimisation can be done by using `-fprofile-generate` and `-fprofile-use` as compiler options.
